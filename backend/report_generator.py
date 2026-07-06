import requests
import json
from backend.models import TripData, AnalysisResult

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_report(trip: TripData, analysis: AnalysisResult) -> str:
    prompt = f"""
Tu es un expert en éco-conduite automobile.

Données du trajet :
- Vitesse moyenne : {trip.vitesse_moyenne} km/h
- Régime moteur moyen : {trip.rpm_moyen} tr/min
- Accélération moyenne : {trip.acceleration_moyenne} m/s²
- Consommation : {trip.consommation} L/100km
- Freinages brusques : {trip.freinages_brutaux}

Analyse :
- Style de conduite : {analysis.style}
- Score écologique : {analysis.eco_score}/100
- Risque : {analysis.risk}

Rédige un rapport clair et pédagogique (5–7 lignes) en français,
avec des conseils concrets d’éco-conduite.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": True
        },
        stream=True,      # 🔥 CRITIQUE
        timeout=None      # 🔥 CRITIQUE
    )

    report = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            report += data.get("response", "")

    return report.strip()
