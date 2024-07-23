from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

ENVIRONMENT = os.getenv('ENVIRONMENT')
load_dotenv(f'.env.{ENVIRONMENT}')

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        yield db
    finally:
        # Close the session when it is no longer needed
        db.close()

def lifespan(app: FastAPI):   
    db = SessionLocal()

    yield

    # Dispose the engine when the server is shut down
    db.close()
    engine.dispose()

def create_app():
    app = FastAPI(lifespan=lifespan)

    @app.get('/ms-2/health')
    def health():
        return JSONResponse(content={'status': 'ok'})
    
    @app.get('/ms-2/db/health')
    def db_ready(db: Session = Depends(get_db)):
        try:
            db.execute(text('SELECT 1'))
            return JSONResponse(content={'status': 'ok'})
        except Exception as e:
            print(e)
            return JSONResponse(content={'status': 'error'}, status_code=500)
    
    return app