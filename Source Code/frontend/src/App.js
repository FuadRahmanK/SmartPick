import React, { useState, useRef, useEffect } from "react";
import "./styles.css";

function App() {

  const initialGreeting = {
    sender: "bot",
    text: "Hi! I'm SmartPick. What kind of phone are you looking for?"
  };

  const [messages, setMessages] = useState([initialGreeting]);
  const [recommendations, setRecommendations] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isClearing, setIsClearing] = useState(false);

  const messagesEndRef = useRef(null);

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
        if (data.ai_text) {
          setMessages(prev => [...prev, { sender: "bot", text: data.ai_text }]);
        }
        setRecommendations(data.data || []);
      }

    } catch (error) {
      setMessages(prev => [...prev, { sender: "bot", text: "Something went wrong." }]);
    }

    setLoading(false);
  };

  const startNewConversation = async () => {
    setIsClearing(true);

    try {
      await fetch("/reset", { method: "POST" });
    } catch (error) {
      console.error("Reset failed");
    }

    setTimeout(() => {
      setMessages([initialGreeting]);
      setRecommendations([]);
      setInput("");
      setIsClearing(false);
    }, 300);
  };

  return (
    <div className={`app ${isClearing ? "fade-out" : "fade-in"}`}>

      <div className="messages">

        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender} fade-message`}>
            {msg.text}
          </div>
        ))}

        {recommendations.length > 0 && (
          <div className="recommendations">
            {recommendations.map((phone, index) => (
              <div
                key={index}
                className="card fade-card"
                style={{ animationDelay: `${index * 0.15}s` }}
              >

                {index === 0 && (
                  <div className="top-badge">Top Pick</div>
                )}

                <img
                  src={phone.image_url}
                  alt={phone.name}
                  className="phone-image"
                />

                <div className="card-content">
                  <h3>#{index + 1} {phone.name}</h3>
                  <p className="price">₹{phone.price}</p>
                  <p>Processor: {phone.processor_name}</p>
                  <p>Score: {phone.final_score}</p>

                  <div className="score-bar">
                    <div
                      className="score-fill"
                      style={{ width: `${phone.final_score * 10}%` }}
                    ></div>
                  </div>

                  {phone.buy_url && (
                    <a
                      href={phone.buy_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="buy-btn"
                    >
                      Buy Now
                    </a>
                  )}

                </div>
              </div>
            ))}

            <button
              className="new-chat-btn"
              onClick={startNewConversation}
            >
              Start New Conversation
            </button>

          </div>
        )}

        {loading && (
          <div className="message bot typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}

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
  );
}

export default App;