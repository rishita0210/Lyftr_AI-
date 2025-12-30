from app.models import init_db

@app.on_event("startup")
def startup():
    init_db()
