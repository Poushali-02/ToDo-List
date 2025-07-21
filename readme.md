# To-Do List Application 📝

A simple, lightweight web-based To-Do List application built with Flask. This application allows you to add and delete tasks, helping you keep track of your daily to-dos.

## ✨ Features

  * **Add Tasks**: Easily add new tasks to your list.
  * **View Tasks**: See all your current tasks displayed.
  * **Delete Tasks**: Remove completed or unwanted tasks from the list.
  * **Flash Messages**: Get instant feedback on task additions and deletions (e.g., "Task added successfully\!").
  * **Responsive Design**: Basic styling with Bootstrap 5 for a clean, mobile-friendly interface.

## 💻 Technologies Used

  * **Python**: The core programming language.
  * **Flask**: A micro web framework for Python.
  * **HTML**: For structuring the web pages.
  * **CSS (Bootstrap 5)**: For styling and responsive design.
  * **.env**: To manage environment variables (specifically for `SECRET_KEY`).

## 🚀 Getting Started

Follow these steps to get a copy of the project up and running on your local machine.

### Prerequisites

  * Python 3.x installed on your system.
  * `pip` (Python package installer).

### Installation

1.  **Clone the repository** (if you've pushed it to GitHub):

    ```bash
    git clone https://github.com/Poushali-02/ToDo-List.git
    cd ToDo-List
    ```

2.  **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:

      * On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
      * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required packages**:

    ```bash
    pip install requirements.txt
    ```

5.  **Create a `.env` file**:
    In the root directory of your project (same level as `app.py`), create a file named `.env` and add your Flask secret key. This is crucial for Flask's session management.

    ```env
    FLASK_SECRET_KEY='your_very_secret_random_key_here'
    ```

    *Replace `'your_very_secret_random_key_here'` with a long, random string. You can generate one with `python -c 'import os; print(os.urandom(24))'`.*

### Running the Application

1.  **Start the Flask development server**:

    ```bash
    python app.py
    ```

2.  **Open your browser**:
    Navigate to `http://127.0.0.1:5000/`. You should see your To-Do List application\!

## 💡 How It Works

  * Tasks are stored in a **Python list** (`task`) in memory. This means your tasks will **not persist** if you restart the Flask server.
  * The `add` route handles POST requests from the form, appending new tasks to the list.
  * The `delete` route removes tasks based on their index in the list.
  * The **Post/Redirect/Get (PRG) pattern** is used after form submissions (`/add`, `/delete`) to prevent duplicate submissions on page refresh.
  * `flash()` messages are used to provide user feedback, displayed using Jinja2 in `index.html`.

## ⏭️ Future Enhancements

  * **Database Persistence**: Implement a database (e.g., SQLite with Flask-SQLAlchemy) to store tasks so they persist even after the server restarts.
  * **Mark as Complete**: Add functionality to mark tasks as completed (e.g., striking them through or moving them to a "completed" section).
  * **Edit Task**: Allow users to modify existing tasks.
  * **User Accounts**: Implement user authentication (e.g., with Flask-Login) so each user has their own personal To-Do list.
  * **Reminders**: Add a feature to set reminders for tasks.
  * **Improved UI/UX**: Enhance the styling and user experience further.

## 🤝 Contributing

Feel free to fork this repository and contribute\! Pull requests are welcome.

## 📄 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE). (You should create a `LICENSE` file in your repository if you want to explicitly state the license).