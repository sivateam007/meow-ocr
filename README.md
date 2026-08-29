# Tamil PDF OCR Web App

Offline, web-based OCR application for extracting Tamil text from PDF files. Hosted on Render, accessible from mobile and desktop.

## Features
- Fully offline OCR processing (no external APIs)
- Supports Tamil language (தமிழ்) by default
- Processes PDF files up to 100MB
- Mobile-responsive web interface
- Returns downloadable `.txt` output with page separators

## Project Structure
```
render ocr/
├── Dockerfile          # Linux container setup with Tesseract & Poppler
├── requirements.txt    # Python dependencies
├── app.py              # Flask web application
├── templates/
│   └── index.html     # Mobile-friendly upload form
└── .gitignore         # Excludes unnecessary files
```

## Deployment to Render

### Step 1: Create Git Repository
```bash
cd "C:\Users\siva\Desktop\render ocr"
git init
git add .
git commit -m "Initial commit: Tamil PDF OCR app"
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
- Install Tesseract with Tamil language pack
- Install Poppler utilities
- Start the Flask application

### Step 4: Test
- Access your app at the provided Render URL (e.g., `https://your-app.onrender.com`)
- Upload a Tamil PDF from mobile or desktop
- Download the extracted `.txt` file

## Local Testing (Optional)
```bash
cd "C:\Users\siva\Desktop\render ocr"
pip install -r requirements.txt

# Windows: Set Tesseract path if needed
# set TESSERACT_PATH="C:\Program Files\Tesseract-OCR\tesseract.exe"

# Run the app
python app.py
```
Visit `http://localhost:8080` in your browser.

## Future Extensions
- Add support for more Tesseract languages (English, Hindi, etc.)
- Add image file support (PNG, JPG) for mobile document photos
- Add in-browser text preview alongside download
- User accounts with OCR history
- Background task processing for large PDFs (to avoid Render timeout)

## Notes
- Render free tier has a 30-second request timeout. Large/multi-page PDFs may timeout.
- For production use with large files, consider upgrading to a paid Render plan.
- OCR processing happens entirely on the server using locally installed Tesseract.
