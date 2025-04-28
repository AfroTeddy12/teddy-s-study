# AI-Powered Flashcard System

This is a Python-based flashcard system that uses Google's Gemini AI to generate flashcards, read them aloud, and answer questions about the content.

## Features

- Generate flashcards on any topic using Gemini AI
- Text-to-speech functionality to read flashcards aloud
- Ask questions about the current flashcard and get AI-generated answers
- Navigate through flashcards easily

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

To get a Google API key:
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key and paste it in your `.env` file

## Usage

Run the application:
```bash
python flashcard_system.py
```

The program will present a menu with the following options:
1. Generate new flashcards - Enter a topic to create flashcards
2. Read current card - Hear the current flashcard read aloud
3. Ask a question about current card - Get AI-generated answers about the current card
4. Next card - Move to the next flashcard
5. Previous card - Move to the previous flashcard
6. Exit - Close the program

## Requirements

- Python 3.7+
- Google API key for Gemini AI
- Internet connection for AI functionality
- Text-to-speech system (pyttsx3) 