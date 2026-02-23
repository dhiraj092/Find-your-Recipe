AI Recipe Finder

Streamlit + OpenAI | Applied LLM Project

AI Recipe Finder is an interactive web application that generates cuisine-specific recipes based on ingredients provided by the user. It integrates OpenAI’s GPT model with a Streamlit interface to demonstrate practical LLM deployment in a consumer-facing application.

The project showcases structured prompting, API integration, session management, and user-centered design.

Problem Statement

Many users have limited ingredients at home and struggle to decide what to cook. This application solves that problem by:

Analyzing available ingredients

Suggesting compatible cuisines

Generating complete structured recipes

Providing relevant cooking video search guidance

Core Features

Ingredient-based cuisine suggestion using GPT

Structured recipe generation including:

Recipe name

Cooking time

Difficulty level

Ingredient quantities

Substitution suggestions

Step-by-step instructions

YouTube search term generation for guided cooking

Downloadable recipe output

Multi-step UI workflow using Streamlit session state

Secure API key handling via Streamlit Secrets

Technical Architecture
1. Frontend Layer

Streamlit handles:

User input

Pantry selection

Multi-step state management

Rendering generated outputs

2. AI Layer

OpenAI GPT model performs:

Cuisine classification based on ingredient combinations

Structured recipe generation

Video search term generation

Separate prompts are used for:

Cuisine suggestion

Recipe creation

Video search optimization

This separation improves modularity and output consistency.

3. Security

API key stored in .streamlit/secrets.toml

No hard-coded credentials

Basic error handling for API failures

Tech Stack

Python

Streamlit

OpenAI API

GPT-3.5 Turbo

Session state management

Prompt engineering for structured output

Project Structure
├── app.py
├── README.md
└── .streamlit/
    └── secrets.toml

app.py contains application logic and AI integration.

secrets.toml stores environment variables (not committed).

Installation
Clone the Repository
git clone https://github.com/your-username/ai-recipe-finder.git
cd ai-recipe-finder
Install Dependencies
pip install streamlit openai
Configure API Key

Create .streamlit/secrets.toml:

api_key = "YOUR_OPENAI_API_KEY"

Do not commit this file.

Running the Application
streamlit run app.py

The app launches locally in your browser.

Implementation Highlights

Uses structured prompt templates to enforce consistent recipe formatting.

Extracts recipe name programmatically from model output.

Splits logic into modular functions for maintainability.

Uses Streamlit session state for multi-step interaction.

Integrates external video search dynamically without embedding.
