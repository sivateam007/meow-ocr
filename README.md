# Meow OCR 🐱

**Live site:** https://www.meowocr.work.gd

Free, 24x7 online OCR + translation web app that extracts text from PDFs and images (Tamil தமிழ், English, Hindi, and 19+ languages) and can translate the result. Cat-branded 🐾, mobile-friendly, and hosted on Render.

## Features
- PDF & image OCR (Tesseract, on-server — no external APIs)
- Supports Tamil (தமிழ்), English, Hindi, Telugu, Bengali and 19+ languages with auto-detection
- Translation of extracted text (Google Translate)
- Cloud recovery via Mega (recover completed OCR results)
- Processes PDFs up to 100MB (batched for speed)
- Mobile-responsive web interface
- Returns downloadable `.txt` output with page separators
- Keepalive uptime monitoring, SEO-ready (sitemap, robots.txt, canonical URLs, JSON-LD)

## Project Structure
```
render ocr/
├── Dockerfile              # Linux container setup with Tesseract & Poppler
├── requirements.txt        # Python dependencies
├── app.py                  # Flask web application (OCR + translate + cloud)
├── render.yaml             # Render service config
├── templates/
│   ├── index.html          # Upload + OCR + Translate UI, Meow gallery
│   ├── downloads.html      # Download results + cloud recovery panel
│   ├── processing.html     # Processing/progress page
│   ├── progress_check.html # Live task progress page
│   └── how_to_use.html, privacy.html, terms.html
├── static/
│   ├── style.css
│   └── images/             # Meow cat branding & gallery images
└── .gitignore
```

## Live Deployment
- **URL:** https://www.meowocr.work.gd
- **Platform:** Render (free Docker plan)
- **Health check:** `https://www.meowocr.work.gd/healthz`
- **Uptime monitoring:** UptimeRobot (every 5 min)

## Deployment to Render

### Step 1: Create Git Repository
```bash
cd "D:\project"
git init
git add .
git commit -m "Initial commit: Meow OCR app"
```

### Step 2: Push to GitHub/GitLab
1. Create a new repository on GitHub/GitLab
2. Push the code:
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 3: Deploy on Render
1. Sign up/login to [Render](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub/GitLab repository
4. Configure:
   - **Runtime**: Docker
   - **Instance Type**: Free (or paid for larger files/longer timeouts)
5. Click "Create Web Service"

Render will automatically:
- Build the Docker image
- Install Tesseract with Tamil + multi-language packs
- Install Poppler utilities
- Start the Flask application

### Step 4: Test
- Access your app at the provided Render URL (e.g., `https://scantext-ocr.onrender.com` or your custom domain)
- Upload a PDF/image from mobile or desktop
- Download the extracted `.txt` file

## Env Variables (Render → Environment)
- `SITE_URL` — canonical site URL (e.g. `https://www.meowocr.work.gd`)
- `FLASK_SECRET_KEY` — app secret
- `MEGA_EMAIL` / `MEGA_PWD` — Mega cloud (for cloud recovery)
- `GA4_ID` / `CLARITY_ID` — optional Google Analytics 4 / Microsoft Clarity (unset = off)
- `OCR_SPACE_API_KEY` — optional faster external OCR (fallback if set)

## Notes
- Render free tier has a 30-second request timeout. Large/multi-page PDFs may be slow — OCR is processed in background batched tasks.
- OCR processing happens entirely on the server using locally installed Tesseract (with optional external OCR API fallback).
- The `work.gd` free domain may be blocked on some networks; a real domain is recommended for best reliability.
