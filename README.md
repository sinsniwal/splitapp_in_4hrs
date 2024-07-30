# Split App
## Project Resources



## Instructions to Run

### Backend:
To run the backend application, follow these steps:

1. Make sure you have Docker installed on your system.
2. Open your terminal.
3. Run the following command to start the backend server (using Docker):
    ```bash
    docker build -t backend .
    docker run -p 8000:8000 -d backend
    ```

### Backend
- **Description:** The backend component serves as the core of the Split Expenses App, handling API endpoints, and authentication.
- **Framework:** Django Rest Framework is chosen for the backend development, facilitating the creation of robust RESTful APIs.
- **Database:** SQLite is employed as the database management system, providing efficient storage and retrieval of data.

## Project Structure

### Backend
- **Dockerfile:** Contains instructions for building Docker images.
- **project:** Main directory containing Django app modules.
    - **myapi:** Implements APIs for managing expenses and authentication.
    - **mainApp:** Contains main settings and URL configurations for the Django project.
- **manage.py:** Django management script for running administrative tasks.

### Other Files
- **requirements.txt:** Lists all Python dependencies required for the project.
