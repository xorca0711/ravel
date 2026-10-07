"""Author the two qualitative documentation SVGs; no measured data or model fits."""
from pathlib import Path
from html import escape
import textwrap

ROOT = Path(__file__).resolve().parents[3]
TEAL, INK, MUTED, RULE = '#247F7B', '#283E49', '#566A74', '#DDE7EB'


class Plate:
    def __init__(self, width, height, title, desc):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                      f'<title>{escape(title)}</title><desc>{escape(desc)}</desc>',
                      f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>']

    def box(self, x, y, w, h, fill='#F5F9FA', stroke=RULE):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def text(self, x, y, text, size=24, color=INK, weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>')

    def para(self, x, y, text, width=60, size=23, gap=31, color=INK):
        for i, line in enumerate(textwrap.wrap(text, width=width)):
            self.text(x, y+i*gap, line, size, color)

    def arrow(self, x1, y1, x2, y2, color=TEAL):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"/>')
        if y1 == y2:
            d = 1 if x2 > x1 else -1
            points=f'{x2},{y2} {x2-12*d},{y2-7} {x2-12*d},{y2+7}'
        else:
            d = 1 if y2 > y1 else -1
            points=f'{x2},{y2} {x2-7},{y2-12*d} {x2+7},{y2-12*d}'
        self.parts.append(f'<polygon points="{points}" fill="{color}"/>')

    def cell(self, x, y, color):
        self.parts.append(f'<ellipse cx="{x}" cy="{y}" rx="13" ry="13" fill="{color}"/>')
        self.parts.append(f'<ellipse cx="{x+2}" cy="{y-1}" rx="5" ry="6" fill="#FFFFFF" fill-opacity="0.6"/>')

    def save(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(self.parts+['</svg>'])+'\n', encoding='utf-8')


def a30():
    p=Plate(1680,1330,'A30 | Paired CSF–blood inflammatory RNA programmes',
            'Hypothesis illustration. Qualitative proposed comparison, alternatives and conditional extensions; no measured cell counts or experimental results.')
    p.text(60,60,'A30  /  HYPOTHESIS ILLUSTRATION',22,TEAL,700)
    p.text(60,112,'Does the CSF-associated RNA difference persist within comparable T-cell states?',32,INK,600)
    p.text(60,150,'Paired human samples • donor is the biological unit • association before mechanism',23,MUTED)
    p.box(60,178,1560,145,'#EAF5F3','#C0DDD7')
    p.text(85,215,'WORKING HYPOTHESIS',20,TEAL,700)
    p.para(85,252,'In paired CSF and blood, the inflammatory RNA programme remains higher in CSF within comparable CD4 T-cell states after accounting for measured activation and composition. Regulatory-associated RNA is evaluated separately, without presuming unchanged regulatory function.',width=126,size=23,gap=30)

    p.text(60,366,'01  DEFINE THE PAIRED COMPARISON',22,TEAL,700)
    p.box(60,386,975,265)
    p.text(86,423,'Same donor • paired sampling • putative CD4 identity needs qualification',23,INK,600)
    for x,label in [(180,'Blood'),(700,'CSF')]:
        p.box(x,447,190,120,'#FFFFFF')
        for dx,dy,c in [(38,35,TEAL),(85,34,'#A7628A'),(138,35,'#6D8DA3'),(52,80,'#6D8DA3'),(110,78,TEAL)]:
            p.cell(x+dx,447+dy,c)
        p.text(x+60,598,label,25,INK,600)
    p.arrow(386,505,680,505)
    p.text(423,478,'paired difference',21,TEAL)
    p.text(410,548,'CSF minus blood',22,INK)
    p.text(88,631,'Cell symbols are qualitative; colour denotes possible states, not observed counts.',20,MUTED)
    p.box(1060,386,560,265,'#FFFFFF')
    p.text(1085,423,'MEASURED ENDPOINT',21,TEAL,700)
    p.para(1085,461,'Inflammatory RNA programme, within comparable states and measured activation.',width=40,size=24,gap=32)
    p.para(1085,568,'Regulatory RNA is separate. Neither score measures secretion or suppressive function.',width=42,size=23,gap=31)

    p.text(60,700,'02  INTERPRET ALTERNATIVES THAT CAN COEXIST',22,TEAL,700)
    cards=[('Residual activation','Gene-disjoint panels and broad tertiles do not guarantee balance. A residual RNA difference is not activation independence.'),
           ('Trafficking and composition','Different subsets or clones can enter CSF. Missing state overlap limits the decomposition; shared TCR does not prove residency.'),
           ('Measurement validity','Check lineage, depth, null-gene background and donor support. Non-significance is not equivalence or unchanged function.')]
    for i,(title,body) in enumerate(cards):
        x=60+i*530;p.box(x,722,500,193);p.text(x+24,761,title,26,INK,600);p.para(x+24,802,body,width=40,size=23,gap=30)

    p.text(60,963,'03  EXTEND ONLY AS THE QUESTION REQUIRES',22,TEAL,700)
    cards=[('First: qualify the RNA contrast','Barcode/QC trail, activation balance, null calibration and common-state support. A new numerical pass needs a versioned amendment.'),
           ('Conditional: phenotype + clones','Paired protein/TCR can resolve phenotype and clonal overlap. Functional claims need a suitable functional assay, not markers alone.'),
           ('Conditional: perturbation','A defined intervention versus control can test an effect. Add rescue or factorial arms only for the intended stronger inference.')]
    for i,(title,body) in enumerate(cards):
        x=60+i*530;p.box(x,985,500,200,'#EAF5F3','#C0DDD7');p.text(x+24,1024,title,24,INK,600);p.para(x+24,1065,body,width=40,size=23,gap=30)
    p.para(60,1233,'Persistence → residual association. Attenuation → measured features contribute. Imprecision → unresolved.',width=135,size=23)
    p.text(60,1282,'v2 • 7 October 2026 • Proposed, not scientifically accepted • Assay, timing and precision remain to be qualified',21,MUTED)
    p.save(ROOT/'RQ_Specified/A30_csf_compartment_effector_state/schematics/hypothesis_v2.svg')


def workflow():
    p=Plate(1480,1660,'Agent decision workflow',
            'Declared repository workflow. Design follows purpose; alternative explanations do not mandate experimental arms. Instructions, runtime checks and human judgment have different roles.')
    p.text(60,65,'RAVEL  /  AGENT DECISION WORKFLOW',23,TEAL,700)
    p.text(60,113,'Choose the design for the question and the intended inference',33,INK,600)
    p.text(60,153,'Proposed clarification • 7 October 2026 • No validator or frozen evidence changed',23,MUTED)
    for y,title,body in [(193,'1  Establish scope and current state','User request → Git/base/working tree → registry → current result and amendment'),
                         (309,'2  Classify the purpose','Reading/docs • metadata • description/exploration • prediction • confirmation')]:
        p.box(60,y,1360,90);p.text(84,y+34,title,25,INK,600);p.text(84,y+68,body,23,MUTED)
    p.arrow(740,283,740,309)
    p.arrow(380,399,380,440);p.arrow(1045,399,1045,440)
    p.box(60,440,600,245,'#EAF5F3','#C0DDD7');p.text(85,480,'READING / DOCUMENTATION',23,TEAL,700)
    p.para(85,525,'Inspect sources, correct current wording, preserve historical records and align the diagram.',width=44,size=25,gap=34)
    p.para(85,640,'No biological rerun solely for a wording fix.',width=43,size=23,gap=31)
    p.box(695,440,725,245);p.text(720,480,'METADATA / NUMERICAL WORK',23,TEAL,700)
    p.para(720,525,'Specify purpose, unit, endpoint, comparator or estimand, outcome exposure and interpretation limit.',width=49,size=25,gap=34)
    p.para(720,640,'Add a prediction for hypothesis-driven work.',width=49,size=23,gap=31)
    p.arrow(1045,685,1045,727)
    p.box(695,727,725,157,'#FFFFFF');p.text(720,767,'3  Assess a relevant alternative or validity threat',24,INK,600)
    p.para(720,809,'Mutant versus control may suffice. Additional arms must earn their place through the intended claim.',width=51,size=24,gap=33)
    p.arrow(1045,884,1045,924)
    p.box(695,924,725,171,'#EAF5F3','#C0DDD7');p.text(720,965,'4  Qualify → freeze → execute → verify',25,TEAL,700)
    p.para(720,1007,'Resolve decision-relevant gaps; register/freeze a contract, preflight inputs, use the runner, then verify receipts plus independent arithmetic/QC.',width=51,size=24,gap=32)
    p.box(60,727,600,368,'#FFFFFF');p.text(85,767,'IF ESSENTIAL EVIDENCE IS MISSING',22,TEAL,700)
    p.para(85,814,'Hold only the dependent numerical step. Record the unknown and continue independent reading, metadata recovery or design work.',width=41,size=25,gap=35)
    p.para(85,1000,'Do not invent a mechanism, sample size or human approval to complete a template.',width=43,size=24,gap=33)
    p.arrow(695,947,660,947)
    p.arrow(1045,1095,1045,1133);p.arrow(360,1095,360,1247)
    p.box(695,1133,725,90);p.text(720,1168,'5  Interpret the actual endpoint',25,INK,600)
    p.text(720,1202,'Effects, uncertainty, mixed outcomes and limits',24,MUTED)
    p.arrow(1045,1223,1045,1247)
    p.parts.append('<line x1="60" y1="560" x2="30" y2="560" stroke="#247F7B" stroke-width="3"/>')
    p.parts.append('<line x1="30" y1="560" x2="30" y2="1275" stroke="#247F7B" stroke-width="3"/>')
    p.arrow(30,1275,60,1275)
    p.box(60,1247,1360,120);p.text(85,1286,'6  Deliver reviewable work',27,INK,600)
    p.para(85,1318,'Current docs + PROGRESS + required checks against the current base. Preserve unfavorable results and earlier versions.',width=105,size=24,gap=32)
    p.arrow(740,1367,740,1395)
    p.box(60,1395,1360,183,'#EAF5F3','#C0DDD7');p.text(85,1436,'THREE DIFFERENT AUTHORITIES',23,TEAL,700)
    p.text(85,1478,'Instructions guide an agent. Runtime/CI checks test declared structure and provenance.',25,INK)
    p.text(85,1519,'Scientific acceptance and protected policy decisions require their recorded authority.',25,INK)
    p.text(85,1554,'A successful run, p-value or schematic does not establish a mechanism or human approval.',23,MUTED)
    p.text(60,1621,'This is a documented workflow, not an OS sandbox or a claim to expose private model reasoning.',22,MUTED)
    p.save(ROOT/'docs/schematics/agent_decision_workflow_v1.svg')


if __name__ == '__main__':
    a30()
    workflow()
