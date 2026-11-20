
from fastapi import APIRouter, HTTPException
from app.schemas import JobCreate, JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])

_db: dict[int, JobRead] = {}

@router.get("", response_model=list[JobRead])
async def list_jobs():
    return list(_db.values())

@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: int):
    if job_id not in _db:
        raise HTTPException(status_code=404, detail="Job not found")
    return _db[job_id]


_next_id = 1

@router.post("", response_model=JobRead, status_code=201)
async def create_job(job: JobCreate):
    global _next_id

    new_job = JobRead(id=_next_id, **job.model_dump())

    _db[_next_id] = new_job
    _next_id += 1

    return new_job


@router.put("/{job_id}", response_model=JobRead)
async def update_job(job_id: int, job: JobCreate):
    if job_id not in _db:
        raise HTTPException(status_code=404, detail="Job not found")

    updated_job = JobRead(id=job_id, **job.model_dump())
    _db[job_id] = updated_job

    return updated_job


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: int):
    if job_id not in _db:
        raise HTTPException(status_code=404, detail="Job not found")

    del _db[job_id]


