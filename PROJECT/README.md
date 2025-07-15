Instructions for using the code

This code was created to collect, manipulate, and correlate data about a top 50 actor list from a
given IMDb dataset (found in the .zip file). It retrieves information about the listed actors, the
movies they starred in, and additional details about those movies. The code can also work with any
list of actors/movies, as long as the IDs are recognized by the TMDB API (some adjustments may be 
needed in such cases). Specifically, this code gathers the following information about actors/actresses:

- Actors/Actresses biography 
- Awards to actor/actresses in different years
- Movie names, genres, ratings, and release years

Required Libraries
To execute this code correctly, you need the following libraries:

- Pandas:

	Official installation guide: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
	Install command via pip: pip install pandas

- Streamlit:

	Official installation guide: https://docs.streamlit.io/library/get-started/installation
	Install command via pip: pip install streamlit


- Matplotlib:

	Official installation guide: https://matplotlib.org/stable/users/installing.html
	Install command via pip: pip install matplotlib

Steps to use the program:
1. Prepare the Files
Ensure that all classes and files are located in the same directory. It is advised to extract the files
from the .zip archive to avoid issues. While it is possible to run the program directly 
within the archive, keep in mind that the .csv files will be saved outside the directory.

2. Setup Requirements
Ensure a stable internet connection to retrieve data.
Place a .csv file containing the actor IDs in the same directory, and name it top50Actors.csv 
(make a backup copy, as the file will be modified).

3. Initial Data Processing
The Actors class processes the top50Actors.csv file by:
Dropping unnecessary columns ('Created', 'Modified', 'Description' by default, but this can be customized).
Renaming the 'Const' column to 'ID'.
Removing non-numeric values from the 'ID' column.
These modifications are optional but make the file more readable and easier to use. 
This step is only required the first time, as the changes are saved to the original file.

4. Fetch Additional Data
Use the Fetcher class to retrieve more data via the TMDB API and RAPID API. For access, 
you will need API keys, which can be obtained by creating accounts (both APIs are open source).
For RAPID look for IMDb API and subscribe with a free plan (API used: https://rapidapi.com/apidojo/api/imdb8/playground/apiendpoint_9470f3e3-8e65-4450-98f8-1c9dd538e289). 
After entering the keys (the keys can be entered in ActorsWebsiteApp constructor):
The build_actor_dataframe() method adds more details to top50Actors.csv and saves it as top50Actors_updated.csv.
The build_movie_dataframe() method creates another file, top50Actors_films.csv, containing movies each actor 
has starred in, their ratings, genres, and release years.
Note: Retrieving data for movies and awards may take a few minutes. 
For faster execution, consider using NVIDIA CUDA technology or optimizing with a lower-level/multi-threaded language.

5. Run the User Interface
To display the user interface, run the ActorsWebsiteApp class. Use the following command to launch the local website:
streamlit run "name_of_the_class.py" (in this case streamlit run Main.py)
If this command doesn't work, try:
python -m streamlit "name_of_the_class.py"
Ensure you run the command from the correct directory.
A browser window will open, displaying the interface, which allows users to explore the dataset interactively.

NOTES:
If the program is not running correctly, try extracting all files from the archive.
Ensure the correct directory structure and API key setup before running.

