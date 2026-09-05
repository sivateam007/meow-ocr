"""One-time job: measure the average pitch of every built-in voice and save
voice_f0_profiles.json so /api/voice/analyze can match a user's sample to the
closest-sounding voice.

Usage:  python calibrate_voices.py [lang_codes...]
Run with no args to calibrate all voices (takes a few minutes).
Pass lang codes (tam en hin) to skip already-measured voices or do a subset.
"""
import asyncio
import json
import os
import sys
import tempfile
import time

import edge_tts

import app
import voice_analyzer as va

PROFILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_f0_profiles.json")


async def _synth(text, voice):
    c = edge_tts.Communicate(text, voice=voice, rate="+0%", pitch="+0Hz")
    buf = b""
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            buf += chunk["data"]
    return buf


def main():
    only = {x for x in sys.argv[1:] if x}
    profiles = {}
    if os.path.exists(PROFILES_PATH):
        try:
            profiles = json.load(open(PROFILES_PATH, encoding="utf-8"))
        except Exception:
            profiles = {}

    new_count = 0
    with tempfile.TemporaryDirectory() as tmp:
        for code, grp in app.TTS_VOICES.items():
            if only and code not in only:
                continue
            for voice, _, _ in grp:
                if voice in profiles:
                    continue
                loc = voice.split("-")[0].lower()
                sample = app.TTS_PREVIEW_SAMPLES.get(loc, app.TTS_PREVIEW_SAMPLES["en"])
                try:
                    mp3 = asyncio.run(_synth(sample, voice))
                    if not mp3:
                        raise RuntimeError("empty synth")
                    tmp_path = os.path.join(tmp, voice.replace("/", "_") + ".mp3")
                    with open(tmp_path, "wb") as f:
                        f.write(mp3)
                    pcm = va.decode_to_pcm(tmp_path)
                    res = va.analyze_pitch(pcm)
                    if res:
                        profiles[voice] = {"hz": res["median_hz"], "frames": res["frames"]}
                        new_count += 1
                        print(f"{code:7s} {voice:35s} -> {res['median_hz']} Hz  ({res['frames']} frames)", flush=True)
                    else:
                        print(f"{code:7s} {voice:35s} -> NO PITCH DETECTED", flush=True)
                    os.remove(tmp_path)
                except Exception as e:
                    print(f"{code:7s} {voice:35s} -> ERROR {str(e)[:100]}", flush=True)
                json.dump(profiles, open(PROFILES_PATH, "w", encoding="utf-8"), indent=1)
                time.sleep(0.4)

    print(f"\nDone. {new_count} new voices calibrated; total cached = {len(profiles)}")
    json.dump(profiles, open(PROFILES_PATH, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()