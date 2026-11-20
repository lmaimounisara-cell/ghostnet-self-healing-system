from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import JobCreate, JobRead
from app.models import Job
from app.db import get_session
router = APIRouter(prefix="/jobs", tags=["jobs"])

_db: dict[int, JobRead] = {}

@router.get("", response_model=list[JobRead])
async def list_jobs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Job))
    return result.scalars().all()

@router.get("/{job_id}", response_model=JobRead)
async def get_job(
    job_id: int,
    session: AsyncSession = Depends(get_session)
):
    job = await session.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

_next_id = 1

@router.post("", response_model=JobRead, status_code=201)
async def create_job(
    job: JobCreate,
    session: AsyncSession = Depends(get_session)
):
    new_job = Job(
        name=job.name,
        priority=job.priority
    )

    session.add(new_job)
    await session.commit()
    await session.refresh(new_job)

    return new_job


@router.put("/{job_id}", response_model=JobRead)
async def update_job(
    job_id: int,
    job: JobCreate,
    session: AsyncSession = Depends(get_session)
):
    existing_job = await session.get(Job, job_id)

    if existing_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_job.name = job.name
    existing_job.priority = job.priority

    await session.commit()
    await session.refresh(existing_job)

    return existing_job


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    session: AsyncSession = Depends(get_session)
):
    job = await session.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    await session.delete(job)
    await session.commit()


