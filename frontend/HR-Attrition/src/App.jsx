import React from "react";
import PredictionForm from "./components/PredictionForm";
import "./App.css";

export default function App() {
  return (
    <div className="App">
      <header>
        <h1>HR Attrition Predictor</h1>
      </header>

      <main>
        <PredictionForm />
      </main>
    </div>
  );
}
