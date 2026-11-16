from flask import Flask
from backend.routes.api_routes import api_bp

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    
    # Register API Blueprint
    app.register_blueprint(api_bp)
    
    # Enable CORS for React frontend development/production
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        return response

    @app.route('/')
    def index():
        return {"message": "Football Tactical Analytics API Backend is running. Frontend served via React or static templates."}

    return app

app = create_app()
