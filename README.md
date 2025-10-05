# MediCore: AI-Powered Healthcare Diagnostic Platform

## Description

MediCore is an AI-powered platform designed to provide real-time diagnostic assistance to healthcare professionals. It leverages state-of-the-art machine learning models to analyze medical images (like X-rays, CT scans, and MRIs) and generate accurate, automated diagnostic reports.

## Prerequisites

- Python (3.9 or higher)
- Docker & Docker Compose
- An AWS account (for cloud deployment)

## Basic Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd medicore
    ```

2.  **Set up the environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    ```bash
    cp .env.example .env
    # Fill in the values in .env
    ```

5.  **Run the application:**
    ```bash
    uvicorn backend.app.main:app --reload
    ```