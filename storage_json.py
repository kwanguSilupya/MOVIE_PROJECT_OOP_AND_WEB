import json
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initialize the JSON storage with a specific file path.

        Args:
            file_path (str): Path to the JSON file for this storage.
        """
        self.file_path = file_path

    def _load_movies(self):
        """Internal method to load movies from the JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                movies = json.load(file)
                if not isinstance(movies, dict):
                    print("Data format error. Resetting to an empty dictionary.")
                    return {}
                print(f"Loaded movies: {movies}")  # Debugging
                return movies
        except FileNotFoundError:
            print(f"File not found: {self.file_path}. Returning an empty dictionary.")  # Debugging
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}. Returning an empty dictionary.")  # Debugging
            return {}

    def _save_movies(self, movies):
        """Internal method to save movies to the JSON file."""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(movies, file, indent=4)
        except IOError:
            print("Error saving movies. Please try again.")

    def list_movies(self):
        """Returns all movies in the storage."""
        return self._load_movies()

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the storage.

        Args:
            title (str): Movie title.
            year (int): Release year.
            rating (float): Rating (0.0 - 10.0).
            poster (str): URL or path to the movie poster.
        """
        movies = self._load_movies()
        if title in movies:
            print(f"Movie '{title}' already exists.")
            return
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)
        print(f"Movie '{title}' added successfully!")

    def delete_movie(self, title):
        """
        Deletes a movie from the storage.

        Args:
            title (str): Movie title to delete.
        """
        movies = self._load_movies()
        if title not in movies:
            print(f"Movie '{title}' not found.")
            return
        del movies[title]
        self._save_movies(movies)
        print(f"Movie '{title}' deleted successfully!")

    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the storage.

        Args:
            title (str): Movie title to update.
            rating (float): New rating (0.0 - 10.0).
        """
        movies = self._load_movies()
        if title not in movies:
            print(f"Movie '{title}' not found.")
            return
        movies[title]['rating'] = rating
        self._save_movies(movies)
        print(f"Movie '{title}' updated successfully!")