import json
import requests
import pandas as pd

class TMDBActorData:
    def __init__(self, api_key, api_key_rapid):
        """
        Constructor to initialize the object with the TMDB and RAPID API key.
        """
        self.api_key = api_key
        self.api_key_rapidapi = api_key_rapid
        # Headers for accessing the TMDB API
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        #Headers for accessing the RAPID API
        self.headers_rapidapi = {
            "X-RapidAPI-Key": self.api_key_rapidapi,
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }

    # Function to find an actor by their ID in the TMDB API
    def find_actor(self, actor_id):
        url_actor = f"https://api.themoviedb.org/3/find/nm{actor_id}?external_source=imdb_id&language=english"
        response = requests.get(url_actor, headers=self.headers)
        return response.json()

    # Function to get movie details by its ID from the TMDB API
    def get_movie_details(self, movie_id):
        url_movie = f"https://api.themoviedb.org/3/movie/{movie_id}"
        response = requests.get(url_movie, headers=self.headers)
        return response.json()

    # Function to get actor details by their ID from the TMDB API
    def get_actor_details(self, actor_id):
        url_actor = f"https://api.themoviedb.org/3/person/{actor_id}"
        response = requests.get(url_actor, headers=self.headers)
        return response.json()

    # Function to check if the actor was found in the response
    def actor_founded(self, data):
        if 'person_results' in data and len(data['person_results']) > 0:
            return True
        return False

    # Function to get film data (movie credits) for an actor
    def get_film_data(self, actor_id):
        url_films = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits"
        response_films = requests.get(url_films, headers=self.headers)
        return response_films.json()

    #This function retrieves an actor's awards using Rapid's API
    def get_actor_awards(self,actor_id):
       
        url = "https://imdb8.p.rapidapi.com/actors/get-awards"
        actor_id = str(actor_id)
        querystring = {"nconst": f"nm{actor_id}"}  

        try:
            response = requests.get(url, headers=self.headers_rapidapi, params=querystring)
            response.raise_for_status()  
            data = response.json()
            
            awards_list = set()
            if "resource" in data and "awards" in data["resource"]:
                for award in data["resource"]["awards"]:
                    award_title = award.get("awardName", "Unknown Award")
                    award_year = award.get("year", "Unknown Year")
                    awards_list.add(f"{award_title} {award_year}")
            
            return awards_list if awards_list else ["No awards found."]
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching actor awards: {e}")
            return ["Error fetching data."]

    # Function to build a dataframe of actors with additional details
    def build_actor_dataframe(self, actors_file='top50Actors.csv', output_file='top50Actors_updated.csv'):
        try:
            df = pd.read_csv(actors_file, dtype={'ID': str})
        except FileNotFoundError:
            print(f"Error: {actors_file} not found. Please ensure the file exists.")
            return
        
        # Add new columns to the dataframe for actor details
        df['Birth Place'] = ""
        df['Gender'] = ""
        df['Profile Picture URL'] = ""
        df['Awards'] = ""
        df['Biography'] = ""

        # Iterate over each actor in the dataframe
        for idx, ID in df.iterrows():
            data = self.find_actor(ID['ID'])
            if self.actor_founded(data):
                actor_id = data['person_results'][0]['id']
                actor_details = self.get_actor_details(actor_id)

                birth_place = actor_details.get('place_of_birth', 'place of birth not available')
                gender = 'Male' if actor_details.get('gender') == 2 else 'Female' if actor_details.get('gender') == 1 else 'Not specified'
                profile_path = actor_details.get('profile_path', None)
                awards = self.get_actor_awards(ID['ID'])
                biography = actor_details.get('biography', 'Biography not available')
                
                # Construct the profile image URL if available
                profile_image_url = f"https://image.tmdb.org/t/p/w500{profile_path}" if profile_path else "Profile picture not available"

                # Add the details to the dataframe
                df.at[idx, 'Birth Place'] = birth_place
                df.at[idx, 'Gender'] = gender
                df.at[idx, 'Profile Picture URL'] = profile_image_url
                df.at[idx, 'Biography'] = biography
                df.at[idx, 'Awards'] = awards
                
                
            else:
                print(f"Couldn't find actor with ID {ID['ID']}.")

        # Save the updated dataframe to a new CSV file
        df.to_csv(output_file, index=False)

    # Function to build a dataframe of movies for each actor
    def build_movie_dataframe(self, actors_file='top50Actors.csv', output_file='top50Actors_films.csv'):
        try:
            df = pd.read_csv(actors_file, dtype={'ID': str})
        except FileNotFoundError:
            print(f"Error: {actors_file} not found. Please ensure the file exists.")
            return
        
        # Create an empty list to store movie data
        films_list = []

        # Iterate over each actor in the dataframe
        for ID in df['ID']:
            data = self.find_actor(ID)
            if self.actor_founded(data):
                actor_id = data['person_results'][0]['id']
                actor_name = data['person_results'][0]['name']
                films_data = self.get_film_data(actor_id)

                if 'cast' in films_data and len(films_data['cast']) > 0:
                    # Iterate over each movie of the actor
                    for film in films_data['cast']:
                        movie_id = film['id']
                        movie_title = film['title']

                        # Get the movie details
                        movie_details = self.get_movie_details(movie_id)
                        genres = ', '.join([genre['name'] for genre in movie_details['genres']])
                        rating = movie_details['vote_average'] if movie_details['vote_average'] > 0 else 'Rating not available'

                        release_date = film.get('release_date', 'release date not available')
                        release_year = release_date[:4] if release_date != 'release date not available' else release_date

                        # Add movie details to the list
                        films_list.append({
                            'ID': ID,
                            'Actor': actor_name,
                            'Title': movie_title,
                            'Release Year': release_year,
                            'Genre': genres,
                            'Rating': rating
                        })
            else:
                print(f"Couldn't find any movie for actor with ID {ID}.")

        # Create a dataframe from the movie list
        films_df = pd.DataFrame(films_list)
        # Save the dataframe to a CSV file
        films_df.to_csv(output_file, index=False)
        print(f"Movie data saved to {output_file}")



