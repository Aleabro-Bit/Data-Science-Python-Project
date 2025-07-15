import Actors
import ActorsWebsiteApp 
import pandas as pd

class Main:
    def __init__(self):
        try:
            self.actors_df = pd.read_csv("top50Actors.csv")
        except FileNotFoundError:
            print("Error: CSV file not found. Please ensure 'top50Actors.csv' exists before running the program.")
        

    def execute (self):
        """
        This function will retrieve the top 50 actors list from the .csv file 
        and update the file by dropping unnecessary columns and renaming the 'Const' column to 'ID'
        To be executed only once
        """
        self.actors = Actors.Actors()
        self.actors.csvManipulation(['Created','Modified', 'Description'])
        
        
        #This function will create the website
        #After running this function type to the terminal: streamlit run Main.py
        #NOTE: IF THE PROGRAM IS STILL CREATING THE CSV FILES, 
        #WAIT FOR IT TO FINISH BEFORE RUNNING THE WEBSITE
        
        
        self.website = ActorsWebsiteApp.ActorsWebsiteApp()
        self.website.run()
        
        

if __name__ == "__main__":
    main = Main()
    main.execute()
        