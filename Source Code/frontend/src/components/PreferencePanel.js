import React from "react";

function PreferencePanel({ preferences }) {
  return (
    <div className="preferences-panel">
      <h3>Your Requirements</h3>
      {Object.keys(preferences).length === 0 ? (
        <p>No preferences captured yet.</p>
      ) : (
        <ul>
          {Object.entries(preferences).map(([key, value]) => (
            <li key={key}>
              <strong>{key}</strong>: {value}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default PreferencePanel;