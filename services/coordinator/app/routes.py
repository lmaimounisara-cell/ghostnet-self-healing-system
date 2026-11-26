import logging

import httpx
from aio_pika.exceptions import AMQPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Job
from app.publisher import publish_job_created
from app.schemas import JobCreate, JobRead
from app.worker_client import get_worker_capacity

router = APIRouter(prefix="/jobs", tags=["jobs"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[JobRead])
async def list_jobs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job))
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobRead)
async def get_job(
    job_id: int,
    session: AsyncSession = Depends(get_session),
):
    job = await session.get(Job, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("", response_model=JobRead, status_code=201)
async def create_job(
    job: JobCreate,
    session: AsyncSession = Depends(get_session),
):
    try:
        available = await get_worker_capacity()
    except (httpx.HTTPError, TimeoutError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Workers service temporarily unavailable",
        ) from exc

    if not available:
        raise HTTPException(
            status_code=503,
            detail="No worker capacity available",
        )

    new_job = Job(name=job.name, priority=job.priority, email=job.email)
    session.add(new_job)
    await session.commit()
    await session.refresh(new_job)

    try:
        await publish_job_created(new_job.id, new_job.email)
    except (AMQPException, OSError) as exc:
        logger.warning(
            "Could not publish job.created for job %s: %s", new_job.id, exc
        )

    return new_job


@router.put("/{job_id}", response_model=JobRead)
async def update_job(
    job_id: int,
    job: JobCreate,
    session: AsyncSession = Depends(get_session),
):
    existing_job = await session.get(Job, job_id)

    if existing_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    existing_job.name = job.name
    existing_job.priority = job.priority
    existing_job.email = job.email

    await session.commit()
    await session.refresh(existing_job)

    return existing_job


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    session: AsyncSession = Depends(get_session),
):
    job = await session.get(Job, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    await session.delete(job)
    await session.commit()