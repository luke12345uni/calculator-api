from fastapi import FastAPI, HTTPException

app = FastAPI(title="Calculator API", version="1.0.0")

@app.get("/add")
def add(a: float, b: float):
    return {"operation": "addition", "result": a + b}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"operation": "subtraction", "result": a - b}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"operation": "multiplication", "result": a * b}

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"operation": "division", "result": a / b}

@app.get("/health")
def health():
    return {"status": "ok"}
