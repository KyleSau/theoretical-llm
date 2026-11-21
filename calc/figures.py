#!/usr/bin/env python3
"""
figures.py - draws the SVG charts in diagrams/ from the numbers in sizing.py.

    python3 calc/figures.py

Standard library only. Every chart is written twice, as *-light.svg and
*-dark.svg, so the docs can show the right one for the reader's GitHub theme.
The same numbers appear as a table next to each chart in the docs.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sizing  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagrams")
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", series="#2a78d6", context="#898781",
                  border="#e1e0d9", wash="#2a78d6"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", series="#3987e5", context="#898781",
                 border="#2c2c2a", wash="#3987e5"),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(w: int, h: int, t: dict, title: str, subtitle: str, body: str, desc: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}" font-family="{FONT}">
<title>{esc(title)}</title>
<desc>{esc(desc)}</desc>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" fill="{t['surface']}" stroke="{t['border']}"/>
<text x="24" y="34" font-size="15" font-weight="600" fill="{t['ink']}">{esc(title)}</text>
<text x="24" y="54" font-size="12" fill="{t['ink2']}">{esc(subtitle)}</text>
{body}
</svg>
"""


def nice_step(vmax: float, target: int = 5) -> float:
    raw = vmax / target
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def hbar(name: str, title: str, subtitle: str, rows: list, fmt, desc: str,
         label_w: int = 290, tick_fmt=None) -> None:
    """Ranked horizontal bars, one hue, value at the tip."""
    rows = sorted(rows, key=lambda r: -r[1])
    tick_fmt = tick_fmt or fmt
    w = 760
    x0 = 24 + label_w
    x1 = w - 24 - 78
    top = 78
    row_h = 30
    bar_h = 14
    vmax = max(v for _, v in rows)
    step = nice_step(vmax)
    axis_max = math.ceil(vmax / step) * step
    plot_h = row_h * len(rows)
    h = top + plot_h + 40

    def sx(v: float) -> float:
        return x0 + (x1 - x0) * v / axis_max

    for mode, t in THEMES.items():
        b: list = []
        ticks = int(round(axis_max / step))
        for i in range(ticks + 1):
            v = i * step
            x = sx(v)
            color = t["axis"] if i == 0 else t["grid"]
            b.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{top + plot_h}" stroke="{color}" stroke-width="1"/>')
            b.append(f'<text x="{x:.1f}" y="{top + plot_h + 18}" font-size="11" fill="{t["muted"]}" text-anchor="middle">{esc(tick_fmt(v))}</text>')
        for i, (label, v) in enumerate(rows):
            cy = top + i * row_h + row_h / 2
            y = cy - bar_h / 2
            bw = sx(v) - x0
            b.append(f'<text x="{x0 - 10}" y="{cy + 4:.1f}" font-size="12.5" fill="{t["ink2"]}" text-anchor="end">{esc(label)}</text>')
            if bw >= 5:
                b.append(f'<path d="M{x0},{y:.1f} h{bw - 4:.1f} a4,4 0 0 1 4,4 v{bar_h - 8} a4,4 0 0 1 -4,4 h-{bw - 4:.1f} z" fill="{t["series"]}"/>')
            else:
                b.append(f'<rect x="{x0}" y="{y:.1f}" width="{max(bw, 1.5):.1f}" height="{bar_h}" fill="{t["series"]}"/>')
            b.append(f'<text x="{x0 + bw + 8:.1f}" y="{cy + 4:.1f}" font-size="12" fill="{t["ink"]}">{esc(fmt(v))}</text>')
        svg = frame(w, h, t, title, subtitle, "\n".join(b), desc)
        with open(os.path.join(OUT, f"{name}-{mode}.svg"), "w") as f:
            f.write(svg)


SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def param_chart(d: dict) -> None:
    """Parameters against training compute, log-log. The plan is the emphasis; published models are context."""
    w, h = 760, 560
    left, right, top, bottom = 76, 28, 108, 60
    x_lo, x_hi = 23.0, 29.0   # log10 FLOPs
    y_lo, y_hi = 10.0, 14.0   # log10 parameters
    pw, ph = w - left - right, h - top - bottom

    def sx(v: float) -> float:
        return left + (math.log10(v) - x_lo) / (x_hi - x_lo) * pw

    def sy(v: float) -> float:
        return top + ph - (math.log10(v) - y_lo) / (y_hi - y_lo) * ph

    tr, mp = d["training"], d["model"]
    k = 6 * 21.62

    # (label, compute, total params, active params or None, label dx, dy, anchor)
    published = [
        ("GPT-3", 3.14e23, 1.75e11, None, 9, 4, "start"),
        ("Chinchilla", 5.76e23, 7.0e10, None, 10, 14, "start"),
        ("DeepSeek-V3", 3.3e24, 6.71e11, 3.7e10, -10, 4, "end"),
        ("Mistral Large 4", 1.24e25, 1.0e12, 5.2e10, -10, -8, "end"),
        ("MAI-Base-2, 2.8T", 2.4e25, 2.8e12, 8.0e10, -10, -8, "end"),
        ("Llama 3.1 405B", 3.8e25, 4.05e11, None, 10, 14, "start"),
    ]
    opt = tr["dense_100_day"]
    plan = [
        ("Pilot, dense 1T", tr["pilot_1t_dense"]["flops"], 1e12, None, 11, 15, "start"),
        ("Flagship, sparse", tr["flagship_moe"]["flops"], mp["total_params"], mp["active_params"], -12, 34, "end"),
        (f"Dense optimum, {opt['active'] / 1e12:.0f}T", opt["flops"], opt["active"], None, 12, 16, "start"),
    ]

    for mode, t in THEMES.items():
        b: list = []
        # grid and axes
        for e in range(int(x_lo), int(x_hi) + 1):
            x = left + (e - x_lo) / (x_hi - x_lo) * pw
            b.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + ph}" stroke="{t["grid"]}" stroke-width="1"/>')
            b.append(f'<text x="{x:.1f}" y="{top + ph + 18}" font-size="11" fill="{t["muted"]}" text-anchor="middle">10{str(e).translate(SUP)}</text>')
        for e, lab in ((10, "10B"), (11, "100B"), (12, "1T"), (13, "10T"), (14, "100T")):
            y = top + ph - (e - y_lo) / (y_hi - y_lo) * ph
            b.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + pw}" y2="{y:.1f}" stroke="{t["grid"]}" stroke-width="1"/>')
            b.append(f'<text x="{left - 8}" y="{y + 4:.1f}" font-size="11" fill="{t["muted"]}" text-anchor="end">{lab}</text>')
        b.append(f'<line x1="{left}" y1="{top + ph}" x2="{left + pw}" y2="{top + ph}" stroke="{t["axis"]}" stroke-width="1"/>')
        b.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + ph}" stroke="{t["axis"]}" stroke-width="1"/>')
        b.append(f'<text x="{left + pw / 2:.1f}" y="{h - 16}" font-size="12" fill="{t["ink2"]}" text-anchor="middle">Training compute for the run (FLOPs, log scale)</text>')
        b.append(f'<text transform="translate(20,{top + ph / 2:.1f}) rotate(-90)" font-size="12" fill="{t["ink2"]}" text-anchor="middle">Parameters (log scale)</text>')

        # compute-optimal line: N = sqrt(C / (6 * 21.62))
        xa, xb = 10 ** x_lo, 10 ** x_hi
        b.append(f'<line x1="{sx(xa):.1f}" y1="{sy(math.sqrt(xa / k)):.1f}" x2="{sx(xb):.1f}" y2="{sy(math.sqrt(xb / k)):.1f}" stroke="{t["context"]}" stroke-width="2" stroke-linecap="round"/>')
        # the two limits: data (horizontal) and 100 days of the campus (vertical)
        cx = tr["dense_100_day"]["flops"]
        b.append(f'<line x1="{left}" y1="{sy(1e13):.1f}" x2="{left + pw}" y2="{sy(1e13):.1f}" stroke="{t["series"]}" stroke-width="1" opacity="0.55"/>')
        b.append(f'<line x1="{sx(cx):.1f}" y1="{top}" x2="{sx(cx):.1f}" y2="{top + ph}" stroke="{t["series"]}" stroke-width="1" opacity="0.55"/>')
        b.append(f'<text x="{left + 8}" y="{sy(1e13) - 7:.1f}" font-size="11" fill="{t["ink2"]}">Data limit: about 216T tokens supports about 10T parameters</text>')
        b.append(f'<text transform="translate({sx(cx) + 14:.1f},{top + ph - 8}) rotate(-90)" font-size="11" fill="{t["ink2"]}">Compute limit: 100 days of the full campus</text>')

        def point(row, color, strong):
            label, c, total, active, dx, dy, anchor = row
            x, y = sx(c), sy(total)
            if active:
                ya = sy(active)
                b.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ya:.1f}" stroke="{color}" stroke-width="2"/>')
                b.append(f'<circle cx="{x:.1f}" cy="{ya:.1f}" r="4" fill="{t["surface"]}" stroke="{color}" stroke-width="2"/>')
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 if strong else 5}" fill="{color}" stroke="{t["surface"]}" stroke-width="2"/>')
            weight = ' font-weight="600"' if strong else ""
            fill = t["ink"] if strong else t["ink2"]
            b.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" font-size="{12 if strong else 11}" fill="{fill}" text-anchor="{anchor}"{weight}>{esc(label)}</text>')
            if strong and active:
                note = f"{total / 1e12:.0f}T total, {active / 1e12:.1f}T active"
                b.append(f'<text x="{x + dx:.1f}" y="{y + dy + 15:.1f}" font-size="11" fill="{t["ink2"]}" text-anchor="{anchor}">{note}</text>')

        for row in published:
            point(row, t["context"], False)
        for row in plan:
            point(row, t["series"], True)

        # legend
        ly = 76
        b.append(f'<circle cx="{left + 6}" cy="{ly - 4}" r="5" fill="{t["series"]}"/>')
        b.append(f'<text x="{left + 18}" y="{ly}" font-size="11.5" fill="{t["ink2"]}">This plan</text>')
        b.append(f'<circle cx="{left + 96}" cy="{ly - 4}" r="5" fill="{t["context"]}"/>')
        b.append(f'<text x="{left + 108}" y="{ly}" font-size="11.5" fill="{t["ink2"]}">Published models</text>')
        b.append(f'<circle cx="{left + 228}" cy="{ly - 4}" r="4" fill="{t["surface"]}" stroke="{t["context"]}" stroke-width="2"/>')
        b.append(f'<text x="{left + 240}" y="{ly}" font-size="11.5" fill="{t["ink2"]}">Hollow marker: parameters active per token (mixture-of-experts)</text>')
        b.append(f'<line x1="{left}" y1="{ly + 14}" x2="{left + 14}" y2="{ly + 14}" stroke="{t["context"]}" stroke-width="2" stroke-linecap="round"/>')
        b.append(f'<text x="{left + 22}" y="{ly + 18}" font-size="11.5" fill="{t["ink2"]}">Compute-optimal line: about 20 training tokens per parameter (Hoffmann et al. 2022)</text>')

        svg = frame(w, h, t, "How many parameters the campus can train",
                    "A sparse model reaches the 10-trillion data limit inside the compute limit; a dense one stops near 6 trillion.",
                    "\n".join(b),
                    "Log-log chart of model parameters against training compute, with the compute-optimal line, "
                    "published models, and this plan's pilot, sparse flagship and dense 100-day optimum.")
        with open(os.path.join(OUT, f"parameters-vs-compute-{mode}.svg"), "w") as f:
            f.write(svg)


ZONES = {
    "light": dict(compute="#2a78d6", power="#eb6834", cooling="#1baf7a", neutral="#898781"),
    "dark": dict(compute="#3987e5", power="#d95926", cooling="#199e70", neutral="#898781"),
}


def site_plan(d: dict) -> None:
    """Schematic campus layout. A diagram, not a chart: every block is labeled directly."""
    w, h = 760, 548
    cl = d["cluster"]
    halls = 8
    hall_mw = 1000 / halls
    racks_per_hall = cl["gpu_racks"] // halls

    for mode, t in THEMES.items():
        z = ZONES[mode]
        b: list = []

        def block(x, y, bw, bh, color, lines, size=11.0, bold_first=True):
            b.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="4" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-width="1.2"/>')
            n = len(lines)
            y0 = y + bh / 2 - (n - 1) * 7 + 4
            for i, line in enumerate(lines):
                weight = ' font-weight="600"' if (i == 0 and bold_first) else ""
                fill = t["ink"] if i == 0 else t["ink2"]
                b.append(f'<text x="{x + bw / 2}" y="{y0 + i * 14:.1f}" font-size="{size}" fill="{fill}" text-anchor="middle"{weight}>{esc(line)}</text>')

        # site boundary (double line = perimeter fence)
        b.append(f'<rect x="24" y="72" width="712" height="412" rx="10" fill="none" stroke="{t["axis"]}" stroke-width="1"/>')
        b.append(f'<rect x="29" y="77" width="702" height="402" rx="7" fill="none" stroke="{t["axis"]}" stroke-width="1"/>')

        # power zone (west)
        block(42, 90, 150, 54, z["power"], ["Grid substation A", "345 kV, two feeders"])
        block(42, 154, 150, 150, z["power"], ["On-site generation", "1.3 GW gas turbines", "bridge and backup"])
        block(42, 314, 150, 66, z["power"], ["Battery storage", "400 MW / 800 MWh"])
        block(42, 390, 150, 54, z["power"], ["Grid substation B", "345 kV, two feeders"])
        for y in (117, 417):
            b.append(f'<line x1="6" y1="{y}" x2="42" y2="{y}" stroke="{z["power"]}" stroke-width="2"/>')
        b.append(f'<line x1="6" y1="229" x2="42" y2="229" stroke="{t["context"]}" stroke-width="2"/>')

        # data halls: two rows of four, cooling yards on the outer sides
        xs = [214, 320, 426, 532]
        for i, x in enumerate(xs):
            block(x, 90, 92, 22, z["cooling"], ["Dry coolers"], size=10, bold_first=False)
            block(x, 116, 92, 118, z["compute"], [f"Hall {i + 1}", f"{hall_mw:.0f} MW IT", f"{racks_per_hall} GPU racks"])
            block(x, 310, 92, 118, z["compute"], [f"Hall {i + 5}", f"{hall_mw:.0f} MW IT", f"{racks_per_hall} GPU racks"])
            block(x, 432, 92, 22, z["cooling"], ["Dry coolers"], size=10, bold_first=False)
        # utility spine
        b.append(f'<rect x="214" y="244" width="410" height="56" rx="4" fill="{t["neutral"] if "neutral" in t else z["neutral"]}" fill-opacity="0.10" stroke="{z["neutral"]}" stroke-width="1"/>')
        b.append(f'<text x="419" y="268" font-size="11" font-weight="600" fill="{t["ink"]}" text-anchor="middle">Utility spine</text>')
        b.append(f'<text x="419" y="284" font-size="11" fill="{t["ink2"]}" text-anchor="middle">Medium-voltage feeders, coolant headers, fiber trunks</text>')

        # network and operations (east)
        block(642, 90, 78, 62, z["neutral"], ["Network", "core A"], bold_first=False)
        block(642, 162, 78, 72, z["neutral"], ["Operations", "center and", "offices"], bold_first=False)
        block(642, 244, 78, 56, z["neutral"], ["Logistics", "and spares"], bold_first=False)
        block(642, 310, 78, 62, z["neutral"], ["Network", "core B"], bold_first=False)
        block(642, 382, 78, 62, z["neutral"], ["Gatehouse,", "security"], bold_first=False)
        for y in (121, 341):
            b.append(f'<line x1="720" y1="{y}" x2="754" y2="{y}" stroke="{z["neutral"]}" stroke-width="2"/>')

        # legend / key under the site
        ky = 510
        items = [(z["compute"], "Compute halls"), (z["cooling"], "Heat rejection"),
                 (z["power"], "Power"), (z["neutral"], "Network and operations")]
        x = 24
        for color, label in items:
            b.append(f'<rect x="{x}" y="{ky - 10}" width="12" height="12" rx="2" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-width="1.2"/>')
            b.append(f'<text x="{x + 18}" y="{ky}" font-size="11" fill="{t["ink2"]}">{esc(label)}</text>')
            x += 18 + len(label) * 6.2 + 22
        b.append(f'<text x="24" y="{ky + 20}" font-size="11" fill="{t["muted"]}">West side: two 345 kV lines and the gas pipeline (grey). East side: two separate fiber routes. Double outline: perimeter fence.</text>')

        svg = frame(w, h, t, "Campus site plan",
                    "Schematic, not to scale. About 4 square kilometers; eight halls give 1 GW of IT load.",
                    "\n".join(b),
                    "Schematic site plan: power plant, substations and batteries on the west side, eight data halls "
                    "with dry-cooler yards in the center, network cores and operations buildings on the east side.")
        with open(os.path.join(OUT, f"campus-site-plan-{mode}.svg"), "w") as f:
            f.write(svg)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    d = sizing.build()
    param_chart(d)
    site_plan(d)

    hbar("token-mix", "Pretraining token mix",
         f"Trillions of tokens by source. Total {d['data_mix']['total_t']:.0f} trillion.",
         [("Open web text, filtered", 60), ("Video frames (licensed)", 60),
          ("Two more passes over the best text and code", 34),
          ("Synthetic and self-generated", 30), ("Native audio", 10), ("Code", 6),
          ("Books, papers, patents, law", 6), ("Image-text pairs", 5),
          ("Licensed forums and news", 3), ("Transcribed speech", 2)],
         lambda v: f"{v:.0f}T", "Ranked bar chart of pretraining tokens by source.")

    co = d["cost"]
    short = {
        "GPU racks": "GPU racks",
        "Scale-out network, optics, cabling": "Network, optics, cabling",
        "Storage": "Storage",
        "CPU fleet (data processing, RL environments)": "CPU fleet",
        "Buildings, electrical, cooling": "Buildings, electrical, cooling",
        "On-site generation": "On-site generation",
        "Battery storage": "Battery storage",
        "Substations and grid interconnect": "Substations, grid interconnect",
        "Land and site works": "Land and site works",
    }
    hbar("capex", "Capital cost by line",
         f"Billions of US dollars. Total about ${co['capex_total_usd_b']:.0f} billion for the 1 GW campus.",
         [(short[k], v) for k, v in co["capex"].items()],
         lambda v: f"${v:.2f}B" if v < 1 else (f"${v:.1f}B" if v < 10 else f"${v:.0f}B"), "Ranked bar chart of capital cost by line item.",
         tick_fmt=lambda v: f"${v:.0f}B")

    tm = d["team"]
    hbar("headcount", "Headcount by function",
         f"Permanent staff at launch. Total about {tm['headcount']:,}.",
         [(n.split(" (")[0], h) for n, h, _ in tm["rows"]],
         lambda v: f"{v:.0f}", "Ranked bar chart of headcount by function.")
    print("wrote", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
