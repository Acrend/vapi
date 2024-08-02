import pandas as pd

data_at = pd.read_csv("hard_database/data.csv")
data_at_select = data_at[['id','name','description','eligibility','project_examples']].dropna(subset='description')

sub_min_description = 3000

data_at_select = data_at_select[data_at_select['description'].apply(len)>sub_min_description].reset_index(drop=True)

class DataBaseManip():
    def __init__(self,database):
        self.database = database
        self.index_list = list(database['id'])
        self.database['llm_sub_info'] = "# Titre\n" + self.database['name'].apply(str) + "\n\n# Déscription\n"  + self.database['description'].apply(str) + "\n\n# Eligbilité\n"  + self.database['eligibility'].apply(str)
        
    def format_sub(self,sub_id):
        return self.database[self.database['id']==sub_id]["llm_sub_info"][0]


dbm = DataBaseManip(data_at_select)