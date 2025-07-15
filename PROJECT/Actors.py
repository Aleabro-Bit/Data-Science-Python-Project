import pandas as pd

class Actors:
    def __init__(self):
        try:
            self.topActors = pd.read_csv("top50Actors.csv")
        except FileNotFoundError:
            print("Error: CSV file not found. Please ensure 'top50Actors.csv' exists.")
            self.topActors = pd.DataFrame()  # Initialize an empty DataFrame as fallback

    def csvManipulation(self, columns_to_drop):
        try:
            if 'ID' in self.topActors.columns and not any(column in self.topActors.columns for column in columns_to_drop):
                #print("The .csv file was already updated, no futher action needed.")
                return
            # Drop unnecessary columns
            self.topActors = self.topActors.drop(columns=columns_to_drop, axis=1)
            # Rename "Const" column to "ID" only if Const column exists
            if 'Const' in self.topActors.columns:
                self.topActors = self.topActors.rename(columns={'Const': 'ID'})
            # Removing the 'nm' prefix from the 'ID' column
            if 'ID' in self.topActors.columns:
                self.topActors['ID'] = self.topActors['ID'].apply(lambda x: x[2:] if isinstance(x, str) else x)
            # Save updated DataFrame back to CSV
            self.topActors.to_csv("top50Actors.csv", index=False)
        except KeyError as e:
            print(f"Error: Column not found - {e}")
    
    """
    Unused Methods
    """
    # Retrieve the list of actor names
    def getNameList(self):
        try:
            return self.topActors["Name"]
        except KeyError:
            print("Error: 'Name' column not found in the CSV.")
            return []

    def printList(self):
        # Print the current DataFrame
        if not self.topActors.empty:
            print(self.topActors)
        else:
            print("No data available.")





        
                
        