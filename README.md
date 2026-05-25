# DHH — Developers Hiring Hub

Built by **Quick Red Tech Software Development Studio**.

DHH is a premium developer hiring ecosystem focused on GitHub-powered credibility, real-world developer verification, portfolio intelligence, and recruiter discovery.

## Tech Stack

### Frontend
- **HTML5/CSS3**: Vanilla architecture for performance.
- **GSAP**: High-end animations and smooth transitions.
- **Responsive Design**: Mobile-first approach.
- **Glassmorphism**: Modern SaaS UI style.

### Backend
- **Flask**: Python-based microframework.
- **Blueprints**: Modular architecture.
- **JWT**: Secure authentication.
- **Socket.IO**: Real-time notifications and activity.
- **PostgreSQL**: Robust data persistence (Neon).
- **Redis (Optional)**: Caching and rate limiting.

## Project Structure
```text
/backend
  /app
    /models     # SQLAlchemy Models
    /routes     # API Endpoints
    /services   # Business Logic (GitHub Analytics)
    /utils      # Helpers & Socket events
  /run.py       # Entry point
/frontend
  /static       # CSS, JS, Images
  /templates    # HTML Views
  index.html    # Landing Page
  dashboard.html# Developer Dashboard
  search.html   # Recruiter Hub
```

## Features
1. **GitHub Intelligence**: Auto-sync repositories, stars, and contribution patterns.
2. **AI Developer Score**: proprietary scoring based on commit frequency, project quality, and collaboration.
3. **Smart Matching**: Timezone and stack-aware hiring search.
4. **Real-time Feed**: Live updates on hiring status and contributions.
5. **Premium UI**: Dark-mode optimized, neon-accented, glassmorphism interface.

## Installation & Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create a `.env` file with `DATABASE_URL`, `JWT_SECRET_KEY`, and `GITHUB_TOKEN`.
4. Run `python run.py`.

### Frontend
Serve the `frontend` folder using any static server (e.g., Live Server, Nginx, or Vercel).

## Deployment
- **Frontend**: Deploy to **Vercel** or Netlify.
- **Backend**: Deploy to **Render**, **Railway**, or **Heroku**.
- **Database**: Use **Neon.tech** for serverless PostgreSQL.
