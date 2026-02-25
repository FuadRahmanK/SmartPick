import React, { useState, useRef, useEffect } from "react";
import "./styles.css";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! I'm SmartPick. What kind of phone are you looking for?" }
  ]);
  const [recommendations, setRecommendations] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, recommendations]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      if (data.type === "question") {
        setMessages(prev => [...prev, { sender: "bot", text: data.message }]);
        setRecommendations([]);
      }

      if (data.type === "recommendation") {

        if (data.summary) {
          setMessages(prev => [...prev, { sender: "bot", text: data.summary }]);
        }

        if (data.ai_text) {
          setMessages(prev => [...prev, { sender: "bot", text: data.ai_text }]);
        }

        setRecommendations(data.data || []);

        if (data.follow_up) {
          setMessages(prev => [...prev, { sender: "bot", text: data.follow_up }]);
        }
      }

    } catch (error) {
      setMessages(prev => [...prev, { sender: "bot", text: "Something went wrong." }]);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="chat-area">

        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}

          {recommendations.length > 0 && (
            <div className="recommendations">
              {recommendations.map((phone, index) => (
                <div key={index} className="card">
                  <strong>#{index + 1} {phone.name}</strong>
                  <div>Price: ₹{phone.price}</div>
                  <div>Processor: {phone.processor_name}</div>
                  <div>Score: {phone.final_score}</div>
                </div>
              ))}
            </div>
          )}

          {loading && <div className="message bot">Thinking...</div>}

          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            placeholder="Type your requirement..."
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>

      </div>
    </div>
  );
}

export default App;