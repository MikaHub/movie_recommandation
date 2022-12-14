import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.movie_recommendations import find_similar_movies
from backend.SVD.movie import get_high_recommended_movies

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_recommendation/{movie_id}")
def get_recommendation_by_id(movie_id: int):
    movies = find_similar_movies(movie_id)
    return movies


@app.get("/user_recommendation/{user_id}")
def get_user_recommendation(user_id: int):
    movie = get_high_recommended_movies(user_id)
    return movie


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")