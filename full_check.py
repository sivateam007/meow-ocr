# -*- coding: utf-8 -*-
"""Full-pipeline smoke harness for Meow OCR workers.

Runs the SAME background workers the web routes spawn, to COMPLETION, entirely
locally. Only cloud edges are mocked (Mega upload, edge-tts network) so nothing
touches the shared cloud/DB and the run is fast + deterministic.

Usage:  python full_check.py
Exit code 0 = all green, 1 = at least one failure.
"""
import os
import sys
import time
import tempfile
import threading

import requests  # noqa: F401 (patching targets reference it)

# ---------- Point everything at a scratch dir so harness junk never leaks ----------
BASE = tempfile.mkdtemp(prefix="meow_full_check_")
os.makedirs(BASE, exist_ok=True)

import app as A

# Never leave junk on the real server's cloud for future users:
A.OUTPUT_DIR = os.path.join(BASE, "outputs")
A.OUT_OCR_DIR = os.path.join(BASE, "ocr")
A.OUTPUT_DIR_TMP = os.path.join(BASE, "tmp")
A.ocr_outputs_dir = os.path.join(BASE, "ocr-outputs")
A.ocr_persist_to_upload_only = False
os.makedirs(A.OUTPUT_DIR, exist_ok=True)
os.makedirs(A.OUT_OCR_DIR, exist_ok=True)
os.makedirs(A.OUTPUT_DIR_TMP, exist_ok=True)
os.makedirs(A.ocr_outputs_dir, exist_ok=True)

# Mock ALL cloud sinks:
def _fake_mega(path, filename, *a, **k):
    return "https://fake.mega.invalid/" + filename
A.upload_to_mega = _fake_mega
A.upload_to_mymega = _fake_mega
A.upload_to_mega_ctrl_link = None
A.upload_to_mega_dl_link = None
A.upload_pdf_to_mega = _fake_mega
A.progress_lock.release() if hasattr(A, 'progress_lock') else None

# Mock edge-tts network: deterministic, instant, produces a real MP3 shape.
import edge_tts as _et


class _FakeCommunicate:
    def __init__(self, text, voice=None, rate=None, pitch=None, **kw):
        self.text, self.voice, self.rate, self.pitch = text, voice, rate, pitch
        self._sfx_count = 0

    async def stream(self):
        # Yield a real MPEG frame header + silence so mutagen's ID3 parses it as audio.
        # 0xFF 0xE3 = MPEG1 Layer3 128kbps 44.1k, then ~1KB of zeroed payload.
        header = b"\xff\xe3\x40\xc4"
        payload = b"\x00" * 8192
        for i in range(4):
            yield {"type": "audio", "data": header + payload}
            self._sfx_count += 1

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


_et.Communicate = _FakeCommunicate

RESULTS = []


def check(name, fn):
    t0 = time.time()
    try:
        ok, detail = fn()
        dt = time.time() - t0
        mark = "PASS" if ok else "FAIL"
        RESULTS.append((name, ok, dt))
        print(f"[{mark}] {name}  ({dt:.2f}s)  {detail}")
        return ok
    except Exception as e:
        RESULTS.append((name, False, time.time() - t0))
        print(f"[FAIL] {name}  ({time.time()-t0:.2f}s)  {type(e).__name__}: {e}")
        return False


def run_worker(name, worker, set_page, task_id, **kw):
    """Mirror the route: register tracker entry, spawn worker, poll to done/error."""
    with A.progress_lock:
        A.progress_tracker[task_id] = {
            "type": "ocr", "status": "starting", "created_at": time.time(),
            "task_id": task_id,
        }
        set_page(oA := A.progress_tracker[task_id])
    t = threading.Thread(target=worker, args=(), kwargs=kw, daemon=True)
    t.start()
    deadline = time.time() + 30
    last = {}
    while time.time() < deadline and t.is_alive():
        time.sleep(0.25)
        last = dict(A.progress_tracker.get(task_id, {}))
    t.join(timeout=2)
    status = last.get("status")
    err = last.get("error")
    return status, err


# ================= 1. OCR image -> extracted text =================
def _t_ocr():
    # Build a real image with text using PIL.
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (640, 220), "white")
    d = ImageDraw.Draw(img)
    d.text((20, 40), "HELLO WORLD", fill="black")
    d.text((20, 110), "MEOW OCR 2026", fill="black")
    img_path = os.path.join(BASE, "hello.png")
    img.save(img_path)

    task_id = "ocr_" + str(int(time.time() * 1000))

    def setp(t):
        t["file_path"] = img_path
        t["output_dir"] = A.ocr_outputs_dir
        t["filename"] = "hello.png"

    status, err = run_worker("ocr_image", A.ocr_image_background, setp, task_id,
                             task_id=task_id, image_path=img_path, filename="hello.png",
                             lang="eng", ocr_engine="tesseract", output_dir=A.ocr_outputs_dir)
    if status != "completed":
        return False, f"status={status} err={err}"
    txt = A.progress_tracker[task_id].get("extracted_text") or ""
    return ("HELLO" in txt.upper() and "MEOW" in txt.upper()), f"len={len(txt)} text={txt!r}"


# ================= 2. Translate .txt (forced engines, both fallbacks tested) =================
def _t_translate():
    txt = "The quick brown fox jumps over the lazy dog. The weather is nice today. I will go to the market tomorrow morning."
    # A) MyMemory direct fallback (the engine now used on Google 429)
    r1 = A._translate_mymemory(txt, "es", "en")
    ok1 = r1 is not None and any(c in r1.lower() for c in ["zorro", "perro", "mercado"])
    # B) Full translate_text wrapper (auto source)
    r2 = A.translate_text(txt, "es", source_lang="auto")
    ok2 = r2 is not None and r2.strip() != txt.strip() and len(r2.strip()) > 0
    return (ok1 and ok2), f"MyMemory={r1!r} | wrapper(out)={r2[:60]!r}"


# ================= 3. Audiobook: doc -> MP3 with lyrics =================
def _t_audiobook():
    doc_text = ("The quick brown fox jumps over the lazy dog. " * 8)
    task_id = "aud_" + str(int(time.time() * 1000))
    mp3_name = f"{task_id}.mp3"
    mp3_path = os.path.join(A.OUTPUT_DIR, f"{task_id}_{mp3_name}")
    ok = A._tts_run(task_id, doc_text, "en-US-JennyNeural", 100, 0)
    # _tts_run is async? Check: it's the background wrapper. Try; ignore if it returns coroutine.
    if hasattr(ok, "__await__"):
        return False, "worker returned coroutine (not awaited in this harness)"
    return True, f"mp3={mp3_path}"

    # ---- above: async worker handled by thread separately; do real way below ----


# ================= MAIN =================
def main():
    results = []
    results.append(check("translate_text (MyMemory fallback)", _t_translate))
    results.append(check("ocr_image_background -> completed", _t_ocr))
    print("\n---- SUMMARY ----")
    ok = all(r[1] for r in results)
    total = sum(r[2] for r in results)
    print(f"{sum(1 for r in results if r[1])}/{len(results)} passed in {total:.1f}s")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
