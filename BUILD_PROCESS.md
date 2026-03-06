# BUILD PROCESS

This document explains the development process of **SmartPick**, describing how the project evolved from a simple rule-based prototype into a deployed conversational smartphone recommendation system.

The system was developed iteratively, with multiple improvements to the dataset, recommendation logic, user interaction, and deployment architecture.

---

## 1. Initial Idea and First Steps

The initial goal was to build a system that could help users choose smartphones based on their preferences such as camera quality, battery life, performance, and price.

The first step was creating a structured dataset of smartphones.
A dataset of **61 smartphones** was compiled containing attributes such as:

* name
* brand
* price
* processor name
* camera score
* battery score
* performance score
* display score
* software score
* value score

Each feature score was initially represented using **whole numbers from 0–10**.

These values allowed the system to compare phones using a weighted scoring approach.

---

## 2. First Prototype: Fully Rule-Based System

The first working prototype was a **fully rule-based recommendation system** that ran locally.

The system:

* asked predefined questions
* expected structured answers
* used deterministic logic to compute recommendations

While this system worked technically, it felt **very rigid and unnatural** because users had to respond in very specific formats.

---

## 3. Improving Interaction with AI

To make the system more conversational, I explored adding an AI layer.

The initial idea was to integrate the **OpenAI API** to:

* rewrite system questions in a more natural conversational tone
* understand flexible user responses

However, OpenAI required a paid API plan, which was not ideal for development and experimentation.

As an alternative approach, I switched to using **Ollama with the Mistral model** running locally.
This allowed the system to interpret natural language inputs without requiring an external paid service.

Importantly, the **core recommendation engine remained deterministic**.
AI was only used for language understanding, while the decision logic itself remained rule-based and explainable.

---

## 4. Improving the Decision Logic

After implementing conversational input, I realized the system still asked too many unnecessary questions.

To improve efficiency and personalization, I made several changes:

* implemented **dynamic question skipping**, allowing the system to skip questions when enough information was already available
* introduced **feature weight normalization**, ensuring that the scoring system remained balanced regardless of user input

These changes made the recommendations more tailored to the user instead of producing general suggestions.

---

## 5. Refactoring the Frontend

The original interface was very basic and static.

To improve usability, I refactored the frontend using **React**.

This change allowed the application to support:

* a conversational chat interface
* dynamic UI updates
* smoother interaction with the backend

Additional UI improvements included:

* acknowledgment responses after user inputs
* a header displaying the application name
* a **dark mode toggle**

These changes significantly improved the overall user experience.

---

## 6. Enhancing the User Experience

Further improvements focused on making the recommendations more visually informative.

I extended the dataset to include:

* phone images
* purchase links

These were displayed in recommendation cards on the frontend.

Additional UI features were added, including:

* smooth UI transitions
* typing animations to simulate chatbot responses

These improvements helped make the system feel more like a conversational assistant rather than a static tool.

---

## 7. Dataset Refinement

During testing, I noticed that using **whole number feature scores (0–10)** sometimes produced less precise rankings.

To improve the recommendation quality, I refactored the dataset so that feature scores used **decimal values between 0–10** instead.  
This allowed more granular distinctions between devices and produced more accurate recommendations.

Additionally, I introduced a **processor_score** attribute to the dataset.  
This score represents the relative performance capability of the phone’s processor and is used to refine the overall performance evaluation.

The system then computes an **effective performance score** by combining the performance score and processor score, allowing the recommendation engine to better reflect real-world device performance.

---

## 8. Deployment Challenges and Architecture Changes

The next goal was to make the system publicly accessible online.

However, running **Ollama with a local Mistral model** on a cloud server would require paid infrastructure.

To solve this problem, I explored alternative AI providers and decided to use the **Groq API**, which provides fast inference for open-source models without requiring local model hosting.

This required several changes to the system:

* replacing the Ollama integration with Groq API calls
* adapting the backend to run in a hosted environment

The final deployment architecture became:

Frontend → **Vercel**
Backend API → **Render**
AI processing → **Groq API**

---

## 9. Final Deployment and Repository Setup

After completing the system improvements and architecture changes:

* the backend was deployed on **Render**
* the frontend was deployed on **Vercel**
* environment variables were configured for the Groq API

Finally, the full project code was uploaded to a **GitHub repository**, and the live application was successfully deployed.

The system is now publicly accessible at:

https://smart-pick-eight.vercel.app/

---

## Key Technical Challenges

During development, several technical challenges were encountered:

**Making the conversation feel natural**

The initial rule-based system required users to respond with specific formats, which made the interaction feel rigid.  
Introducing an AI layer helped interpret natural language responses and improved the conversational experience.

**Balancing AI usage with deterministic decision logic**

While AI was useful for understanding user inputs, relying on it for recommendations could produce inconsistent results.  
To maintain reliability, AI was limited to language understanding while the recommendation engine remained deterministic.

**Improving recommendation precision**

Using whole-number feature scores initially produced less precise rankings.  
Refining the dataset to use decimal scores allowed more granular distinctions between devices.

**Deploying AI processing in a cloud environment**

Running a local model with Ollama was not practical for cloud deployment without paid infrastructure.  
Switching to the Groq API allowed the system to maintain AI capabilities while remaining easily deployable.

These challenges influenced several design decisions and helped shape the final architecture of the system.

---

## Summary

The project evolved from a simple rule-based prototype into a conversational smartphone recommendation system through several iterations. Improvements were made to the dataset, decision logic, and user interface, while different AI integration approaches were explored. The final system combines deterministic recommendation logic with AI-assisted natural language understanding and is deployed online for public use.