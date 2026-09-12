"""Blog data and helpers for Meow OCR."""
import html as _html

BLOG_POSTS = [
    {
        "slug": "how-to-extract-text-from-scanned-pdf",
        "title": "How to Extract Text from a Scanned PDF in 2026 (Free, No Signup)",
        "description": "Step-by-step guide to extract editable text from any scanned PDF using free online OCR tools. No software install, no watermark.",
        "date": "2026-09-08",
        "updated": "2026-09-08",
        "category": "Guide",
        "read_time": "4 min",
        "cover_alt": "Extract text from scanned PDF free online",
        "content": """
<h2>Why Extract Text from a Scanned PDF?</h2>
<p>Scanned PDFs are just images locked inside a PDF container. You cannot copy, search or edit the text inside them. An <strong>OCR (Optical Character Recognition)</strong> tool reads the image and converts it into real, editable text you can paste anywhere.</p>

<h2>Step 1 — Open Meow OCR</h2>
<p>Go to <a href="/">meowocr.onrender.com</a> in any browser. No account needed.</p>

<h2>Step 2 — Upload Your PDF</h2>
<p>Drag and drop your scanned PDF or click <strong>Choose File</strong>. You can also select specific pages with the page-range option — useful for large documents.</p>

<h2>Step 3 — Pick a Language</h2>
<p>Choose the language of your document. Meow OCR supports <strong>19+ languages</strong> including Tamil, Hindi, English, French, Chinese and Arabic. The tool can also auto-detect the language.</p>

<h2>Step 4 — Download the Text</h2>
<p>Click <strong>Extract</strong>. Within seconds your text is ready. You can copy it directly or download a <code>.txt</code> file. Results auto-delete after 2 days for privacy.</p>

<h2>Tips for Better Accuracy</h2>
<ul>
<li>Use a clean scan — avoid blurry or rotated images.</li>
<li>Select the correct language for the best recognition.</li>
<li>For multi-page PDFs, process all pages at once instead of one by one.</li>
<li>If the scan is tilted, use a tool to deskew it before uploading.</li>
</ul>

<h2>FAQ</h2>
<h3>Is Meow OCR really free?</h3>
<p>Yes. No signup, no credit card, no watermark on the extracted text.</p>

<h3>What file types are supported?</h3>
<p>PDF, JPG, PNG, TIFF, BMP and scanned document images.</p>

<h3>Is my data safe?</h3>
<p>Files are processed in a secure environment and auto-deleted after 2 days. We never share or sell your data.</p>
""",
    },
    {
        "slug": "best-free-ocr-tools-compared",
        "title": "Best Free OCR Tools in 2026 — Meow OCR vs Alternatives",
        "description": "Compare the best free online OCR tools of 2026. Meow OCR, Google Drive OCR, OnlineOCR.net and more — features, accuracy and privacy compared.",
        "date": "2026-09-08",
        "updated": "2026-09-08",
        "category": "Comparison",
        "read_time": "5 min",
        "cover_alt": "Best free OCR tools comparison 2026",
        "content": """
<h2>What Makes a Good Free OCR Tool?</h2>
<p>The best OCR tools combine <strong>accuracy</strong>, <strong>speed</strong>, <strong>language support</strong> and <strong>privacy</strong>. Here is how the most popular free options compare.</p>

<h2>1. Meow OCR</h2>
<p><strong>Best for:</strong> Quick, private text extraction from PDFs and images.</p>
<ul>
<li>19+ languages with auto-detection</li>
<li>No signup, no watermark</li>
<li>Auto-delete after 2 days</li>
<li>Works on PDF, JPG, PNG, TIFF, BMP</li>
</ul>
<p><a href="/">Try Meow OCR free →</a></p>

<h2>2. Google Drive OCR</h2>
<p><strong>Best for:</strong> Google Workspace users who already store files in Drive.</p>
<ul>
<li>Built-in to Google Docs</li>
<li>Supports English, Spanish, French and more</li>
<li>Requires a Google account</li>
<li>Files stay in your Google Drive</li>
</ul>

<h2>3. OnlineOCR.net</h2>
<p><strong>Good for:</strong> One-off conversions.</p>
<ul>
<li>Free tier limited to 20 pages/hour</li>
<li>Supports 25+ languages</li>
<li>Requires email for full results</li>
<li>Output as TXT, DOCX or PDF</li>
</ul>

<h2>4. Tesseract (Desktop)</h2>
<p><strong>Best for:</strong> Developers and power users comfortable with the command line.</p>
<ul>
<li>100% free and open-source</li>
<li>Works offline</li>
<li>No web interface — requires installation</li>
<li>Best accuracy with pre-processed images</li>
</ul>

<h2>Comparison Table</h2>
<div class="table-wrap">
<table border="1" cellpadding="8" cellspacing="0" style="width:100%;border-collapse:collapse;">
<thead><tr><th>Feature</th><th>Meow OCR</th><th>Google Drive</th><th>OnlineOCR</th><th>Tesseract</th></tr></thead>
<tbody>
<tr><td>No signup</td><td>Yes</td><td>No</td><td>No</td><td>Yes</td></tr>
<tr><td>PDF support</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Languages</td><td>19+</td><td>10+</td><td>25+</td><td>100+</td></tr>
<tr><td>Auto-delete</td><td>2 days</td><td>Never</td><td>No</td><td>Local only</td></tr>
<tr><td>Watermark</td><td>None</td><td>None</td><td>None</td><td>None</td></tr>
</tbody>
</table>
</div>

<h2>Our Recommendation</h2>
<p>For quick, private text extraction with no strings attached, <strong>Meow OCR</strong> is the simplest choice. For large-scale or offline work, Tesseract is powerful but requires setup.</p>
""",
    },
    {
        "slug": "how-to-convert-image-to-text",
        "title": "How to Convert an Image to Text Online (JPG, PNG, TIFF)",
        "description": "Learn how to convert any image — JPG, PNG, TIFF or screenshot — into editable text using free online OCR. Copy-paste in seconds.",
        "date": "2026-09-07",
        "updated": "2026-09-07",
        "category": "Guide",
        "read_time": "3 min",
        "cover_alt": "Convert image to text online free",
        "content": """
<h2>Why Convert Images to Text?</h2>
<p>Screenshots, scanned documents and photos contain text you cannot copy. OCR technology reads the image and turns it into editable, searchable text.</p>

<h2>How to Do It with Meow OCR</h2>
<ol>
<li>Go to <a href="/">meowocr.onrender.com</a>.</li>
<li>Click <strong>Choose File</strong> or drag your image into the upload area.</li>
<li>Select the document language (or let the tool auto-detect).</li>
<li>Click <strong>Extract</strong> — the text appears in seconds.</li>
<li>Copy the text or click <strong>Download</strong> to save as a <code>.txt</code> file.</li>
</ol>

<h2>Supported Image Formats</h2>
<ul>
<li><strong>JPG / JPEG</strong> — the most common photo format</li>
<li><strong>PNG</strong> — screenshots and web images</li>
<li><strong>TIFF</strong> — high-quality scans</li>
<li><strong>BMP</strong> — uncompressed bitmaps</li>
</ul>

<h2>Tips for Best Results</h2>
<ul>
<li>Ensure the image is at least <strong>300 DPI</strong> for print scans.</li>
<li>Crop out irrelevant borders before uploading.</li>
<li>For handwritten text, select "Handwriting" mode if available.</li>
<li>Multiple images? Process them one at a time or batch-convert with a script.</li>
</ul>

<h2>Privacy Note</h2>
<p>Meow OCR auto-deletes all uploaded files after <strong>2 days</strong>. Your images are never stored permanently or shared with third parties.</p>
""",
    },
    {
        "slug": "tamil-ocr-extract-tamil-text",
        "title": "Tamil OCR — Extract Tamil Text from PDF & Images Online",
        "description": "Free Tamil OCR: convert Tamil PDFs, scanned documents and images into editable Tamil text. Supports Unicode Tamil, no signup required.",
        "date": "2026-09-06",
        "updated": "2026-09-06",
        "category": "Language",
        "read_time": "3 min",
        "cover_alt": "Tamil OCR extract Tamil text from documents",
        "content": """
<h2>What is Tamil OCR?</h2>
<p>Tamil OCR (Optical Character Recognition) reads Tamil text from scanned PDFs, images and documents and converts it into editable digital text. This is especially useful for digitizing old Tamil books, government forms and handwritten notes.</p>

<h2>How to Use Tamil OCR with Meow OCR</h2>
<ol>
<li>Go to <a href="/tamil-ocr">Meow OCR Tamil</a>.</li>
<li>Upload your Tamil PDF or image.</li>
<li>The language is pre-set to Tamil — just click <strong>Extract</strong>.</li>
<li>Copy or download the extracted Tamil text.</li>
</ol>

<h2>Why Meow OCR for Tamil?</h2>
<ul>
<li><strong>Unicode support</strong> — extracted Tamil renders correctly in any app.</li>
<li><strong>No signup</strong> — use it anonymously.</li>
<li><strong>Fast</strong> — results in seconds, not minutes.</li>
<li><strong>Free</strong> — no watermarks, no paywalls.</li>
</ul>

<h2>Common Use Cases</h2>
<ul>
<li>Digitizing Tamil newspapers and magazines</li>
<li>Extracting text from Tamil government documents</li>
<li>Converting Tamil handwriting to digital text</li>
<li>Searching through old Tamil books</li>
</ul>

<h2>Other Supported Languages</h2>
<p>Meow OCR also supports Hindi, English, French, German, Chinese, Japanese, Arabic and 12 more languages. <a href="/">Try it free →</a></p>
""",
    },
    {
        "slug": "digitize-handwritten-notes-ocr",
        "title": "How to Digitize Handwritten Notes with OCR (2026 Guide)",
        "description": "Convert handwritten notes to digital text using free OCR tools. Learn what works, what doesn't and how to get the best results.",
        "date": "2026-09-05",
        "updated": "2026-09-05",
        "category": "Guide",
        "read_time": "4 min",
        "cover_alt": "Digitize handwritten notes with OCR",
        "content": """
<h2>Can OCR Read Handwriting?</h2>
<p>Modern OCR engines have gotten surprisingly good at reading neat handwriting. Messy scrawl is still a challenge, but legible cursive and printed handwriting convert fairly well.</p>

<h2>Step-by-Step: Digitize Your Notes</h2>
<ol>
<li><strong>Photograph your notes</strong> — use good lighting and keep the page flat. A scanner app (like Microsoft Lens or Google Scan) works best.</li>
<li><strong>Upload to an OCR tool</strong> — <a href="/">Meow OCR</a> accepts images directly. No conversion needed.</li>
<li><strong>Select the language</strong> matching your notes.</li>
<li><strong>Review the output</strong> — OCR is not 100% accurate on handwriting. Proofread and fix any misread characters.</li>
</ol>

<h2>Tips for Better Handwriting Recognition</h2>
<ul>
<li><strong>Use lined paper</strong> — helps the OCR engine align text lines.</li>
<li><strong>Write neatly</strong> — print-style letters convert better than cursive.</li>
<li><strong>Use a dark pen</strong> — high contrast between ink and paper improves accuracy.</li>
<li><strong>Scan at 300 DPI or higher</strong> — low resolution = more errors.</li>
<li><strong>Crop tightly</strong> — remove margins and background clutter.</li>
</ul>

<h2>What About Cursive Handwriting?</h2>
<p>Cursive is harder for OCR engines. If your cursive is very flowing, consider using a tool that supports handwriting-specific models. Meow OCR handles printed handwriting well; for heavy cursive, you may need to correct more in the output.</p>

<h2>After Extraction</h2>
<p>Once digitized, your notes become searchable, copy-pasteable and easy to organize. Save them in Google Docs, Notion or any note app. <a href="/">Extract text now →</a></p>
""",
    },
    {
        "slug": "online-ocr-vs-desktop-ocr",
        "title": "Online OCR vs Desktop OCR — Which Should You Use?",
        "description": "Should you use an online OCR tool or install desktop software? Compare convenience, accuracy, privacy and cost to pick the right option.",
        "date": "2026-09-04",
        "updated": "2026-09-04",
        "category": "Comparison",
        "read_time": "4 min",
        "cover_alt": "Online OCR vs desktop OCR comparison",
        "content": """
<h2>The Quick Answer</h2>
<p>For most people, <strong>online OCR</strong> (like <a href="/">Meow OCR</a>) is faster and simpler. Desktop OCR is better for offline work, bulk processing or extreme privacy requirements.</p>

<h2>Online OCR — Pros and Cons</h2>
<div class="table-wrap">
<table border="1" cellpadding="8" cellspacing="0" style="width:100%;border-collapse:collapse;">
<thead><tr><th>Pros</th><th>Cons</th></tr></thead>
<tbody>
<tr><td>No installation needed</td><td>Requires internet connection</td></tr>
<tr><td>Works on any device</td><td>Files uploaded to a server (even briefly)</td></tr>
<tr><td>Usually free for light use</td><td>Limited file size or page count</td></tr>
<tr><td>Always up-to-date engine</td><td>Less control over processing</td></tr>
</tbody>
</table>
</div>

<h2>Desktop OCR — Pros and Cons</h2>
<div class="table-wrap">
<table border="1" cellpadding="8" cellspacing="0" style="width:100%;border-collapse:collapse;">
<thead><tr><th>Pros</th><th>Cons</th></tr></thead>
<tbody>
<tr><td>Works fully offline</td><td>Requires installation</td></tr>
<tr><td>No data leaves your machine</td><td>Can be expensive (Adobe Acrobat, ABBYY)</td></tr>
<tr><td>Bulk processing support</td><td>Needs updates and maintenance</td></tr>
<tr><td>Full control over settings</td><td>Only works on your computer</td></tr>
</tbody>
</table>
</div>

<h2>When to Choose Online OCR</h2>
<ul>
<li>You need a quick one-off conversion</li>
<li>You're on a phone or shared computer</li>
<li>You don't want to install anything</li>
<li>The document is not highly sensitive</li>
</ul>

<h2>When to Choose Desktop OCR</h2>
<ul>
<li>You process thousands of pages per week</li>
<li>You need 100% offline processing (legal/medical docs)</li>
<li>You need batch automation with custom scripts</li>
<li>You already own desktop OCR software</li>
</ul>

<h2>Our Pick</h2>
<p>For everyday use, <a href="/">Meow OCR</a> gives you the best balance of speed, simplicity and privacy — with zero setup and no account required.</p>
""",
    },
]


def get_all_posts():
    """Return posts sorted newest-first."""
    return sorted(BLOG_POSTS, key=lambda p: p["date"], reverse=True)


def get_post(slug):
    """Return a single post by slug, or None."""
    for p in BLOG_POSTS:
        if p["slug"] == slug:
            return p
    return None


def get_recent_posts(count=3):
    """Return the most recent posts (for homepage widget)."""
    return get_all_posts()[:count]


def escape(s):
    return _html.escape(s)
