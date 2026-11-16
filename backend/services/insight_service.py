import pandas as pd
from backend.services.data_service import data_service

class InsightService:
    def get_insights_summary(self):
        """Get general insights overview"""
        if data_service.df_model.empty:
            return {'error': 'Data not available'}
        
        try:
            total_players = len(data_service.players_df) if not data_service.players_df.empty else 0
            total_records = len(data_service.df_model)
            avg_impact = float(data_service.df_model['Impact_Score'].mean()) if 'Impact_Score' in data_service.df_model.columns else 0.0
            
            return {
                'total_players': total_players,
                'total_records': total_records,
                'average_impact_score': round(avg_impact, 2),
                'years_covered': data_service.years
            }
        except Exception as e:
            print(f"Error in get_insights_summary: {e}")
            return {'error': str(e)}

    def get_impact_over_time(self, player_id):
        """Get impact score trend over time for a player"""
        if data_service.df_model.empty:
            return []
        
        player_df = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
        if player_df.empty:
            return []
        
        try:
            trend_data = []
            grouped = player_df.groupby('Year')['Impact_Score'].mean().reset_index()
            for _, row in grouped.iterrows():
                trend_data.append({
                    'year': int(row['Year']),
                    'impact_score': round(float(row['Impact_Score']), 2)
                })
            return sorted(trend_data, key=lambda x: x['year'])
        except Exception as e:
            print(f"Error in get_impact_over_time: {e}")
            return []

    def get_seasonal_performance(self, player_id):
        """Get season-by-season performance metrics for a player"""
        if data_service.df_model.empty:
            return []
        
        player_df = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
        if player_df.empty:
            return []
        
        try:
            seasonal = []
            metrics = ['Passing', 'Shooting', 'Creativity', 'Dribbling', 'Defense', 'Impact_Score']
            available_metrics = [m for m in metrics if m in player_df.columns]
            
            grouped = player_df.groupby('Year')[available_metrics].mean().reset_index()
            for _, row in grouped.iterrows():
                season_record = {'year': int(row['Year'])}
                for m in available_metrics:
                    season_record[m.lower()] = round(float(row[m]), 2)
                seasonal.append(season_record)
            return sorted(seasonal, key=lambda x: x['year'])
        except Exception as e:
            print(f"Error in get_seasonal_performance: {e}")
            return []

    def get_tactic_frequency(self, player_id):
        """Get tactic frequency for a player"""
        if data_service.df_model.empty:
            return []
        
        player_df = data_service.df_model[data_service.df_model['Player_ID'] == player_id]
        if player_df.empty:
            return []
        
        try:
            frequencies = []
            for col in data_service.tactic_columns:
                val = float(player_df[col].mean())
                frequencies.append({
                    'component': col,
                    'frequency': round(val, 2)
                })
            return frequencies
        except Exception as e:
            print(f"Error in get_tactic_frequency: {e}")
            return []

insight_service = InsightService()
