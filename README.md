# AI Receptionist for Dr. Adrin

This project implements an AI-powered receptionist for Dr. Adrin using a web-based chat interface. The backend is built using Quart, a Python web framework similar to Flask but with support for asynchronous operations. The project leverages the Qdrant vector database and the SentenceTransformers library to understand and respond to user inputs.

## Features

- **Natural Language Understanding**: The AI receptionist can understand user intents like reporting an emergency or leaving a message.
- **Emergency Handling**: When a user reports an emergency, the system asynchronously retrieves relevant instructions while keeping the user engaged.
- **Automatic Follow-up**: The system automatically recalls and updates the user on the status of their emergency after a predefined delay.
- **Simple Web Interface**: A frontend is provided for interacting with the AI receptionist, built with HTML, CSS, and JavaScript.

## Project Structure

- `app.py`: The backend application written in Python using the Quart framework.
- `templates/index.html`: The frontend template with the chat interface.
- `static`: A directory to place static files like CSS or JavaScript (if needed).
- `requirements.txt`: A list of Python dependencies required to run the project.

## Requirements

- Python 3.7+
- The dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ai-receptionist.git
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

4. **Run the application:**

   ```bash
   python app.py
   ```

   The application will start in debug mode, and you can access it by navigating to `http://127.0.0.1:5000/` in your web browser.

## Usage

1. **Start the server** by running `python app.py`.
2. **Open your web browser** and go to `http://127.0.0.1:5000/`.
3. **Interact with the AI Receptionist** by typing your queries into the chat interface.

## Customization

- **Qdrant Configuration**: The Qdrant client is initialized with specific URL and API key details. If you have your own Qdrant instance, update these details in `app.py`.
- **Emergency Instructions**: The system retrieves instructions from the Qdrant vector database based on user input. You can customize these instructions by modifying the Qdrant collection.

## Example Interaction Flow

1. The AI asks, "How can I assist you today?"
2. The user types, "I have an emergency."
3. The AI responds, "What is your emergency?"
4. The user describes the emergency, e.g., "I'm having chest pain."
5. The AI starts retrieving instructions and asks, "I am checking what you should do immediately. Meanwhile, can you tell me which area you are located right now?"
6. The user provides a location, e.g., "123 Main St."
7. The AI provides an estimated time of arrival for Dr. Adrin and gives initial instructions on what to do next.

## Frontend Details

The frontend is a simple HTML page (`index.html`) with a chat interface. It uses JavaScript (with Axios) to send user input to the backend and display responses.

### File: `index.html`

- The chat interface is created with basic HTML and styled with inline CSS.
- JavaScript handles the sending of messages and updates to the conversation state.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Quart**: For providing a simple and powerful async web framework.
- **Qdrant**: For offering an efficient vector search engine.
- **SentenceTransformers**: For enabling natural language understanding capabilities.
```

### How to Use This `README.md`:

- Replace `"https://github.com/yourusername/ai-receptionist.git"` with the actual URL of your GitHub repository if you have one.
- Ensure you have a `LICENSE` file if you plan to include the License section.
- Customize any other parts of the `README.md` as necessary to fit your specific project details.

This `README.md` provides an overview of the project, installation instructions, usage details, and more, making it easy for others to understand and use your project.