from flask import Flask, request, jsonify
from datetime import datetime
import calendar
import os
app = Flask(__name__)


# Middleware to enable CORS
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

@app.route('/api', methods=['GET'])
def get_info():
    try:
        slack_name = request.args.get('slack_name')
        track = request.args.get('track')

        # Check if both 'slack_name' and 'track' parameters are provided
        if not slack_name or not track:
            return jsonify({'message': 'Both slack_name and track parameters are required.'}), 400

        # Get the script's directory path
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Define your my_info dictionary
        current_day = calendar.day_name[datetime.now().weekday()]
        utc_time = datetime.utcnow().isoformat()

        # GitHub repo URL and file URL based on the script's location
        github_repo_url = 'https://github.com/OD2022/HNGx'
        github_file_url = f'{github_repo_url}/blob/main/{os.path.relpath(__file__, script_directory)}'

        my_info = {
            'slack_name': slack_name,
            'current_day': current_day,
            'utc_time': utc_time,
            'track': track,
            'github_file_url': github_file_url,
            'github_repo_url': github_repo_url,
            'status_code': 200
        }

        # Return specific information in JSON format
        return jsonify(my_info)

    except Exception as error:
        return jsonify({'message': f'An Error Occurred: {str(error)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
