from movie_app import MovieApp
from storage_json import StorageJson

# Create a StorageJson instance
storage = StorageJson("movies.json")

# Create a MovieApp instance with the storage instance
movie_app = MovieApp(storage)

# Run the movie app
movie_app.run()