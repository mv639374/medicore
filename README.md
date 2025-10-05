# MediCore - AI-Powered Healthcare Diagnostic Platform

## Project Overview
MediCore is an AI-powered platform designed to provide real-time diagnostic assistance to healthcare professionals. It leverages state-of-the-art machine learning models to analyze medical images and generate accurate, automated diagnostic reports.

## Features
* Real-time AI-driven diagnostic analysis.
* Support for various medical imaging formats (DICOM, PNG, JPEG).
* Automated report generation.
* HIPAA-compliant data handling and security.
* Role-based access control for different healthcare professionals.

## Prerequisites
* Python 3.9+
* Docker & Docker Desktop
* PostgreSQL 14+
* Node.js 18+

## Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd medicore
    ```
2.  **Setup Backend:**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Setup Frontend:**
    ```bash
    cd ../frontend
    npm install
    ```
4.  **Configure environment variables:**
    ```bash
    cp .env.example .env
    # Fill in the values in .env
    ```

## Quick Start
1.  **Run the backend server:**
    ```bash
    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
2.  **Run the frontend application:**
    ```bash
    cd frontend
    npm run dev
    ```


## Docker Setup
This project uses Docker Compose for a consistent development environment.

### Prerequisites
- Docker Desktop 4.0+
- docker-compose 2.0+

### Running with Docker
1.  **Copy the environment file:** `cp .env.example .env` (and fill in your secrets).
2.  **Build and start all services:**
    ```bash
    docker-compose up -d --build
    ```
3.  **View logs:**
    ```bash
    docker-compose logs -f backend
    ```
4.  **Stop services:**
    ```bash
    docker-compose down
    ```
5.  **Access the container shell:**
    ```bash
    docker-compose exec backend bash
    ```




## API Access & Documentation
The API is served at `http://localhost:8000`. You can access the health check endpoint to verify it's running:
```bash
curl http://localhost:8000/health
```

For detailed information on all available endpoints, authentication, and request/response formats, please see the **[API Documentation](https://www.google.com/search?q=./docs/api/api-overview.md)**.


## Project Structure
*(A brief overview of the directory structure will be added here later)*

## Contributing
Contributions are welcome. Please follow the standard fork, branch, and pull request workflow.

## License
This project is licensed under the MIT License.





























