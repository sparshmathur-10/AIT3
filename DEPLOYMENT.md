# AITodo Deployment Guide

## Overview

This guide covers deploying both the Django backend and React frontend to Render.

## Backend Deployment (Django)

### 1. Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `aitodo-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn aitodo.wsgi:application --bind 0.0.0.0:$PORT`

### 2. Environment Variables

Set these in Render dashboard:

```
SECRET_KEY=your_django_secret_key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgres://... (from Render PostgreSQL)
GOOGLE_CLIENT_ID=your_google_client_id
GITHUB_TOKEN=your_github_token
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
JWT_SECRET_KEY=your_jwt_secret
```

### 3. Database Setup

1. Create PostgreSQL database in Render
2. Copy the DATABASE_URL to environment variables
3. The build script will run migrations automatically

## Frontend Deployment (React)

### 1. Create Render Static Site

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `aitodo-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

### 2. Environment Variables

Set these in Render dashboard:

```
REACT_APP_API_URL=https://your-backend-app-name.onrender.com/api
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
```

## Google OAuth Setup

### 1. Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Configure:
   - **Application type**: Web application
   - **Authorized JavaScript origins**:
     - `http://localhost:3000` (development)
     - `https://your-frontend-domain.com` (production)
   - **Authorized redirect URIs**:
     - `http://localhost:3000` (development)
     - `https://your-frontend-domain.com` (production)

### 2. Update Environment Variables

- Backend: `GOOGLE_CLIENT_ID=your_client_id`
- Frontend: `REACT_APP_GOOGLE_CLIENT_ID=your_client_id`

## GitHub Token Setup

### 1. Create Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Copy token to backend environment: `GITHUB_TOKEN=your_token`

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm start
```

### Environment Files

Create `.env` files in both directories:

**Backend (.env):**

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
GOOGLE_CLIENT_ID=your_google_client_id
GITHUB_TOKEN=your_github_token
```

**Frontend (.env):**

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
```

## Testing

### 1. Backend API

Test endpoints with curl or Postman:

```bash
# Test Google auth (requires valid token)
curl -X POST http://localhost:8000/api/auth/google/ \
  -H "Content-Type: application/json" \
  -d '{"token": "your_google_token"}'

# Test todos (requires auth)
curl -X GET http://localhost:8000/api/todos/ \
  -H "Authorization: Bearer your_jwt_token"
```

### 2. Frontend

1. Open http://localhost:3000
2. Click "Sign in with Google"
3. Add some todos
4. Test "Plan with AI" functionality

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure CORS_ALLOWED_ORIGINS includes your frontend domain
2. **Database Connection**: Verify DATABASE_URL is correct
3. **Google OAuth**: Check client ID and authorized origins
4. **Build Failures**: Check build logs in Render dashboard

### Logs

- Backend logs: Render dashboard → Web Service → Logs
- Frontend build logs: Render dashboard → Static Site → Logs

## Security Notes

1. **Never commit .env files** to version control
2. **Use strong secret keys** for production
3. **Enable HTTPS** (automatic on Render)
4. **Regular security updates** for dependencies
5. **Monitor logs** for suspicious activity

## Performance Optimization

1. **Database indexing** for large datasets
2. **Caching** for frequently accessed data
3. **CDN** for static assets (automatic on Render)
4. **Image optimization** for profile pictures
5. **Code splitting** in React (already implemented)
