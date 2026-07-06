from backend.models import AnalysisResult, TripData

def analyze_driving(trip: TripData) -> AnalysisResult:

    if (
        trip.vitesse_moyenne > 90
        and trip.rpm_moyen > 3000
        and trip.acceleration_moyenne > 2.5
        and trip.consommation > 8
    ):
        style = "Agressif"
        eco_score = 50
        risk = "Usure moteur, freins et surconsommation"
        advice = "Réduisez les accélérations brusques et stabilisez votre vitesse"

    elif trip.vitesse_moyenne > 60 or trip.acceleration_moyenne > 1.8:
        style = "Dynamique"
        eco_score = 70
        risk = "Usure modérée des freins"
        advice = "Anticipez le trafic pour limiter les accélérations"

    else:
        style = "Éco"
        eco_score = 90
        risk = "Faible"
        advice = "Très bonne conduite, continuez ainsi"

    return AnalysisResult(
        style=style,
        eco_score=eco_score,
        risk=risk,
        advice=advice
    )
