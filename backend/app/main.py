from fastapi import FastAPI

app = FastAPI(
    title="Medicore API",
    version="1.0.0",
    description="AI-Powered Healthcare Diagnostic Platform API"
)

@app.get("/")
def read_root():
    """Root endpoint for the API"""
    return {"status": "ok", "message": "Medicore API is running"}

@app.get("/health")
def health_check():
    """Health Check endpoint for monitoring."""
    return {"status": "healthy", "version":"1.0.0"}


# Will come back to this file later to add middleware, routes, etc.