# System Architecture

```mermaid
graph TD

User --> ReactUI
ReactUI --> FlaskAPI
FlaskAPI --> ConversationManager

ConversationManager --> InputParser
ConversationManager --> AILayer

ConversationManager --> DecisionEngine

DecisionEngine --> SmartphoneDataset

DecisionEngine --> Recommendations
Recommendations --> ReactUI