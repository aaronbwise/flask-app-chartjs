# Budget App

This Flask-based application is designed for the entry, storage, and visualization of monthly budget information.
**NB: Deployment is pending!**

## Features

- **User Registration & Login:** Secure user authentication system.
- **Budget Data Entry:** Users can input their monthly budget details.
- **Data Visualization:** Utilizes Chart.js to visualize budget data in an easily digestible format.
- **Responsive Design:** Accessible on various devices, ensuring a seamless user experience.

## Technologies Used

- **Flask:** A lightweight WSGI web application framework.
- **Chart.js:** Simple yet flexible JavaScript charting for designers & developers.
- **Bootstrap:** For responsive and mobile-first front-end web development.
- **SQLAlchemy:** SQL toolkit and Object-Relational Mapping (ORM) for Python.
- **Pillow:** Python Imaging Library for adding image processing capabilities.

## Code Structure

- `run.py`: The entry point of the application. Starts the Flask server.
- `forms.py`: Contains the form classes for user input (registration, login, data entry).
- `models.py`: Defines the database models for SQLAlchemy ORM.
- `routes.py`: Includes all the route definitions for the application.
- `templates/`: This directory contains HTML templates for rendering views.
    - `about.html`: About page of the application.
    - `home.html`: Home page template.
    - `landing_page.html`: The landing page of the app.
    - `login.html`: User login page.
    - `register.html`: User registration page.
- `static/`: Contains static files like CSS, JS, and images.

## Getting Started

### Prerequisites

- Python 3.6+
- Flask
- SQLAlchemy

### Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/aaronbwise/flask-app-chartjs.git
   ```
2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python run.py
   ```

---

![alt text](https://github.com/aaronbwise/flask-app-chartjs/blob/main/landing_page.jpg)
