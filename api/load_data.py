import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.getcwd()
data_file_path = os.path.join(BASE_DIR, "hard_database", "data.csv")

class DataBaseManip:
    def __init__(self, database):
        self.database = database
        self.index_list = list(database['id'])
        self.database = self.database.set_index('id')
        self.database['llm_sub_info'] = "# Titre\n" + self.database['name'].apply(str) + "\n\n# Déscription\n" + self.database['description'].apply(str) + "\n\n# Eligbilité\n" + self.database['eligibility'].apply(str)

    def format_sub(self, sub_id):
        return self.database.loc[sub_id]['llm_sub_info']

    def main_info_field(self,sub_id):
        at_main_link = "https://aides-territoires.beta.gouv.fr" 
        sub_at_link = at_main_link + dbm.database.loc[sub_id]['url']
        sub_deadline = dbm.database.loc[sub_id]['submission_deadline']
        sub_start = dbm.database.loc[sub_id]['start_date']
        sub_upper_rate = dbm.database.loc[sub_id]['subvention_rate_upper_bound']
        sub_lower_rate = dbm.database.loc[sub_id]['subvention_rate_lower_bound']

        return {'sub_at_link':sub_at_link,'sub_deadline':sub_deadline,'sub_start':sub_start}

    def second_info_field(self,sub_id):
        return {}

def load_db():
    global dbm
    try:
        data_at = pd.read_csv(data_file_path)
    except FileNotFoundError:
        raise Exception(f"Le fichier {data_file_path} est introuvable.")
    except pd.errors.EmptyDataError:
        raise Exception(f"Le fichier {data_file_path} est vide ou mal formaté.")

    # data_at_select = data_at[['id', 'name', 'description', 'eligibility', 'project_examples']].dropna(subset=['description'])
    data_at_select = data_at.dropna(subset=['description']).fillna("N/A")

    sub_min_description = 3000

    data_at_select = data_at_select[data_at_select['description'].apply(len) > sub_min_description].reset_index(drop=True)

    dbm = DataBaseManip(data_at_select)
    return dbm

# Charger les données à l'initialisation du module
load_db()