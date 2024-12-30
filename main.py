from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp
import os
import json


# The StorageJson class remains part of the main.py file
class StorageJson:
    def __init__(self, file_path):
        self.file_path = file_path
        # Automatically create the file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump({}, file)
                print(f"Created new file: {file_path}")

    def list_movies(self):
        try:
            with open(self.file_path, 'r') as file:
                movies = json.load(file)
                # Ensure the data is a dictionary
                if not isinstance(movies, dict):
                    print("Data format error. Resetting to an empty dictionary.")
                    return {}
                return movies
        except FileNotFoundError:
            print(f"File not found: {self.file_path}. Returning an empty dictionary.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.file_path}. Returning an empty dictionary.")
            return {}

    def add_movie(self, title, year, rating, poster):
        movies = self.list_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)
        print(f"Movie '{title}' added successfully.")

    def delete_movie(self, title):
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            with open(self.file_path, 'w') as file:
                json.dump(movies, file, indent=4)
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def update_movie(self, title, rating):
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            with open(self.file_path, 'w') as file:
                json.dump(movies, file, indent=4)
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")


# Main function to run the app
def main():
    """
    Main menu for the Movies App Reloaded.
    Provides options to list, add, delete movies, and show statistics.
    """
    print("Welcome to the Movies App Reloaded!")
    user = input("Enter your username: ").strip()
    if not user:
        print("Invalid username. Exiting...")
        return

    # Ask the user to choose the storage format
    storage_format = input("Choose storage format (1 for JSON, 2 for CSV): ").strip()

    if storage_format == "1":
        # Use StorageJson for JSON storage
        storage = StorageJson(f"{user}.json")
    elif storage_format == "2":
        # Use StorageCsv for CSV storage
        storage = StorageCsv(f"{user}.csv")
    else:
        print("Invalid choice. Exiting...")
        return

    movie_app = MovieApp(storage)

    # Ensure all movies have a 'poster' key in the JSON file
    if isinstance(storage, StorageJson):
        movies = storage.list_movies()
        updated = False
        for title, details in movies.items():
            if "poster" not in details:
                movies[title]["poster"] = "No poster available"
                updated = True

        if updated:
            with open(f"{user}.json", 'w') as file:
                json.dump(movies, file, indent=4)
            print("Updated movies file to include missing 'poster' fields.")

    # Run the movie app
    movie_app.run()


if __name__ == "__main__":
    main()