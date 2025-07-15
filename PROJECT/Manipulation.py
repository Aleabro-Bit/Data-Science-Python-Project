import pandas as pd

class Manipulation:
    def __init__(self, actors_file="top50Actors_updated.csv", movies_file="top50Actors_films.csv"):
        # Load the CSV files only once during initialization
        try:
            self.actors = pd.read_csv(actors_file, dtype={'ID': str})
            self.movies = pd.read_csv(movies_file, dtype={'ID': str})
        except FileNotFoundError:
            print("Error: CSV file not found. Please ensure the csv exists.")

    # Given an actor ID, this method returns the actor's movies from the movies dataframe
    def get_actor_movies(self, actor_id):
        actor_movies = self.movies[self.movies['ID'] == actor_id]
        if actor_movies.empty:
            print(f"No movies found for actor with ID {actor_id}.")
        return actor_movies

    # Method to filter the ratings, it drops non-numeric values and sorts the data
    def filtering_ratings(self, movie_data):
        # Remove movies with "Rating not available" and convert ratings to numeric
        movie_data = movie_data[movie_data['Rating'] != 'Rating not available']
        movie_data['Rating'] = pd.to_numeric(movie_data['Rating'], errors='coerce')
        # Drop rows where Rating is NaN (after conversion)
        movie_data = movie_data.dropna(subset=['Rating'])
        return movie_data

    # Method to get the top 5 movies based on the rating from any given movie data
    def get_top_movies(self, movie_data):
        movie_data = self.filtering_ratings(movie_data)  # Filter the movie data first
        top_movies = movie_data.sort_values(by='Rating', ascending=False).head(5)
        return top_movies

    # Method to get the top 5 movies of an actor based on their movies' ratings
    def actor_top_movies(self, actor_id):
        # Fetch actor's movies
        actor_movies = self.get_actor_movies(actor_id)
        if actor_movies.empty:
            return pd.DataFrame()  # Return an empty DataFrame if no movies found for the actor
        # Get the top movies from the actor's movies
        return self.get_top_movies(actor_movies)

    # Method to get average rating of movies from an actor
    def actor_avg_rating(self, actor_id):
        actor_movies = self.get_actor_movies(actor_id)
        if actor_movies.empty:
            return None  # If no movies are found for the actor
        actor_movies = self.filtering_ratings(actor_movies)
        average_rating = actor_movies['Rating'].mean()
        return average_rating
