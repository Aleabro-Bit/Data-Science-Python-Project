import streamlit as st
import pandas as pd
import Manipulation as mp
import Plotting as plt
import os
import Fetcher 

class ActorsWebsiteApp:
    def __init__(self):
        """
        This function will retrieve all data from TMDB API
        and update the actor dataframe/csv file with additional details and create
        the movie dataframe/csv file with movie details
        NOTE: ---INSERT YOUR API KEY IN THE FETCHER FUNCTION---
        To be executed only once
        """      
        if not os.path.exists("top50Actors_updated.csv") or not os.path.exists("top50Actors_films.csv"):
            print("CSV files not found. Creating files using Fetcher.")
            #PUT YOUR TMDB API KEY DOWN HERE AS FIRST ARGUMENT AND RAPID'S KEY AS SECOND
            self.fetcher = Fetcher.TMDBActorData(
                "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNGRkYzE3OGYwYWE0M2Q0MzYzNTUxNWFkMGQxMDU0MiIsIm5iZiI6MTczMjMyNDI0My4xODQsInN1YiI6IjY3NDEyYjkzNGEzZGMxNzgxNzNkNDZhZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.036ytlNgFHhTSA53Z75E5ORRG5T9ush8_s8w3yIOngI",
                "1c2f6ccd2emsh3fef5ccd1a88e8ap1e1f51jsn8a60c5d18428"
            )
            if not os.path.exists("top50Actors_updated.csv"):
                self.fetcher.build_actor_dataframe()
            if not os.path.exists("top50Actors_films.csv"):
                self.fetcher.build_movie_dataframe()

        # Loading CSV files
        try:
            self.actors = pd.read_csv("top50Actors_updated.csv", dtype={'ID': str})
            self.movies = pd.read_csv("top50Actors_films.csv", dtype={'ID': str})
        except Exception as e:
            print(f"Error loading CSV files: {e}")
            raise FileNotFoundError("Required CSV files could not be found or created.")
        self.manipulator = mp.Manipulation()
        self.plotter = plt.Plotting()
        self.df = pd.DataFrame({
            "Name": self.actors["Name"],
            "ID": self.actors["ID"]
        })
            

    def run(self):
        st.title("🎥 Top 50 Hollywood Actors and Actresses")
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", [
            "Home Page", "Actor List", "Movie List", "Actor Details",
            "Average Rating (All time)", "Average Rating (each year)",
            "Top 5 Movies of all time", "Actor Awards"])

        if page == "Home Page":
            self.homepage()
        elif page == "Actor List":
            self.show_actor_list()
        elif page == "Actor Details":
            self.actor_details()
        elif page == "Movie List":
            self.movie_list()
        elif page == "Top 5 Movies of all time":
            self.goat_movies()
        elif page == "Average Rating (All time)":
            self.avg_movie_rating()
        elif page == "Average Rating (each year)":
            self.avg_year_rating()
        elif page == "Actor Awards":
            self.show_awards()

    def homepage(self):
        st.header("🌟 Welcome!")
        st.markdown(
            """
            Welcome to the **Top 50 Hollywood Actors and Actresses** website! 🎬  
            Explore the world of cinema's most iconic stars and their incredible work.  
            Use the sidebar to navigate through our features:
            """
        )
        st.subheader("🔎 What You Can Find Here")
        st.markdown(
            """
            - **Actor List**: Browse through the top 50 actors and actresses.  
            - **Movie List**: Explore movies featuring these stars.  
            - **Actor Details**: Dive into individual profiles with detailed information.  
            - **Average Ratings**: See how their movies perform over time.  
            - **Top 5 Movies**: Discover the highest-rated movies ever!  
            """
        )
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hollywood_Sign_%28Zuschnitt%29.jpg/1200px-Hollywood_Sign_%28Zuschnitt%29.jpg", 
                 use_container_width=True, caption="Explore Hollywood's Best")

        st.markdown("---")
        st.caption("✨ Created with Streamlit | Data powered by TMDB API")

    def show_actor_list(self):
        st.header("List of Top 50 Actors")
        st.dataframe(self.df)  # Display the table of actors

    def actor_details(self):
        st.header("Actor Details")
        actor_name = st.selectbox("Choose an actor:", self.df["Name"])
        actor_id = self.df[self.df["Name"] == actor_name]["ID"].iloc[0]
        
        # Display the actor's profile picture
        profile_image_url = self.actors[self.actors['ID'] == actor_id]['Profile Picture URL'].values[0]
        if profile_image_url and profile_image_url != "Profile picture not available":
            st.image(profile_image_url, caption=actor_name, width=150)
        
        details = {
            "Birth Date": self.actors[self.actors['ID'] == actor_id]['Birth Date'].values[0],
            "Birth Place": self.actors[self.actors['ID'] == actor_id]['Birth Place'].values[0],
            "Gender": self.actors[self.actors['ID'] == actor_id]['Gender'].values[0],
            "Famous for": self.actors[self.actors['ID'] == actor_id]['Known For'].values[0], 
            "Biography":  self.actors[self.actors['ID'] == actor_id]['Biography'].values[0]
        }
        
        for label, value in details.items():
            st.text(f"{label}: {value}")

        st.write("Actor's top 5 Movies:")
        st.write(self.manipulator.actor_top_movies(actor_id)[['Title', 'Release Year', 'Genre', 'Rating']])
        st.write("Filmography:")
        st.write(self.movies[self.movies['ID'] == actor_id][['Title', 'Release Year', 'Genre', 'Rating']])
        st.pyplot(self.plotter.plot_movies_by_genre(actor_id))

    def movie_list(self):
        st.header("List of Movies")
        unique_movies = self.movies.drop_duplicates(subset=['Title'])
        unique_movies = unique_movies[['Title', 'Release Year', 'Genre', 'Rating']]
        st.dataframe(unique_movies)
        st.pyplot(self.plotter.plot_genre_distribution())

    def goat_movies(self):
        st.header("Top 5 Movies of all time")
        st.write("Here are the top movies from the dataset:")
        st.caption("(ratings are based on the TMDB rating)")
        top_movies = self.manipulator.get_top_movies(self.movies)
        for _, movie in top_movies.iterrows():
            st.write(f"Title: {movie['Title']}, Rating: {movie['Rating']}, Year: {int(movie['Release Year'])}")

    def avg_movie_rating(self):
        actor_name = st.selectbox("Choose an actor for their average rating:", self.df["Name"])
        actor_id = self.df.loc[self.df["Name"] == actor_name, "ID"].iloc[0]
        actor_movies = self.manipulator.get_actor_movies(actor_id)
        actor_movies = self.manipulator.filtering_ratings(actor_movies)
        if not actor_movies.empty:  
            mean_rating = actor_movies['Rating'].mean()
            st.write(f"The average rating for {actor_name} is: {mean_rating:.2f}")
        else:
            st.write(f"No valid ratings available for {actor_name}.")

    def avg_year_rating(self):
        st.header("Average Rating of Movies Each Year")
        actor_name = st.selectbox("Choose an actor for their average rating:", self.df["Name"])
        actor_id = self.df.loc[self.df["Name"] == actor_name, "ID"].iloc[0]
        movies_filtered = self.movies[self.movies['ID'] == actor_id]
        movies_filtered = self.manipulator.filtering_ratings(movies_filtered)   
        movies_filtered['Release Year'] = pd.to_numeric(movies_filtered['Release Year'], errors='coerce')
        movies_filtered = movies_filtered.dropna(subset=['Release Year'])
        if not movies_filtered.empty:
            average_ratings = movies_filtered.groupby('Release Year')['Rating'].mean()
            st.write(average_ratings)
        else:
            st.write("No valid ratings available for movies.")

    def show_awards(self):
        st.header("Actor Awards")
        actor_name = st.selectbox("Choose an actor:", self.df["Name"])
        actor_id = self.df[self.df["Name"] == actor_name]["ID"].iloc[0]

        awards = self.actors[self.actors['ID'] == actor_id]["Awards"].values[0]
        
        formatted_awards = awards.replace(", ", "\n") \
                         .replace("{", "") \
                         .replace("}", "") \
                         .replace("'", "")
        st.write("Awards:")
        st.text(formatted_awards)
        