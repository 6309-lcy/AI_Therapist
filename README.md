#  Mental Health Chatbot

**AI Therapist Demo**  
A voice- and text-based AI-powered mental health support chatbot that detects user sentiment, responds empathetically, and connects to emergency services when needed. This demo simulates core functionality for future integration into a physical companion product.

---

##  Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Authors](#authors)

---

##  Features

-  **Text and Voice Interaction**  
  Users can interact through a web-based chat interface.

-  **Sentiment Analysis**  
  Detects emotional tone and flags negative or depressive input.

-  **Alert System**  
  Triggers hotline numbers or emergency contact calls when danger(Sentimental Score getting too high) is detected.

-  **User Reports**  
  Records and categorizes issues for therapist follow-up.

-  **Referral Logic**  
  Connects users to real therapists for escalated support. Booking service system (To be integrated)

---

##  Project Structure
```
mental_health_chatbot/ 
│
├── app/
│ ├── models/ # User profiles, sentiment analyzer
│ ├── services/ # Voice services, LLM (chatbot), alerts
│ ├── static/ # CSS and JS assets
│ ├── templates/ # HTML templates (chat, report, homepage)
│ ├── init.py # App factory
│ ├── extensions.py # App extensions (e.g., database)
│ └── routes.py # Flask routes and logic
│
├── instance/
│ ├── chatbot.db # SQLite database for users & logs
├── config.py # App configuration
├── reset_data.py # Script to reset database
├── run.py # Entry point to start the app
├── .env # Environment variables (not tracked)
├── .gitignore # Git ignored files
└── requirements.txt # Python dependencies
```
---

## Usage

- **Interface**
  index.html: Landing page

  chat.html: AI-powered chat interface

  report.html: Display emotional report and flagged incidents

- **Features Demoed**:
  Real-time chatbot interaction

  Emotion detection and escalation simulation

  User mood history and profile tracking

---

## Technologies Used
- **Flask** – lightweight backend framework

- **Jinja2** – for HTML templates

- **SQLite** – database to store logs and users

- **Custom ML models** – for sentiment analysis (placeholder) | Used vaderSentiment's Sentimental Model here. Can be replaced by custom sentimental model

- **HTML/CSS/JS** – for front-end structure and interaction

- **Conversational AI** - for real time chatbot interaction | Used Elevenlabs conversational ai here.

---

## Run the demo
- **Prerequisites**
  -  Python 3.10
  -  requirements.txt
  -  Elevenlabs API key and Elevenlabs Conversational AI agentID
-  **Steps**
  -  Create .env in the same dir as mental-health-chatbot
  -  Create variable "agent_id" & "ELEVENLABS_API_KEY"
  -  Change sentimental model as you like (if you wish to)

---
## Authors
Lam Cheuk Yin, Anson; Poon Man Hin, Gordon – Initial development and concept



