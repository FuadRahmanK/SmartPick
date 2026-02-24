import React, { useState } from "react";
import "./styles.css";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! I'm SmartPick. What kind of phone are you looking for?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };

    // Use functional update to avoid stale state bug
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      if (data.type === "question") {
        setMessages(prev => [
          ...prev,
          { sender: "bot", text: data.message }
        ]);
      }

      if (data.type === "recommendation") {

        if (data.summary) {
          setMessages(prev => [
            ...prev,
            { sender: "bot", text: data.summary }
          ]);
        }

        if (data.ai_text) {
          setMessages(prev => [
            ...prev,
            { sender: "bot", text: data.ai_text }
          ]);
        }

        if (data.data && Array.isArray(data.data)) {
          data.data.forEach((phone, index) => {
            setMessages(prev => [
              ...prev,
              {
                sender: "bot",
                text: `#${index + 1} ${phone.name} (₹${phone.price})
Score: ${phone.final_score}
Processor: ${phone.processor_name}`
              }
            ]);
          });
        }

        if (data.follow_up) {
          setMessages(prev => [
            ...prev,
            { sender: "bot", text: data.follow_up }
          ]);
        }
      }

    } catch (error) {
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: "Something went wrong. Please try again." }
      ]);
    }

    setLoading(false);
    setInput("");
  };

  return (
    <div className="app">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="message bot">Typing...</div>}
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