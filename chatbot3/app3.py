from flask import Flask, render_template, request, jsonify
import ollama
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cyber Crime Portal Information
def get_cyber_crime_info():
    return {
        "portal": "https://cybercrime.gov.in/",
        "helpline": "1930 (Available 24/7)",
        "email": "cybercrime-mha@gov.in",
        "police_station": "Contact your nearest cyber crime police station",
        "international_help": "Check your country's government website for cyber crime laws."
    }

# Function to check if query is about cyber crime
def is_cyber_crime_query(user_input):
    keywords = ["report cyber crime", "cyber crime portal", "helpline", "authority", "contact", "report fraud", "cyber police", "cyber security help"]
    return any(keyword in user_input.lower() for keyword in keywords)

# Function to chat with Ollama
def chat_with_ollama(user_input):
    try:
        response = ollama.chat(model='gemma:2b', messages=[{'role': 'user', 'content': user_input}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

# API for chatbot interactions (text + image)
@app.route('/chat', methods=['POST'])
def chat():
    if 'image' in request.files:  # Check if an image is uploaded
        image = request.files['image']
        if image.filename != '':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            return jsonify({"image_url": f"/{image_path}"})

    elif request.json and 'message' in request.json:  # Handle text messages
        user_message = request.json['message']
        if is_cyber_crime_query(user_message):
            return jsonify({"cyber_crime_info": get_cyber_crime_info()})
        return jsonify({"message": chat_with_ollama(user_message)})

    return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)
