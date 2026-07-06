import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

export default function TripChart({ trip }) {
 const maxValues = {
  vitesse: 130,
  rpm: 6000,
  acceleration: 5,
  consommation: 15,
};

const data = {
  labels: [
    "Vitesse",
    "RPM",
    "Accélération",
    "Consommation",
  ],
  datasets: [
    {
      label: "Niveau (%)",
      data: [
        (trip.vitesse_moyenne / maxValues.vitesse) * 100,
        (trip.rpm_moyen / maxValues.rpm) * 100,
        (trip.acceleration_moyenne / maxValues.acceleration) * 100,
        (trip.consommation / maxValues.consommation) * 100,
      ],
      backgroundColor: [
        "#3b82f6",
        "#ef4444",
        "#f59e0b",
        "#10b981",
      ],
      borderRadius: 8,
    },
  ],
};


 const options = {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: (value) => value + "%",
      },
    },
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => ctx.raw.toFixed(1) + "%",
      },
    },
  },
};


  return <Bar data={data} options={options} />;
}
