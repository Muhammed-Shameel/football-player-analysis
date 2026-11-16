import os
import pickle
import joblib
import numpy as np
import pandas as pd
from backend.config import MODELS
from backend.services.data_service import data_service

class MLService:
    def load_model(self, model_name):
        """Load the specified model - with joblib and pickle fallback"""
        model_path = MODELS.get(model_name)
        if model_path and os.path.exists(model_path):
            try:
                try:
                    return joblib.load(model_path)
                except Exception:
                    with open(model_path, 'rb') as f:
                        return pickle.load(f)
            except Exception as e:
                print(f"Error loading model {model_name}: {e}")
                return None
        return None

    def get_player_features(self, player_id, year=None):
        """Get features for a specific player, optionally filtered by year"""
        if data_service.df_model.empty:
            return None
            
        player_tactic_data = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
        if year:
            player_tactic_data = player_tactic_data[player_tactic_data['Year'] == year]
        
        if len(player_tactic_data) == 0:
            return None
        
        feature_columns = ['Start_encoded', 'CrdY_flag', 'CrdR_flag', 'Outcome_encoded', 
                          'Venue_Away', 'Venue_Home', 'PK_bin', 'PKatt_bin', 'Passing', 
                          'Shooting', 'Creativity', 'Dribbling', 'Defense', 'Impact_Score', 
                          'Year_Encoded', 'Pos_Attacking Mid', 'Pos_Central Mid', 
                          'Pos_Centre Back', 'Pos_Defensive Mid', 'Pos_Forward', 
                          'Pos_Left Back', 'Pos_Left Winger', 'Pos_Right Back']
        
        try:
            features_series = player_tactic_data[feature_columns].mean()
            if isinstance(features_series, pd.Series):
                features_array = features_series.values.astype(float)
            else:
                features_array = np.array([float(features_series)], dtype=float)
            return features_array.reshape(1, -1)
        except Exception as e:
            print(f"Error converting features: {e}")
            return None

    def get_player_scores(self, player_id, year=None):
        """Get player scores for a specific year or all years if year is None"""
        if data_service.df_model.empty:
            return None
            
        player_data_filtered = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
        if year:
            player_data_filtered = player_data_filtered[player_data_filtered['Year'] == year]
        
        if len(player_data_filtered) == 0:
            return None
        
        try:
            scores = {
                'Passing': float(player_data_filtered['Passing'].mean()),
                'Shooting': float(player_data_filtered['Shooting'].mean()),
                'Creativity': float(player_data_filtered['Creativity'].mean()),
                'Dribbling': float(player_data_filtered['Dribbling'].mean()),
                'Defense': float(player_data_filtered['Defense'].mean())
            }
            return scores
        except Exception as e:
            print(f"Error calculating player scores: {e}")
            return None

    def get_aggregated_player_data(self, player_id):
        """Get aggregated player data across all years"""
        if data_service.df_model.empty:
            return None
            
        player_data_all_years = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
        if len(player_data_all_years) == 0:
            return None
        
        try:
            aggregated_data = {
                'Passing': float(player_data_all_years['Passing'].mean()),
                'Shooting': float(player_data_all_years['Shooting'].mean()),
                'Creativity': float(player_data_all_years['Creativity'].mean()),
                'Dribbling': float(player_data_all_years['Dribbling'].mean()),
                'Defense': float(player_data_all_years['Defense'].mean()),
                'Impact_Score': float(player_data_all_years['Impact_Score'].mean()),
                'Best_Tactic': 'Unknown'
            }
            
            if 'Best_Tactic' in player_data_all_years.columns:
                mode_series = player_data_all_years['Best_Tactic'].mode()
                if not mode_series.empty:
                    aggregated_data['Best_Tactic'] = str(mode_series.iloc[0])
            
            return aggregated_data
        except Exception as e:
            print(f"Error getting aggregated player data: {e}")
            return None

    def get_formation_for_component(self, component):
        mapping = {
            'Tactic_Component_1': '4-3-3 Possession / Attacking',
            'Tactic_Component_2': '4-2-3-1 Balanced / Direct',
            'Tactic_Component_3': '3-5-2 Wing-Back Overload',
            'Tactic_Component_4': '4-4-2 Low Block / Counter',
            'Tactic_Component_5': '4-3-1-2 Narrow Diamond',
            'Tactic_Component_6': '5-3-2 Defensive Resilience',
            'Tactic_Component_7': '4-1-4-1 High Press'
        }
        return mapping.get(component, 'Standard Tactical Setup')

    def get_tactic_description(self, component):
        mapping = {
            'Tactic_Component_1': 'Focuses on short passing, high possession, and creating chances through sustained build-up play.',
            'Tactic_Component_2': 'Emphasizes quick transitions, direct passing, and exploiting space behind defensive lines.',
            'Tactic_Component_3': 'Utilizes wing-backs for width, overlapping runs, and crossing opportunities into the box.',
            'Tactic_Component_4': 'Prioritizes defensive solidity, disciplined shape, and rapid counter-attacks upon winning possession.',
            'Tactic_Component_5': 'Congests the central midfield, encouraging quick one-twos and through balls from the attacking midfielder.',
            'Tactic_Component_6': 'Strengthens the defensive line with three center-backs and two wing-backs to neutralize opposition threats.',
            'Tactic_Component_7': 'Applies intense pressure high up the pitch to force turnovers and immediate scoring opportunities.'
        }
        return mapping.get(component, 'General tactical component maximizing player output.')

    def get_shared_tactical_recommendations(self, player_id, model_name='XGBoost', year=None):
        """Shared function for getting tactical recommendations"""
        try:
            if data_service.df_model.empty:
                return {'error': 'Model data not available - df_model.csv not loaded'}
            
            player_model_data = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
            if len(player_model_data) == 0:
                return {'error': f'Player {player_id} not found in model data'}
            
            year_int = None
            if year and str(year).strip() and str(year).lower() not in ['all', 'all years']:
                try:
                    year_int = int(year)
                except ValueError:
                    return {'error': f'Invalid year format: {year}'}
            
            if year_int:
                year_data = player_model_data[player_model_data['Year'] == year_int]
                if len(year_data) == 0:
                    return {'error': f'No data found for player {player_id} in year {year_int}'}
                player_model_data = year_data
            
            recommendations = []
            best_tactic_data = None
            
            for component in data_service.tactic_columns:
                try:
                    value = round(float(player_model_data[component].mean()), 2)
                    recommendations.append({
                        'component': component,
                        'value': value,
                        'impact': value
                    })
                except Exception:
                    continue
            
            if recommendations:
                best_recommendation = max(recommendations, key=lambda x: x['value'])
                best_tactic = best_recommendation['component']
                tactic_value = best_recommendation['value']
                best_tactic_data = {
                    'component': best_tactic,
                    'value': tactic_value,
                    'formation': self.get_formation_for_component(best_tactic),
                    'description': self.get_tactic_description(best_tactic)
                }
            
            return {
                'recommendations': recommendations,
                'best_tactic_data': best_tactic_data,
                'player_model_data': player_model_data
            }
        except Exception as e:
            print(f"Error in get_shared_tactical_recommendations: {e}")
            return {'error': f'Error generating tactical recommendations: {str(e)}'}

ml_service = MLService()
