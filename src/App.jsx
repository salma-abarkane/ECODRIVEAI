import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";
import TripChart from "./TripChart";

export default function App() {
  const [trip, setTrip] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const resultRef = useRef(null);

  const simulateTrip = async () => {
    const res = await axios.get("http://127.0.0.1:8000/simulate");
    setTrip(res.data);
    setAnalysis(null);
  };

 const analyzeTrip = async () => {
  try {
    setIsLoading(true);

    const res = await axios.post(
      "http://127.0.0.1:8000/full-report",
      trip
    );

    setAnalysis(res.data);
    if (resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth" });
    }
  } catch (err) {
    const msg = (err.response && (err.response.data.detail || JSON.stringify(err.response.data))) || err.message;
    setAnalysis(null);
  } finally {
    setIsLoading(false);
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
          <button className="button success" onClick={analyzeTrip} disabled={isLoading}>
            {isLoading ? "Analyse en cours..." : "Analyser la conduite"}
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
        <div className="card" ref={resultRef}>
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
