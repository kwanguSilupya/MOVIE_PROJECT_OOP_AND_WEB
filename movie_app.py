class MovieApp:
    def __init__(self, storage):
        """
        Initializes the MovieApp with a given storage interface.
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        Lists all the movies stored in the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
        else:
            for title, details in movies.items():
                year = details.get("year", "Unknown year")
                rating = details.get("rating", "Unknown rating")
                poster = details.get("poster", "No poster available")
                print(f"{title} - Year: {year}, Rating: {rating}, Poster: {poster}")

    def _command_movie_stats(self):
        """
        Displays movie statistics such as total number of movies and average rating.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found to display statistics.")
            return

        try:
            total_ratings = sum(float(movie.get("rating", 0)) for movie in movies.values() if movie.get("rating"))
            average_rating = total_ratings / len(movies)
            print(f"Total movies: {len(movies)}")
            print(f"Average rating: {average_rating:.2f}")
        except ValueError as e:
            print(f"Error calculating statistics: {e}")

    def _generate_website(self):
        """
        Generate a simple webpage from the movie list (optional).
        """
        movies = self._storage.list_movies()
        with open("movies.html", "w") as file:
            file.write("<html><head><title>Movies</title></head><body><h1>Movies List</h1><ul>")
            for title, details in movies.items():
                file.write(f"<li>{title} - Year: {details.get('year', 'N/A')}, Rating: {details.get('rating', 'N/A')}</li>")
            file.write("</ul></body></html>")
        print("Website generated: movies.html")

    def run(self):
        """
        Runs the app, displays the menu, and executes the user commands.
        """
        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Movie Stats")
            print("4. Generate Website")

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
                self._command_list_movies()
            elif choice == 2:
                title = input("Enter movie title: ").strip()
                try:
                    year = int(input("Enter movie release year: "))
                    rating = float(input("Enter movie rating (0.0 - 10.0): "))
                    poster = input("Enter movie poster URL or path: ").strip()
                    self._storage.add_movie(title, year, rating, poster)
                except ValueError:
                    print("Invalid input. Year must be an integer and rating must be a number.")
            elif choice == 3:
                self._command_movie_stats()
            elif choice == 4:
                self._generate_website()
            else:
                print("Invalid choice. Please select a valid option.")