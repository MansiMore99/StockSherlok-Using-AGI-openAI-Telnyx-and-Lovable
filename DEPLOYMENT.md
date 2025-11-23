# Deployment Guide

This guide covers different ways to deploy StockSherlok.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)

## Local Development

### Quick Start

Run the automated setup script:

```bash
./setup.sh
```

Or follow manual steps:

### Backend

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create and configure `.env`:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Start the server:
```bash
python app.py
```

Server will be available at `http://localhost:5000`

### Frontend

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

App will open at `http://localhost:3000`

## Docker Deployment

### Using Docker Compose (Recommended)

#### Production Deployment

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_key_here
TELNYX_API_KEY=your_key_here
TELNYX_PHONE_NUMBER=your_number_here
```

2. Build and start services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: `http://localhost`
- Backend API: `http://localhost:5000`

4. View logs:
```bash
docker-compose logs -f
```

5. Stop services:
```bash
docker-compose down
```

#### Development with Hot Reload

For development with code hot-reloading:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

This mounts your source code as volumes for live updates.

### Individual Docker Containers

#### Backend
```bash
cd backend
docker build -t stocksherlok-backend .
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your_key \
  -e TELNYX_API_KEY=your_key \
  stocksherlok-backend
```

#### Frontend
```bash
cd frontend
docker build -t stocksherlok-frontend .
docker run -p 80:80 stocksherlok-frontend
```

## Cloud Deployment

### Heroku

#### Backend

1. Create a Heroku app:
```bash
heroku create stocksherlok-api
```

2. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your_key
heroku config:set TELNYX_API_KEY=your_key
heroku config:set TELNYX_PHONE_NUMBER=your_number
```

3. Deploy:
```bash
cd backend
git subtree push --prefix backend heroku main
```

#### Frontend

1. Build the production version:
```bash
cd frontend
npm run build
```

2. Deploy to Netlify/Vercel or serve with static hosting

### AWS

#### Using Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB application:
```bash
cd backend
eb init -p python-3.10 stocksherlok
```

3. Create environment:
```bash
eb create stocksherlok-env
```

4. Set environment variables:
```bash
eb setenv OPENAI_API_KEY=your_key
eb setenv TELNYX_API_KEY=your_key
```

5. Deploy:
```bash
eb deploy
```

### Google Cloud Platform

#### Using Cloud Run

1. Build container:
```bash
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/stocksherlok
```

2. Deploy:
```bash
gcloud run deploy stocksherlok \
  --image gcr.io/PROJECT_ID/stocksherlok \
  --platform managed \
  --set-env-vars OPENAI_API_KEY=your_key
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | `sk-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELNYX_API_KEY` | Telnyx API key for voice features | - |
| `TELNYX_PHONE_NUMBER` | Your Telnyx phone number | - |
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Backend server port | `5000` |
| `REACT_APP_API_URL` | Backend API URL for frontend | `http://localhost:5000/api` |

## Production Considerations

### Security

1. **Never commit API keys** - Use environment variables
2. **Enable HTTPS** - Use SSL certificates in production
3. **Rate limiting** - Implement API rate limiting
4. **CORS** - Configure CORS for your domain only

### Performance

1. **Caching** - Implement Redis caching for stock data
2. **CDN** - Use CDN for frontend static assets
3. **Load balancing** - Use load balancer for multiple backend instances
4. **Database** - Add PostgreSQL for storing analysis history

### Monitoring

1. **Logging** - Implement structured logging
2. **Error tracking** - Use Sentry or similar
3. **Metrics** - Monitor API response times
4. **Alerts** - Set up alerts for errors and downtime

## Scaling

### Horizontal Scaling

1. Use container orchestration (Kubernetes, ECS)
2. Implement message queue for async processing
3. Add read replicas for database

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Implement caching layer

## Troubleshooting

### Backend won't start
- Check Python version (3.8+)
- Verify all dependencies installed
- Check API keys in `.env`
- Review logs for errors

### Frontend won't connect to backend
- Verify backend is running
- Check `REACT_APP_API_URL` in frontend `.env`
- Check CORS settings in backend

### Docker issues
- Ensure Docker is running
- Check port availability
- Review Docker logs: `docker-compose logs`

## Support

For issues and questions:
- Check the main [README.md](../README.md)
- Review API documentation
- Open an issue on GitHub
