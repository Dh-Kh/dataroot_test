# AI Chatbot with Google Docs Integration

This FastAPI-powered AI chatbot seamlessly integrates with Google Docs, allowing users to have natural language conversations and then save the chat history directly into a Google Doc.

## Features

- **Intelligent Conversation:** Powered by OpenAI's language models (e.g., GPT-3.5) for engaging and informative interactions.
- **Google Docs Integration:** Automatically save chat transcripts to Google Docs for easy reference and organization.
- **Session Management:** Maintains conversation history using Redis for personalized interactions.
- **FastAPI Framework:**  Ensures high performance, scalability, and a modern web API experience.
- **Background Tasks:** Uses background tasks (e.g., Celery) to handle Google Docs interactions asynchronously.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Dh-Kh/dataroot_test.git
   ```

2. **Set up your Environment Variables**

3. **Obtain Google API Credentials**

4. **Run the Application**
  ```bash
  docker-compose build
  docker-compose up -d
  docker-compose run app python3 main.py
  docker-compose run redis redis-cli
  ```
