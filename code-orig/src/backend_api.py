from flask import Flask, request, jsonify
import random
import hashlib

app = Flask(__name__)

# For authenticating requests using an API key
target_hash = '9f90d4580a3502e96fbb7607213d478d'

def verify_api_key(api_key):
    # Hash the API key using MD5
    hashed_api_key = hashlib.md5(api_key.encode()).hexdigest()
    return hashed_api_key == target_hash

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = request.args.get('api_key')

    # Check if the city parameter is missing
    if not city:
        return jsonify({'error': 'City parameter is missing'}), 400

    # Check if the API key is missing 
    if not api_key:
        return jsonify({'error': 'API key is missing'}), 401
        
    # Check if the API key is invalid
    if not verify_api_key(api_key):
        return jsonify({'error': 'Invalid API key'}), 401

    # Generate random weather data
    temperature = random.randint(-20, 40)
    conditions = ['Sunny', 'Cloudy', 'Rainy', 'Snowy']
    condition = random.choice(conditions)

    weather_data = {
        'city': city,
        'condition': condition,
        'temperature': temperature,
    }

    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
