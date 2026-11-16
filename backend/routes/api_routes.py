from flask import Blueprint, request, jsonify
from backend.services.data_service import data_service
from backend.services.ml_service import ml_service
from backend.services.manager_service import manager_service
from backend.services.insight_service import insight_service
from backend.config import MODELS, MODEL_PERFORMANCE, BEST_MODEL

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/players', methods=['GET'])
def get_players():
    """Get list of all players and years available with image URLs"""
    try:
        players = []
        if not data_service.players_df.empty:
            for _, row in data_service.players_df.iterrows():
                pid = str(row['Player_ID'])
                name = str(row['Player_Name'])
                players.append({
                    'Player_ID': pid,
                    'Player_Name': name,
                    'image_url': f"/static/images/{pid}_img.jpg"
                })
        return jsonify({
            'players': players,
            'years': data_service.years,
            'models': list(MODELS.keys()),
            'model_performance': MODEL_PERFORMANCE,
            'best_model': BEST_MODEL
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/managers', methods=['GET'])
def get_managers_list():
    """Get list of all available managers from data source"""
    try:
        managers = []
        if not data_service.manager_data.empty:
            for _, row in data_service.manager_data.iterrows():
                mid = str(row['Manager_ID'])
                if mid == 'M21':
                    continue
                mname = str(row['Manager_Name'])
                managers.append({'manager_id': mid, 'manager_name': mname})
        else:
            if not data_service.df_model.empty:
                m_ids = data_service.df_model['Manager_ID'].dropna().unique()
                for mid in m_ids:
                    if str(mid) == 'M21':
                        continue
                    managers.append({'manager_id': str(mid), 'manager_name': f"Manager {mid}"})
        return jsonify({'managers': managers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/player-info', methods=['GET'])
def get_player_info():
    """Get player info and scores with image URL"""
    player_id = request.args.get('player_id')
    year = request.args.get('year')
    
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    try:
        year_int = int(year) if year and year.isdigit() else None
        scores = ml_service.get_player_scores(player_id, year_int)
        agg_data = ml_service.get_aggregated_player_data(player_id)
        
        player_name = f"Player {player_id}"
        if not data_service.player_data.empty:
            p_row = data_service.player_data[data_service.player_data['Player_ID'] == player_id]
            if not p_row.empty:
                player_name = str(p_row.iloc[0]['Common_Name'])
        
        return jsonify({
            'player_id': player_id,
            'player_name': player_name,
            'image_url': f"/static/images/{player_id}_img.jpg",
            'scores': scores or {},
            'aggregated_data': agg_data or {}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/recommendations', methods=['GET', 'POST'])
def get_recommendations():
    """Get tactical recommendations for a player with enriched metadata"""
    player_id = request.args.get('player_id') or (request.json and request.json.get('player_id')) or request.form.get('player_id')
    model_name = request.args.get('model') or (request.json and request.json.get('model')) or request.form.get('model_name', BEST_MODEL)
    if model_name not in MODELS:
        model_name = BEST_MODEL
    year = request.args.get('year') or (request.json and request.json.get('year')) or request.form.get('year')
    
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    try:
        result = ml_service.get_shared_tactical_recommendations(player_id, model_name, year)
        if 'error' in result:
            return jsonify(result), 400
        
        player_name = f"Player {player_id}"
        if not data_service.player_data.empty:
            p_row = data_service.player_data[data_service.player_data['Player_ID'] == player_id]
            if not p_row.empty:
                player_name = str(p_row.iloc[0]['Common_Name'])
                
        recommendations = result.get('recommendations', [])
        for r in recommendations:
            comp = r['component']
            r['name'] = manager_service.format_tactic_component_name(comp)
            r['formation'] = ml_service.get_formation_for_component(comp)
            r['description'] = ml_service.get_tactic_description(comp)

        best_tactic = result.get('best_tactic_data', {})
        if best_tactic and 'component' in best_tactic:
            best_tactic['name'] = manager_service.format_tactic_component_name(best_tactic['component'])
            best_tactic['descriptors'] = manager_service.get_tactic_descriptors(best_tactic['component'])

        return jsonify({
            'player_id': player_id,
            'player_name': player_name,
            'image_url': f"/static/images/{player_id}_img.jpg",
            'year': year or 'All Years',
            'model': model_name,
            'recommendations': recommendations,
            'best_tactic_data': best_tactic,
            'components_data': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/managers-for-player', methods=['GET', 'POST'])
def get_managers_for_player():
    """Get top recommended managers for a player"""
    player_id = request.args.get('player_id') or (request.json and request.json.get('player_id')) or request.form.get('player_id')
    model_name = request.args.get('model') or (request.json and request.json.get('model')) or request.form.get('model_name', BEST_MODEL)
    if model_name not in MODELS:
        model_name = BEST_MODEL
    year = request.args.get('year') or (request.json and request.json.get('year')) or request.form.get('year')
    
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    try:
        year_int = int(year) if year and str(year).isdigit() else None
        top_managers = manager_service.get_top_managers_for_player(player_id, year_int, model_name, num_managers=5)
        return jsonify({
            'player_id': player_id,
            'recommended_managers': top_managers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/manager-analysis', methods=['GET'])
def get_manager_analysis():
    """Get full manager analysis payload"""
    manager_id = request.args.get('manager_id')
    if not manager_id:
        return jsonify({'error': 'Manager ID is required'}), 400
    
    try:
        data = manager_service.get_manager_analysis_data(manager_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/insights', methods=['GET'])
def get_insights():
    """Get general insights summary"""
    try:
        summary = insight_service.get_insights_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/impact-over-time', methods=['GET'])
def get_impact_over_time():
    """Get impact score trend over time"""
    player_id = request.args.get('player_id')
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    try:
        trend = insight_service.get_impact_over_time(player_id)
        return jsonify({'player_id': player_id, 'impact_trend': trend})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/seasonal-performance', methods=['GET'])
def get_seasonal_performance():
    """Get seasonal performance metrics"""
    player_id = request.args.get('player_id')
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    try:
        seasonal = insight_service.get_seasonal_performance(player_id)
        return jsonify({'player_id': player_id, 'seasonal_performance': seasonal})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tactic-frequency', methods=['GET'])
def get_tactic_frequency():
    """Get tactic frequency"""
    player_id = request.args.get('player_id')
    if not player_id:
        return jsonify({'error': 'Player ID is required'}), 400
    
    try:
        freq = insight_service.get_tactic_frequency(player_id)
        return jsonify({'player_id': player_id, 'tactic_frequency': freq})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
