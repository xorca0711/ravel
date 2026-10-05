"""Generate the inert experimental-design schematics for A28, A29 and A30.

Allowed elements only (svg/title/desc/rect/line/ellipse/polygon/text/a), no
style attributes, no event handlers, no url() references, links pinned to a
repository blob at a fixed revision. Every figure labels itself a hypothesis
illustration and nothing on the page stands for a measured quantity.

Design: the figure is laid out as the experiment a reader would actually set
up, top to bottom.

  1. ARMS      the culture conditions or sample strata, drawn as dishes
  2. READOUTS  what is measured on every arm, with the unit stated
  3. DECISION  each outcome pattern and the conclusion it would license

Rival explanations are not a separate column; they are the alternative outcome
rows of the decision table, which is where a bench scientist meets them.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

FONT = "Segoe UI,Arial,sans-serif"
INK, MUTE, FAINT, RULE = "#33434D", "#6B7B85", "#9AA8B0", "#E4EAEE"
PANEL, ACCENT = "#FBFCFD", "#2E8B86"
PROP, RIVAL, NEUTRAL = "#4C86B0", "#C98A5B", "#92A1AA"
MEDIA = "#EAF1F5"
W, H = 1680, 1240


def esc(s):
    return escape(str(s))


def text(x, y, s, size=22, weight="400", fill=INK, anchor="start", spacing=None):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{sp}>{esc(s)}</text>')


def rect(x, y, w, h, fill="white", stroke="none", sw=1, rx=0):
    st = "" if stroke == "none" else f' stroke="{stroke}" stroke-width="{sw}"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>'


def line(x1, y1, x2, y2, colour, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" '
            f'stroke-width="{sw}"{d}/>')


def dot(cx, cy, r, fill, stroke=None, sw=1.6):
    stroke = stroke or fill
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def wrap(x, y, s, width, size=19, fill=INK, lead=26, weight="400"):
    words, line_, out, n = s.split(), "", [], 0
    for w in words:
        trial = (line_ + " " + w).strip()
        if len(trial) * size * 0.52 > width and line_:
            out.append(text(x, y + n * lead, line_, size, weight, fill)); n += 1; line_ = w
        else:
            line_ = trial
    if line_:
        out.append(text(x, y + n * lead, line_, size, weight, fill)); n += 1
    return "\n".join(out), y + n * lead


def dish(cx, cy, colour, n_cells=5):
    """Culture dish seen from above: rim, media, a few qualitative cells."""
    parts = [dot(cx, cy, 40, MEDIA, RULE, 1.6), dot(cx, cy, 32, "white", "none", 0)]
    offs = [(-13, -9), (11, -12), (16, 8), (-9, 12), (0, -1), (-21, 2), (22, -2)]
    for i in range(min(n_cells, len(offs))):
        dx, dy = offs[i]
        parts.append(dot(cx + dx, cy + dy, 5.2, colour, colour, 0))
    return "\n".join(parts)


def section(o, x, y, w, label):
    o.append(text(x, y, label, 14, "700", FAINT, spacing="2"))
    o.append(line(x, y + 10, x + w, y + 10, RULE, 1.2))


def build(qid, headline, premise, arms_title, arms, readouts, decisions, revision, page):
    link = (f"https://github.com/xorca0711/scRNA_seq/blob/{revision}/"
            f"docs/research_dossiers/{qid}.md")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">'
         f'<title id="title">{qid}</title>'
         f'<desc id="desc">Original hypothesis illustration of a proposed experimental design. '
         f'Dishes, markers and positions are qualitative and stand for conditions, not for '
         f'measured values. Read the full caption and sources.</desc>',
         rect(0, 0, W, H, "white")]
    L, RGT = 72, 1608
    o.append(text(L, 50, qid, 19, "700", ACCENT, spacing="1"))
    o.append(text(L + 46, 50, "PROPOSED EXPERIMENTAL DESIGN", 15, "600", FAINT, spacing="2"))
    o.append(text(RGT, 50, "HYPOTHESIS ILLUSTRATION \u00b7 NOT A RESULT", 14, "600", FAINT, "end",
                  spacing="1"))
    o.append(line(L, 66, RGT, 66, RULE, 1.4))
    o.append(text(L, 112, headline, 30, "600", INK))
    blk, y = wrap(L, 156, premise, RGT - L, 19, MUTE, 27)
    o.append(blk)

    y += 34
    section(o, L, y, RGT - L, arms_title)
    y += 52
    aw = (RGT - L) / len(arms)
    for i, a in enumerate(arms):
        cx = L + aw * i + aw / 2
        if i:
            o.append(line(L + aw * i, y - 6, L + aw * i, y + 190, RULE, 1.0))
        o.append(dish(cx, y + 56, a["colour"], a.get("n", 5)))
        o.append(text(cx, y + 16, a["tag"], 13, "700", a["colour"], "middle", spacing="1"))
        o.append(text(cx, y + 124, a["name"], 18, "600", INK, "middle"))
        sub, _ = wrap(cx - aw / 2 + 26, y + 150, a["sub"], aw - 52, 15, MUTE, 20)
        o.append(sub)
    y += 214

    section(o, L, y, RGT - L, "MEASURED ON EVERY ARM")
    y += 44
    rw = (RGT - L - 3 * 18) / 4
    for i, r in enumerate(readouts):
        x = L + i * (rw + 18)
        o.append(rect(x, y, rw, 112, PANEL, RULE, 1.2, 12))
        o.append(rect(x, y, 4, 112, r.get("colour", PROP), "none", 0, 0))
        o.append(text(x + 20, y + 32, r["head"], 17, "600", INK))
        blk2, _ = wrap(x + 20, y + 58, r["body"], rw - 40, 14.5, MUTE, 20)
        o.append(blk2)
    y += 150

    section(o, L, y, RGT - L, "WHAT EACH OUTCOME WOULD MEAN")
    y += 34
    cw1 = 600
    o.append(text(L + 20, y + 16, "IF THE READOUT SHOWS", 13, "700", FAINT, spacing="1"))
    o.append(text(L + cw1 + 32, y + 16, "THEN", 13, "700", FAINT, spacing="1"))
    y += 28
    for i, d in enumerate(decisions):
        rh = d.get("h", 52)
        if i % 2 == 0:
            o.append(rect(L, y, RGT - L, rh, PANEL, "none", 0, 8))
        o.append(rect(L, y + 9, 4, rh - 18, d.get("colour", PROP), "none", 0, 2))
        c1, _ = wrap(L + 20, y + 24, d["if"], cw1 - 30, 15, INK, 19)
        o.append(c1)
        c2, _ = wrap(L + cw1 + 32, y + 24, d["then"], RGT - L - cw1 - 52, 15, MUTE, 19)
        o.append(c2)
        y += rh

    fy = H - 92
    o.append(line(L, fy - 22, RGT, fy - 22, RULE, 1.2))
    o.append(text(L, fy, "Dishes and markers stand for conditions and cells, not for measured "
                         "values; no count, size or position here is data.", 14.5, "400", MUTE))
    o.append(text(L, fy + 22, "The design is proposed and unexecuted. Nothing here certifies a "
                              "mechanism, a protein measurement or laboratory access.",
                  14.5, "400", MUTE))
    o.append(f'<a href="{link}"><rect x="{L}" y="{fy + 34}" width="330" height="24" '
             f'fill="transparent"/></a>')
    o.append(text(L, fy + 52, f"Dossier: docs/research_dossiers/{qid}.md", 14.5, "400", ACCENT))
    o.append(text(RGT, fy, "v1 qualitative hypothesis illustration", 14, "400", FAINT, "end"))
    o.append(text(RGT, fy + 22, f"Source: branch revision {revision[:7]}", 14, "400", FAINT, "end"))
    o.append(text(RGT, fy + 52, page, 14, "400", FAINT, "end"))
    o.append("</svg>")
    return "\n".join(o) + "\n"


REG = "#5B9B86"
EFF = "#C97F63"


def main(root: Path, revision: str) -> int:
    specs = {}

    specs["A28"] = dict(
        dirname="A28_th17_arm_asymmetry",
        headline="Do the two arms of the pathogenicity score move one at a time, or together?",
        premise=("The score is pro-inflammatory minus pro-regulatory, so it can rise either way. "
                 "In the deposited data each perturbation moved one arm only \u2014 and a different "
                 "arm each time. Stain both arms in the same cell under both perturbations and the "
                 "question is settled on the joint distribution, which no RNA summary can give."),
        arms_title="CULTURE ARMS \u00b7 NAIVE CD4 T CELLS, MOUSE AS UNIT",
        arms=[
            dict(tag="ARM 1", name="Th17n, 25 mM glucose", colour=NEUTRAL, n=5,
                 sub="Reference condition. TGF-\u03b2 + IL-6."),
            dict(tag="ARM 2", name="Th17n, 1 mM glucose", colour=PROP, n=5,
                 sub="Nutrient restriction. The perturbation that moved the regulatory arm."),
            dict(tag="ARM 3", name="Th17p cytokines", colour=PROP, n=6,
                 sub="IL-1\u03b2 + IL-6 + IL-23. The perturbation that moved the effector arm."),
            dict(tag="ARM 4", name="Arm 2 + division matched", colour=RIVAL, n=4,
                 sub="Growth held constant, so a division effect cannot masquerade as competence."),
        ],
        readouts=[
            dict(head="Foxp3 + CTLA4 protein", colour=REG,
                 body="Intracellular stain, per cell. The regulatory arm, measured as protein "
                      "rather than as a module score."),
            dict(head="IL-17A + IL-17F protein", colour=EFF,
                 body="Same cells, same stain panel. The effector arm. Both arms in one cell is "
                      "the whole point."),
            dict(head="Division tracker", colour=RIVAL,
                 body="Dye dilution. Low glucose slows division, and cycle phase was regressed out "
                      "of the published latent space."),
            dict(head="Joint distribution", colour=PROP,
                 body="The endpoint is the 2-D distribution per mouse, not two marginal means. "
                      "4 arms \u00d7 \u22653 mice."),
        ],
        decisions=[
            dict(colour=PROP, h=58,
                 **{"if": "Arm 2: Foxp3 and CTLA4 fall, IL-17 unchanged. Arm 3: IL-17 rises, "
                          "Foxp3 and CTLA4 unchanged.",
                    "then": "The two competences are separately regulated. A one-sided score move "
                            "is a real biological statement, and the two perturbations must be "
                            "reported as different cell states."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "Both arms move reciprocally in both arms 2 and 3.",
                    "then": "One latent axis. The one-sided move was a property of gene lists built "
                            "from opposing polarisations; report the score as a single axis."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "The cells losing Foxp3 are not the cells gaining IL-17.",
                    "then": "Composition, not within-cell transition \u2014 the same reading the "
                            "glucose decomposition reached, and the score is tracking a mixture."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "Arm 4 abolishes the effect seen in arm 2.",
                    "then": "A division confound. Neither arm claim survives, and any future "
                            "comparison must be growth-matched."}),
            dict(colour=NEUTRAL, h=52,
                 **{"if": "Mouse-to-mouse variation exceeds the arm differences.",
                    "then": "Inconclusive at this precision. Report the achieved precision; do not "
                            "add conditions to recover a sign."}),
        ],
        page="01 / 03")

    specs["A29"] = dict(
        dirname="A29_pgam_effector_mechanism",
        headline="Which of three mechanisms raises Th17 effector output when PGAM is restricted?",
        premise=("PGAM sits two steps upstream of phosphoenolpyruvate, which is a published "
                 "inhibitor of the Th17 programme through JunB. Blocking PGAM should lower PEP and "
                 "release that brake \u2014 but the source reports PEP label unchanged, and proposes "
                 "stress instead. One culture experiment separates PEP, demand relief and stress."),
        arms_title="CULTURE ARMS \u00b7 TH17N POLARISATION, MOUSE AS UNIT",
        arms=[
            dict(tag="ARM 1", name="Vehicle", colour=NEUTRAL, n=5,
                 sub="Solvent-matched reference."),
            dict(tag="ARM 2", name="PGAM restricted", colour=PROP, n=6,
                 sub="EGCG, plus titrated Pgam1 knockdown as the specificity control."),
            dict(tag="ARM 3", name="PGAM restricted + PEP", colour=PROP, n=5,
                 sub="PEP supplementation. The rescue arm that isolates the metabolite route."),
            dict(tag="ARM 4", name="Growth slowed, PGAM intact", colour=RIVAL, n=4,
                 sub="mTORC1 inhibition or serine restriction. Demand relief without PGAM."),
        ],
        readouts=[
            dict(head="PEP, 2PG, 3PG pools", colour=PROP,
                 body="Targeted metabolomics, absolute pools. A 15-minute label ratio cannot tell a "
                      "steady pool from a falling one."),
            dict(head="IL-17A protein", colour=EFF,
                 body="Per cell, so output is not inferred from transcript abundance or from a "
                      "bulk library average."),
            dict(head="p-eIF2\u03b1 and ATF4 protein", colour=RIVAL,
                 body="The stress route at the level it is actually set, rather than through its "
                      "downstream target transcripts."),
            dict(head="Division + RNA content", colour=RIVAL,
                 body="Dye dilution and per-cell RNA or ribosome content, so dilution and "
                      "compositional effects are measured, not argued."),
        ],
        decisions=[
            dict(colour=PROP, h=58,
                 **{"if": "Arm 2 lowers the PEP pool, and arm 3 abolishes the IL-17 increase.",
                    "then": "The metabolite route. PGAM restriction acts by releasing PEP inhibition "
                            "of JunB/BATF/IRF4; the stress premise is unnecessary and should be "
                            "withdrawn as the stated mechanism."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "The PEP pool is genuinely unchanged in arm 2.",
                    "then": "The metabolite route is eliminated on the authors' own measurement "
                            "extended to pools. Demand relief and the serine branch remain."}),
            dict(colour=PROP, h=52,
                 **{"if": "Arm 4 reproduces the IL-17 increase with p-eIF2\u03b1 flat.",
                    "then": "Demand relief. Effector output tracks growth reduction however it is "
                            "produced, and PGAM is not special."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "p-eIF2\u03b1 and ATF4 protein rise in arm 2 despite falling target transcripts.",
                    "then": "Transcript modules mis-read the response. The stress premise survives "
                            "at protein level and the E3 conclusion is transcript-limited."}),
            dict(colour=NEUTRAL, h=52,
                 **{"if": "The IL-17 increase disappears once per-cell RNA content is accounted for.",
                    "then": "Compositional. The measured effector gain does not support increased "
                            "output per cell."}),
        ],
        page="02 / 03")

    specs["A30"] = dict(
        dirname="A30_csf_compartment_effector_state",
        headline="Is the CSF effector elevation a compartment state, or just more activation?",
        premise=("In ten donors the pro-inflammatory arm is higher in CSF than in that donor's own "
                 "blood, and the regulatory arm is not. But activation is higher in CSF too. "
                 "Stratifying on activation defined from genes outside both modules is the "
                 "comparison that separates them, and it runs on data already in hand."),
        arms_title="SAMPLE STRATA \u00b7 PAIRED WITHIN DONOR, DONOR AS UNIT (n = 10)",
        arms=[
            dict(tag="STRATUM 1", name="Blood, low activation", colour=NEUTRAL, n=4,
                 sub="Reference. Activation score from genes disjoint from both modules."),
            dict(tag="STRATUM 2", name="CSF, low activation", colour=PROP, n=5,
                 sub="The decisive cell. Compartment differs, activation matched."),
            dict(tag="STRATUM 3", name="Blood, high activation", colour=NEUTRAL, n=5,
                 sub="Activation differs, compartment held."),
            dict(tag="STRATUM 4", name="CSF, high activation", colour=RIVAL, n=6,
                 sub="Where compartment and activation coincide, as in the unstratified contrast."),
        ],
        readouts=[
            dict(head="Pro-inflammatory arm", colour=EFF,
                 body="Donor-level mean score against a matched-size random-set null, 1,000 draws, "
                      "reported per stratum."),
            dict(head="Pro-regulatory arm", colour=REG,
                 body="Always reported alongside on the same null, whichever way the "
                      "pro-inflammatory arm falls."),
            dict(head="Composition vs within-state", colour=RIVAL,
                 body="The paired difference split into a mixture term and a within-state term, as "
                      "done for the mouse glucose effect."),
            dict(head="Not available here", colour=NEUTRAL,
                 body="Shared-clone TCR comparison across compartments. Without it, residency "
                      "cannot be excluded by any analysis."),
        ],
        decisions=[
            dict(colour=PROP, h=58,
                 **{"if": "Stratum 2 still exceeds stratum 1 on the pro-inflammatory arm, with the "
                          "pro-regulatory arm flat.",
                    "then": "A compartment-associated effector state not reducible to activation. "
                            "The arm asymmetry becomes a reportable contrast against the mouse "
                            "result, still short of causation."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "The elevation collapses once activation is matched.",
                    "then": "Activation explains it. The result is downgraded to an activation "
                            "correlate and the arm-asymmetry claim is withdrawn."}),
            dict(colour=RIVAL, h=52,
                 **{"if": "The composition term carries the paired difference.",
                    "then": "A mixture shift, not a within-cell state \u2014 consistent with the "
                            "described CSF-enriched Th17-lineage subset."}),
            dict(colour=NEUTRAL, h=52,
                 **{"if": "Ten donors cannot separate the strata.",
                    "then": "Precision-limited and reported as such. A null here is never evidence "
                            "of absence; do not relax the stratification to recover significance."}),
        ],
        page="03 / 03")

    written = []
    for qid, s in specs.items():
        svg = build(qid, s["headline"], s["premise"], s["arms_title"], s["arms"],
                    s["readouts"], s["decisions"], revision, s["page"])
        out = root / "RQ_Specified" / s["dirname"] / "schematics" / "hypothesis_v1.svg"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(svg, encoding="utf-8", newline="\n")
        written.append(str(out.relative_to(root)))
    print("\n".join(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), sys.argv[2]))
