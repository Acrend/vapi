import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.getcwd()
data_file_path = os.path.join(BASE_DIR, "hard_database", "data.csv")

class DataBaseManip:
    def __init__(self, database):
        self.database = database
        self.index_list = list(database['id'])
        self.database['llm_sub_info'] = "# Titre\n" + self.database['name'].apply(str) + "\n\n# Déscription\n" + self.database['description'].apply(str) + "\n\n# Eligbilité\n" + self.database['eligibility'].apply(str)

    def format_sub(self, sub_id):
        return self.database[self.database['id'] == sub_id]["llm_sub_info"].values[0]

def load_db():
    global dbm
    try:
        data_at = pd.read_csv(data_file_path)
    except FileNotFoundError:
        raise Exception(f"Le fichier {data_file_path} est introuvable.")
    except pd.errors.EmptyDataError:
        raise Exception(f"Le fichier {data_file_path} est vide ou mal formaté.")

    data_at_select = data_at[['id', 'name', 'description', 'eligibility', 'project_examples']].dropna(subset=['description'])

    sub_min_description = 3000

    data_at_select = data_at_select[data_at_select['description'].apply(len) > sub_min_description].reset_index(drop=True)

    dbm = DataBaseManip(data_at_select)
    return dbm

# Charger les données à l'initialisation du module
load_db()