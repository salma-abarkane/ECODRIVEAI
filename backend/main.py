from fastapi import FastAPI
from backend.models import TripData, AnalysisResult
from backend.obd_simulator import generate_trip
from backend.ai import analyze_driving
from backend.report_generator import generate_report
from backend.models import FullReport
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from backend.database import trips_collection

app = FastAPI(title="EcoDriveAI API",
    description="API d’analyse intelligente de conduite à partir de données OBD-II simulées",
    version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Status"])
def root():
    """
    Vérifie que l'API EcoDriveAI fonctionne correctement.
    """
    return {"message": "EcoDriveAI API is running"}


@app.get("/simulate", response_model=TripData, tags=["Simulation"])
def simulate_trip():
    """
    Simule un trajet automobile via des données OBD-II :
    - vitesse moyenne
    - régime moteur moyen
    - nombre de freinages brusques
    """
    return generate_trip()


@app.post("/full-report", response_model=FullReport, tags=["Rapport IA"])
def full_report(trip: TripData):
    analysis = analyze_driving(trip)
    report = generate_report(trip, analysis)

    document = {
        "date": datetime.utcnow(),
        "trip": trip.dict(),
        "analysis": {
            "style": analysis.style,
            "eco_score": analysis.eco_score,
            "risk": analysis.risk,
            "advice": analysis.advice,
        },
        "generated_report": report,
    }

    trips_collection.insert_one(document)

    return FullReport(
        style=analysis.style,
        eco_score=analysis.eco_score,
        risk=analysis.risk,
        advice=analysis.advice,
        generated_report=report,
    )
