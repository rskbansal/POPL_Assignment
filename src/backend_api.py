from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = request.args.get('api_key')
    if not city:
        return jsonify({'error': 'City parameter is missing'}), 400

    # Generate random weather data
    temperature = random.randint(0, 40)
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
