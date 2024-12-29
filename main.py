from storage_json import StorageJson
import os
import json


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

    storage = StorageJson(f"{user}.json")

    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie rating")

        try:
            choice = int(input("\nChoose an option: "))
        except KeyboardInterrupt:
            print("\nExiting program.")
            break
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 4.")
            continue

        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 1:
            movies = storage.list_movies()
            if not movies:
                print("No movies found.")
            else:
                for title, details in movies.items():
                    print(f"{title} - Year: {details['year']}, Rating: {details['rating']}, Poster: {details['poster']}")
        elif choice == 2:
            title = input("Enter movie title: ").strip()
            try:
                year = int(input("Enter movie release year: "))
                rating = float(input("Enter movie rating (0.0 - 10.0): "))
                poster = input("Enter movie poster URL or path: ").strip()
                storage.add_movie(title, year, rating, poster)
            except ValueError:
                print("Invalid input. Year must be an integer and rating must be a number.")
        elif choice == 3:
            title = input("Enter movie title to delete: ").strip()
            storage.delete_movie(title)
        elif choice == 4:
            title = input("Enter movie title to update: ").strip()
            try:
                rating = float(input("Enter new movie rating (0.0 - 10.0): "))
                storage.update_movie(title, rating)
            except ValueError:
                print("Invalid input. Rating must be a number.")
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()