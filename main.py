import os
import json
import requests
from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def generate_website(movies, template_file, output_file):
    """
    Generates an HTML website from the template and movie data.
    """
    try:
        with open(template_file, 'r') as template:
            html_template = template.read()

        # Replace __TEMPLATE_TITLE__ placeholder
        html_template = html_template.replace("__TEMPLATE_TITLE__", "My Movie Collection")

        # Generate the movie grid HTML
        movie_grid = ""
        for title, details in movies.items():
            movie_card = f"""
            <div class="movie-card">
                <img src="{details.get('poster_url', '#')}" alt="{title} poster">
                <h3>{title}</h3>
                <p>Year: {details.get('year', 'Unknown')}</p>
                <p>Rating: {details.get('rating', 'Unknown')}</p>
            </div>
            """
            movie_grid += movie_card

        # Replace __TEMPLATE_MOVIE_GRID__ placeholder
        html_template = html_template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        # Write the final HTML to the output file
        with open(output_file, 'w') as output:
            output.write(html_template)

        print("Website was generated successfully.")

    except FileNotFoundError:
        print(f"Error: Template file '{template_file}' not found.")
    except Exception as e:
        print(f"Error generating website: {e}")


def main():
    print("Welcome to the Movies App Reloaded!")
    user = input("Enter your username: ").strip()
    if not user:
        print("Invalid username. Exiting...")
        return

    # Ask the user to choose the storage format
    storage_format = input("Choose storage format (1 for JSON, 2 for CSV): ").strip()

    if storage_format == "1":
        storage = StorageJson(f"{user}.json")
    elif storage_format == "2":
        storage = StorageCsv(f"{user}.csv")
    else:
        print("Invalid choice. Exiting...")
        return

    api_key = input("Enter your OMDb API key: ").strip()
    if not api_key:
        print("Invalid API key. Exiting...")
        return

    movie_app = MovieApp(storage)

    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Generate website")

        try:
            choice = int(input("\nChoose an option: "))
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
                    print(f"{title} - Year: {details.get('year')}, Rating: {details.get('rating')}")
        elif choice == 2:
            movie_title = input("Enter a movie title to fetch from OMDb API: ").strip()
            if movie_title:
                movie_data = fetch_movie_data_from_api(movie_title, api_key)
                if "error" in movie_data:
                    print(f"Error fetching movie data: {movie_data['error']}")
                else:
                    storage.add_movie(movie_data["title"], movie_data["year"], movie_data["rating"],
                                      movie_data["poster"], movie_data["poster_url"])
        elif choice == 3:
            title = input("Enter movie title to delete: ").strip()
            storage.delete_movie(title)
        elif choice == 4:
            movies = storage.list_movies()
            if not movies:
                print("No movies available to generate the website.")
            else:
                generate_website(movies, "template.html", "index.html")
        else:
            print("Invalid choice. Please select a valid option.")

    try:
        movie_app.run()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting...")