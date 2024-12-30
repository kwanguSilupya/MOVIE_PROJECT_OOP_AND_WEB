import csv
import os

class StorageCsv:
    def __init__(self, file_path):
        self.file_path = file_path
        # Create the CSV file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["title", "rating", "year", "poster"])
                writer.writeheader()
            print(f"Created new CSV file: {file_path}")

    def list_movies(self):
        movies = {}
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row["title"]
                    movies[title] = {
                        "rating": float(row["rating"]),
                        "year": int(row["year"]),
                        "poster": row.get("poster", "No poster available")
                    }
            return movies
        except FileNotFoundError:
            print(f"File not found: {self.file_path}. Returning an empty dictionary.")
            return {}
        except Exception as e:
            print(f"Error reading CSV file: {e}. Returning an empty dictionary.")
            return {}

    def add_movie(self, title, year, rating, poster):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "rating", "year", "poster"])
            writer.writerow({
                "title": title,
                "rating": rating,
                "year": year,
                "poster": poster
            })
        print(f"Movie '{title}' added successfully.")

    def delete_movie(self, title):
        movies = self.list_movies()
        if title in movies:
            # Remove the movie from the list
            movies.pop(title)
            # Rewrite the CSV file with the updated list
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["title", "rating", "year", "poster"])
                writer.writeheader()
                for movie in movies.values():
                    writer.writerow(movie)
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def update_movie(self, title, rating):
        movies = self.list_movies()
        if title in movies:
            # Update the rating of the movie
            movies[title]["rating"] = rating
            # Rewrite the CSV file with the updated rating
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["title", "rating", "year", "poster"])
                writer.writeheader()
                for movie in movies.values():
                    writer.writerow(movie)
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")