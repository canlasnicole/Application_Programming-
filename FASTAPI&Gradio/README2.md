#  FastAPI and Gradio: Quotes Management System

This project is a sophisticated quote management and retrieval application. It combines the high-performance capabilities of **FastAPI** with the intuitive, rapid-prototyping power of **Gradio** for the frontend.

---

##  Project Links
* **Live Demo:** [Hugging Face Spaces](https://huggingface.co/spaces/canlasnicole/app.py)
* **Backend Framework:** [FastAPI Documentation](https://fastapi.tiangolo.com/)

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

##  Features

* **Comprehensive CRUD Logic:** Fully implemented Create, Read, Update, and Delete functions using SQLite.
* **Data Validation:** Utilizes Pydantic's `BaseModel` to ensure every quote has a valid text, author, and category.
* **Asynchronous Backend:** Built on FastAPI for high-speed API responses and scalability.
* **Interactive UI:** A Gradio interface that allows users to manage the database without writing code.
* **Database Persistence:** Reliable storage using SQLite (`quotes.db`).

---

##  File Overview

### 1. `main_CRUD.py` (The Engine)
This file contains the core database operations. Based on the implementation:
* **Schemas:** Defines `명언_모델` and `명언_생성_모델`.
* **Create (`명언_추가하기`):** Injects new quotes into the database.
* **Read (`모든_명언_가져오기`):** Retrieves all entries sorted by the latest ID.
* **Update (`명언_수정하기`):** Modifies existing quotes based on their Unique ID.
* **Delete (`명언_삭제하기`):** Removes specific entries from the system.

### 2. `main_server.py`
The FastAPI application layer that maps the CRUD functions to accessible URL endpoints.

### 3. `app.py`
The "Glue" of the project. It launches the Gradio interface and connects it to the FastAPI backend, providing the final URL for the user.

---

##  Installation & Setup

### 1. Environment Setup
```bash
# Create a virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
