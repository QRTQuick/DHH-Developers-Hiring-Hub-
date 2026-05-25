# DHH - Developers Hiring Hub

A premium ecosystem for hiring developers based on real code and GitHub-powered credibility.

**Built by:** [Quick Red Tech Software Development Studio](https://quickredtech.com)

## Project Structure

```
/workspace
├── backend/                 # Flask API Backend
│   ├── app/                # Application package
│   │   ├── __init__.py     # App factory
│   │   ├── config.py       # Configuration
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── run.py              # Entry point
│   ├── requirements.txt    # Python dependencies
│   ├── pyproject.toml      # Vercel configuration
│   └── .env.example        # Environment variables template
├── frontend/               # Static Frontend
│   ├── index.html          # Home page
│   ├── search.html         # Search page
│   ├── dashboard.html      # Dashboard
│   ├── sitemap.xml         # SEO sitemap
│   ├── robots.txt          # Robots configuration
│   ├── vercel.json         # Frontend routing
│   └── static/             # CSS, JS, images
└── vercel.json             # Root Vercel configuration
```

## Deployment to Vercel

### Prerequisites
1. Vercel account
2. GitHub repository connected to Vercel

### Environment Variables (Set in Vercel Dashboard)

Required variables for production:

```bash
# Flask
SECRET_KEY=your-production-secret-key

# Database (Vercel PostgreSQL or external)
DATABASE_URL=postgresql://...

# JWT
JWT_SECRET_KEY=your-jwt-secret

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# GitHub OAuth (for GitHub integration)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Redis (optional, for caching)
REDIS_URL=redis://...
```

### Deploy Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Root Directory: Leave as `/` (monorepo setup)

3. **Configure Environment Variables**
   - Add all required environment variables in Vercel dashboard

4. **Deploy**
   - Vercel will automatically detect the configuration
   - Click "Deploy"

## Features

- 🔐 JWT Authentication
- 📧 Email notifications
- 🔗 GitHub integration
- 🚀 Real-time updates with Socket.IO
- 💾 PostgreSQL database
- 🎨 Modern responsive UI
- 📱 Mobile-friendly design
- 🔍 Developer search functionality
- 📊 Dashboard analytics

## Local Development

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python run.py
```

### Frontend Setup

Open `frontend/index.html` in a browser or use a local server:

```bash
cd frontend
python -m http.server 8000
```

## Technology Stack

**Backend:**
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-SocketIO
- PostgreSQL

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- GSAP Animations
- Google Fonts

**Deployment:**
- Vercel
- Vercel PostgreSQL (optional)

## License

© 2024 Quick Red Tech Software Development Studio

---

**Built with ❤️ by Quick Red Tech**
