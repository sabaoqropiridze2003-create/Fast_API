from fastapi import FastAPI, Path, Query

app = FastAPI()

# დავალება 37

# @app.get("/products")
# def get_all_products():
#     return {"message": "retrieved succsessfully"}

# @app.post("/products")
# def create_product(product: dict):
#     return {"message": "created product", "product": product}

# @app.put("/update")
# def update_product(new_product: dict):
#     return {"message": "updated product", "product": new_product}

# @app.patch("/update_item")
# def patch_product(new_product: dict):
#     return {"message": "updated product", "product": new_product}

# @app.delete("/delete_item")
# def delete_product(id: int):
#     return {"message": "deleted product", "deleted product with id": id}

# დავალე 38


movies = [
    {"id": 1, "title": "The Matrix", "genre": "Action", "year": 1999, "rating": 8.7},
    {"id": 2, "title": "The Dark Knight", "genre": "Action", "year": 2008, "rating": 9.0},
    {"id": 3, "title": "Inception", "genre": "Sci-Fi", "year": 2010, "rating": 8.8},
    {"id": 4, "title": "The Hangover", "genre": "Comedy", "year": 2009, "rating": 7.7},
    {"id": 5, "title": "Interstellar", "genre": "Sci-Fi", "year": 2014, "rating": 8.7},
    {"id": 6, "title": "Parasite", "genre": "Drama", "year": 2019, "rating": 8.5},
]

@app.get("/movies")
def get_movies(genre: str | None = None, year: int | None = None, min_rating: float | None = None, search: str | None = None):
    filtered_movies = movies

    if genre:
        filtered_movies = [movie for movie in filtered_movies if movie["genre"].lower() == genre.lower()]

    if year:
        filtered_movies = [movie for movie in filtered_movies if movie["year"] == year]

    if min_rating is not None:
        filtered_movies = [movie for movie in filtered_movies if movie["rating"] >= min_rating]

    if search:
        filtered_movies = [movie for movie in filtered_movies if search.lower() in movie["title"].lower()]

    return filtered_movies

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int = Path(..., ge=1)):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"message": "Movie not found"}