# Interactive AI Chat Application

## Introduction

This project involves creating a frontend application using React that enables users to have interactive conversations with a custom AI model. The application utilizes a provided Google Colab notebook for running the AI model and an example Python file for interacting with it.

## Video Walkthrough

A video walkthrough of the application's features and functionality can be found [here](https://drive.google.com/file/d/1tScaxRKfHUBE8zI-uFX1Z67fYY9dANlf/view).

## Features

- User-friendly chat interface for interactive conversations
- Integration of AI model for generating responses to user messages
- Message limit of 25 messages per user
- Optional login system for tracking users' messages
- Bonus Points: Incorporation of Silero Text-to-Speech (TTS) for voice output

## Getting Started

To get started with the application, follow these steps:

1. Clone this repository.
   ```bash
   git clone https://github.com/git-rishab/run-your-gpt.git
2. Set up the backend server using Flask.
   - Set Up a Virtual Environment: `python -m venv venv`
   - Activate virtual Environment:
       - For Windows: `venv\Scripts\activate`
       - For Mac and Linux: `source venv/bin/activate`
    - Install Dependencies: `pip install -r requirements.txt`
    - Set up the environments variable by giving the `MONGO` url in .env file
    - Run the server: `flask run --reload`
3. Change the streaming server url at line 18 of chatStream.py that is given by running the code in [notebook](https://colab.research.google.com/drive/1BkL7zYVYtn0JPYKMPJ0tJmK-zMtINx0P?usp=sharing).
4. Set up the frontend:
   - Install Dependencies: `npm i`
   - Start the frontend: `npm run dev`

## API Endpoints

- `/login` POST: Endpoint for user login
- `/register` POST: Endpoint for user registration
- `/audio` POST: Endpoint for text to speech conversion
- `/chat` POST: Endpoint for interacting with the AI model

## Tech Stack

- Frontend: React with Mantine UI
- Backend: Flask

## Screenshots of Application
- **Fig 1: Login Page of the Application**
---
![Screenshot (670)](https://github.com/git-rishab/run-your-gpt/assets/114337213/afadfdb7-63a3-4ac7-9d2e-87d78e5ddd2b)
---
- **Fig 2: Chat Interface**
---
![Screenshot (671)](https://github.com/git-rishab/run-your-gpt/assets/114337213/e67443a5-b096-4362-8533-0a316ce785be)
---


For more detailed instructions and code explanations, refer to the provided Google Colab notebook and example Python file.

For any further questions or assistance, please reach out to [rishabkumarchaurasiya@gmail.com](mailto:rishabkumarchaurasiya@gmail.com).
