# AI Recipe Finder

## Streamlit + OpenAI | Applied LLM Project

AI Recipe Finder is an interactive web application that generates cuisine-specific recipes based on ingredients provided by the user. It integrates OpenAI’s GPT model with a Streamlit interface to demonstrate practical LLM deployment in a consumer-facing application.

The project showcases structured prompting, API integration, session management, and user-centered design.

---

## Problem Statement

Many users have limited ingredients at home and struggle to decide what to cook. This application solves that problem by:

- Analyzing available ingredients  
- Suggesting compatible cuisines  
- Generating complete structured recipes  
- Providing relevant cooking video search guidance  

---

## Core Features

- Ingredient-based cuisine suggestion using GPT  
- Structured recipe generation including:
  - Recipe name  
  - Cooking time  
  - Difficulty level  
  - Ingredient quantities  
  - Substitution suggestions  
  - Numbered instructions  
- YouTube search term generation for guided cooking  
- Downloadable recipe output  
- Multi-step UI workflow using Streamlit session state  
- Secure API key handling via Streamlit Secrets  

---

## Technical Architecture

### Frontend Layer
Built using Streamlit to handle:
- User input  
- Pantry selection  
- Multi-step state management  
- Rendering structured AI outputs  

### AI Integration Layer
OpenAI GPT model performs:
- Cuisine classification  
- Recipe generation  
- Video search term generation  

Separate prompts are used for:
- Cuisine suggestion  
- Recipe creation  
- Video search optimization  

This modular design improves clarity and maintainability.

---

## Tech Stack

- Python  
- Streamlit  
- OpenAI API  
- GPT-3.5 Turbo  
- Prompt engineering  
- Session state management  

---

## Project Structure

├── app.py
├── README.md
└── .streamlit/
└── secrets.toml


---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/ai-recipe-finder.git
cd ai-recipe-finder

**Install dependencies**
pip install streamlit openai

**Configure API Key**
Create .streamlit/secrets.toml:

api_key = "YOUR_OPENAI_API_KEY"

Do not commit this file.

**Run the Application**
streamlit run app.py


