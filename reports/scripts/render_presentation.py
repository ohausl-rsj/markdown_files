#!/usr/bin/env python3
"""Vyrenderuje .pptx do PNG (přes PDF) pro vizuální kontrolu.

macOS: export do PDF přes Microsoft PowerPoint (AppleScript),
jinak přes LibreOffice (soffice), pokud je k dispozici.
PDF → PNG pomocí PyMuPDF (pip install pymupdf).

Použití: python3 render_presentation.py <soubor.pptx> [výstupní_složka]
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf


def to_pdf(pptx: Path, pdf: Path) -> None:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf.parent), str(pptx)],
                       check=True)
        (pdf.parent / (pptx.stem + ".pdf")).rename(pdf)
        return
    # PowerPoint je sandboxovaný: soubor zkopírujeme do jeho kontejneru, otevřeme přes
    # Launch Services (AppleScript „open“ končí chybou -9074) a uložíme jako PDF.
    box = Path.home() / "Library/Containers/com.microsoft.Powerpoint/Data/Documents"
    src, tmp = box / ("_render_" + pptx.name), box / ("_render_" + pdf.name)
    shutil.copy(pptx, src)
    tmp.unlink(missing_ok=True)
    subprocess.run(["open", "-g", "-a", "Microsoft PowerPoint", str(src)], check=True)
    script = f'''
    tell application "Microsoft PowerPoint"
        repeat 60 times
            try
                if (name of active presentation) is "{src.name}" then exit repeat
            end try
            delay 0.5
        end repeat
        set p to active presentation
        save p in ((POSIX file "{tmp}") as string) as save as PDF
        close p saving no
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)
    shutil.move(str(tmp), pdf)
    src.unlink(missing_ok=True)


def main():
    pptx = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else pptx.parent / (pptx.stem + "_png")
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / (pptx.stem + ".pdf")
    to_pdf(pptx, pdf)
    doc = pymupdf.open(pdf)
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=110).save(out / f"slide_{i:02d}.png")
    print(f"{len(doc)} slidů → {out}")


if __name__ == "__main__":
    main()
