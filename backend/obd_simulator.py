import random
from backend.models import TripData

def generate_trip():
    speeds = [random.randint(0, 130) for _ in range(10)]
    rpms = [random.randint(800, 4000) for _ in range(10)]

    acceleration = round(random.uniform(0.5, 3.5), 2)  # m/s²
    consommation = round(random.uniform(4.5, 10.0), 2) # L/100km

    return TripData(
        vitesse_moyenne=round(sum(speeds) / len(speeds), 2),
        rpm_moyen=round(sum(rpms) / len(rpms), 2),
        acceleration_moyenne=acceleration,
        consommation=consommation,
        freinages_brutaux=random.randint(0, 5)
    )
