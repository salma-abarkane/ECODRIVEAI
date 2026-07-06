import { useState } from "react";
import axios from "axios";
import "./App.css";
import TripChart from "./TripChart";

export default function App() {
  const [trip, setTrip] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const simulateTrip = async () => {
    const res = await axios.get("http://127.0.0.1:8000/simulate");
    setTrip(res.data);
    setAnalysis(null);
  };

 const analyzeTrip = async () => {
  try {
    console.log("Trip envoyé :", trip);

    const res = await axios.post(
      "http://127.0.0.1:8000/full-report",
      trip
    );

    console.log("Réponse analyse :", res.data);
    setAnalysis(res.data);
  } catch (err) {
    console.error("Erreur analyse :", err);
  }
};


  return (
    <div className="container">
      <div className="header">
        <h1>🚗 EcoDriveAI</h1>
        <p>Analyse intelligente et éco-responsable de la conduite</p>
      </div>

      <div className="buttons">
        <button className="button primary" onClick={simulateTrip}>
          Simuler un trajet
        </button>

        {trip && (
          <button className="button success" onClick={analyzeTrip}>
            Analyser la conduite
          </button>
        )}
      </div>

      {trip && (
        <div className="card">
          <h2>Données du trajet</h2>
         
         <pre>{JSON.stringify(trip, null, 2)}</pre>
        <h2>📊 Graphique du trajet</h2>
    <TripChart trip={trip} />
        </div>
        
      )}

      {analysis && (
        <div className="card">
          <h2>Résultat IA</h2>
          <p><b>Style :</b> {analysis.style}</p>
          <p><b>Eco-score :</b> {analysis.eco_score}</p>
          <p><b>Risque :</b> {analysis.risk}</p>
          <p><b>Conseil :</b> {analysis.advice}</p>
           <hr />

    <h3>🧠 Rapport IA</h3>
    <p style={{ whiteSpace: "pre-line" }}>
      {analysis.generated_report}
    </p>
        </div>
      )}
    </div>
  );
}
