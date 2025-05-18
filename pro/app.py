from flask import Flask, render_template, request, jsonify
from chatbot_module import chatbot_response as get_chatbot_response

app = Flask(__name__, static_folder='static')

# Serve the HTML file with the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

# Endpoint to handle chatbot interactions
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get the user's message from the request
        user_message = request.json['message']
        
        # Process the user's message using your chatbot logic
        bot_response = get_chatbot_response(user_message)
        
        # Return the bot's response as JSON
        return jsonify({'message': bot_response})
    except Exception as e:
        return jsonify({'message': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)