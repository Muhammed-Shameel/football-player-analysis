import unittest
import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app import app, get_player_scores, get_tactical_recommendations, get_manager_summary

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test that the home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Football Tactical Recommendations Dashboard', response.data)

    def test_get_player_info(self):
        """Test the get_player_info endpoint"""
        response = self.app.get('/get_player_info?player_id=P01')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Player_ID', data)
        self.assertEqual(data['Player_ID'], 'P01')

    def test_get_recommendations(self):
        """Test the get_recommendations endpoint"""
        response = self.app.post('/get_recommendations', 
                                data={'player_id': 'P01', 'model_name': 'XGBoost'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('recommendations', data)
        self.assertIn('best_component', data)

    def test_get_manager_summary(self):
        """Test the get_manager_summary endpoint"""
        response = self.app.get('/get_manager_summary')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)

if __name__ == '__main__':
    unittest.main()