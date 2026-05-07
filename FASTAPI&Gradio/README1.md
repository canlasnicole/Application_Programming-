# FastAPI and Gradio: Quotes Management System

This project is a quote management and retrieval application. It utilizes FastAPI for the backend infrastructure and Gradio to provide a user-friendly interface for interacting with the data.

---

## Getting Started

Follow these steps to set up the project locally using VS Code.

### 1. Open Project Folder
Launch VS Code and open the directory containing the project files.

### 2. Configure Virtual Environment
Create and activate a virtual environment to isolate project dependencies.
* Open Terminal: Ctrl + Shift + ` (or Terminal > New Terminal)
* Create Environment: python -m venv venv
* Activate Environment: .\venv\Scripts\activate

### 3. Install Required Libraries
Install the necessary frameworks by running the following command:
pip install fastapi uvicorn gradio

---

## Project Structure and Files

The repository is organized with the following key components:

* app.py: The main execution file integrating the Gradio UI and FastAPI backend.
* client.py: A script designed for testing client-side requests.
* main_CRUD.py: Contains the logic for database generation and CRUD (Create, Read, Update, Delete) operations.
* main_server.py: Handles the FastAPI server instance and route configurations.
* quotes.db: The SQLite database file storing the quotes.
* requirements.txt: A list of Python library dependencies required for the project.

---

## Execution and Deployment

### Local Execution
Running the project locally will generate a link to http://127.0.0.1:8000.
1. Activate your virtual environment.
2. Run: python app.py
3. Click the local link provided in the terminal to access the interface.

### Hugging Face Deployment
The project has been deployed via Hugging Face Spaces for easy access and live demonstrations.
* Main Interface: Access the quote search, verification, and real-time multi-language translation features.
* API Documentation: Test the backend functionality visually through the CRUD interface.

---

## Conclusion
This system combines a high-performance FastAPI backend with an intuitive Gradio interface. By deploying to Hugging Face, the application ensures global accessibility without requiring manual local setup, providing a solid foundation for future data management features.
