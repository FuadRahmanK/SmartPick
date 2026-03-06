# SmartPick

SmartPick is an intelligent conversational system that helps users choose the best smartphone based on their preferences such as budget, operating system, and feature priorities like camera, battery, performance, display, and software quality.

Instead of showing a simple list of phones, SmartPick interacts with the user through a conversation to understand their needs and then recommends the most suitable devices using a deterministic scoring algorithm.

The system combines rule-based logic with AI-powered natural language understanding to create a reliable and flexible recommendation experience.

---

## Live Demo

The project is fully deployed and can be accessed online:

https://smart-pick-eight.vercel.app/

The frontend is hosted on **Vercel**, and the backend API is hosted on **Render**.

Tech Stack: **React • Flask • Groq API • Vercel • Render**

---

## Problem Understanding

Choosing a smartphone today is difficult because:

- There are hundreds of available models
- Specifications are complex for non-technical users
- Different users value different features
- Traditional comparison sites require manual filtering

The goal of this project is to build a **decision companion system** that:

1. Conversationally gathers user preferences
2. Converts those preferences into structured data
3. Applies a deterministic ranking algorithm
4. Recommends the most suitable smartphones

---

## Assumptions Made

- Users may describe preferences using natural language.
- Budget is the primary filtering constraint.
- Feature importance can be mapped to a rating scale between 1 and 5.
- Smartphone scores are normalized between 0 and 10.

---

## Dataset

The system uses a structured dataset of 61 smartphones across both Android and iOS platforms.

Each phone includes:

- name
- brand
- price
- processor
- processor_score
- camera_score
- battery_score
- performance_score
- display_score
- software_score
- value_score

---

## Recommendation Algorithm

The system ranks smartphones using a weighted scoring model.

The recommendation process follows these steps:

1. Filter phones within the user's budget
2. Apply OS preference filtering
3. Ask the user about feature priorities
4. Convert feature importance ratings into normalized feature weights
5. Compute a weighted score for each phone
6. Rank phones by score
7. Return the top three recommendations

User feature importance ratings (1–5) are first amplified and normalized so that the weights sum to 1.  
This emphasizes stronger preferences while keeping the scoring scale consistent.

The final score for each phone is then calculated as:

```
Score =
camera_weight × camera_score +
battery_weight × battery_score +
performance_weight × effective_performance +
display_weight × display_score +
software_weight × software_score +
value_weight × value_score
```

Where performance is adjusted using processor score:

```
effective_performance =
0.7 × performance_score +
0.3 × processor_score
```

---

## Design Decisions

**Hybrid AI + Rule System**

Rule-based parsing is fast and reliable for structured patterns such as budgets and OS preferences.  
AI fallback ensures the system can handle flexible natural language input.

AI is used only for natural language processing tasks:

- correcting spelling mistakes
- extracting structured information
- inferring feature importance ratings

The recommendation logic itself remains deterministic to ensure consistency and explainability.

**Deterministic Recommendation Engine**

The ranking algorithm is deterministic to guarantee repeatable and explainable recommendations.

**Variance-Based Question Selection**

The system asks about features with the highest variance among remaining phones to maximize information gain.

---

## Edge Cases Considered

- No phones available within the specified budget
- User does not specify OS preference
- User provides ambiguous input
- AI response parsing failure
- Invalid feature rating input
- Empty recommendation results

Fallback logic ensures the system continues functioning in these scenarios.

---

## Future Improvements

- Larger smartphone dataset
- User preference learning
- Explainable recommendation reasoning
- Real-time price tracking
- Phone comparison interface

---