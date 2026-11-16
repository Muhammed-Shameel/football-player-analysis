import pandas as pd
import pickle
import json
import joblib
from backend.config import (
    PLAYER_DATA_PATH,
    DF_MODEL_PATH,
    TEAM_DATA_PATH,
    MANAGER_DATA_PATH,
    MANAGER_FORMATION_PATH,
    MANAGER_TACTICS_PATH,
    MANAGER_TACTIC_SUMMARY_PATH,
    LABEL_ENCODER_PATH
)

class DataService:
    def __init__(self):
        self.player_data = pd.DataFrame()
        self.df_model = pd.DataFrame()
        self.team_data = pd.DataFrame()
        self.manager_data = pd.DataFrame()
        self.manager_formation_data = pd.DataFrame()
        self.manager_tactics = {}
        self.manager_tactic_summary = {}
        self.label_encoder = None
        self.players_df = pd.DataFrame(columns=['Player_ID', 'Player_Name'])
        self.years = []
        self.tactic_columns = []
        
        self.load_all_data()

    def load_all_data(self):
        # Load player.xlsx
        try:
            self.player_data = pd.read_excel(PLAYER_DATA_PATH)
        except Exception as e:
            print(f"Error loading {PLAYER_DATA_PATH}: {e}")
            self.player_data = pd.DataFrame()

        # Load df_model.csv
        try:
            self.df_model = pd.read_csv(DF_MODEL_PATH)
        except Exception as e:
            print(f"Error loading {DF_MODEL_PATH}: {e}")
            self.df_model = pd.DataFrame()

        # Load team.csv
        try:
            try:
                self.team_data = pd.read_csv(TEAM_DATA_PATH, encoding='utf-8')
            except Exception:
                try:
                    self.team_data = pd.read_csv(TEAM_DATA_PATH, encoding='latin-1')
                except Exception:
                    self.team_data = pd.read_excel(TEAM_DATA_PATH)
        except Exception as e:
            print(f"Error loading {TEAM_DATA_PATH}: {e}")
            self.team_data = pd.DataFrame()

        # Load manager.xlsx
        try:
            self.manager_data = pd.read_excel(MANAGER_DATA_PATH)
        except Exception as e:
            print(f"Error loading {MANAGER_DATA_PATH}: {e}")
            self.manager_data = pd.DataFrame()

        # Load manager_formation.xlsx
        try:
            self.manager_formation_data = pd.read_excel(MANAGER_FORMATION_PATH)
        except Exception as e:
            print(f"Error loading {MANAGER_FORMATION_PATH}: {e}")
            self.manager_formation_data = pd.DataFrame()

        # Load manager tactics JSON
        try:
            with open(MANAGER_TACTICS_PATH, 'r') as f:
                self.manager_tactics = json.load(f)
        except Exception as e:
            print(f"Error loading {MANAGER_TACTICS_PATH}: {e}")
            self.manager_tactics = {}

        # Load manager tactic summary JSON
        try:
            with open(MANAGER_TACTIC_SUMMARY_PATH, 'r') as f:
                self.manager_tactic_summary = json.load(f)
        except Exception as e:
            print(f"Error loading {MANAGER_TACTIC_SUMMARY_PATH}: {e}")
            self.manager_tactic_summary = {}

        # Load label encoder
        try:
            try:
                self.label_encoder = joblib.load(LABEL_ENCODER_PATH)
            except Exception:
                with open(LABEL_ENCODER_PATH, 'rb') as f:
                    self.label_encoder = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load {LABEL_ENCODER_PATH}: {e}")

        # Process players list
        if not self.player_data.empty:
            try:
                self.players_df = self.player_data[['Player_ID', 'Common_Name']].drop_duplicates()
                self.players_df.columns = ['Player_ID', 'Player_Name']
            except Exception as e:
                print(f"Error processing player data: {e}")
                self.players_df = pd.DataFrame(columns=['Player_ID', 'Player_Name'])

        # Process years
        if not self.df_model.empty:
            try:
                self.years = sorted(self.df_model['Year'].unique().tolist())
            except Exception as e:
                print(f"Error getting years from df_model: {e}")
                self.years = []

        # Process tactic columns
        if not self.df_model.empty:
            self.tactic_columns = [col for col in self.df_model.columns if col.startswith('Tactic_Component_')]

data_service = DataService()
