from pydantic import BaseModel



class TripData(BaseModel):
    vitesse_moyenne: float
    rpm_moyen: float
    freinages_brutaux: int
    acceleration_moyenne: float   
    consommation: float
class AnalysisResult(BaseModel):
    style: str
    eco_score: int
    risk: str
    advice: str
class FullReport(BaseModel):
    style: str
    eco_score: int
    risk: str
    advice: str
    generated_report: str
