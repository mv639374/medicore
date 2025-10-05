# MediCore API Documentation

## Overview
Welcome to the MediCore API. This document provides all the information you need to interact with the MediCore platform programmatically.

## Base URL
All API URLs are relative to the following base URL:
`http://localhost:8000/api/v1`

## Authentication
The API uses **Bearer Token** authentication. You must include an `Authorization` header with your API requests.

**Example:**
`Authorization: Bearer <your_jwt_token_here>`

## Response Format
All responses are in **JSON** format. A successful request will typically return a `200 OK` status code.

## Error Handling
Errors are returned using standard HTTP status codes. The response body will contain a JSON object with a `detail` key explaining the error.

**Example Error Response (`404 Not Found`):**
```json
{
  "detail": "Patient with ID 123 not found."
}
````

## Rate Limiting

(To be defined later)

## API Versioning

The API is versioned using a URL prefix (`/api/v1`). Any backward-incompatible changes will result in a new version number.

-----

*(This document will be expanded with details for each endpoint as they are created.)*

````

---
