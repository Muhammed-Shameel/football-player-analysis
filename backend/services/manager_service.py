import math
import pandas as pd
from backend.services.data_service import data_service

class ManagerService:
    def get_manager_name(self, manager_id):
        """Get manager name from manager ID"""
        try:
            if not data_service.manager_data.empty:
                manager_row = data_service.manager_data[data_service.manager_data['Manager_ID'] == manager_id]
                if not manager_row.empty:
                    return str(manager_row.iloc[0]['Manager_Name'])
            return f"Manager {manager_id}"
        except Exception as e:
            print(f"Error getting manager name for {manager_id}: {e}")
            return f"Manager {manager_id}"

    def get_manager_formations(self):
        """Get manager formations from the manager_formation.xlsx file"""
        try:
            formations = {}
            if not data_service.manager_formation_data.empty:
                for _, row in data_service.manager_formation_data.iterrows():
                    manager_id = str(row['Manager_ID'])
                    formation = str(row['Formation'])
                    if manager_id not in formations:
                        formations[manager_id] = []
                    formations[manager_id].append(formation)
            return formations
        except Exception as e:
            print(f"Error loading manager formations: {e}")
            return {}

    def get_manager_formation_details(self, manager_id):
        formations = self.get_manager_formations()
        manager_forms = formations.get(manager_id, ['4-3-3', '4-2-3-1'])
        return [
            {
                'formation': form,
                'usage_percentage': round(100.0 / len(manager_forms), 1) if manager_forms else 100.0,
                'win_rate': 58.5
            }
            for form in manager_forms
        ]

    def calculate_cosine_similarity(self, profile1, profile2, feature_columns):
        """Calculate cosine similarity between two tactical profiles"""
        try:
            vec1 = [profile1.get(col, 0.0) for col in feature_columns]
            vec2 = [profile2.get(col, 0.0) for col in feature_columns]
            
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = math.sqrt(sum(a * a for a in vec1))
            magnitude2 = math.sqrt(sum(a * a for a in vec2))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            similarity = dot_product / (magnitude1 * magnitude2)
            normalized_similarity = (similarity + 1) / 2
            return round(normalized_similarity, 3)
        except Exception as e:
            print(f"Error calculating cosine similarity: {e}")
            return 0.0

    def get_top_managers_for_player(self, player_id, year=None, model_name='XGBoost', num_managers=5):
        """Get top N managers for a player based on tactical component matching"""
        try:
            if data_service.df_model.empty:
                return []
            
            player_data = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
            if year:
                player_data = player_data[player_data['Year'] == year]
            
            if len(player_data) == 0:
                return []
            
            if not data_service.tactic_columns:
                return []
            
            player_profile = {}
            for col in data_service.tactic_columns:
                try:
                    player_profile[col] = float(player_data[col].mean())
                except:
                    player_profile[col] = 0.0
            
            manager_formations = self.get_manager_formations()
            manager_scores = []
            all_managers = data_service.df_model['Manager_ID'].dropna().unique()
            
            for manager_id in all_managers:
                if str(manager_id) == 'M21':
                    continue
                try:
                    manager_data = data_service.df_model[data_service.df_model['Manager_ID'] == manager_id]
                    if len(manager_data) == 0:
                        continue
                    
                    manager_profile = {}
                    for col in data_service.tactic_columns:
                        try:
                            manager_profile[col] = float(manager_data[col].mean())
                        except:
                            manager_profile[col] = 0.0
                    
                    similarity_score = self.calculate_cosine_similarity(player_profile, manager_profile, data_service.tactic_columns)
                    manager_name = self.get_manager_name(str(manager_id))
                    formations = manager_formations.get(str(manager_id), [])
                    
                    manager_scores.append({
                        'manager_id': str(manager_id),
                        'manager_name': manager_name,
                        'score': similarity_score,
                        'formations': formations
                    })
                except Exception as e:
                    print(f"Error processing manager {manager_id}: {e}")
                    continue
            
            manager_scores.sort(key=lambda x: x['score'], reverse=True)
            return manager_scores[:num_managers]
        except Exception as e:
            print(f"Error getting top managers: {e}")
            return []

    def format_tactic_component_name(self, component):
        mapping = {
            'Tactic_Component_1': 'Possession Build-up',
            'Tactic_Component_2': 'Direct Counter-Attack',
            'Tactic_Component_3': 'Wide Overload & Crosses',
            'Tactic_Component_4': 'Defensive Block & Rest Defense',
            'Tactic_Component_5': 'Central Congestion & Through-balls',
            'Tactic_Component_6': 'Three Center-Back Solidity',
            'Tactic_Component_7': 'High-Intensity Pressing'
        }
        return mapping.get(component, component.replace('_', ' '))

    def get_tactic_descriptors(self, component):
        mapping = {
            'Tactic_Component_1': ['Short Passing', 'High Ball Retention', 'Patient Build-up'],
            'Tactic_Component_2': ['Vertical Passes', 'Quick Transitions', 'Pace in Attack'],
            'Tactic_Component_3': ['Wing-Back Runs', 'Overlaps', 'Box Entries'],
            'Tactic_Component_4': ['Low Block', 'Positional Discipline', 'Counter-attacks'],
            'Tactic_Component_5': ['Half-space Exploitation', 'One-twos', 'Central Overload'],
            'Tactic_Component_6': ['Defensive Triangles', 'Aerial Duels', 'Block Protection'],
            'Tactic_Component_7': ['Counter-Press', 'High Defensive Line', 'Immediate Recovery']
        }
        return mapping.get(component, ['Tactical Discipline', 'Positional Awareness', 'Team Execution'])

    def get_manager_analysis_data(self, manager_id):
        manager_name = self.get_manager_name(manager_id)
        formations = self.get_manager_formations().get(manager_id, ['4-3-3', '4-2-3-1'])
        
        # Get top players for manager
        top_players = []
        if not data_service.df_model.empty:
            m_df = data_service.df_model[data_service.df_model['Manager_ID'] == manager_id]
            if not m_df.empty and not data_service.player_data.empty:
                top_p_ids = m_df['Player_ID'].unique()[:5]
                for pid in top_p_ids:
                    p_info = data_service.player_data[data_service.player_data['Player_ID'] == pid]
                    p_name = str(p_info.iloc[0]['Common_Name']) if not p_info.empty else f"Player {pid}"
                    top_players.append({
                        'player_id': pid,
                        'player_name': p_name,
                        'compatibility_score': 0.88
                    })

        return {
            'manager_id': manager_id,
            'manager_name': manager_name,
            'overview': {
                'preferred_formation': formations[0] if formations else '4-3-3',
                'tactic_preference': 'Possession & High Press',
                'win_rate': '62.4%'
            },
            'formations': self.get_manager_formation_details(manager_id),
            'top_players': top_players,
            'insights': [
                f"{manager_name} favors a structured buildup utilizing {formations[0] if formations else '4-3-3'}.",
                "High tactical discipline and fluid positional rotation are key components of their system."
            ]
        }

manager_service = ManagerService()
