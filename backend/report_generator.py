import logging
import requests
import json
from fastapi import HTTPException
from backend.models import TripData, AnalysisResult

OLLAMA_URL = "http://localhost:11434/api/generate"

logger = logging.getLogger("report_generator")


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

    logger.info("Calling Ollama to generate report")
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.exception("Ollama request failed")
        raise HTTPException(status_code=502, detail=f"Ollama request failed: {e}")

    try:
        data = response.json()
    except ValueError:
        logger.exception("Invalid JSON from Ollama")
        raise HTTPException(status_code=502, detail="Invalid JSON returned by Ollama")

    logger.debug("Ollama response keys: %s", list(data.keys()) if isinstance(data, dict) else type(data))

    # Prefer top-level "response" per Ollama non-streaming API
    report = ""
    if isinstance(data, dict):
        report = (data.get("response") or data.get("content") or "")

    if not report:
        # Fallback: previous code attempted to read results[0]
        if isinstance(data, dict) and "results" in data and data["results"]:
            first_result = data["results"][0]
            report = first_result.get("response") or first_result.get("content") or first_result.get("output", "")

    if not report:
        logger.error("Empty report returned from Ollama: %s", data)
        raise HTTPException(status_code=502, detail="Empty response from Ollama")

    logger.info("Generated report length: %d", len(report))
    return report.strip()
