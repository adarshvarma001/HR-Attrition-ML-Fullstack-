import React, { useEffect, useState } from "react";

const BACKEND = import.meta.env.VITE_API_URL || "http://localhost:5000";

const defaultJobRoles = [
  "Sales Executive",
  "Research Scientist",
  "Laboratory Technician",
  "Manufacturing Director",
  "Healthcare Representative",
  "Manager",
  "Sales Representative",
  "Research Director",
  "Human Resources"
];

export default function PredictionForm() {
  const [meta, setMeta] = useState(null);
  const [result, setResult] = useState(null);

  const [form, setForm] = useState({
    Age: 30,
    MonthlyIncome: 3000,
    JobRole: "Sales Executive",
    TotalWorkingYears: 5,
    WorkLifeBalance: 3,
    DistanceFromHome: 10,
    YearsSinceLastPromotion: 1,
    PerformanceRating: 3,
    OverTime: "No"
  });

  useEffect(() => {
    // Fetch metadata (OHE categories etc)
    fetch(`${BACKEND}/meta`)
      .then(res => res.json())
      .then(data => setMeta(data))
      .catch(() => setMeta(null));
  }, []);

  const jobRoles =
    meta?.meta?.ohe_categories?.flat() || defaultJobRoles;

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setResult(null);

    const payload = {
      ...form,
      Age: Number(form.Age),
      MonthlyIncome: Number(form.MonthlyIncome),
      TotalWorkingYears: Number(form.TotalWorkingYears),
      WorkLifeBalance: Number(form.WorkLifeBalance),
      DistanceFromHome: Number(form.DistanceFromHome),
      YearsSinceLastPromotion: Number(form.YearsSinceLastPromotion),
      PerformanceRating: Number(form.PerformanceRating)
    };

    const res = await fetch(`${BACKEND}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    setResult(data);
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Age</label>
        <input
          type="number"
          name="Age"
          value={form.Age}
          onChange={handleChange}
        />

        <label>Monthly Income</label>
        <input
          type="number"
          name="MonthlyIncome"
          value={form.MonthlyIncome}
          onChange={handleChange}
        />

        <label>Job Role</label>
        <select name="JobRole" value={form.JobRole} onChange={handleChange}>
          {jobRoles.map((role, i) => (
            <option key={i} value={role}>
              {role}
            </option>
          ))}
        </select>

        <label>Total Working Years</label>
        <input
          type="number"
          name="TotalWorkingYears"
          value={form.TotalWorkingYears}
          onChange={handleChange}
        />

        <label>Work Life Balance (1 to 4)</label>
        <select
          name="WorkLifeBalance"
          value={form.WorkLifeBalance}
          onChange={handleChange}
        >
          <option value={1}>1 (Low)</option>
          <option value={2}>2</option>
          <option value={3}>3 (Good)</option>
          <option value={4}>4 (Best)</option>
        </select>

        <label>Distance From Home (km)</label>
        <input
          type="number"
          name="DistanceFromHome"
          value={form.DistanceFromHome}
          onChange={handleChange}
        />

        <label>Years Since Last Promotion</label>
        <input
          type="number"
          name="YearsSinceLastPromotion"
          value={form.YearsSinceLastPromotion}
          onChange={handleChange}
        />

        <label>Performance Rating (1–5)</label>
        <select
          name="PerformanceRating"
          value={form.PerformanceRating}
          onChange={handleChange}
        >
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
          <option value={4}>4</option>
          <option value={5}>5</option>
        </select>

        <label>Over Time</label>
        <select
          name="OverTime"
          value={form.OverTime}
          onChange={handleChange}
        >
          <option value="No">No</option>
          <option value="Yes">Yes</option>
        </select>

        <button type="submit">Predict</button>
      </form>

      {result && (
        <div className="result-box">
          <h3>Prediction Result</h3>
          <p>
            <strong>Attrition Probability:</strong>{" "}
            {result.attrition_probability * 100}%
          </p>
          <p>
            <strong>Predicted Label:</strong> {result.attrition_label}
          </p>
          <p>
            <strong>Suggestions:</strong> {result.suggestions}
          </p>
        </div>
      )}
    </div>
  );
}
