# RESEARCH LOG

This document records research, search queries, and AI usage during the development of SmartPick.

---

# 1. AI Prompts and Usage

AI was used during development to explore design ideas, generate datasets, improve system architecture, and refine documentation.

Below are the major prompts and ideas explored.

---

## Project Planning and System Design

Initial planning prompts focused on defining the problem and designing a system that could act as a **Decision Companion System**.

* I am assigned a home assignment by a company to build a "Decision Companion System" that assists users in making a real-world decision. I plan to build a system that helps users choose a smartphone within a budget using a web interface.

* The project needs to include a Git repository with source code, README.md, design diagrams, BUILD_PROCESS.md, and RESEARCH_LOG.md.

* I want users to type requirements conversationally and return ranked smartphone recommendations.

* I want the system to behave like a conversation and ask follow-up questions when necessary.

---

## Dataset Design

* I want to build a dataset containing at least 50 smartphones focused on the Indian market between ₹10,000 and ₹2,00,000.

* The dataset should include whether the phone is Android or iOS.

* Software experience should be treated as a weighted feature similar to camera or battery.

* Generate a structured dataset outline with brand distribution.

* Generate a partially filled sample dataset so I can replicate the scoring pattern.

* Include processor information such as Snapdragon or Apple A-series chips in the dataset.

AI outputs were used as **guidance only**, while final scores and device selections were manually verified.

---

## Conversational System Design

AI prompts were used to explore how the system should behave as a conversational assistant.

* The user should interact with the system through a chat-style interface.

* System should dynamically decide what question to ask next based on the information already provided.

* System should ask follow-up questions if the budget or feature preferences are unclear.

* Ask about important features such as performance, battery, camera, display, and software before giving final recommendations.

* Skip questions for features that were already mentioned by the user.

* Short acknowledgement responses should be included so the system feels interactive without feeling robotic.

This research helped shape the **adaptive conversational flow and dynamic question selection logic** used in the system.

---

## Hybrid AI + Rule-Based Architecture

Several prompts explored different architectures for combining AI with deterministic logic.

* Should I build a fully AI-driven system or a hybrid rule-based system?

* I want the recommendation engine to remain deterministic but use AI for natural language understanding.

* I want hybrid rule-based intent detection with AI phrasing.

The final architecture chosen was:

* **Rule-based parsing for structured information**
* **AI for interpreting natural language inputs**
* **Deterministic scoring algorithm for recommendations**

---

## Debugging and System Refinement

* The frontend and backend are greeting twice and the system says something went wrong at the end.

* Remove greeting from the backend and keep it in the frontend.

* The system gets stuck repeatedly asking about the budget.

* Normalize feature weights before calculating recommendations.

* If the user does not specify Android or iOS, treat it as no preference.

* Add fallback logic so the system still works if AI responses fail.

---

## UI and UX Improvements

* Improve UI layout with structured chat messages and recommendation cards.

* Add a dark mode option.

* Add phone images and purchase links to recommendation cards.

* Add typing animations and smooth transitions to improve interaction.

* Add a button to start a new conversation after recommendations are shown.

---

## Deployment Architecture

AI was also used to explore deployment strategies.

* Is it better to run a local LLM or use a hosted model when deploying a web application?

* What free AI models are suitable for hosting?

Initially the system used **Ollama with the Mistral model** locally.

However, hosting a local LLM required paid infrastructure, so the system was later migrated to use the **Groq API** for AI processing.

---

## Documentation Assistance

AI was also used to help structure documentation files required for submission:

* README.md
* BUILD_PROCESS.md
* RESEARCH_LOG.md

AI outputs were reviewed and edited to accurately reflect the actual implementation.

---

# 2. Google Searches

Several Google searches were used to gather factual data and implementation guidance.

* best smartphones in India across all price ranges
* authoritative sources for evaluating processor performance, camera quality, battery life, display quality, software experience, and overall value
* specifications and pricing information for the selected 61 smartphones
* best free AI models for local development
* best AI models suitable for hosted applications
* how to create architecture diagrams
* sources for phone images and purchase links

These searches were used to ensure that the dataset and system design were based on realistic information.

---

# 3. YouTube Resources

YouTube tutorials were used to learn implementation and deployment techniques.

* how to build a chatbot using Python
* how to deploy a Flask backend using Render
* how to configure environment variables for API keys
* how to deploy a React frontend and connect it to a backend API

These resources helped implement and deploy the full-stack application.

---

# 4. How AI Outputs Were Used

AI-generated suggestions were used as **guidance and starting points**.

During development:

Accepted outputs:

* architectural suggestions
* conversational flow ideas
* dataset structure guidance
* documentation structuring

Modified outputs:

* AI-generated code suggestions were often adjusted to fit the existing system architecture.

Rejected outputs:

* AI-generated recommendation logic was rejected to ensure the final recommendation system remained deterministic and explainable.

---

# Summary

AI tools and online resources were used throughout development to assist with planning, design, debugging, and documentation. However, the final system architecture, recommendation logic, dataset construction, and deployment decisions were carefully reviewed and implemented manually to ensure correctness and reliability.
