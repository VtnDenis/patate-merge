"""Génère les répliques des patates en voix neuronales (edge-tts).

Lit les répliques directement dans index.html (source unique) et écrit
audio/t{tier}_{i}.mp3 + audio/n_{key}.mp3.
"""
import asyncio, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

# ---- répliques : extraites de TIERS[i].lines ----
raw = re.findall(r"lines:\[(.*?)\],\s*col:", HTML, flags=re.S)
tiers = []
for chunk in raw:
    tiers.append(json.loads("[" + chunk + "]"))
assert len(tiers) == 14, f"14 paliers attendus, trouvé {len(tiers)}"

NARR = {
    "welcome": "Bienvenue dans Patate Merge.",
    "episode": "Nouvel épisode.",
    "overflow": "La patate a débordé.",
    "rare": "Oh, une patate rare !",
    "hop": "Hop.",
}

# ---- casting ----
VOICE = [
    ("fr-FR-HenriNeural",   "+2%"),    # 0 brute
    ("fr-FR-DeniseNeural",  "+4%"),    # 1 vapeur
    ("fr-FR-EloiseNeural",  "+10%"),   # 2 frite
    ("pt-PT-DuarteNeural",  "+2%"),    # 3 portugaise
    ("fr-FR-RemyMultilingualNeural", "+2%"),   # 4 bretonne
    ("fr-FR-HenriNeural",   "+6%"),    # 5 chef
    ("it-IT-DiegoNeural",   "+2%"),    # 6 italienne
    ("fr-FR-RemyMultilingualNeural", "+4%"),   # 7 cosmonaute
    ("fr-FR-VivienneMultilingualNeural", "+12%"),  # 8 influenceuse
    None, None, None, None, None,       # 9-13 : audio réel découpé dans le reel
]
NARR_VOICE = ("fr-FR-HenriNeural", "-12%")


async def synth(text, voice, rate, out: Path, sem: asyncio.Semaphore):
    import edge_tts
    async with sem:
        for attempt in range(3):
            try:
                comm = edge_tts.Communicate(text, voice, rate=rate)
                await comm.save(str(out))
                if out.exists() and out.stat().st_size > 1200:
                    return True
            except Exception as e:
                print("  retry", out.name, e)
                await asyncio.sleep(1.2 + attempt)
    print("  FAIL", out.name)
    return False


async def main():
    outdir = ROOT / "audio"
    outdir.mkdir(exist_ok=True)
    sem = asyncio.Semaphore(4)
    jobs = []
    for i, lines in enumerate(tiers):
        cast = VOICE[i]
        if cast is None:
            continue
        voice, rate = cast
        for k, text in enumerate(lines):
            jobs.append((text, voice, rate, outdir / f"t{i}_{k}.mp3"))
    for key, text in NARR.items():
        jobs.append((text, NARR_VOICE[0], NARR_VOICE[1], outdir / f"n_{key}.mp3"))

    print(f"{len(jobs)} répliques à générer…")
    results = await asyncio.gather(*(synth(t, v, r, o, sem) for t, v, r, o in jobs))
    ok = sum(results)
    total = sum(f.stat().st_size for f in outdir.glob("*.mp3"))
    print(f"{ok}/{len(jobs)} ok — {total/1024:.0f} Ko")
    if ok != len(jobs):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
