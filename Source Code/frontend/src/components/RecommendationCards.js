import React from "react";

function RecommendationCards({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  return (
    <div className="recommendations-section">
      <h2>Recommended Devices</h2>

      <div className="cards">
        {recommendations.map((phone, index) => (
          <div key={index} className="card">
            <h3>#{index + 1} {phone.name}</h3>
            <p><strong>Price:</strong> ₹{phone.price}</p>
            <p><strong>Processor:</strong> {phone.processor_name}</p>
            <p><strong>Score:</strong> {phone.final_score}</p>

            <div className="score-bar">
              <div
                className="score-fill"
                style={{ width: `${phone.final_score * 10}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationCards;