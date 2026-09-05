"""Voice analysis helpers for the "My Voice" feature (pitch/speed matching).

Pure numpy + ffmpeg — no heavy audio deps. Used by app.py endpoints and by
the one-time calibrate_voices.py job that measures each built-in voice's
average fundamental frequency.
"""
import shutil
import subprocess

import numpy as np

SAMPLE_RATE = 16000
MIN_HZ = 60
MAX_HZ = 400


def find_ffmpeg():
    return shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")


def decode_to_pcm(audio_path, sr=SAMPLE_RATE):
    """Decode any audio file to mono float32 PCM at ``sr`` via ffmpeg."""
    ff = find_ffmpeg()
    if not ff:
        raise RuntimeError("ffmpeg not found on this server")
    cmd = [ff, "-v", "error", "-i", audio_path, "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0 or not proc.stdout:
        err = (proc.stderr or b"").decode("utf-8", "replace")[:300]
        raise ValueError(err or "Could not decode audio")
    arr = np.frombuffer(proc.stdout, dtype=np.int16).astype(np.float32) / 32768.0
    if arr.size < sr:
        raise ValueError("Audio is too short (need at least 1 second)")
    return arr


def _frame_f0(frame, sr=SAMPLE_RATE, min_hz=MIN_HZ, max_hz=MAX_HZ):
    """Fundamental frequency of one frame via normalized autocorrelation (ACF).
    Returns 0.0 when the frame is unvoiced/ambiguous."""
    frame = frame - frame.mean()
    n = len(frame)
    min_lag = int(sr / max_hz)
    max_lag = int(sr / min_hz)
    if min_lag < 1 or max_lag >= n:
        return 0.0
    energy = float(np.dot(frame, frame))
    if energy <= 1e-7:
        return 0.0
    ac = np.correlate(frame, frame, "full")[n - 1: n + max_lag]
    rn = ac / energy
    cand = rn[min_lag: max_lag + 1]
    idx = int(np.argmax(cand))
    if cand[idx] < 0.4:
        return 0.0
    return sr / float(min_lag + idx)


def analyze_pitch(pcm, sr=SAMPLE_RATE):
    """Median/mean/min/max fundamental frequency over voiced frames.
    Returns None when no clear voice is found."""
    frame_len = int(0.04 * sr)
    hop = int(0.02 * sr)
    n = len(pcm)
    if n < frame_len:
        return None
    rms_global = float(np.sqrt(np.mean(pcm ** 2)))
    thresh = max(0.008, rms_global * 0.5)
    f0s = []
    for start in range(0, n - frame_len + 1, hop):
        frame = pcm[start: start + frame_len]
        rms = float(np.sqrt(np.mean(frame ** 2)))
        if rms < thresh:
            continue
        f0 = _frame_f0(frame, sr)
        if f0:
            f0s.append(f0)
    if len(f0s) < 10:
        return None
    arr = np.asarray(f0s)
    return {
        "median_hz": round(float(np.median(arr)), 1),
        "mean_hz": round(float(np.mean(arr)), 1),
        "min_hz": round(float(np.min(arr)), 1),
        "max_hz": round(float(np.max(arr)), 1),
        "frames": int(len(arr)),
    }


def estimate_wpm(pcm, sr=SAMPLE_RATE):
    """Rough speaking rate in words-per-minute from syllable-nucleus peaks."""
    n = len(pcm)
    if n < sr:
        return None
    frame_len = int(0.03 * sr)
    hop = int(0.01 * sr)
    energies = []
    for start in range(0, n - frame_len + 1, hop):
        frame = pcm[start: start + frame_len]
        energies.append(float(np.sqrt(np.mean(frame ** 2))))
    e = np.asarray(energies)
    if e.size < 5:
        return None
    e = np.convolve(e, np.ones(3) / 3, mode="same")
    min_dist = max(1, int(0.12 / 0.01))
    thr = max(float(np.percentile(e, 40)), float(np.mean(e)) * 0.6)
    peaks = 0
    i = 0
    while i < e.size:
        if e[i] > thr:
            win_start = max(0, i - min_dist // 2)
            win_end = min(e.size, i + min_dist // 2 + 1)
            if e[i] >= float(np.max(e[win_start: win_end])):
                peaks += 1
                i += min_dist
            else:
                i += 1
        else:
            i += 1
    dur = (e.size - 1) * 0.01
    if dur <= 0 or peaks <= 0:
        return None
    wpm = int(round((peaks / dur) * 60.0 / 1.7))
    return max(40, min(300, wpm))


def gender_from_hz(hz):
    """Coarse gender estimate from median voice frequency."""
    return "female" if hz >= 160 else "male"


def suggest_voice(median_hz, gender, lang, profiles, lang_gender_voices):
    """Pick the built-in voice (in ``lang`` + ``gender``) whose measured pitch
    is closest to the user's. Returns a dict or None. Clamps pitch to +/-50Hz."""
    cands = (lang_gender_voices.get(lang) or {}).get(gender, [])
    if not cands:
        return None
    scored = []
    for v in cands:
        prof = profiles.get(v) or {}
        hz = prof.get("hz")
        if hz:
            scored.append((abs(median_hz - hz), v, hz))
    if not scored:
        return None
    scored.sort(key=lambda x: x[0])
    diff, voice, voice_hz = scored[0]
    pitch = int(round(median_hz - voice_hz))
    pitch = max(-50, min(50, pitch))
    return {
        "voice": voice,
        "pitch": pitch,
        "voice_hz": round(voice_hz, 1),
        "match_diff": round(diff, 1),
    }


def suggest_rate(wpm):
    if not wpm:
        return 100
    rate = int(round(wpm / 150.0 * 100))
    return max(50, min(200, rate))