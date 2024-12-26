# Intelligent Business Template Plugin: Supercharge Your Planning with AI

This plugin is your AI-powered assistant for creating professional business documents. By analyzing your conversations and uploaded transcripts, it automatically generates detailed templates, saving you time and effort.

## Table of Contents

*   [Overview](#overview)
*   [Key Features](#key-features)
*   [Benefits](#benefits)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Configuration](#configuration)
        *   [Backend Configuration (`.env`)](#backend-configuration-env)
        *   [Frontend Configuration (`.env`)](#frontend-configuration-env)
    *   [Running the Plugin](#running-the-plugin)
*   [Usage](#usage)
    *   [Connecting to Messaging Platforms (Future)](#connecting-to-messaging-platforms-future)
    *   [Uploading Transcripts](#uploading-transcripts)
    *   [Generating Templates](#generating-templates)
    *   [Exporting Templates](#exporting-templates)
*   [Architecture](#architecture)
    *   [Backend (Flask)](#backend-flask)
    *   [Frontend (Next.js)](#frontend-nextjs)
*   [Technology Stack](#technology-stack)
*   [Contributing](#contributing)
*   [Roadmap](#roadmap)
*   [License](#license)
*   [Support](#support)
*   [FAQ](#faq)
*   [Troubleshooting](#troubleshooting)
*   [Deployment](#deployment)

## Overview

Planning is crucial for any successful venture, but creating detailed business documents can be time-consuming. This plugin bridges the gap by using AI to extract key information from your discussions and automatically generate professional templates.

## Key Features

*   **Multi-Platform Integration:** Connect with Slack, (coming soon: Microsoft Teams and slack). Direct transcript uploads are also available (.txt,.pdf,.docx).
*   **Intelligent NLP Processing:** Advanced Natural Language Processing (NLP) powered by OpenAI extracts key points, action items, and relevant data from your conversations.
*   **Versatile Template Generation:** Create three core template types:
    *   **Business Plans:** Comprehensive plans covering all aspects of your business.
    *   **Pitch Decks:** Engaging presentations for investors and stakeholders.
    *   **Marketing Strategies:** Targeted strategies to reach your desired audience.
*   **Industry-Specific Templates (Future):** Tailored templates for specific industries like SaaS, E-commerce, and B2B.
*   **Flexible Export Options:** Export your templates in Word (.docx), PDF, or PowerPoint (.pptx) formats. Integrations with Notion and Google Docs are planned.
*   **Real-Time AI Suggestions (Future):** Get AI-powered prompts during conversations to ensure you capture all necessary information.

## Benefits

*   **Save Time and Effort:** Automate the tedious process of creating business documents.
*   **Improve Decision-Making:** Gain valuable insights from your discussions to make informed decisions.
*   **Enhance Collaboration:** Facilitate clear communication and shared understanding.
*   **Create Professional Documents:** Generate polished templates that impress.

## Getting Started

### Prerequisites

*   Python 3.7+ (Recommended: 3.9+)
*   Node.js 16+ (LTS Recommended) and npm or yarn
*   A Firebase project with Firestore enabled. You'll need a service account key file.
*   An OpenAI API key.
*   (Optional) Accounts and necessary configurations for Slack, Microsoft Teams, and WhatsApp Business API (when fully implemented).

### Installation

1.  Clone the repository: `git clone https://github.com/your-username/intelligent-business-template-plugin.git`
2.  Navigate to the project directory: `cd intelligent-business-template-plugin`
3.  Install dependencies:
    *   Backend: `cd backend && pip install -r requirements.txt`
    *   Frontend: `cd frontend && npm install` (or `yarn install`)

### Configuration

#### Backend Configuration (`.env`)

Create a `.env` file in the `backend` directory and populate it with the following, replacing placeholders with your actual values:

```
SECRET_KEY=a_strong_random_secret_key # Generate a strong random key (e.g., using `openssl rand -hex 32`)
OPENAI_API_KEY=your_actual_openai_api_key
FIREBASE_CREDENTIALS=path/to/your/firebase_credentials.json # or set GOOGLE_APPLICATION_CREDENTIALS environment variable
YOUR_SLACK_BOT_TOKEN=your_slack_bot_token
YOUR_TEAMS_WEBHOOK_URL=your_microsoft_teams_webhook_url
GOOGLE_SERVICE_ACCOUNT_CREDENTIALS=path/to/your/google_cloud_credentials.json # Required for Google Docs integration
YOUR_NOTION_INTEGRATION_TOKEN=your_notion_integration_token # Required for Notion integration
```

**Important Notes for Firebase Credentials:**
*   The recommended and most secure way is to set the `FIREBASE_CREDENTIALS` environment variable to the *absolute* path of your service account key JSON file.
*   Alternatively, you can set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable, which is useful for deployments on Google Cloud environments.
*   Storing the `serviceAccountKey.json` file directly in the `backend` directory is the least secure option and is strongly discouraged for production environments.

#### Frontend Configuration (`.env`)

Create a `.env` file in the `frontend` directory:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000 # Or your deployed backend URL (e.g., [invalid URL removed])
```

### Running the Plugin

1.  **Backend:** Open a terminal in the `backend` directory and run: `python main.py`
2.  **Frontend:** Open another terminal in the `frontend` directory and run: `npm run dev` (or `yarn dev`)

Open http://localhost:3000 in your browser.

## Usage

### Connecting to Messaging Platforms (Future)

This feature is currently under development. Detailed instructions will be provided upon release.

### Uploading Transcripts

1.  Navigate to the plugin's home page.
2.  Click the "Upload Transcript" button.
3.  Select your transcript file (.txt,.pdf, or.docx).
4.  Confirm the upload.

### Generating Templates

1.  After uploading a transcript or (in the future) connecting to a messaging platform, select the desired template type (Business Plan, Pitch Deck, or Marketing Strategy).
2.  The plugin will process the data and generate a preview of the template.
3.  Review the generated content.

### Exporting Templates

1.  Once you're satisfied with the generated template, choose the desired export format (Word, PDF, or PowerPoint).
2.  Click the "Export" button. The file will be downloaded to your computer.

## Architecture

### Backend (Flask)

The backend is built using Flask and handles the core logic:

*   `app/routes/`: Defines API endpoints for communication with the frontend.
*   `app/services/`: Contains the business logic for:
    *   `messaging.py`: Integrations with messaging platforms.
    *   `nlp_processor.py`: NLP processing using the OpenAI API.
    *   `template_service.py`: Template generation and export functions.
*   `app/models/`: Defines data models, such as the `TemplateModel`.
*   `app/utils/`: Contains utility functions and configuration.
*   `app/templates/`: Stores industry-specific template structures.

### Frontend (Next.js)

The frontend is built with Next.js and provides the user interface:

*   `components/`:
```Y4:0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/status-development-orange)](https://github.com/your-username/intelligent-business-template-plugin)
[![GitHub Issues](https://img.shields.io/github/issues/your-username/intelligent-business-template-plugin)](https://github.com/your-username/intelligent-business-template-plugin/issues)
[![GitHub Pull Requests](https://img.shields.io/github/pulls/your-username/intelligent-business-template-plugin)](https://github.com/your-username/intelligent-business-template-plugin/pulls)
[![Netlify Status](https://api.netlify.com/api/v1/badges/your-netlify-site-id/deploy-status)](https://app.netlify.com/sites/your-netlify-site-name/deploys) [![Vercel Status](https://vercel.com/badge?app=your-vercel-app-id&token=your-vercel-token)](https://vercel.com/your-username/your-project-name)
