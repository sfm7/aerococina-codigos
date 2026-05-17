#!/usr/bin/env python3
"""
Generate all QR PNGs for Codigos de Contenedores aerococina.

USAGE:
    pip install qrcode[pil]
    python generate_qrs.py

The script reads the bodega HTML files, extracts every <div class="pc-code">CODE</div>,
and generates one PNG per code at qr_bodegas/{LETTER}/{CODE}.png

Re-run this script whenever:
- Plans change (mensual rotation)
- New containers are added
- Bodegas are added/removed

The codes embedded in the QR are the raw text (ej. "C1EX") — what MOST/Vector receive
when the operator scans the QR.
"""
import re
import qrcode
from pathlib import Path

# Adjust this to point to your folder containing the bodega HTMLs
HTML_DIR = Path(".")  # current folder

# Output base — relative to where you run the script
OUT_BASE = Path("./qr_bodegas")

BODEGAS = {
    "X": "Codigos_Containers_X_Mexico_City.html",
    "N": "Codigos_Containers_N_AIFA.html",
    "C": "Codigos_Containers_C_Cancún.html",
    "G": "Codigos_Containers_G_Guadalajara.html",
    "Y": "Codigos_Containers_Y_Mérida.html",
    "M": "Codigos_Containers_M_Monterrey.html",
    "T": "Codigos_Containers_T_Tijuana.html",
    "L": "Codigos_Containers_L_Toluca.html",
}

# QR style — aerococina branding
QR_FILL_COLOR = "#1B2A4E"   # aero-navy
QR_BACK_COLOR = "white"
QR_BOX_SIZE = 10
QR_BORDER = 2
QR_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_M  # 15% recovery

total = 0
for letter, filename in BODEGAS.items():
    src = HTML_DIR / filename
    if not src.exists():
        print(f"⚠️  Skipping {letter}: {src} not found")
        continue

    html = src.read_text(encoding="utf-8")
    codes = sorted(set(re.findall(r'<div class="pc-code">([^<]+)</div>', html)))

    out_dir = OUT_BASE / letter
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Bodega {letter}: {len(codes)} codes → {out_dir}")

    for code in codes:
        qr = qrcode.QRCode(
            version=None,
            error_correction=QR_ERROR_CORRECTION,
            box_size=QR_BOX_SIZE,
            border=QR_BORDER,
        )
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image(fill_color=QR_FILL_COLOR, back_color=QR_BACK_COLOR)
        img.save(out_dir / f"{code}.png", "PNG", optimize=True)
        total += 1

print(f"\n✅ Done. Generated {total} QR PNGs in {OUT_BASE.resolve()}")
