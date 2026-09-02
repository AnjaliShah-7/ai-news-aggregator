https://openai.com/news/
https://www.anthropic.com/engineering
https://www.anthropic.com/research

AI News Aggregator
This project is an end-to-end Generative AI system that automates the collection, processing, and curation of news updates. It utilizes a modular agentic architecture to deliver a personalized daily digest directly to your inbox.

🏗️ Architecture
The system is built on a clean separation of concerns, utilizing a base agent class for extensibility and specialized services for each stage of the pipeline:

mermaid
graph TD
Sources[YouTube / OpenAI / Anthropic] --> Scrapers
Scrapers --> DB[(PostgreSQL)]
DB --> DigestAgent[Digest Agent]
DigestAgent --> DB
DB --> CuratorAgent[Curator Agent]
CuratorAgent --> EmailAgent[Email Agent]
EmailAgent --> User[User Inbox]

🛠️ Tech Stack
Language: Python
Database: PostgreSQL (SQLAlchemy)
AI/LLM: OpenAI GPT-4o mini
Orchestration: Custom Runner & Agentic Flow
Deployment: Docker & Render
🚀 Project Components
Scrapers: Monitors and extracts content from defined sources, filtering for the last 24 hours.
Digest Agent: Summarizes technical articles and videos into concise, actionable markdown snippets.
Curator Agent: Ranks content based on a customizable User Profile to ensure relevance.
Email Agent: Formats and delivers the final ranked digest.
⚙️ Getting Started
Environment Setup: Configure your .env file with necessary API keys.
Database: Initialize the PostgreSQL schema using the provided Docker configuration.
Run: Execute the daily_runner.py to trigger the full end-to-end pipeline.