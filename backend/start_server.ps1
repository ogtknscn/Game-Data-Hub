# Start backend server with SQLite
$env:USE_SQLITE = "true"
Write-Host "Starting backend server on http://localhost:8000"
Write-Host "API Docs: http://localhost:8000/api/docs"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

