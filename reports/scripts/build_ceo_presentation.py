#!/usr/bin/env python3
"""Generuje prezentaci „IT, Data & AI Automation“ pro CEO.

Zdroj obsahu: reports/q3_report_ideas.md
Zadání:       reports/zadani_prezentace_CEO.md
Výstup:       reports/output/CEO_reporting_IT_Data_AI.pptx

Požadavky: pip install python-pptx pillow
Spuštění:  python3 reports/scripts/build_ceo_presentation.py

Skript na konci provede i orientační kontrolu přetékání textu (měří text
fontem Aptos, pokud je k dispozici) a vypíše varování.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "CEO_reporting_IT_Data_AI.pptx"

# ---------------------------------------------------------------- barvy
NAVY = "14213D"
NAVY2 = "23365F"
INK = "1E2533"
GREY_D = "4A5568"
GREY = "8A94A6"
GREY_L = "D9DEE6"
GREY_BG = "F3F5F8"
WHITE = "FFFFFF"
ACCENT = "E3A008"      # jediná akcentní barva (zvýraznění, rizika, RSJ Custody)
ACCENT_BG = "FDF4DC"
RED = "C53030"         # jen pro překročení budgetu (čerpání nad 100 %)

AREA = {               # barvy oblastí projektů – konzistentní na všech slidech
    "Core IT": "2B6CB0",
    "AI automatizace": "7B4FB8",
    "Development": "1F9E89",
    "Reporting": "B04A6F",
}

FONT = "Aptos"
FOOTER = "RSJ Investments · IT, Data & AI Automation"

SLIDE_W, SLIDE_H = 13.333, 7.5
LM = 0.6                      # levý okraj
CW = SLIDE_W - 2 * LM         # šířka obsahu

_text_registry: list[dict] = []   # pro kontrolu přetékání
_current_slide_no = 0


def rgb(h: str) -> RGBColor:
    return RGBColor.from_string(h)


# ---------------------------------------------------------------- helpery
def shape(slide, kind, x, y, w, h, fill=None, line=None, radius=None, line_w=0.75):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(line_w)
    else:
        s.line.fill.background()
    if radius is not None and len(s.adjustments) > 0:
        s.adjustments[0] = radius
    s.text_frame.text = ""
    return s


def rect(slide, x, y, w, h, fill=None, line=None, **kw):
    return shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill, line, **kw)


def rrect(slide, x, y, w, h, fill=None, line=None, radius=0.08, **kw):
    return shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, line, radius=radius, **kw)


def _set_bullet(p, indent_in=0.18):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(int(Inches(indent_in))))
    pPr.set("indent", str(-int(Inches(indent_in))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buFont = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"})
    buChar = pPr.makeelement(qn("a:buChar"), {"char": "•"})
    pPr.append(buFont)
    pPr.append(buChar)


def fill_text(target, paras, size=14, color=INK, bold=False, align="l", anchor="t",
              margin=(0.08, 0.05, 0.08, 0.05), spacing=1.0, box=None):
    """paras: str | list[str | dict]. dict: text|runs, size, bold, color, bullet, space_before, align."""
    tf = target.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    ml, mt, mr, mb = margin
    tf.margin_left, tf.margin_top = Inches(ml), Inches(mt)
    tf.margin_right, tf.margin_bottom = Inches(mr), Inches(mb)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = paras.split("\n")
    measured = []
    for i, para in enumerate(paras):
        if isinstance(para, str):
            para = {"text": para}
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        a = para.get("align", align)
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[a]
        p.line_spacing = spacing
        if para.get("space_before"):
            p.space_before = Pt(para["space_before"])
        if para.get("bullet"):
            _set_bullet(p)
        runs = para.get("runs") or [(para.get("text", ""), {})]
        psize = para.get("size", size)
        for txt, ro in runs:
            r = p.add_run()
            r.text = txt
            f = r.font
            f.name = FONT
            f.size = Pt(ro.get("size", psize))
            f.bold = ro.get("bold", para.get("bold", bold))
            f.italic = ro.get("italic", False)
            f.color.rgb = rgb(ro.get("color", para.get("color", color)))
        measured.append({
            "runs": [(t, ro.get("size", psize), ro.get("bold", para.get("bold", bold))) for t, ro in runs],
            "space_before": para.get("space_before", 0),
            "bullet": bool(para.get("bullet")),
        })
    if box:
        x, y, w, h = box
        _text_registry.append({
            "slide": _current_slide_no, "w": w - ml - mr, "h": h - mt - mb,
            "paras": measured, "spacing": spacing,
            "preview": "".join(t for t, *_ in measured[0]["runs"])[:50] if measured else "",
        })
    return target


def text(slide, x, y, w, h, paras, **kw):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    return fill_text(tb, paras, box=(x, y, w, h), **kw)


def label(shp, x, y, w, h, paras, **kw):
    """Text uvnitř tvaru (rozměry kvůli kontrole přetékání)."""
    return fill_text(shp, paras, box=(x, y, w, h), **kw)


def pill(slide, x, y, w, h, txt, fill, color=WHITE, size=10, bold=True):
    s = rrect(slide, x, y, w, h, fill=fill, radius=0.5)
    label(s, x, y, w, h, txt, size=size, color=color, bold=bold, align="c", anchor="m",
          margin=(0.04, 0.0, 0.04, 0.0))
    return s


def custody_tag(slide, x, y, w=1.0, h=0.24, size=8.5):
    return pill(slide, x, y, w, h, "RSJ Custody", ACCENT, color=NAVY, size=size)


def icon(slide, kind, x, y, d=0.62, bg=NAVY2, fg=WHITE):
    rect_ = shape(slide, MSO_SHAPE.OVAL, x, y, d, d, fill=bg)
    pad = d * 0.24
    shape(slide, kind, x + pad, y + pad, d - 2 * pad, d - 2 * pad, fill=fg)
    return rect_


def arrow_right(slide, x, y, w=0.35, h=0.3, fill=GREY):
    return shape(slide, MSO_SHAPE.RIGHT_ARROW, x, y, w, h, fill=fill)


def arrow_down(slide, x, y, w=0.3, h=0.3, fill=GREY):
    return shape(slide, MSO_SHAPE.DOWN_ARROW, x, y, w, h, fill=fill)


def new_slide(prs, title, notes, number=True):
    global _current_slide_no
    _current_slide_no += 1
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = rgb(WHITE)
    if title:
        rect(s, LM, 0.38, 0.55, 0.06, fill=ACCENT)
        text(s, LM - 0.08, 0.5, CW + 0.16, 0.85, title, size=26, bold=True, color=NAVY,
             anchor="t", margin=(0.08, 0.02, 0.08, 0.02))
    if number:
        rect(s, LM, 6.98, CW, 0.012, fill=GREY_L)
        text(s, LM - 0.08, 7.03, 8, 0.3, FOOTER, size=10, color=GREY, margin=(0.08, 0, 0.08, 0))
        text(s, SLIDE_W - LM - 1.0 + 0.08, 7.03, 1.0, 0.3, str(_current_slide_no), size=10,
             color=GREY, align="r", margin=(0.08, 0, 0.08, 0))
    s.notes_slide.notes_text_frame.text = notes
    return s


def phase_pill(slide, x, y, phase, w=None, fill=NAVY2, size=10):
    w = w or max(0.9, 0.11 * len(phase) + 0.35)
    return pill(slide, x, y, w, 0.28, phase, fill, size=size)


def card(slide, x, y, w, h, area_color, top_bar=0.08, fill=GREY_BG):
    rrect(slide, x, y, w, h, fill=fill, radius=0.04)
    rect(slide, x, y, w, top_bar, fill=area_color)


# ---------------------------------------------------------------- slidy
def s01_title(prs):
    s = new_slide(prs, None, (
        "Dobrý den, rád bych vám představil, kde dnes IT útvar stojí, jak pokračují naše projekty a kam "
        "chceme směřovat. Prezentace je informativní, nic nepředkládám ke schválení. Projdeme stav týmu, "
        "prostředí a bezpečnosti, přehled projektů po oblastech, spolupráci s RSJ Custody, budget a výhled. "
        "Celou prezentací se táhnou tři sdělení: stabilizace týmu, ladění stávajících systémů a AI jako hlavní směr."
    ), number=False)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = rgb(NAVY)
    rect(s, 0, 0, 0.28, SLIDE_H, fill=ACCENT)
    rect(s, 1.1, 2.35, 0.9, 0.08, fill=ACCENT)
    text(s, 1.02, 2.6, 10.5, 1.2, "IT, Data & AI Automation", size=54, bold=True, color=WHITE)
    text(s, 1.02, 3.75, 10.5, 0.7, "Stav útvaru, projektů a výhled", size=26, color="C9D3E6")
    text(s, 1.02, 5.6, 10.5, 0.5, "Ondřej Hausl, vedoucí IT útvaru · listopad 2026", size=16, color=WHITE)
    text(s, 1.02, 6.05, 10.5, 0.4, "RSJ Investments", size=13, color="9AA8C2")


def s02_summary(prs):
    s = new_slide(prs, "IT je stabilizované, ladí stávající systémy a AI je hlavní směr", (
        "Shrnu to do čtyř vět. Po obtížném startu, kdy hned po mém nástupu odešli dva ze tří techniků, je tým "
        "doplněný a pracuje řízeně. V souladu s vaším požadavkem se soustředíme na ladění a plné využití systémů, "
        "které už máme, nové projekty otevíráme jen tam, kde stávající řešení nevyhovuje. Hlavním směrem je AI, "
        "kterou zavádíme řízeně a stavíme pro ni datový základ a cloudové prostředí. "
        "V přehledu máme 19 projektů, z toho 4 v provozu, 3 v oblasti AI a 6 realizujeme společně s IS útvarem RSJ Custody."
    ))
    msgs = [
        ("Stabilizace", "Po odchodu 2 ze 3 techniků je tým rychle doplněný a pracuje řízeně."),
        ("Tuning", "Ladíme a naplno využíváme stávající systémy, nové projekty jen tam, kde nestačí."),
        ("AI", "AI zavádíme řízeně a stavíme pro ni kvalitní data a moderní cloudové prostředí."),
        ("Spolupráce", "Klíčové projekty skupiny posouváme společně s IS útvarem RSJ Custody."),
    ]
    y = 1.6
    for i, (k, m) in enumerate(msgs):
        rrect(s, LM, y, 7.3, 1.1, fill=GREY_BG, radius=0.06)
        pill(s, LM + 0.2, y + 0.32, 0.46, 0.46, str(i + 1), NAVY, size=14)
        text(s, LM + 0.85, y + 0.12, 6.3, 0.86, [
            {"text": k, "size": 12, "bold": True, "color": ACCENT if i == 3 else NAVY2},
            {"text": m, "size": 15, "color": INK},
        ], anchor="m")
        y += 1.25
    kpis = [("19", "projektů v přehledu", NAVY), ("4", "projekty v provozu", NAVY),
            ("3", "AI projekty", AREA["AI automatizace"]), ("6", "projektů s RSJ Custody", ACCENT)]
    x0, y0, kw, kh = 8.3, 1.6, 2.1, 2.35
    for i, (n, t, c) in enumerate(kpis):
        x = x0 + (i % 2) * (kw + 0.23)
        yy = y0 + (i // 2) * (kh + 0.2)
        rrect(s, x, yy, kw, kh, fill=WHITE, line=GREY_L, radius=0.06)
        rect(s, x + 0.25, yy + 0.3, 0.45, 0.06, fill=c)
        text(s, x + 0.15, yy + 0.45, kw - 0.3, 1.1, n, size=60, bold=True, color=c if c != ACCENT else NAVY)
        text(s, x + 0.15, yy + 1.55, kw - 0.3, 0.65, t, size=14, color=GREY_D)


def s03_start(prs):
    s = new_slide(prs, "Po obtížném startu je tým doplněný a plní požadavek na tuning", (
        "Hlavním požadavkem na začátku roku byl tuning stávající infrastruktury a aplikací, tedy nevymýšlet nové "
        "projekty, ale vyladit to, co už máme. Nastoupil jsem 1. 9. 2025 a krátce poté odešli dva ze tří techniků, "
        "oba zkušení. Zůstal L1 technik Jan Kridlo. Tým jsem rychle doplnil: 1. 1. 2026 nastoupil Jiří Severa "
        "a 2. 2. 2026 Frederik Urban. Část práce mi předal bývalý kontraktor, který dál působí jako externí "
        "projektový manažer. Od srpna 2026 spolupracujeme s externím konzultantem Jakubem Filipem na AI automatizacích."
    ))
    # levá karta – požadavek CEO
    rrect(s, LM, 1.6, 4.6, 5.0, fill=NAVY, radius=0.04)
    text(s, LM + 0.35, 1.9, 3.9, 0.4, "POŽADAVEK CEO", size=12, bold=True, color=ACCENT)
    text(s, LM + 0.35, 2.4, 3.9, 2.4,
         "„Není třeba vymýšlet nové projekty, ale spíše vyladit to, co už máme.“",
         size=22, bold=True, color=WHITE, spacing=1.05)
    text(s, LM + 0.35, 5.0, 3.9, 1.3, [
        "Tuning aktuální infrastruktury a aplikací je rámcem pro všechny projekty IT útvaru.",
    ], size=13, color="C9D3E6")
    # pravá časová osa
    events = [
        ("1. 9. 2025", "Nástup vedoucího IT útvaru", False),
        ("ihned poté", "Odchod 2 ze 3 techniků, zůstává L1 technik", True),
        ("1. 1. 2026", "Nástup IT administrátora Jiřího Severy", False),
        ("2. 2. 2026", "Nástup IT administrátora Frederika Urbana", False),
        ("8/2026", "Start spolupráce s externím konzultantem pro AI", False),
        ("10/2026", "Frederik Urban plně na vývoj AI automatizací", False),
        ("31. 12. 2026", "Končí jeden IT administrátor", False),
    ]
    x0 = 5.75
    text(s, x0, 1.55, 6.9, 0.4, "Vývoj týmu", size=14, bold=True, color=NAVY2)
    rect(s, x0 + 1.55, 2.12, 0.03, 4.25, fill=GREY_L)
    y = 2.05
    for d, t, hl in events:
        dot = ACCENT if hl else NAVY2
        shape(s, MSO_SHAPE.OVAL, x0 + 1.46, y + 0.13, 0.21, 0.21, fill=dot)
        text(s, x0, y, 1.38, 0.48, d, size=13, bold=True, color=NAVY, align="r", anchor="m")
        text(s, x0 + 1.85, y, 5.0, 0.48, t, size=14, color=INK, anchor="m", bold=hl)
        y += 0.64


def s04_env(prs):
    s = new_slide(prs, "Prostředí stojí na cloudu, bezpečnost má nástroje, ale ne vlastníka", (
        "Skupina razí filozofii cloud first. Lokálně v pražské kanceláři máme jen síť, tedy firewall, switche, "
        "přístupové body, kamery a senzory. V Azure provozujeme 14 virtuálních serverů a PaaS služby jako App Service, "
        "Azure SQL a Blob storage. V M365 využíváme téměř celé portfolio včetně Intune, Defenderu a Copilota, "
        "licence E5 a u části uživatelů E7. Na serverech v Azure stále běží Active Directory, které potřebuje "
        "současný DMS; cílem je AD zrušit a provozovat jen Entra ID. Bezpečnost řídíme modelem tří linií obrany, "
        "IT jako první linie dodává data a druhá linie je nezávisle hodnotí; samostatná security pozice dnes neexistuje."
    ))
    # vrstvy
    text(s, LM, 1.5, 6.0, 0.4, "Vrstvy prostředí", size=14, bold=True, color=NAVY2)
    layers = [
        ("SaaS", "Microsoft 365: Exchange, SharePoint Online, Intune, Defender, Copilot, Entra ID", NAVY),
        ("PaaS", "Azure App Service, Azure SQL, Blob storage, síť – nové aplikace", NAVY2),
        ("IaaS", "Virtuální servery v Azure, mj. AD pro současný DMS, které zrušíme", "51658C"),
        ("On-premise", "Jen síť v kanceláři Praha", "8A97B3"),
    ]
    y = 1.98
    for name, desc, c in layers:
        rrect(s, LM, y, 1.45, 0.78, fill=c, radius=0.1)
        label(s.shapes[-1], LM, y, 1.45, 0.78, name, size=14, bold=True, color=WHITE, align="c", anchor="m")
        rrect(s, LM + 1.55, y, 4.55, 0.78, fill=GREY_BG, radius=0.1)
        text(s, LM + 1.65, y, 4.4, 0.78, desc, size=12.5, color=INK, anchor="m")
        y += 0.9
    # šipka cloud first
    shape(s, MSO_SHAPE.UP_ARROW, LM + 6.25, 2.0, 0.42, 3.5, fill=ACCENT)
    tb = text(s, LM + 6.46 - 1.25, 3.55, 2.5, 0.4, "cloud first", size=13, bold=True, color=NAVY, align="c",
              anchor="m")
    tb.rotation = -90
    text(s, LM, 5.75, 6.7, 0.8, [{"runs": [
        ("12 klíčových aplikací ", {"bold": True, "color": NAVY}),
        ("provozujeme sami nebo s RSJ Custody – přehled v příloze.", {}),
    ]}], size=13, color=INK)

    # bezpečnost
    xr = 7.75
    text(s, xr, 1.5, 4.98, 0.4, "Bezpečnost", size=14, bold=True, color=NAVY2)
    for i, t in enumerate(["Defender XDR", "MS Sentinel (SIEM)"]):
        pill(s, xr + i * 2.55, 1.98, 2.43, 0.42, t, AREA["Core IT"], size=12)
    lines_ = [
        ("1. linie", "IT útvar – výkon, data pro DORA", NAVY2),
        ("2. linie", "IKT risk a Compliance – nezávislý dohled", "51658C"),
        ("3. linie", "Interní audit – nezávislé ověření", "8A97B3"),
    ]
    y = 2.6
    for i, (n, d, c) in enumerate(lines_):
        rrect(s, xr, y, 1.15, 0.62, fill=c, radius=0.1)
        label(s.shapes[-1], xr, y, 1.15, 0.62, n, size=12.5, bold=True, color=WHITE, align="c", anchor="m")
        rrect(s, xr + 1.25, y, 3.73, 0.62, fill=GREY_BG, radius=0.1)
        text(s, xr + 1.35, y, 3.6, 0.62, d, size=12, color=INK, anchor="m")
        y += 0.72
    rrect(s, xr, 4.85, 4.98, 1.15, fill=ACCENT_BG, line=ACCENT, radius=0.06)
    rect(s, xr, 4.85, 0.09, 1.15, fill=ACCENT)
    text(s, xr + 0.25, 4.9, 4.6, 1.05, [
        {"text": "Riziko: security nemá vlastníka", "bold": True, "color": NAVY, "size": 14},
        {"text": "Samostatná security pozice neexistuje. Agendu sdílejí administrátoři, dohled supluje vedoucí IT.",
         "size": 12.5, "space_before": 4},
    ], color=INK)


def s05_team(prs):
    s = new_slide(prs, "Tým je doplněný, rizikem jsou oblasti závislé na jednotlivcích", (
        "Interní tým tvoří čtyři lidé v Core IT a AI automatizaci a reporting, který jsem po dohodě s CFO "
        "Markem Capákem organizačně převzal pod IT, zatím ne formálně. Jiří Severa k 31. 12. 2026 končí. "
        "Dušan Marko je formálně zaměstnancem RSJ Custody a je plně alokován pro RSJ Investments, odpovídá za vývoj MDM, "
        "Cashflow a DWH. Orbit nám dodává licence, spravuje Azure subscription a pomáhá s konzultacemi a kapacitou, "
        "Jakub Filip s námi od srpna 2026 vyvíjí AI automatizace. Hlavním rizikem je, že security nemá vlastníka "
        "a některé oblasti drží jediný člověk, například síť a infrastrukturu nebo přípravu dat v DWH."
    ))
    # vedoucí
    cx = LM + 1.5 * 2.7 + 0.15
    rrect(s, cx - 1.6, 1.5, 3.2, 0.72, fill=NAVY, radius=0.1)
    label(s.shapes[-1], cx - 1.6, 1.5, 3.2, 0.72, [
        {"text": "Ondřej Hausl", "bold": True, "size": 14},
        {"text": "vedoucí IT útvaru · governance, projekty", "size": 10.5, "color": "C9D3E6"},
    ], color=WHITE, align="c", anchor="m")
    rect(s, cx - 0.01, 2.22, 0.02, 0.25, fill=GREY)
    rect(s, LM + 1.35, 2.46, 5.7, 0.02, fill=GREY)
    cols = [
        ("Core IT", AREA["Core IT"], [
            ("Jan Kridlo", "IT administrátor · L1 podpora, DMS, Projects, Invoices, MDM"),
            ("Jiří Severa", "IT administrátor · cloud, identita, endpoint · do 31. 12. 2026"),
        ]),
        ("AI automatizace", AREA["AI automatizace"], [
            ("Frederik Urban", "vývoj AI automatizací (od 10/2026), síť a infrastruktura"),
        ]),
        ("Data & reporting", AREA["Reporting"], [
            ("Marina Bartošová", "reportingový specialista · reporty pro RSJ Investments a RSJ Services"),
        ]),
    ]
    cw, gap = 2.7, 0.15
    for i, (name, c, people) in enumerate(cols):
        x = LM + i * (cw + gap)
        rect(s, x + cw / 2 - 0.01, 2.47, 0.02, 0.2, fill=GREY)
        rrect(s, x, 2.67, cw, 0.45, fill=c, radius=0.15)
        label(s.shapes[-1], x, 2.67, cw, 0.45, name, size=13, bold=True, color=WHITE, align="c", anchor="m")
        y = 3.22
        for n, r in people:
            rrect(s, x, y, cw, 1.12, fill=GREY_BG, radius=0.06)
            text(s, x + 0.1, y + 0.05, cw - 0.2, 1.02, [
                {"text": n, "bold": True, "size": 13, "color": NAVY},
                {"text": r, "size": 11, "color": GREY_D},
            ], anchor="m")
            y += 1.2
    # externí partneři
    xe = LM + 3 * (cw + gap) + 0.2
    we = SLIDE_W - LM - xe
    rrect(s, xe, 1.5, we, 4.05, fill=WHITE, line=GREY_L, radius=0.04)
    text(s, xe + 0.15, 1.58, we - 0.3, 0.4, "Externí partneři", size=13, bold=True, color=NAVY2)
    ext = [
        ("Dušan Marko", "RSJ Custody, plně pro RSJ Investments · MDM, Cashflow, DWH", True),
        ("IS útvar RSJ Custody", "Tomáš Málek · vývoj aplikací (BOSS, Založení fondu)", True),
        ("Orbit s. r. o.", "licence, Azure, konzultace a kapacita", False),
        ("Jakub Filip", "externí konzultant pro AI automatizace", False),
    ]
    y = 2.03
    for n, r, cust in ext:
        text(s, xe + 0.15, y, we - 0.3, 0.85, [
            {"text": n, "bold": True, "size": 12.5, "color": NAVY},
            {"text": r, "size": 10.5, "color": GREY_D},
        ])
        if cust:
            custody_tag(s, xe + we - 1.12, y + 0.05, w=0.98, h=0.22, size=8)
        y += 0.86
    # riziko
    rrect(s, LM, 5.82, CW, 0.92, fill=ACCENT_BG, line=ACCENT, radius=0.08)
    rect(s, LM, 5.82, 0.09, 0.92, fill=ACCENT)
    text(s, LM + 0.3, 5.86, CW - 0.5, 0.84, [{"runs": [
        ("Hlavní riziko: ", {"bold": True, "color": NAVY}),
        ("security nemá vlastníka a některé oblasti stojí na jednom člověku "
         "(síť a infrastruktura, L1 podpora, příprava dat v DWH).", {}),
    ]}], size=14, color=INK, anchor="m")


PROJECTS = [  # (název, oblast, fáze, custody) – dle tabulky Přehled projektů
    ("MS Sentinel", "Core IT", "Dokončení", False),
    ("Propojení HR modulu BOSS s AD", "Core IT", "Provoz", True),
    ("IT service management v Alvao", "Core IT", "Provoz", False),
    ("RBAC", "Core IT", "Realizace", False),
    ("SharePoint governance", "Core IT", "Realizace", False),
    ("AI reporting pro PE/VC tým", "AI automatizace", "Pilot", False),
    ("AI posouzení LPA", "AI automatizace", "PoC", False),
    ("AI vytěžování faktur", "AI automatizace", "Analýza", False),
    ("MDM", "Development", "Provoz", True),
    ("Založení fondu", "Development", "Pilot", True),
    ("DMS", "Development", "Dokončení", False),
    ("BOSS HR", "Development", "Provoz", True),
    ("Auditní workflow", "Development", "Realizace", True),
    ("Nový BOSS", "Development", "Realizace", True),
    ("Projects", "Development", "Analýza", False),
    ("Invoices", "Development", "Nápad", False),
    ("Řízení úkolů a projektů", "Development", "Analýza", False),
    ("Migrace DWH do Fabricu", "Reporting", "Analýza", False),
    ("Databáze KPI", "Reporting", "Analýza", False),
]
PHASES = ["Nápad", "Analýza", "PoC", "Realizace", "Pilot", "Dokončení", "Provoz"]


def legend(s, x, y, areas=("Core IT", "AI automatizace", "Development", "Reporting"), custody=True):
    for a in areas:
        rrect(s, x, y + 0.05, 0.22, 0.22, fill=AREA[a], radius=0.2)
        w = 0.085 * len(a) + 0.15
        text(s, x + 0.27, y, w, 0.32, a, size=11, color=GREY_D, anchor="m", margin=(0.02, 0, 0.02, 0))
        x += 0.27 + w + 0.2
    if custody:
        custody_tag(s, x, y + 0.04, w=1.0, h=0.24)
        text(s, x + 1.05, y, 2.3, 0.32, "společně s RSJ Custody", size=11, color=GREY_D, anchor="m",
             margin=(0.02, 0, 0.02, 0))


def s06_overview(prs):
    s = new_slide(prs, "19 projektů v pohybu: 4 v provozu, 6 společně s RSJ Custody", (
        "Tohle je mapa všech projektů podle fáze, od nápadu po provoz, barevně podle oblasti. V provozu jsou propojení "
        "HR modulu BOSS s AD, IT service management v Alvao, MDM a HR modul BOSS; MDM i BOSS HR dál rozvíjíme. Ve fázi "
        "dokončení jsou MS Sentinel s plánem na 11/2026 a nový DMS. V realizaci jsou vedle RBAC a SharePoint governance "
        "také auditní workflow a nový BOSS s RSJ Custody. Nejvíc projektů je v analýze, mimo jiné řízení úkolů "
        "a projektů, migrace DWH do Fabricu a databáze KPI. Tři AI projekty jsou v různých fázích od analýzy po pilot, "
        "což odpovídá řízenému zavádění. Šest projektů, označených štítkem, realizujeme společně s RSJ Custody."
    ))
    n = len(PHASES)
    gap = 0.07
    cw = (CW - gap * (n - 1)) / n
    top = 1.55
    for i, ph in enumerate(PHASES):
        x = LM + i * (cw + gap)
        kind = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        sh = shape(s, kind, x, top, cw + (0.12 if i < n - 1 else 0), 0.55,
                   fill=NAVY if ph != "Provoz" else NAVY2)
        label(sh, x, top, cw, 0.55, ph, size=13, bold=True, color=WHITE, align="c", anchor="m",
              margin=(0.2, 0, 0.12, 0))
        rect(s, x, top + 0.68, cw, 4.0, fill=GREY_BG)
    by_phase = {p: [] for p in PHASES}
    for p in PROJECTS:
        if p[2]:
            by_phase[p[2]].append(p)
    ph_h, ph_gap = 0.62, 0.14   # nejplnější sloupec (Analýza) má 5 projektů
    for i, ph in enumerate(PHASES):
        x = LM + i * (cw + gap) + 0.08
        y = top + 0.86
        for name, area, _, cust in by_phase[ph]:
            w = cw - 0.16
            rrect(s, x, y, w, ph_h, fill=AREA[area], radius=0.1)
            label(s.shapes[-1], x, y, w, ph_h, name, size=11, bold=True, color=WHITE, align="c", anchor="m",
                  margin=(0.06, 0.03, 0.06, 0.03))
            if cust:
                custody_tag(s, x + w - 1.0 + 0.04, y - 0.12, w=1.0, h=0.24)
            y += ph_h + ph_gap
    legend(s, LM, 6.4)
    unphased = [p[0] for p in PROJECTS if not p[2]]
    if unphased:
        text(s, LM + 8.9, 6.3, CW - 8.9, 0.5, f"{', '.join(unphased)} (s RSJ Custody): fáze se upřesňuje.",
             size=10, color=GREY, align="r", anchor="m")


def s07_core(prs):
    c = AREA["Core IT"]
    s = new_slide(prs, "Core IT: jeden zdroj identit, řízená oprávnění a bezpečnostní dohled", (
        "Core IT projekty na sebe přímo navazují. Data o zaměstnancích vznikají na HR v modulu BOSS a automaticky se "
        "přenášejí do AD a Entra ID; je to v provozu a celý proces je auditovatelný. Na tom stavíme RBAC, tedy oprávnění "
        "podle rolí: aktuálně mapujeme systémy a definujeme role, je to dlouhodobý projekt. MS Sentinel s partnerem Orbit "
        "je ve fázi dokončení: všechny systémy jsou napojené, detekční pravidla vyladěná a playbooky hotové, teď dokončujeme "
        "přehledy a dokumentaci. Po předání ho převezme nová role security & cloud administrátora. Od června 2026 interně "
        "realizujeme SharePoint governance s plánem do 12/2027: děláme revizi sites, pravidla pro zakládání sites a týmů "
        "a dokumentaci vlastníků a účelu, následně srovnáme oprávnění na skupiny podle rolí v návaznosti na RBAC. "
        "Projekt je zároveň předpokladem pro nasazení Microsoft Purview pro klasifikaci a ochranu dat. Alvao jsme "
        "rozšířili na plnohodnotný IT service management včetně evidence IT aktiv podle požadavků DORA."
    ))
    # řetězec
    chain = [("HR modul BOSS", "zdroj dat o zaměstnancích"), ("AD / Entra ID", "identity uživatelů"),
             ("RBAC", "oprávnění podle rolí")]
    bw, aw = 3.3, 0.55
    total = 3 * bw + 2 * (aw + 0.2)
    x = LM + (CW - total) / 2
    for i, (n, d) in enumerate(chain):
        rrect(s, x, 1.55, bw, 0.82, fill=WHITE, line=c, radius=0.12, line_w=1.5)
        label(s.shapes[-1], x, 1.55, bw, 0.82, [
            {"text": n, "bold": True, "size": 15, "color": NAVY},
            {"text": d, "size": 11, "color": GREY_D},
        ], align="c", anchor="m")
        x += bw
        if i < 2:
            arrow_right(s, x + 0.1, 1.8, w=aw, h=0.32, fill=c)
            x += aw + 0.2
    xs = LM + (CW - total) / 2
    rrect(s, xs, 2.5, total, 0.42, fill=c, radius=0.3)
    label(s.shapes[-1], xs, 2.5, total, 0.42,
          "MS Sentinel: bezpečnostní dohled nad celým řetězcem, včetně logů synchronizace",
          size=12.5, bold=True, color=WHITE, align="c", anchor="m")
    cards = [
        ("MS Sentinel", "Dokončení · plán 11/2026",
         "Plný přehled o bezpečnosti, rychlejší odhalení hrozeb a automatická reakce. Naplno využíváme nástroj, "
         "za který už platíme.", False),
        ("Propojení HR modulu BOSS s AD", "Provoz",
         "Údaje o zaměstnancích jsou ve všech systémech stejné a aktuální, bez ručního přepisování.", True),
        ("RBAC", "Realizace · dlouhodobý",
         "Nástup, změna pozice i odchod se řeší přiřazením role. Oprávnění jsou přehledná a auditovatelná.", False),
        ("SharePoint governance", "Realizace · do 12/2027",
         "Každá site má vlastníka a účel, přístupy jsou podle rolí. Přehledné a auditovatelné podle DORA.", False),
        ("IT service management v Alvao", "Provoz",
         "Požadavky, změny a incidenty procházejí jednotným dohledatelným procesem podle DORA.", False),
    ]
    gap = 0.18
    n_c = len(cards)
    w = (CW - (n_c - 1) * gap) / n_c
    for i, (n, ph, b, cust) in enumerate(cards):
        x = LM + i * (w + gap)
        card(s, x, 3.2, w, 3.5, c)
        text(s, x + 0.12, 3.38, w - 0.24, 0.82, n, size=14, bold=True, color=NAVY, anchor="t")
        phase_pill(s, x + 0.15, 4.22, ph, w=min(w - 0.3, 0.1 * len(ph) + 0.4), fill=c, size=9.5)
        text(s, x + 0.12, 4.65, w - 0.24, 1.95, b, size=12, color=INK, spacing=1.05)
        if cust:
            custody_tag(s, x + w - 1.1, 3.08, w=1.0)


def s08_ai(prs):
    c = AREA["AI automatizace"]
    s = new_slide(prs, "AI zavádíme řízeně: od PoC přes pilot do provozu", (
        "AI automatizace vede Frederik Urban, na dvou projektech s externím konzultantem Jakubem Filipem. "
        "AI reporting pro PE/VC tým je v pilotu: řešení zpracuje vstupní data, pomocí AI z nich vytěží potřebné "
        "informace, validuje je a uloží do databáze; teď ho napojujeme na MDM a výstupy později na Power BI. "
        "AI posouzení LPA je ve fázi PoC, pravidla pro posouzení smluv už máme definovaná a po PoC rozhodneme o realizaci. "
        "AI vytěžování faktur je v analýze a navazuje na workflow schvalování faktur v aplikaci Invoices. "
        "Každý projekt prochází PoC a pilotem a výstupy AI kontroluje člověk."
    ))
    stages = ["Analýza", "PoC", "Pilot", "Provoz"]
    gap = 0.07
    sw = (CW - gap * 3) / 4
    for i, st in enumerate(stages):
        x = LM + i * (sw + gap)
        kind = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        sh = shape(s, kind, x, 1.55, sw + (0.12 if i < 3 else 0), 0.55, fill=NAVY)
        label(sh, x, 1.55, sw, 0.55, st, size=14, bold=True, color=WHITE, align="c", anchor="m",
              margin=(0.25, 0, 0.15, 0))
    projects = [
        ("AI vytěžování faktur", 0, "Analýza · od 10/2026 · J. Filip",
         "Méně ručního přepisování faktur v backoffice a účtárně, méně chyb a rychlejší zpracování."),
        ("AI posouzení LPA", 1, "PoC · od 09/2026 · J. Filip",
         "Rychlejší a konzistentní kontrola smluv LPA podle jednotných pravidel, menší riziko přehlédnutí."),
        ("AI reporting pro PE/VC tým", 2, "Pilot · od 06/2026 · interně",
         "Úspora času PE/VC týmu na ručním zpracování dat a méně chyb díky automatické validaci."),
    ]
    for n, col, meta, b in projects:
        x = LM + col * (sw + gap)
        card(s, x, 2.3, sw, 3.3, c)
        text(s, x + 0.15, 2.48, sw - 0.3, 0.75, n, size=16, bold=True, color=NAVY)
        text(s, x + 0.15, 3.18, sw - 0.3, 0.35, meta, size=11, bold=True, color=c)
        text(s, x + 0.15, 3.6, sw - 0.3, 1.9, b, size=13, color=INK, spacing=1.05)
    x = LM + 3 * (sw + gap)
    rrect(s, x, 2.3, sw, 3.3, fill=WHITE, line=GREY_L, radius=0.04)
    text(s, x + 0.2, 2.5, sw - 0.4, 2.9, [
        {"text": "Cíl", "bold": True, "size": 16, "color": NAVY},
        {"text": "Do provozu jde jen řešení, které obstojí v PoC a pilotu.", "size": 13, "color": GREY_D,
         "space_before": 6},
    ])
    rrect(s, LM, 5.85, CW, 0.85, fill=ACCENT_BG, line=ACCENT, radius=0.08)
    rect(s, LM, 5.85, 0.09, 0.85, fill=ACCENT)
    text(s, LM + 0.3, 5.88, CW - 0.5, 0.8, [{"runs": [
        ("Řízené zavádění: ", {"bold": True, "color": NAVY}),
        ("každý projekt prochází PoC a pilotem, výstupy AI kontroluje člověk. "
         "AI stavíme na datech z MDM, výstupy napojujeme do Power BI.", {}),
    ]}], size=14, color=INK, anchor="m")


def s09_dev(prs):
    c = AREA["Development"]
    s = new_slide(prs, "Odcházíme z on-premise SharePointu a stavíme na jednom zdroji dat", (
        "Development projekty mají dva hlavní příběhy. Prvním je odchod z on-premise SharePointu: nový DMS na PaaS "
        "je akceptovaný a teď připravujeme migraci dat ze dvou zdrojů, SPV z původního DMS a fondy ze SharePointu. "
        "Migrace je zároveň příležitostí data vyčistit. Následuje Projects, kde probíhá analýza s plánem na 04/2027, "
        "a v roce 2027 Invoices. Po přesunu všech tří aplikací odstavíme on-premise SharePoint a zrušíme lokální AD. "
        "Druhým příběhem je MDM, které je od 7/2026 v produkci: subjekty vznikají jen v MDM a napojené systémy pracují se "
        "stejnými daty. Na MDM staví i nový projekt řízení úkolů a projektů, který vznikl z poptávky finančního řízení "
        "po opakovaných checklistech pro fondy; přednostně posuzujeme stávající nástroje v M365 a Alvao. S RSJ Custody "
        "realizujeme auditní workflow, které převádí ruční kontroly a schvalování úkonů fondů z e-mailů a tabulek do "
        "dohledatelného procesu s auditní stopou; teď SharePoint Solutions upravuje WF engine. HR modul BOSS je v provozu "
        "a rozvíjí se o nábor a matici rolí a oprávnění. Nový BOSS přepisuje celý systém na bezpečnější platformu, běží "
        "průběžně bez pevného harmonogramu. V reportingu probíhá výběrové řízení na partnera pro migraci DWH do Fabricu "
        "a analýza databáze KPI pro finanční manažery a risk."
    ))
    text(s, LM, 1.45, 8, 0.38, "Migrace z on-premise SharePointu", size=14, bold=True, color=NAVY2)
    steps = [("DMS", "Dokončení", c), ("Projects", "Analýza · plán 04/2027", c),
             ("Invoices", "Nápad · 2027", c), ("Odstavení SharePointu a AD", "2028 · jen Entra ID", NAVY)]
    gap = 0.07
    sw = (CW - gap * 3) / 4
    for i, (n, d, col) in enumerate(steps):
        x = LM + i * (sw + gap)
        kind = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        shape(s, kind, x, 1.88, sw + (0.15 if i < 3 else 0), 0.95, fill=col)
        text(s, x + 0.4, 1.88, sw - 0.75, 0.95, [
            {"text": n, "bold": True, "size": 15},
            {"text": d, "size": 11, "color": "E6F2EF" if col == c else "C9D3E6"},
        ], color=WHITE, align="c", anchor="m", margin=(0.02, 0.02, 0.02, 0.02))
    # MDM hub
    text(s, LM, 3.12, 6, 0.38, "MDM jako jeden zdroj pravdy", size=14, bold=True, color=NAVY2)
    hx, hy = LM + 3.0, 4.85
    sats = [("Helios – Fondy", -2.0, -0.95), ("Helios – SPV", 2.0, -0.95), ("Cashflow", -2.0, 0.0),
            ("DMS", 2.0, 0.0), ("AI reporting PE/VC", -2.0, 0.95), ("další systémy", 2.0, 0.95)]
    for n, dx, dy in sats:
        x1, y1 = hx + dx, hy + dy
        con = s.shapes.add_connector(1, Inches(hx), Inches(hy), Inches(x1), Inches(y1))
        con.line.color.rgb = rgb(GREY_L)
        con.line.width = Pt(1.5)
    for n, dx, dy in sats:
        x1, y1 = hx + dx, hy + dy
        rrect(s, x1 - 0.9, y1 - 0.25, 1.8, 0.5, fill=WHITE, line=GREY_L, radius=0.3)
        label(s.shapes[-1], x1 - 0.9, y1 - 0.25, 1.8, 0.5, n, size=11, color=INK, align="c", anchor="m",
              margin=(0.04, 0, 0.04, 0))
    shape(s, MSO_SHAPE.OVAL, hx - 0.65, hy - 0.65, 1.3, 1.3, fill=c)
    label(s.shapes[-1], hx - 0.65, hy - 0.65, 1.3, 1.3, [
        {"text": "MDM", "bold": True, "size": 18}, {"text": "provoz od 7/2026", "size": 9.5},
    ], color=WHITE, align="c", anchor="m", margin=(0.02, 0, 0.02, 0))
    custody_tag(s, hx - 0.5, hy + 0.58, w=1.0)
    # ostatní projekty
    xr = LM + 6.55
    wr = SLIDE_W - LM - xr
    text(s, xr, 3.12, wr, 0.38, "Další projekty", size=14, bold=True, color=NAVY2)
    dev, rep = AREA["Development"], AREA["Reporting"]
    others = [
        ("Založení fondu", "Pilot · plán 12/2026", dev, True,
         "Jednotný řízený a dohledatelný proces."),
        ("Auditní workflow", "Realizace · od 11/2026", dev, True,
         "Kontroly a schvalování s auditní stopou."),
        ("BOSS HR", "Provoz, další rozvoj", dev, True,
         "Jedna evidence lidí, řízený nástup i odchod."),
        ("Nový BOSS", "Realizace · průběžně", dev, True,
         "Přepis BOSS na bezpečnější platformu."),
        ("Řízení úkolů a projektů", "Analýza · od 08/2026", dev, False,
         "Opakované úkoly vznikají automaticky, nic se neopomene."),
        ("Migrace DWH do Fabricu", "Analýza · výběr partnera", rep, False,
         "Moderní datová platforma propojená s Power BI."),
        ("Databáze KPI", "Analýza · od 10/2026", rep, False,
         "KPI projektů na jednom místě pro finanční manažery a risk."),
    ]
    y, rh = 3.52, 0.45   # 7 řádků musí skončit nad zápatím (6.98)
    for n, ph, col, cust, b in others:
        rrect(s, xr, y, wr, rh, fill=GREY_BG, radius=0.1)
        rect(s, xr, y, 0.08, rh, fill=col)
        runs = ([(ph + " · ", {"bold": True, "color": col})] if ph else []) + [(b, {})]
        text(s, xr + 0.18, y, wr - 0.3, rh, [
            {"text": n, "size": 12, "bold": True, "color": NAVY},
            {"runs": runs, "size": 10},
        ], color=GREY_D, anchor="m", margin=(0.04, 0.01, 0.04, 0.01), spacing=0.95)
        if cust:
            custody_tag(s, xr + wr - 1.1, y + 0.05, w=1.0, h=0.2, size=8)
        y += rh + 0.03


def s10_custody(prs):
    s = new_slide(prs, "S RSJ Custody společně posouváme šest klíčových projektů", (
        "Spolupráce s IS útvarem RSJ Custody je pro nás klíčová a funguje. S Tomášem Málkem máme pravidelné schůzky "
        "a komunikace i spolupráce probíhá bez problémů. Na propojení HR modulu BOSS s AD dodal RSJ Custody export "
        "dat a my přenos do AD, Entra ID a dohled v Sentinelu; je to v provozu. MDM vyvíjí Dušan Marko, formálně z RSJ "
        "Custody, plně alokovaný pro nás, a je od 7/2026 v produkci. Workflow pro založení fondu je v pilotu souběžně "
        "se starým procesem. Auditní workflow je v realizaci, WF engine upravuje SharePoint Solutions. HR modul BOSS "
        "eviduje zaměstnance i externisty a řídí onboarding a offboarding, dál se rozvíjí o nábor a matici rolí "
        "a oprávnění. Nový BOSS je dlouhodobý přepis celého systému na bezpečnější platformu a týká se i propojení s AD a RBAC."
    ))
    items = [
        ("Propojení HR modulu BOSS s AD", "Core IT", "Provoz",
         "Export dat z HR modulu BOSS", "Přenos do AD a Entra ID, dohled v Sentinelu"),
        ("MDM", "Development", "Provoz, další rozvoj",
         "Vývoj (D. Marko), od 7/2026 v produkci", "Správa, řízení projektu, napojování systémů"),
        ("Založení fondu", "Development", "Pilot · plán 12/2026",
         "Vývoj workflow aplikace", "Řízení projektu, pilot se starým procesem"),
        ("Auditní workflow", "Development", "Realizace · od 11/2026",
         "Vývoj (IS útvar)", "Řízení projektu, WF engine od SharePoint Solutions"),
        ("BOSS HR", "Development", "Provoz, další rozvoj",
         "Evidence lidí, onboarding a offboarding, nábor", "Data o zaměstnancích pro AD a RBAC"),
        ("Nový BOSS", "Development", "Realizace · průběžně",
         "Přepis BOSS na novou, bezpečnější platformu", "Návaznost na propojení s AD a RBAC"),
    ]
    gap = 0.16
    w = (CW - (len(items) - 1) * gap) / len(items)
    for i, (n, area, ph, cus, it) in enumerate(items):
        x = LM + i * (w + gap)
        col = AREA[area]
        card(s, x, 1.6, w, 4.15, col)
        text(s, x + 0.12, 1.75, w - 0.24, 0.85, n, size=13, bold=True, color=NAVY)
        text(s, x + 0.12, 2.62, w - 0.24, 0.36, ph, size=10, bold=True, color=col, margin=(0.04, 0.05, 0.04, 0.05))
        rect(s, x + 0.12, 3.0, w - 0.24, 0.012, fill=GREY_L)
        custody_tag(s, x + 0.12, 3.15, w=1.0)
        text(s, x + 0.12, 3.45, w - 0.24, 0.85, cus, size=11.5, color=INK)
        pill(s, x + 0.12, 4.35, 1.0, 0.24, "IT útvar", NAVY2, size=8.5)
        text(s, x + 0.12, 4.65, w - 0.24, 1.0, it, size=11.5, color=INK)
    rrect(s, LM, 6.0, CW, 0.75, fill=NAVY, radius=0.1)
    label(s.shapes[-1], LM, 6.0, CW, 0.75, [{"runs": [
        ("Spolupráce funguje: ", {"bold": True, "color": ACCENT}),
        ("pravidelné schůzky s vedoucím IS útvaru Tomášem Málkem, komunikace i spolupráce bez problémů.", {}),
    ]}], size=14, color=WHITE, align="c", anchor="m")


def s11_budget(prs):
    s = new_slide(prs, "Provozní náklady IT jsou v budgetu: výhled na rok 96 % plánu", (
        "Provozní náklady IT jsou v budgetu. Za první pololetí jsme vyčerpali 83 % plánu, tedy 4,42 z 5,32 mil. Kč. "
        "Výhled na celý rok 2026 je 12,12 mil. Kč proti budgetu 12,62 mil. Kč, tedy 96 % a zhruba půl milionu pod "
        "plánem. Největší položkou jsou mzdy a režie, následují licence. Nad plánem jsou jen služby mimo skupinu, "
        "na 112 %, naopak Azure je výrazně pod plánem. Data jsou z účetnictví k 30. 6. 2026, za Q3 je zatím nemám "
        "a výhled druhého pololetí je odhad."
    ))
    # KPI dlaždice – dle Klíčová čísla v kapitole Budget
    kpis = [("12,62", "mil. Kč", "Budget FY 2026"), ("12,12", "mil. Kč", "Výhled FY 2026"),
            ("96,1 %", "", "Čerpání FY (výhled), úspora 0,50 mil. Kč"), ("83,1 %", "", "Čerpání H1 (4,42 z 5,32 mil. Kč)")]
    gap = 0.2
    kw = (CW - 3 * gap) / 4
    for i, (v, u, t) in enumerate(kpis):
        x = LM + i * (kw + gap)
        hl = i == 2
        rrect(s, x, 1.5, kw, 1.12, fill=ACCENT_BG if hl else GREY_BG, line=ACCENT if hl else None, radius=0.08)
        text(s, x + 0.2, 1.55, kw - 0.4, 0.6, [{"runs": [(v, {"size": 28, "bold": True, "color": NAVY}),
                                                          ("  " + u if u else "", {"size": 13, "color": GREY_D})]}],
             anchor="m")
        text(s, x + 0.2, 2.1, kw - 0.4, 0.5, t, size=11, color=GREY_D, anchor="t", spacing=0.95)
    # graf Budget vs. výhled podle oblastí
    rows = [("Mzdy a režie", 5.65, 5.56, "98,3 %"), ("Licence", 3.43, 3.16, "92,2 %"),
            ("Služby mimo skupinu", 1.91, 2.14, "112,0 %"), ("Azure", 1.61, 1.24, "77,3 %"),
            ("Ostatní náklady", 0.02, 0.02, "98,8 %")]
    gy = 2.85
    text(s, LM, gy, 7.5, 0.38, "Budget vs. výhled FY 2026 podle oblastí (mil. Kč)", size=14, bold=True, color=NAVY2)
    lx = LM + 8.3
    rect(s, lx, gy + 0.13, 0.22, 0.14, fill=GREY_L)
    text(s, lx + 0.27, gy, 1.2, 0.38, "Budget FY", size=11, color=GREY_D, anchor="m")
    rect(s, lx + 1.55, gy + 0.13, 0.22, 0.14, fill=NAVY)
    text(s, lx + 1.82, gy, 1.5, 0.38, "Výhled FY", size=11, color=GREY_D, anchor="m")
    lab_w, bx0, pct_w = 2.3, LM + 2.45, 1.2
    bar_max = CW - (bx0 - LM) - pct_w - 0.75
    vmax = max(max(r[1], r[2]) for r in rows)
    y, rh = gy + 0.5, 0.55
    for n, b, f, pct in rows:
        text(s, LM, y, lab_w, rh - 0.08, n, size=12.5, bold=True, color=INK, anchor="m")
        for k, (val, col) in enumerate(((b, GREY_L), (f, NAVY))):
            by = y + 0.04 + k * 0.22
            bw = max(0.03, bar_max * val / vmax)
            rect(s, bx0, by, bw, 0.18, fill=col)
            text(s, bx0 + bw + 0.05, by - 0.06, 0.7, 0.3, f"{val:.2f}".replace(".", ","), size=10,
                 color=GREY_D, anchor="m", margin=(0.02, 0, 0.02, 0))
        over = float(pct.split()[0].replace(",", ".")) > 100
        text(s, SLIDE_W - LM - pct_w, y, pct_w, rh - 0.08, pct, size=13, bold=True,
             color=RED if over else NAVY, align="r", anchor="m")
        y += rh
    text(s, SLIDE_W - LM - pct_w - 0.4, gy + 0.26, pct_w + 0.4, 0.3, "čerpání FY", size=9.5, color=GREY,
         align="r", anchor="m")
    # komentář
    rrect(s, LM, 6.05, CW, 0.75, fill=GREY_BG, radius=0.1)
    rect(s, LM, 6.05, 0.09, 0.75, fill=ACCENT)
    text(s, LM + 0.3, 6.05, CW - 0.5, 0.75, [
        {"runs": [("Celkově v plánu: ", {"bold": True, "color": NAVY}),
                  ("výhled na rok je o 0,5 mil. Kč pod budgetem.", {})]},
        {"text": "Zdroj: účetnictví k 30. 6. 2026. Data za Q3 zatím nejsou k dispozici, výhled H2 je odhad.",
         "size": 10.5, "color": GREY},
    ], size=14, color=INK, anchor="m")


def s12_target(prs):
    s = new_slide(prs, "Cílový model: kompetence a zastupitelnost místo navyšování", (
        "Cílem není navyšovat počet lidí, ale zajistit kompetence, kontinuitu a nezávislost na jednotlivcích. "
        "Tým chci rozdělit do čtyř oblastí: provoz, bezpečnost, rozvoj a data a reporting. Interní kapacita se změní "
        "ze 6 na 8, a to cíleně do oblastí, které dnes nikdo nevlastní nebo stojí na jednom člověku. Security & cloud "
        "administrátor převezme cloudovou a bezpečnostní agendu a dá bezpečnosti vlastníka, datový specialista zajistí "
        "zastupitelnost v DWH a reportingu. Náklad pozic poměřujeme s nákladem rizika, tedy regulatorním a reputačním "
        "dopadem nezvládnutého incidentu nebo výpadkem nezastupitelného člověka. "
        "Variantou k zvážení je místo náboru IT administrátora do Provozu rozvinout Jana Kridla na administrátora "
        "se zaměřením na cloud (M365 a Azure) a L1 support předat stážistovi; přínosem jsou nižší náklady a využití "
        "znalosti firmy, rizikem čas na rozvoj a omezená kapacita stážisty, takže L1 bude potřebovat zástup."
    ))
    teams = [
        ("Provoz", "Podpora uživatelů, M365, endpoint, DMS a workflow",
         [("J. Kridlo", False), ("IT administrátor (M365, Intune)", False)], "Orbit (L2/L3)"),
        ("Bezpečnost", "Security, identita, Azure, síť, backup",
         [("Security & cloud administrátor", True)], "Orbit, volitelně SOC/MDR"),
        ("Rozvoj", "AI automatizace, vývoj a integrace, MDM",
         [("F. Urban", False), ("D. Marko", False)], "J. Filip"),
        ("Data a reporting", "DWH, Power BI, migrace do Fabricu",
         [("M. Bartošová", False), ("Datový specialista", True)], "Fabric partner"),
    ]
    gap = 0.2
    w = (CW - 3 * gap) / 4
    for i, (n, area, inter, ext) in enumerate(teams):
        x = LM + i * (w + gap)
        rrect(s, x, 1.55, w, 0.55, fill=NAVY, radius=0.12)
        label(s.shapes[-1], x, 1.55, w, 0.55, n, size=15, bold=True, color=WHITE, align="c", anchor="m")
        text(s, x + 0.05, 2.15, w - 0.1, 0.6, area, size=11, color=GREY_D, align="c", anchor="m")
        rrect(s, x, 2.8, w, 1.85, fill=GREY_BG, radius=0.05)
        text(s, x + 0.15, 2.86, w - 0.3, 0.3, "INTERNĚ", size=9.5, bold=True, color=GREY)
        y = 3.2
        for name, new in inter:
            if new:
                rrect(s, x + 0.12, y, w - 0.24, 0.68, fill=ACCENT_BG, line=ACCENT, radius=0.12)
                text(s, x + 0.2, y, w - 0.4, 0.68, [
                    {"text": name, "bold": True, "size": 12, "color": NAVY},
                    {"text": "nová role", "size": 9.5, "bold": True, "color": "9A6B00"},
                ], anchor="m", spacing=0.95)
            else:
                text(s, x + 0.2, y, w - 0.4, 0.6, name, size=12.5, bold=True, color=NAVY, anchor="m")
            y += 0.72
        rrect(s, x, 4.75, w, 0.8, fill=WHITE, line=GREY_L, radius=0.08)
        text(s, x + 0.15, 4.79, w - 0.3, 0.72, [
            {"text": "EXTERNĚ", "size": 9.5, "bold": True, "color": GREY},
            {"text": ext, "size": 12, "color": INK},
        ], anchor="m")
    # KPI + governance
    rrect(s, LM, 5.8, 4.0, 0.95, fill=NAVY, radius=0.1)
    label(s.shapes[-1], LM, 5.8, 4.0, 0.95, [{"runs": [
        ("6 → 8 ", {"bold": True, "size": 26, "color": ACCENT}),
        ("interní kapacita (+2 FTE)", {"size": 14, "color": WHITE}),
    ]}], align="c", anchor="m")
    rrect(s, LM + 4.2, 5.8, CW - 4.2, 0.95, fill=GREY_BG, radius=0.1)
    text(s, LM + 4.4, 5.8, CW - 4.6, 0.95, [
        {"runs": [("Výhled: ", {"bold": True, "color": NAVY}),
                  ("nové role jen tam, kde dnes chybí vlastník nebo zástup. "
                   "Governance a koordinaci projektů drží vedoucí IT jako partner businessu.", {})]},
    ], size=13, color=INK, anchor="m")


def s13_strategy(prs):
    s = new_slide(prs, "AI je hlavní směr, stavíme ho na vyladěných systémech, datech a cloudu", (
        "Strategie projektů stojí na čtyřech pilířích. Prvním je ladění a plné využití toho, co už máme, například "
        "Sentinel, Alvao nebo MDM; nové projekty zakládáme jen tam, kde stávající řešení nevyhovuje. Druhým je AI jako "
        "hlavní směr: automatizujeme opakovanou ruční práci, využíváme M365 Copilot, za který už platíme, a plánujeme "
        "RAG nad DMS. AI zavádíme řízeně přes PoC a pilot a IKT rizika posuzujeme s 2. linií. Třetím jsou kvalitní data: "
        "MDM a HR modul BOSS jako jeden zdroj pravdy, RBAC a Fabric; potřebujeme k tomu i pozici datového specialisty. "
        "Čtvrtým je cloud first, tedy odchod z on-premise SharePointu, lokálního AD a virtuálních serverů v Azure. "
        "Časová osa vychází z výhledu: do konce roku dokončení Sentinelu a DMS, vyhodnocení AI a výběr partnera pro "
        "Fabric, v roce 2027 Projects, Invoices a migrace DWH, v roce 2028 odstavení SharePointu a AD."
    ))
    pillars = [
        (MSO_SHAPE.GEAR_6, "Ladění stávajících systémů",
         "Naplno využíváme, co máme: Sentinel, Alvao, MDM. Nové jen tam, kde to nestačí.", NAVY2),
        (MSO_SHAPE.STAR_4_POINT, "AI",
         "Hlavní směr. Řízeně přes PoC a pilot, výstupy kontroluje člověk. Využíváme M365 Copilot.",
         AREA["AI automatizace"]),
        (MSO_SHAPE.CAN, "Kvalitní data",
         "Jeden zdroj pravdy (MDM, HR modul BOSS), RBAC a Fabric. Nově datový specialista.", NAVY2),
        (MSO_SHAPE.CLOUD, "Cloud first",
         "Odchod z on-premise SharePointu, AD a VM. Vše jako SaaS/PaaS, jen Entra ID.", NAVY2),
    ]
    gap = 0.2
    w = (CW - 3 * gap) / 4
    for i, (ic, n, d, col) in enumerate(pillars):
        x = LM + i * (w + gap)
        hl = i == 1
        rrect(s, x, 1.55, w, 2.4, fill=ACCENT_BG if hl else GREY_BG, line=ACCENT if hl else None, radius=0.05)
        icon(s, ic, x + 0.2, 1.72, d=0.62, bg=col)
        text(s, x + 0.15, 2.4, w - 0.3, 0.6, n, size=14, bold=True, color=NAVY, anchor="m")
        text(s, x + 0.15, 2.95, w - 0.3, 0.95, d, size=12, color=INK, spacing=1.0)
    # časová osa – dle tabulky Výhled v kapitole Strategie projektů
    ty = 4.2
    rect(s, LM, ty + 0.2, CW, 0.05, fill=GREY_L)
    periods = [
        ("Do konce 2026", ["Dokončení Sentinelu (11/2026) a migrace DMS", "Ostrý provoz Založení fondu",
                           "Vyhodnocení pilotů a PoC v AI", "Výběr partnera pro Fabric"]),
        ("2027", ["Migrace Projects (04/2027)", "Migrace a nasazení Invoices", "Rozšíření AI automatizací do provozu",
                  "Migrace DWH do Fabricu"]),
        ("2028", ["Odstavení on-premise SharePointu a lokálního AD", "Rušení virtuálních serverů"]),
        ("Dlouhodobě", ["Plně cloudové prostředí (SaaS/PaaS)", "AI jako běžná součást klíčových procesů",
                        "RBAC napříč všemi systémy"]),
    ]
    for i, (p, items) in enumerate(periods):
        x = LM + i * (w + gap)
        shape(s, MSO_SHAPE.OVAL, x, ty + 0.08, 0.3, 0.3, fill=ACCENT if i == 0 else NAVY)
        text(s, x + 0.38, ty, w - 0.4, 0.45, p, size=15, bold=True, color=NAVY, anchor="m")
        text(s, x, ty + 0.55, w - 0.05, 2.15, [{"text": t, "bullet": True, "space_before": 3} for t in items],
             size=12, color=INK)


def s14_apps(prs):
    s = new_slide(prs, "Příloha: přehled klíčových aplikací", (
        "V příloze je přehled klíčových aplikací, které vyvíjíme a provozujeme my nebo IS útvar RSJ Custody. "
        "DMS, Projects a Invoices dnes fyzicky běží na upraveném on-premise SharePointu na serverech v Azure "
        "a postupně je převádíme na PaaS. MDM je zdrojem kmenových dat pro Helios a Cashflow. Power BI reporting "
        "čerpá data z DWH."
    ))
    apps = [
        ("BOSS", "Evidence kovenantů, úvěrových smluv, modul HR", "SaaS", "RSJ Custody", "RSJ Custody"),
        ("Založení fondu", "Workflow založení fondu", "PaaS", "RSJ Custody", "RSJ Custody"),
        ("MDM", "Master data management – zdroj pravdy", "PaaS", "RSJ Services", "D. Marko"),
        ("Cashflow", "Plánování budgetů na fondech", "PaaS", "RSJ Services", "D. Marko"),
        ("DWH", "Datový sklad, zdroj dat pro reporting", "PaaS", "RSJ Services", "D. Marko"),
        ("Power BI", "Reporting pro RSJ Investments a RSJ Services", "SaaS", "RSJ Services", "M. Bartošová"),
        ("DMS", "Archiv smluv a dokumentace fondů a SPV", "IaaS", "RSJ Services", "SharePoint Solutions"),
        ("Projects", "Workflow investičních rozhodnutí", "IaaS", "RSJ Services", "SharePoint Solutions"),
        ("Invoices", "Workflow schvalování faktur", "IaaS", "RSJ Services", "SharePoint Solutions"),
        ("Helios – Fondy", "Účetnictví pro fondy", "SaaS", "RSJ Custody", "RSJ Custody"),
        ("Helios – SPV", "Účetnictví pro SPV", "SaaS", "RSJ Services", "Nesos"),
        ("Alvao", "IT ServiceDesk, finanční a legal helpdesk", "SaaS", "RSJ Services", "Alvao"),
    ]
    table(s, ["Aplikace", "Popis", "Model", "Správce", "Vývoj / dodavatel"], apps,
          [2.0, 5.0, 1.0, 1.9, 2.23], row_h=0.38, size=11.5)


def s15_projects(prs):
    s = new_slide(prs, "Příloha: detailní přehled projektů", (
        "Detailní tabulka projektů z přehledu, s oblastí, fází, partnerem a termíny. U projektů bez stanoveného termínu "
        "dokončení je uvedena pomlčka. MDM jsem převzal v běhu, v produkci je od 7/2026. Invoices je naplánován na rok 2027. "
        "Nový BOSS nemá pevný harmonogram, postupuje průběžně podle kapacit RSJ Custody. Partnera pro migraci DWH "
        "do Fabricu vybíráme ve výběrovém řízení."
    ))
    rows = [
        ("MS Sentinel", "Core IT", "Dokončení", "Orbit", "05/2026", "11/2026"),
        ("Propojení HR modulu BOSS s AD", "Core IT", "Provoz", "RSJ Custody (IS útvar)", "03/2026", "09/2026"),
        ("IT service management v Alvao", "Core IT", "Provoz", "interně", "09/2025", "02/2026"),
        ("RBAC", "Core IT", "Realizace", "interně", "04/2026", "dlouhodobý"),
        ("SharePoint governance", "Core IT", "Realizace", "interně", "06/2026", "12/2027"),
        ("AI reporting pro PE/VC tým", "AI automatizace", "Pilot", "interně", "06/2026", "–"),
        ("AI posouzení LPA", "AI automatizace", "PoC", "Jakub Filip", "09/2026", "–"),
        ("AI vytěžování faktur", "AI automatizace", "Analýza", "Jakub Filip", "10/2026", "–"),
        ("MDM", "Development", "Provoz, další rozvoj", "D. Marko (RSJ Custody)", "před 09/2025", "průběžně"),
        ("Založení fondu", "Development", "Pilot", "RSJ Custody (IS útvar)", "03/2026", "12/2026"),
        ("DMS", "Development", "Dokončení", "SharePoint Solutions", "04/2026", "–"),
        ("BOSS HR", "Development", "Provoz, další rozvoj", "RSJ Custody (IS útvar)", "01/2026", "průběžně"),
        ("Auditní workflow", "Development", "Realizace", "RSJ Custody (IS útvar), SharePoint Solutions",
         "11/2026", "–"),
        ("Nový BOSS", "Development", "Realizace", "RSJ Custody (IS útvar)", "11/2025", "průběžně, bez harmonogramu"),
        ("Projects", "Development", "Analýza", "SharePoint Solutions", "09/2026", "04/2027"),
        ("Invoices", "Development", "Nápad", "SharePoint Solutions", "2027", "2027"),
        ("Řízení úkolů a projektů", "Development", "Analýza", "interně", "08/2026", "–"),
        ("Migrace DWH do Fabricu", "Reporting", "Analýza", "výběrové řízení", "–", "–"),
        ("Databáze KPI", "Reporting", "Analýza", "interně", "10/2026", "–"),
    ]
    table(s, ["Projekt", "Oblast", "Fáze", "Partner", "Zahájení", "Dokončení"], rows,
          [2.75, 1.4, 1.62, 3.3, 1.0, 2.06], row_h=0.27, size=10, area_col=1)


def table(s, heads, rows, widths, row_h=0.38, size=11.5, area_col=None):
    n = len(rows) + 1
    t = s.shapes.add_table(n, len(heads), Inches(LM), Inches(1.45), Inches(sum(widths)), Inches(row_h * n)).table
    for j, wv in enumerate(widths):
        t.columns[j].width = Inches(wv)
    for i in range(n):
        t.rows[i].height = Inches(row_h)
        for j in range(len(heads)):
            cell = t.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(NAVY if i == 0 else (GREY_BG if i % 2 else WHITE))
            v = heads[j] if i == 0 else rows[i - 1][j]
            col = WHITE if i == 0 else INK
            if i > 0 and area_col is not None and j == area_col:
                col = AREA[v]
            fill_text(cell, v, size=size, bold=(i == 0 or j == 0 or (area_col is not None and j == area_col)),
                      color=col, anchor="m", margin=(0.08, 0.02, 0.08, 0.02),
                      box=(0, 0, widths[j], row_h))


# ---------------------------------------------------------------- kontrola přetékání
def overflow_check() -> list[str]:
    try:
        from PIL import ImageFont
    except ImportError:
        return ["(PIL není k dispozici – kontrola přeskočena)"]
    font_dirs = [Path("/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts"),
                 Path.home() / "Library/Fonts", Path("C:/Windows/Fonts")]
    def find(name):
        for d in font_dirs:
            p = d / name
            if p.exists():
                return str(p)
        return None
    reg, bld = find("Aptos.ttf"), find("Aptos-Bold.ttf")
    if not reg or not bld:
        return ["(font Aptos nenalezen – kontrola přeskočena)"]
    cache = {}
    def font(size, bold):
        k = (size, bold)
        if k not in cache:
            cache[k] = ImageFont.truetype(bld if bold else reg, int(round(size * 10)))  # 10 px = 1 pt
        return cache[k]
    warnings = []
    for e in _text_registry:
        avail_w = e["w"] * 72 * 10
        avail_h = e["h"] * 72
        total_h = 0.0
        for p in e["paras"]:
            sizes = [sz for _, sz, _ in p["runs"]] or [12]
            max_sz = max(sizes)
            indent = 0.18 * 72 * 10 if p["bullet"] else 0
            # rozdělit na slova se zachováním fontu
            words = []
            for t, sz, b in p["runs"]:
                for wd in t.replace("\n", " ").split(" "):
                    if wd:
                        words.append((wd, sz, b))
            lines, cur = 1, 0.0
            for wd, sz, b in words:
                f = font(sz, b)
                ww = f.getlength(wd) + f.getlength(" ")
                if cur + ww > avail_w - indent and cur > 0:
                    lines += 1
                    cur = ww
                else:
                    cur += ww
                if ww > avail_w - indent:
                    warnings.append(f"slide {e['slide']}: slovo „{wd}“ je širší než box")
            total_h += lines * max_sz * 1.2 * e["spacing"] + p["space_before"]
        if total_h > avail_h + 0.5:
            warnings.append(f"slide {e['slide']}: text „{e['preview']}…“ potřebuje {total_h:.0f} pt, box má {avail_h:.0f} pt")
    return warnings


def main():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    for fn in (s01_title, s02_summary, s03_start, s04_env, s05_team, s06_overview, s07_core, s08_ai,
               s09_dev, s10_custody, s11_budget, s12_target, s13_strategy, s14_apps, s15_projects):
        fn(prs)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Uloženo: {OUT} ({len(prs.slides)} slidů)")
    warns = overflow_check()
    if warns:
        print("Varování (možné přetékání textu):")
        for w in warns:
            print("  -", w)
        return 1
    print("Kontrola přetékání: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
