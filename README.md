# Football Tactical Recommendations Dashboard

A Flask web application for a data-driven football analytics capstone project. It uses machine learning models to predict how tactical components impact player performance, recommends optimal tactics for individual players, and matches players with managers whose tactical styles suit them.

## Features

- **Tactical Recommendations Dashboard** — select any player and get predicted impact scores for 7 tactical components (`Tactic_Component_1` through `Tactic_Component_7`), visualized with interactive Plotly charts
- **Multi-Model Selection** — choose between 5 trained ML models (Random Forest, Gradient Boosting, XGBoost, Neural Network, SVM) or use the auto-selected best model
- **Year Filtering** — analyze recommendations for a specific season or across all available years
- **Manager Recommendations** — get the top managers best suited to a player based on tactical compatibility
- **Manager Analysis Page** — per-manager tactical profile: formations, playing style indicators, top players, and tactic usage
- **Tactical Components Page** — deeper breakdown of tactic impact per player
- **Insights Page** — performance trends over time, manager comparison, seasonal performance, and tactic frequency charts
- **Custom Error Pages** — styled 404/500 handlers and graceful degradation when data files or models are missing

## Pages

| Route | Description |
|---|---|
| `/` | Main dashboard — player selection, tactical recommendations table and impact chart |
| `/managers` | Manager recommendations page |
| `/tactical_components` | Tactical component breakdown per player |
| `/manager_analysis` | In-depth analysis of a manager's tactics, formations, and top players |
| `/insights` | Trend charts: impact over time, manager comparison, seasonal performance, tactic frequency |

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/get_player_info` | GET | Player basic info and scores |
| `/get_recommendations` | POST | Tactical recommendations for a player (with model/year selection) |
| `/get_managers_for_player` | POST | Top recommended managers for a player |
| `/get_insights` | GET | Aggregate insights data |
| `/get_impact_over_time` | GET | Impact score trend for a player |
| `/get_manager_comparison` | GET | Manager comparison data for a player |
| `/get_seasonal_performance` | GET | Season-by-season player performance |
| `/get_tactic_frequency` | GET | How often each tactic is used for a player |
| `/get_tactical_components` | GET | Tactical component data |
| `/get_tactic_variable_loadings` | GET | Variable loadings behind a tactical component |
| `/get_manager_analysis` | GET | Full manager analysis payload (info, formations, top players, insights) |
| `/get_manager_tactical_profile` | GET | Manager tactical component data for charting |

## Machine Learning Models

Five supervised models were trained in `CP_model.ipynb` to predict tactical impact classes. Saved artifacts (best + SMOTE variants) live in the project root:

| Model | File | F1 Score |
|---|---|---|
| XGBoost | `xgboost_best.pkl` / `xgboost_smote.pkl` | 0.66 |
| Gradient Boosting | `gradientboost_best.pkl` / `gradientboost_smote.pkl` | 0.65 |
| SVM | `svm_best_model.pkl` | 0.65 |
| Random Forest | `randomforest_best.pkl` / `randomforest_smote.pkl` | 0.64 |
| Neural Network | `neuralnet_best.pkl` / `neuralnet_smote.pkl` | 0.62 |

`label_encoder.pkl` stores the class encoding used during training. XGBoost currently has the best global F1 score and is used as the default model.

## Data Sources

| File | Contents |
|---|---|
| `player.xlsx` | Player master data (IDs, names, attributes) |
| `df_model.csv` | Main modeling dataset — abilities, tactical components, impact score, best tactic, per-year records |
| `player_stat.csv` | Raw player statistics |
| `team.xlsx` | Team data |
| `manager.xlsx` | Manager master data |
| `manager_formation.xlsx` | Formations used by each manager |
| `manager_tactics.json` | Mapping of managers to their tactical components |
| `manager_tactic_summary.json` | Cached manager-level tactic usage summary |
| `factor_loadings.png` | Factor analysis loadings plot (from the notebook) |
| `static/images/` | Player images named `PXX_img.jpg` (e.g. `P01_img.jpg`) |

## Installation

1. Requires Python 3.8+ (project pinned to the versions in `requirements.txt`).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Core packages: `Flask`, `plotly`, `pandas`, `numpy`, `scikit-learn`, `openpyxl`.
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`.

> `app_simple.py` is a reduced fallback version of the app if the full `app.py` fails to start.

## How It Works

1. On startup the app loads all data files (`player.xlsx`, `df_model.csv`, team/manager data, tactics JSON) with per-file error handling — missing files degrade gracefully instead of crashing.
2. When a player (and optionally a model and year) is selected, the app loads the corresponding pickled model and builds the player's feature vector from `df_model.csv`.
3. The model simulates the impact of adjusting each of the 7 tactical components, producing per-component impact scores.
4. Manager recommendations are scored by comparing a player's tactical profile against each manager's known tactics and formations.
5. Results are rendered in tables and interactive Plotly charts across the dashboard pages.

## Project Structure

```
Analysis/
├── app.py                     # Main Flask application (all pages + API endpoints)
├── app_simple.py              # Simplified fallback app
├── CP_model.ipynb             # Jupyter notebook: EDA, factor analysis, model training
├── requirements.txt           # Pinned dependencies
├── *.pkl                      # Trained models + label encoder
├── player.xlsx / team.xlsx / manager*.xlsx / df_model.csv / player_stat.csv   # Data
├── manager_tactics.json       # Manager → tactics mapping
├── templates/
│   ├── index.html             # Main dashboard
│   ├── managers.html          # Manager recommendations
│   ├── manager_analysis.html  # Manager deep-dive
│   ├── tactical_components.html
│   ├── insights.html
│   ├── 404.html / 500.html    # Error pages
├── static/images/             # Player photos (PXX_img.jpg)
├── screenshots/               # Dashboard screenshots/docs
└── test_*.py, check_*.py, debug_*.py   # Manual test & debugging scripts
```

## Testing

Numerous standalone test scripts are included, e.g.:
```bash
python test_app.py          # general app tests
python test_api.py          # API endpoint checks
python check_model.py       # verify model pickles load
python check_players.py     # verify player data pipeline
```

## Troubleshooting

- **Model loading warnings** — pickles were trained with specific scikit-learn/XGBoost versions; mismatches may raise warnings. The app still serves data visualizations even if a model can't be loaded. Install the pinned `requirements.txt` versions for full functionality.
- **Missing data files** — the app starts with empty tables rather than crashing; check the console output for which file failed to load.
- **Port 5000 in use** — change the port in the `app.run()` call at the bottom of `app.py`.
- **Player images not showing** — ensure files follow the `PXX_img.jpg` naming convention in `static/images/`.

## License

This project is for educational purposes only (Capstone Project).
