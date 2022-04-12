import os
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from sqlalchemy import create_engine

from models.task import TaskIn, TaskOut

logger.info("Configure Start")

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        "172.19.0.2",
        5432,
        os.environ["POSTGRES_DB"]
    )

psql_engine = create_engine(
    DATABASE_URL,
    pool_size=3
)

db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
metadata.create_all(psql_engine)

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("task_id", sqlalchemy.INTEGER, autoincrement=True),
    sqlalchemy.Column("description", sqlalchemy.TEXT),
    sqlalchemy.Column("tags", sqlalchemy.ARRAY(item_type=sqlalchemy.TEXT)),
    sqlalchemy.Column("due_date", sqlalchemy.TIMESTAMP)
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    logger.info("Startup")
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown")
    await db.disconnect()


@app.get("/tasks", response_model=List[TaskOut], status_code=status.HTTP_200_OK)
async def read_tasks():
    query = tasks.select()
    return await db.fetch_all(query)


@app.post("/task", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskIn):
    logger.info(task)
    logger.info(type(task))
    query = tasks.insert().values(**task.dict())
    new_task_id = await db.execute(query)
    return {"id": new_task_id}


@app.get("/task/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int):
    query = tasks.select().where(tasks.c.task_id == task_id)
    return await db.fetch_one(query)
