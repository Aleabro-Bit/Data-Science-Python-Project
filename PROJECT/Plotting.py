# Matplotlib is used for plotting the data
import matplotlib.pyplot as plt
import Manipulation as mp
import pandas as pd

class Plotting:
    def __init__(self, actors_file="top50Actors_updated.csv", movies_file="top50Actors_films.csv", manipulator=mp.Manipulation()):
        """
        Initializes the Plotting class by loading the required datasets and setting up the manipulator.
        
        Parameters:
        - actors_file: Path to the CSV file containing actors data.
        - movies_file: Path to the CSV file containing movie data.
        - manipulator: An instance of the Manipulation class used to process data.
        """
        # Load actor and movie data from CSV files
        try:
            self.actors = pd.read_csv(actors_file, dtype={'ID': str})
            self.movies = pd.read_csv(movies_file, dtype={'ID': str})
        except FileNotFoundError:
            print("Error: CSV file not found. Please ensure the CSV files exist.")
            
        self.manipulator = manipulator

    def plot_movies_by_genre(self, actor_id):
        """
        Plots a bar chart showing the distribution of movie genres for a given actor.
        
        Parameters:
        - actor_id: The ID of the actor for whom we want to plot the genre distribution.
        
        Returns:
        - Matplotlib plot: A bar plot of movie counts by genre for the actor.
        """
        # Get the list of movies for the specified actor
        actor_movies = self.manipulator.get_actor_movies(actor_id)
        
        # Split the genres into multiple entries for movies with more than one genre
        exploded_genres = actor_movies['Genre'].str.split(', ').explode()
        
        # Count the frequency of each genre
        genre_counts = exploded_genres.value_counts()

        # Plotting the genre distribution
        plt.figure(figsize=(10, 6))
        genre_counts.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title("Movie Counts by Genre", fontsize=16)
        plt.xlabel("Genre", fontsize=14)
        plt.ylabel("Number of Movies", fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        return plt  # Returning the plot for Streamlit to display

    def plot_genre_distribution(self, threshold=4):
        """
        Plots a pie chart showing the distribution of genres across all movies.
        Genres that represent less than a specified percentage (threshold) are grouped into "Other".
        
        Parameters:
        - threshold: The percentage threshold below which genres are grouped as "Other". Default is 4%.
        
        Returns:
        - Matplotlib plot: A pie chart of genre distribution.
        """
        # Explode the 'Genre' column to split multiple genres into separate rows
        exploded_genres = self.movies['Genre'].str.split(', ').explode()
        
        # Count the frequency of each genre
        genre_counts = exploded_genres.value_counts()
        
        # Calculate the percentage distribution of each genre
        genre_percentage = genre_counts / genre_counts.sum() * 100
        
        # Separate genres below the threshold to group them as 'Other'
        other_genres = genre_percentage[genre_percentage < threshold]
        genre_counts = genre_counts[genre_percentage >= threshold]
        
        # Add 'Other' if there are genres below the threshold
        if len(other_genres) > 0:
            genre_counts['Other'] = other_genres.sum()  # Combine smaller genres into 'Other'

        # Plotting the genre distribution as a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title("Genre Distribution of All Movies", fontsize=14)
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
        
        return plt  # Returning the plot for Streamlit to display
