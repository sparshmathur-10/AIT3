# AITodo - AI-Powered Todo Application

A modern, production-ready todo application with AI-powered task planning built with React, Django, and PostgreSQL.

## Features

- 🔐 Google OAuth Authentication
- ✅ Todo Management (Create, Read, Update, Delete)
- 🤖 AI-Powered Task Planning with DeepSeek API
- 🎨 Modern Black/Red Theme with Material-UI
- 🚀 Production Ready for Render Deployment

## Tech Stack

- **Frontend**: React 18, TypeScript, Material-UI, Google OAuth
- **Backend**: Django 4.2, Django REST Framework, JWT Authentication
- **Database**: PostgreSQL
- **Deployment**: Render

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL
- Google OAuth Client ID
- GitHub Personal Access Token (for DeepSeek API)

### Environment Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your credentials:
   ```
   GOOGLE_CLIENT_ID=your_google_client_id
   GITHUB_TOKEN=your_github_token
   SECRET_KEY=your_django_secret_key
   DATABASE_URL=your_postgres_url
   ```

### Local Development

1. **Backend Setup**:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Production Deployment

1. **Render Setup**:

   - Create a new Web Service
   - Connect your GitHub repository
   - Set environment variables
   - Deploy

2. **Database**:
   - Create PostgreSQL database on Render
   - Update DATABASE_URL in environment variables

## API Endpoints

- `POST /api/auth/google/` - Google OAuth authentication
- `GET /api/todos/` - List todos
- `POST /api/todos/` - Create todo
- `PUT /api/todos/{id}/` - Update todo
- `DELETE /api/todos/{id}/` - Delete todo
- `POST /api/todos/plan/` - AI planning endpoint

## Project Structure

```
AIT3/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── backend/           # Django application
│   ├── aitodo/
│   │   ├── api/
│   │   ├── authentication/
│   │   └── settings/
│   └── manage.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
