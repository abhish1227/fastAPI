import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routers import post, user, auth, votes
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional, List
# import the models module where we define our database models.
from . import models, schemas, utils
# import the database engine to connect to the database.
from .database import engine, get_db
from sqlalchemy.orm import Session  # import Session to manage database sessions

from fastapi.middleware.cors import CORSMiddleware
# This is used for hashing passwords securely.


# creates the tables in the database if they don't exist using sqlalchemy.
# but we don't need it since we are using alembic to create and update tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with PostgreSQL",
              description="A simple FastAPI application with PostgreSQL database",)

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)  # include the post router
app.include_router(user.router)  # include the user router
app.include_router(auth.router)  # include the auth router
app.include_router(votes.router)
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastAPI',
#             user='postgres',
#             password='Abhish_Post27',
#             # This allows us to get results as dictionaries.
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful!")
#         break
#     except Exception as error:
#         print("Database connection failed!")
#         print(f"Error: {error}")
#         time.sleep(2)


# my_posts = [{"title": "Post 1", "content": "Content of Post 1", "id": 101, "published": True},
#             {"title": "Post 2", "content": "Content of Post 2",
#                 "id": 121, "rating": 2.5, "published": False},
#             {"title": "Post 3", "content": "Content of Post 3", "id": 131, "rating": 3}, {"title": "Bihar Tourism", "content": "Rajgir, Nalanda", "published": True, "rating": 9.5, "id": 304153}, {"title": "Fast food in Patna", "content": "Marine Drive", "published": True, "rating": 3.21, "id": 473709}]


@app.get("/", tags=['Root'])
def root():
    # return a dictionary that will be converted to JSON
    return {"message": "Welcome to our API! Hello World!"}
