# Document Processing Service API

This repository contains an API for a document processing service. The service allows users to upload images and PDF files in base64 format. The API will then perform various operations on these files, such as rotating images or converting PDFs to images, and return the results.

## Requirements

The project includes the following features:

- Users can upload images and PDFs in base64 format.
- The API provides several endpoints for managing and processing uploaded files.
- The system stores file paths in the database and saves files on the server.

## Features

1. **API Endpoints:**
    - `POST /api/upload/`: Accepts image and PDF files in base64 format and saves them to the server.
    - `GET /api/images/`: Returns a list of all uploaded images.
    - `GET /api/pdfs/`: Returns a list of all uploaded PDFs.
    - `GET /api/images/{id}/`: Returns the details of a specific image (location, width, height, number of channels).
    - `GET /api/pdfs/{id}/`: Returns the details of a specific PDF (location, number of pages, page width, page height).
    - `DELETE /api/images/{id}/`: Deletes a specific image.
    - `DELETE /api/pdfs/{id}/`: Deletes a specific PDF.
    - `POST /api/rotate/`: Accepts an image ID and rotation angle, rotates the image, and returns the rotated image.
    - `POST /api/convert-pdf-to-image/`: Accepts a PDF ID, converts the PDF to an image, and returns the image.

2. **File Handling:**
    - Images and PDFs are saved on the server.
    - File paths are stored in the database.

3. **Error Handling and Validation:**
    - Proper error handling and validation have been implemented to ensure correct input and file processing.

4. **Docker Support:**
    - The project is Dockerized for easy deployment and testing.

## Project Setup

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/muhammadgalhoum/https://github.com/muhammadgalhoum/DPS.git
cd DPS
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate the dependencies:

```bash
On macOS/Linux:
python3 -m venv venv
On Windows:
python -m venv venv
```

### 3. Activate the Virtual Environment

```bash
On macOS/Linux:
source venv/bin/activate
On Windows:
.\venv\Scripts\activate
```

### 4. Install the Required Dependencies

Install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

Run migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin Access)

Create a superuser to access the Django Admin interface:

```bash
python manage.py createsuperuser
You will be prompted to enter a username, email, and password for the superuser account.
```

### 7. Run the Development Server

Start the development server:

```bash
python manage.py runserver
The server will be available at http://127.0.0.1:8000/.
```

### 8. Test the API with Postman

Open Postman and import the collection which also contains Documentation then test the API endpoints.

### 9. Test the API using pytest

In the main directory run the following command.
```bash
pytest
```

### 10. Docker Setup

To run the project in Docker, follow these steps:

Build the Docker Image and Run the Docker Container:

```bash
docker-compose up --build
```

Access the API: Once the container is running, the API will be available at <http://127.0.0.1:8000/>.
