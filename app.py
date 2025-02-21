from flask import Flask, request, jsonify
from flask_cors import CORS  # Add CORS support
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment variables
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("Missing Google API key - please check your .env file")

@app.route('/')
def home():
    return "Server is running"

@app.route("/get_distance", methods=["POST"])
def get_distance():
    try:
        data = request.json
        user_lat, user_lng = data.get("user_lat"), data.get("user_lng")
        destination = data.get("destination")

        if not user_lat or not user_lng or not destination:
            return jsonify({"error": "Invalid input"}), 400

        # Distance Matrix API URL
        distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={user_lat},{user_lng}&destinations={destination}&key={GOOGLE_MAPS_API_KEY}"

        response = requests.get(distance_url)
        response.raise_for_status()  # Raise exception for bad status codes
        distance_data = response.json()

        if distance_data["status"] == "OK":
            distance_text = distance_data["rows"][0]["elements"][0]["distance"]["text"]
            return jsonify({"distance": distance_text})
        else:
            return jsonify({"error": "Could not calculate distance", "status": distance_data["status"]}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-location", methods=["POST"])
def get_location():
    try:
        # Google Geolocation API URL
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}"
        
        response = requests.post(url)
        response.raise_for_status()
        return jsonify(response.json())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
