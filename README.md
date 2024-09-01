# AI Receptionist for Dr. Adrin

This project implements an AI-powered receptionist for Dr. Adrin using a web-based chat interface. The backend is built using Quart, a Python web framework similar to Flask but with support for asynchronous operations. The project leverages the Qdrant vector database and the SentenceTransformers library to understand and respond to user inputs.

## Features

- **Natural Language Understanding**: The AI receptionist can understand user intents like reporting an emergency or leaving a message.
- **Emergency Handling**: The system provides instructions based on various emergency scenarios, retrieved asynchronously to keep the user engaged.
- **Automatic Follow-up**: The system automatically recalls and updates the user on the status of their emergency after a predefined delay.
- **Custom Responses**: The AI can handle special cases like when a user expresses concern about delays, by providing specific responses.
- **Simple Web Interface**: A frontend is provided for interacting with the AI receptionist, built with HTML, CSS, and JavaScript.

## Project Structure

- `app.py`: The backend application written in Python using the Quart framework.
- `templates/index.html`: The frontend template with the chat interface.
- `requirements.txt`: A list of Python dependencies required to run the project.
- `vector_db_setup.py`: Contains the logic for setting up the Qdrant collections and uploading initial data.

## Requirements

- Python 3.7+
- The dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sankeerthanavenugopal/smallest_ai_assignment.git
   cd ai-receptionist
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Qdrant collections and upload data:**

   Run the `vector_db_setup.py` script to create the collections and upload initial data to Qdrant.

   ```bash
   python vector_db_setup.py
   ```

5. **Run the application:**

   ```bash
   python app.py
   ```

   The application will start in debug mode, and you can access it by navigating to `http://127.0.0.1:5000/` in your web browser.

## Usage

1. **Start the server** by running `python app.py`.
2. **Open your web browser** and go to `http://127.0.0.1:5000/`.
3. **Interact with the AI Receptionist** by typing your queries into the chat interface.
