#!/usr/bin/env python3
"""Build the Compaz Finance concept site: English at /, Simplified Chinese at /sc/.
Run: python3 _build/pages.py  (then python3 _build/fonts.py after Chinese text changes)"""
import os, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "7"  # cache-bust; bump on every CSS/JS change
OFFICIAL = "https://www.compazfinance.co.uk/"
PHONE_TEL = "+447775330483"
PHONE_SHOW = "07775 330483"
EMAIL = "info@compazfinance.co.uk"

LANG = "en"
def L(en, sc):
    return en if LANG == "en" else sc

PAGES = ["index", "services", "about", "contact", "privacy", "404"]
import re

def href(page, lang=None):
    """Link from the current language folder to `page` in `lang`."""
    lang = lang or LANG
    up = "" if LANG == "en" else "../"
    folder = "" if lang == "en" else "sc/"
    name = "" if page == "index" else page + ".html"
    return f"{up}{folder}{name}" or "./"

def asset(p):
    return ("" if LANG == "en" else "../") + "assets/" + p

# ---------------------------------------------------------------- shared
def head(page, title, desc):
    alt_en = f"https://uxcircles.github.io/compazfinance/{'' if page=='index' else page+'.html'}"
    alt_sc = f"https://uxcircles.github.io/compazfinance/sc/{'' if page=='index' else page+'.html'}"
    return f"""<!doctype html>
<html lang="{L('en-GB','zh-Hans')}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="alternate" hreflang="en-GB" href="{alt_en}">
<link rel="alternate" hreflang="zh-Hans" href="{alt_sc}">
<link rel="icon" href="{asset('img/compass.svg')}" type="image/svg+xml">
<link rel="preload" href="{asset('fonts/alegreya.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset('fonts/dmmono-500.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset('site.css')}?v={V}">
<meta name="theme-color" content="#17150f">
</head>
<body>
<a class="skip" href="#main">{L('Skip to content','跳到正文')}</a>
<div class="concept" role="note"><div class="wrap">
<p><span class="tag">{L('Concept','概念')}</span><span class="concept-long">{L('Redesign concept. Not the','网站改版概念，并非')} <a href="{OFFICIAL}">{L('official Compaz Finance website','Compaz Finance 官方网站')}</a>{L('.','。')}</span></p>
<a class="by" href="https://ux-circles.com/professionals"><span class="concept-by">{L('Designed by ','设计：')}</span><strong>UX CIRCLES</strong> ↗</a>
</div></div>
"""

def header(page):
    def nav(p, label):
        cur = ' aria-current="page"' if p == page else ""
        return f'<a href="{href(p)}"{cur}>{label}</a>'
    other = "sc" if LANG == "en" else "en"
    target = page if page != "404" else "index"
    return f"""<header class="site-head"><div class="wrap">
<a class="brand" href="{href('index')}" aria-label="Compaz Finance, {L('home','首页')}"><img src="{asset('img/logo.svg')}" alt="Compaz Finance" width="146" height="34"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">{L('Menu','菜单')}</button>
<nav class="nav" id="nav" aria-label="{L('Main','主菜单')}">
{nav('services', L('Mortgages & protection','房贷与保障'))}
{nav('about', L('About Lily','关于 Lily'))}
{nav('contact', L('Contact','联系'))}
<a class="lang" href="{href(target, other)}" lang="{L('zh-Hans','en')}" hreflang="{L('zh-Hans','en')}">{L('简体中文','English')}</a>
<a class="btn btn-ink head-call" href="tel:{PHONE_TEL}">{PHONE_SHOW}</a>
</nav>
</div></header>
<main id="main">
"""

def footer():
    other = "sc" if LANG == "en" else "en"
    return f"""</main>
<footer class="foot"><div class="wrap">
<div class="foot-top">
<div>
<img src="{asset('img/logo-white.svg')}" alt="Compaz Finance" width="146" height="34">
<p>{L('Mortgage and protection broker, founded in 2020 by Lily Liu. Advice in English and Mandarin.','房贷与保障经纪公司，由 Lily Liu 于2020年创立。可用英语或普通话咨询。')}</p>
</div>
<div>
<h2>{L('Talk to us','联系我们')}</h2>
<ul>
<li><a href="tel:{PHONE_TEL}">{PHONE_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>37 Hillcrest Road, Orpington, BR6 9AN</li>
</ul>
</div>
<div>
<h2>{L('Pages','页面')}</h2>
<ul>
<li><a href="{href('services')}">{L('Mortgages & protection','房贷与保障')}</a></li>
<li><a href="{href('about')}">{L('About Lily','关于 Lily')}</a></li>
<li><a href="{href('contact')}">{L('Contact','联系')}</a></li>
<li><a href="{href('privacy')}">{L('Privacy','隐私')}</a></li>
<li><a href="{href('index', other)}" lang="{L('zh-Hans','en')}">{L('简体中文','English')}</a></li>
</ul>
</div>
</div>
<div class="reg">
<p class="repo">{L('Your home may be repossessed if you do not keep up repayments on your mortgage.','如果您未能按时偿还房贷，您的房屋可能会被收回。')}</p>
<p>{L('Compaz Finance Ltd is authorised and regulated by the Financial Conduct Authority and is entered on the <a href="https://register.fca.org.uk/">Financial Services Register</a> under reference 939072. The Financial Conduct Authority does not regulate most forms of bridging loans.',
'Compaz Finance Ltd 获英国金融行为监管局（FCA）授权并受其监管，<a href="https://register.fca.org.uk/">金融服务登记册</a>编号 939072。FCA 不监管大部分过桥贷款。')}</p>
<p>{L('Financial protection policies typically have no cash-in value at any time and cover will cease at the end of the term. If premiums stop, cover will lapse.','保障类保单通常在任何时候都没有现金价值，保障在期满时终止。若停止缴纳保费，保障将失效。')}</p>
<p>{L(f'To make a complaint, email <a href="mailto:{EMAIL}">{EMAIL}</a>. A summary of our complaints procedure is available on request. If we cannot settle your complaint, you may be entitled to refer it to the <a href="https://www.financial-ombudsman.org.uk">Financial Ombudsman Service</a> (0800 023 4567).',
f'如需投诉，请发电邮至 <a href="mailto:{EMAIL}">{EMAIL}</a>，我们可按要求提供投诉处理程序摘要。如投诉未能解决，您可能有权转交<a href="https://www.financial-ombudsman.org.uk">金融申诉专员服务机构</a>（0800 023 4567）。')}</p>
<p>{L('The guidance on this website is subject to the UK regulatory regime and is aimed at consumers based in the UK.','本网站内容受英国监管制度约束，面向居住在英国的消费者。')}
Compaz Finance Ltd · {L('Registered in England & Wales','英格兰及威尔士注册')} 12961319 · {L('Registered office','注册地址')}: 71-75 Shelton Street, London WC2H 9JQ</p>
<p class="concept-line">{L('Unofficial redesign concept by','非官方网站改版概念，设计：')} <a href="https://ux-circles.com/professionals">UX CIRCLES</a> · © 2026</p>
</div>
</div></footer>
<nav class="mbar" aria-label="{L('Quick actions','快捷操作')}">
<a href="tel:{PHONE_TEL}">{L('Call','致电')}</a>
<a href="mailto:{EMAIL}">{L('Email','电邮')}</a>
<a class="go" href="{href('contact')}">{L('Ask Lily','咨询 Lily')}</a>
</nav>
<script src="{asset('app.js')}?v={V}" defer></script>
</body></html>
"""

# ---------------------------------------------------------------- dial
def dial():
    ticks = []
    for d in range(0, 360, 10):
        long = d % 90 == 0
        r1 = 82 if long else 88
        ticks.append(f'<line x1="0" y1="-{r1}" x2="0" y2="-94" transform="rotate({d})" stroke="currentColor" stroke-width="{1.6 if long else .8}"/>')
    labels = "".join(
        f'<text data-deg="{d}" x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle">{d:03d}</text>'
        for d, x, y in [(0, 0, -70), (90, 70, 0), (180, 0, 70), (270, -70, 0)])
    return f"""<svg class="dial" viewBox="-100 -100 200 200" aria-hidden="true">
<circle r="96" fill="none" stroke="currentColor" stroke-width="1"/>
<circle r="58" fill="none" stroke="currentColor" stroke-width=".6" stroke-dasharray="2 3"/>
{''.join(ticks)}{labels}
<g class="needle" id="needle">
<path d="M0,-80 L7,0 L0,12 L-7,0 Z" fill="#f7931e"/>
<path d="M0,-80 L0,12 L-7,0 Z" fill="#c26e08"/>
</g>
<circle r="5" fill="#17150f" stroke="#f7931e" stroke-width="2"/>
</svg>"""

def field(id_, label, val, pre="", suf="", step="any", mx=None):
    return f"""<div class="field"><label for="{id_}">{label}</label><div class="in">{f'<span>{pre}</span>' if pre else ''}<input id="{id_}" type="number" inputmode="decimal" min="0" step="{step}" value="{val}"{f' max="{mx}"' if mx else ''}>{f'<span>{suf}</span>' if suf else ''}</div></div>"""

BEARINGS = [
    ("buy", 0, ("First home or moving", "首套房或换房")),
    ("remo", 90, ("Remortgage", "转贷 Remortgage")),
    ("btl", 180, ("Buy-to-let", "买房出租 BTL")),
    ("bridge", 270, ("Bridging loan", "过桥贷款")),
]

def tool():
    btns = "".join(
        f'<li><button type="button" data-b="{k}" data-deg="{d}" aria-pressed="{"true" if k=="buy" else "false"}"><span class="deg">{d:03d}°</span>{L(*n)}</button></li>'
        for k, d, n in BEARINGS)
    yrs = L("yrs", "年")
    mo = L("months", "个月")
    forms = f"""
<fieldset data-panel="buy">
<legend>{L('Buying a home','买房自住')}</legend>
<p class="lead">{L('Monthly repayment and Stamp Duty in England, from the price and your deposit.','根据房价和首付，估算每月还款及英格兰印花税。')}</p>
{field('b-price', L('Property price','房价'), 350000, '£', step=1000)}
{field('b-dep', L('Deposit','首付'), 35000, '£', step=1000)}
{field('b-rate', L('Interest rate','利率'), 4.5, '', '%', step=0.05)}
{field('b-term', L('Term','年期'), 30, '', yrs, step=1, mx=40)}
<label class="check"><input type="checkbox" id="b-ftb" checked> {L('First-time buyer (everyone buying has never owned a home)','首次购房（所有共同买家都从未拥有过房产）')}</label>
</fieldset>
<fieldset data-panel="remo" hidden>
<legend>{L('Remortgaging','转贷 Remortgage')}</legend>
<p class="lead">{L('What a different rate would do to your monthly payment, before any fees.','比较新旧利率下的每月还款（未计入任何费用）。')}</p>
{field('r-bal', L('Mortgage left to pay','剩余贷款'), 220000, '£', step=1000)}
{field('r-term', L('Years left','剩余年期'), 22, '', yrs, step=1, mx=40)}
{field('r-now', L('Rate you would move to without a new deal','不换新方案时的利率'), 7.5, '', '%', step=0.05)}
{field('r-new', L('New rate','新利率'), 4.3, '', '%', step=0.05)}
</fieldset>
<fieldset data-panel="btl" hidden>
<legend>{L('Buy-to-let','买房出租')}</legend>
<p class="lead">{L('Interest-only cost against the rent, and Stamp Duty with the additional-property surcharge.','只付利息的月供与租金对比，以及含额外房产附加税的印花税。')}</p>
{field('l-price', L('Property price','房价'), 280000, '£', step=1000)}
{field('l-dep', L('Deposit','首付'), 70000, '£', step=1000)}
{field('l-rate', L('Interest rate','利率'), 5.2, '', '%', step=0.05)}
{field('l-rent', L('Monthly rent','月租'), 1450, '£', step=25)}
<label class="check"><input type="checkbox" id="l-nr"> {L('Buyer not resident in the UK (2% surcharge)','买家非英国居民（另加2%）')}</label>
</fieldset>
<fieldset data-panel="bridge" hidden>
<legend>{L('Bridging loan','过桥贷款')}</legend>
<p class="lead">{L('Buying before you sell: interest rolled up over the term, plus the arrangement fee.','先买后卖：按期累计的利息，加上安排费。')}</p>
{field('g-loan', L('Amount to borrow','借款金额'), 250000, '£', step=1000)}
{field('g-rate', L('Monthly rate','月利率'), 0.85, '', L('% a month','%/月'), step=0.01)}
{field('g-months', L('How long','借款期'), 9, '', mo, step=1, mx=24)}
{field('g-fee', L('Arrangement fee','安排费'), 2, '', '%', step=0.1)}
</fieldset>"""

    def out(k, big_label, unit, rows, cta):
        lis = "".join(f'<li><span>{lab}</span><b id="{k}-o{i}">–</b></li>' for i, lab in enumerate(rows))
        return f"""<div data-panel="{k}"{'' if k=='buy' else ' hidden'}>
<p class="out-label">{big_label}</p>
<p class="out-big" aria-live="polite"><span id="{k}-big">–</span> <small>{unit}</small></p>
<ul class="out-rows">{lis}</ul>
</div>"""
    per_m = L("a month", "每月")
    outs = (
        out("buy", L("Estimated repayment", "估算月供"), per_m,
            [L("Mortgage", "贷款额"), L("Loan to value", "贷款成数 LTV"), L("Stamp Duty (England)", "印花税（英格兰）")], "") +
        out("remo", L("You could pay less by", "每月可少付"), per_m,
            [L("Now", "目前"), L("On the new rate", "新利率"), L("Over a year", "一年合计")], "") +
        out("btl", L("Interest-only payment", "只付利息月供"), per_m,
            [L("Rent covers interest", "租金覆盖利息"), L("Loan to value", "贷款成数 LTV"), L("Stamp Duty (England)", "印花税（英格兰）")], "") +
        out("bridge", L("Total cost to repay", "总还款成本"), "",
            [L("Interest", "利息"), L("Arrangement fee", "安排费"), L("Repay at the end", "到期还款")], "")
    )
    return f"""<div class="tool" id="tool">
<div class="tool-nav">
{dial()}
<ul class="bearings" aria-label="{L('Where are you heading?','您的方向')}">{btns}</ul>
</div>
<form class="tool-form" onsubmit="return false" novalidate>{forms}</form>
<div class="tool-out">
{outs}
<a class="btn btn-orange" id="tool-cta" href="{href('contact')}">{L('Talk this through with Lily','和 Lily 详谈')}</a>
</div>
</div>
<p class="tool-note"><strong>{L('An estimate, not advice.','仅为估算，不构成建议。')}</strong> {L('Rates are examples you can change, not offers. Stamp Duty uses the GOV.UK rates for England and Northern Ireland; Scotland and Wales have their own taxes. Lenders work out rental cover with their own stress rates.','利率为可修改的示例，并非报价。印花税按 GOV.UK 公布的英格兰及北爱尔兰税率计算；苏格兰和威尔士另有税制。出租房贷的租金覆盖率由贷款机构按各自的压力利率计算。')} {L('Your home may be repossessed if you do not keep up repayments on your mortgage.','如果您未能按时偿还房贷，您的房屋可能会被收回。')}</p>"""

# ---------------------------------------------------------------- content
SERVICES = [
    dict(k="buy", deg="000°", anchor="first-home",
         t=("First homes and moving home", "首套房与换房"),
         short=("First-time buyers, home movers and people looking for a better deal than their current lender.", "首次购房、换房，或想找到比现有银行更好方案的客户。"),
         body=[("We sit between you and the lender. First we take time to understand your income, your plans and the home you want. Then we compare rates and terms across lenders, including some deals you can't get by going to a lender directly.",
                "我们是您和贷款机构之间的桥梁。先花时间了解您的收入、计划和想买的房子，再比较各家贷款机构的利率与条款，其中包括一些直接去银行拿不到的方案。"),
               ("Once you choose, we handle the application: the documents, the deadlines and the back-and-forth with the lender, so you know what is needed and when.",
                "选定方案后，申请交给我们：文件、时限、与贷款机构的往来沟通，每一步需要什么、何时需要，都提前告诉您。")],
         ticks=[("Identify suitable deals", "筛选合适方案"), ("Application process", "处理申请"), ("Negotiation", "与贷款机构沟通"), ("Approval support", "审批跟进"), ("Completion assistance", "协助完成交易")]),
    dict(k="remo", deg="090°", anchor="remortgage",
         t=("Remortgaging", "转贷 Remortgage"),
         short=("When your fixed rate ends, move to a better deal instead of your lender's standard rate.", "固定利率到期时，换到更合适的方案，而不是自动转为银行的标准浮动利率。"),
         body=[("If your current deal is ending, we look at what your lender offers and what the rest of the market offers, and help you move to better terms or a lower rate.",
                "现有方案快到期时，我们会比较您现有银行的续约方案和市场上的其他方案，协助您换到更好的条款或更低的利率。")],
         ticks=[("Compare your lender with the market", "比较现有银行与市场方案"), ("Check fees against savings", "核算费用与可节省的金额"), ("Application and paperwork", "申请及文件"), ("Timed for when your deal ends", "配合现有方案到期日")]),
    dict(k="btl", deg="180°", anchor="buy-to-let",
         t=("Buy-to-let", "买房出租 Buy-to-let"),
         short=("Mortgages for landlords and property investors, from a first rental to a growing portfolio.", "为房东和投资者安排出租房贷，无论是第一套出租房还是逐步扩大的物业组合。"),
         body=[("Landlords and investors make up a large part of Compaz Finance's clients. We introduce buy-to-let products suited to your situation and explain how lenders look at rent, deposit and your own income.",
                "房东和物业投资者是 Compaz Finance 的主要客户之一。我们会介绍适合您情况的出租房贷产品，并解释贷款机构如何评估租金、首付以及您本人的收入。")],
         ticks=[("Products matched to you", "按您的情况匹配产品"), ("Rental cover explained", "解释租金覆盖要求"), ("Application and paperwork", "申请及文件"), ("Remortgaging existing lets", "现有出租房转贷")]),
    dict(k="bridge", deg="270°", anchor="bridging",
         t=("Bridging loans", "过桥贷款"),
         short=("Buying a new property before selling the one you have.", "在卖出现有房产之前先买下新房产。"),
         body=[("Bridging loans are short-term loans secured on property, usually repaid within 12 months, sometimes within weeks. They come as open loans (no fixed end date, usually repaid within 12 to 24 months) or closed loans (a fixed repayment date, usually cheaper), and as first or second charge, depending on whether there is already a mortgage on the property.",
                "过桥贷款是以房产作抵押的短期贷款，通常在12个月内还清，有时只需几周。分为开放式（没有固定还款日，一般12至24个月内还清）和封闭式（有固定还款日，通常较便宜），并按房产是否已有房贷分为第一押记或第二押记。"),
               ("They can make a quick purchase possible, but they cost more than a normal mortgage and the property is at risk if you can't repay. You need a clear plan for how the loan will be paid off, and we help you test that plan before you commit.",
                "过桥贷款能让您迅速完成购买，但成本高于一般房贷，若无法还款，房产将有风险。您需要清楚的还款计划，我们会在您决定之前帮您把计划核实清楚。")],
         ticks=[("Market research", "市场调研"), ("Expert advice", "专业建议"), ("Negotiation", "与贷款机构沟通"), ("Streamlined process", "简化流程"), ("Customised solution", "量身定制方案"), ("Legal and regulatory compliance", "符合法律与监管要求")],
         warn=("The Financial Conduct Authority does not regulate most forms of bridging loans.", "英国金融行为监管局（FCA）不监管大部分过桥贷款。")),
    dict(k="protect", deg="◆", anchor="protection",
         t=("Life insurance and protection", "人寿保险与保障"),
         short=("Protection for your family, set alongside your mortgage.", "配合房贷安排，为家人提供保障。"),
         body=[("We look at your age, health, family and the size of your mortgage, compare policies from a range of insurers, and explain the difference between cover such as level term and decreasing term, so the cover lines up with what you owe.",
                "我们会考虑您的年龄、健康、家庭和房贷金额，比较多家保险公司的保单，并解释定额定期与递减定期等不同保障的区别，让保障与您的贷款相匹配。")],
         ticks=[("Assess your needs", "评估需要"), ("Compare quotes", "比较报价"), ("Tailored advice", "量身建议"), ("Simplified process", "简化流程"), ("Ongoing support", "持续跟进")],
         warn=("Financial protection policies typically have no cash-in value at any time and cover will cease at the end of the term. If premiums stop, cover will lapse.", "保障类保单通常在任何时候都没有现金价值，保障在期满时终止。若停止缴纳保费，保障将失效。")),
]

REVIEWS = [  # published on compazfinance.co.uk/About (name shown above each quote there)
    ("Compaz Finance has given very friendly and professional advice, particularly with introducing mortgage BTL products suited to my individual needs. I strongly recommend it.", "Landlord", None),
    ("I am extremely satisfied with the services provided. The communication was clear and timely, and the efficiency with which everything was handled exceeded my expectations. Highly professional and reliable. I would definitely recommend!", "Leung Effie", None),
    ("A very professional team. Thank you very much for your help. Your careful, patient, and professional explanations have allowed us to better understand our needs. If any of my friends need a loan, I will be the first to recommend you to them.", "Consumer", None),
    ("Very helpful and high quality. Reminds you how to deal with each step, helped in finding the right product and interest rate, thank you so much.", "郭洁", None),
    ("Excellent service, very easy to communicate, clear instruction for all the documents needed, very friendly and patient.", "Dong", None),
    ("Very professional, trustworthy and responsible. She does the job quickly.", "Zhiqun Liu", None),
]

def reviews(n=None):
    items = REVIEWS[:n] if n else REVIEWS
    out = []
    for q, who, role in items:
        name = f"<b>{who}</b>" if who else f"<b>{L('Client','客户')}</b>"
        if role: name += f" · {role}"
        out.append(f'<blockquote class="review" lang="en"><p>“{q}”</p><footer>{name}</footer></blockquote>')
    return f'<div class="reviews">{"".join(out)}</div><p class="reviews-src">{L("Reviews as published on the Compaz Finance website. Some wording lightly tidied for spelling.","以上评价摘自 Compaz Finance 官网，保留原文（英文），仅修正个别拼写。")}</p>'

ROUTE = [
    (("Your situation", "了解您的情况"), ("Income, deposit, plans and timing, in English or Mandarin.", "收入、首付、计划和时间，英语或普通话均可。")),
    (("Suitable deals", "筛选方案"), ("Rates and terms compared across lenders, including broker-only products.", "比较各家贷款机构的利率和条款，包括只通过经纪提供的产品。")),
    (("Application", "提交申请"), ("A clear list of documents, checked before anything is sent.", "清楚列出所需文件，提交前逐一核对。")),
    (("Negotiation", "沟通协商"), ("We deal with the lender's questions so you don't have to.", "由我们回应贷款机构的各种问题。")),
    (("Approval", "审批"), ("Valuation, underwriting and the mortgage offer, followed up.", "估价、审核和贷款批核书，全程跟进。")),
    (("Completion", "完成交易"), ("Working with your solicitor through to the keys.", "与您的律师配合，直到拿到钥匙。")),
]

# ---------------------------------------------------------------- pages
def page_index():
    rose = ""
    pos = {"buy": "n", "remo": "e", "btl": "s", "bridge": "w", "protect": "c"}
    for s in SERVICES:
        icon = f'<img src="{asset("img/compass.svg")}" alt="" width="54" height="54">' if s["k"] == "protect" else ""
        deg = L("At the centre", "核心") if s["k"] == "protect" else s["deg"]
        rose += f"""<article class="card {pos[s['k']]}">{icon}<div class="deg">{deg}</div><h3>{L(*s['t'])}</h3><p>{L(*s['short'])}</p><a href="{href('services')}#{s['anchor']}">{L('How it works','了解详情')}</a></article>"""
    route = "".join(f"<li><h3>{L(*t)}</h3><p>{L(*d)}</p></li>" for t, d in ROUTE)
    return f"""
<section class="hero" aria-labelledby="h1">
<div class="wrap">
<p class="hero-meta">{L('Mortgage &amp; protection broker · Orpington · English and 普通话','房贷与保障经纪 · 伦敦 Orpington · 英语及普通话')}</p>
<h1 id="h1">{L('Find your bearing in the mortgage maze','在英国贷款买房，先定方向')}</h1>
<p class="hero-sub">{L('Lily Liu set up Compaz Finance in 2020 to guide homeowners, landlords and investors through UK mortgages, in English and Mandarin. Pick where you are heading and see the numbers first.',
'Lily Liu 于2020年创立 Compaz Finance，用中英双语为自住业主、房东和投资者解答英国房贷的大小问题。先选择您的方向，看看大概的数字。')}</p>
{tool()}
</div>
</section>

<section class="sec" aria-labelledby="h-rose">
<div class="wrap">
<div class="sec-head">
<h2 id="h-rose">{L('Four directions, with protection at the centre','四个方向，保障居中')}</h2>
<p>{L('Most clients come to Compaz Finance for one of four things. Life insurance sits in the middle because it protects whichever one you choose.','大部分客户找 Compaz Finance 是为了以下四件事之一。人寿保障放在中间，因为无论选哪个方向，都需要它来守护。')}</p>
</div>
<div class="rose">{rose}</div>
</div>
</section>

<section class="sec alt" aria-labelledby="h-route">
<div class="wrap">
<div class="sec-head">
<h2 id="h-route">{L('From first call to the keys','从第一通电话到拿钥匙')}</h2>
<p>{L('The route a typical purchase takes with us. You always know which waypoint you are at and what comes next.','一般买房的流程如下。每到一站，您都清楚自己在哪里、下一步是什么。')}</p>
</div>
<ol class="route">{route}</ol>
</div>
</section>

<section class="sec" aria-labelledby="h-lily">
<div class="wrap founder">
<div>
<h2 id="h-lily">{L('One broker, two languages, since 2020','一位经纪，两种语言，始于2020年')}</h2>
<blockquote><p>{L('“Compaz Finance treats each customer as an individual, truly listening to and understanding their needs.”','“Compaz Finance 把每位客户都当作独立的个体，认真倾听，真正理解他们的需要。”')}</p>
<footer>{L('From the Compaz Finance story','摘自 Compaz Finance 简介')}</footer></blockquote>
<p style="margin-top:22px"><a class="btn btn-ink" href="{href('about')}">{L('About Lily and the firm','关于 Lily 和公司')}</a></p>
</div>
<ul class="facts">
<li><span>2020</span><div>{L('Founded by Lily Liu, drawing on her experience in the UK mortgage industry','由 Lily Liu 创立，她在英国房贷行业拥有丰富经验')}</div></li>
<li><span>EN · 中文</span><div>{L('Bilingual advice in English and Mandarin','可用英语或普通话咨询')}</div></li>
<li><span>{L('Hundreds','数百位')}</span><div>{L('Clients across the UK: homeowners, landlords and property investors','客户遍布英国：自住业主、房东及物业投资者')}</div></li>
<li><span>FCA 939072</span><div>{L('Authorised and regulated by the Financial Conduct Authority','获英国金融行为监管局授权并受其监管')}</div></li>
</ul>
</div>
</section>

<section class="sec alt" aria-labelledby="h-rev">
<div class="wrap">
<div class="sec-head"><h2 id="h-rev">{L('What clients say','客户评价')}</h2></div>
{reviews(3)}
<p><a href="{href('about')}#reviews">{L('Read all reviews','查看全部评价')}</a></p>
</div>
</section>
{contact_band()}
"""

def contact_band():
    return f"""<section class="contact-band" aria-labelledby="h-band"><div class="wrap">
<h2 id="h-band">{L('Not sure which way to go? Ask Lily','不确定往哪个方向走？问问 Lily')}</h2>
<div class="acts">
<a class="btn btn-ink" href="tel:{PHONE_TEL}">{L('Call','致电')} {PHONE_SHOW}</a>
<a class="btn btn-line" href="{href('contact')}">{L('Send a message','留言咨询')}</a>
</div></div></section>"""

def page_services():
    blocks = ""
    for s in SERVICES:
        body = "".join(f"<p>{L(*p)}</p>" for p in s["body"])
        ticks = "".join(f"<li>{L(*t)}</li>" for t in s["ticks"])
        warn = f'<p class="warn">{L(*s["warn"])}</p>' if s.get("warn") else ""
        calc = "" if s["k"] == "protect" else f'<p><a class="btn btn-ink" href="{href("index")}?b={s["k"]}#tool">{L("Try the numbers","试算一下")}</a></p>'
        side = L("Centre of the compass", "罗盘中心") if s["k"] == "protect" else L("Bearing", "方位")
        blocks += f"""<section class="svc" id="{s['anchor']}" aria-labelledby="h-{s['anchor']}">
<div class="side"><div class="deg">{s['deg']}</div><p>{side}</p></div>
<div class="body"><h2 id="h-{s['anchor']}">{L(*s['t'])}</h2><p><strong>{L(*s['short'])}</strong></p>{body}<ul class="ticks">{ticks}</ul>{warn}{calc}</div>
</section>"""
    return f"""<section class="page-head"><div class="wrap">
<h1>{L('Mortgages and protection','房贷与保障')}</h1>
<p>{L('What Compaz Finance does at each bearing, and what to expect when you work with us.','Compaz Finance 在每个方向上能为您做什么，以及合作时会经历什么。')}</p>
</div></section>
<div class="wrap">{blocks}</div>
<section class="sec alt" aria-labelledby="h-why"><div class="wrap">
<div class="sec-head"><h2 id="h-why">{L('Why use a broker','为什么找经纪')}</h2></div>
<div class="svc" style="border:0;padding:0"><div></div><div class="benefits">
<div><h3>{L('A wider range of lenders','更多贷款机构可选')}</h3><p>{L('Including products not available directly to consumers, which can mean better rates and terms.','包括不直接向公众提供的产品，可能带来更好的利率和条款。')}</p></div>
<div><h3>{L('Advice that fits you','切合您的建议')}</h3><p>{L('Recommendations built on your finances and goals, not a lender’s sales targets.','建议基于您的财务状况和目标，而不是银行的销售指标。')}</p></div>
<div><h3>{L('Possible savings','可能节省开支')}</h3><p>{L('Lender relationships can help with rates, terms and avoiding some fees.','与贷款机构的关系有助于争取利率、条款并避免部分费用。')}</p></div>
<div><h3>{L('Less time and stress','省时省心')}</h3><p>{L('We manage the paperwork and the communication with lenders for you.','文件和与贷款机构的沟通都由我们处理。')}</p></div>
</div></div></div></section>
{contact_band()}"""

def page_about():
    return f"""<section class="page-head"><div class="wrap">
<h1>{L('Your guide in the mortgage maze','英国房贷迷宫里的向导')}</h1>
<p>{L('Compaz Finance has been serving the community’s mortgage needs since 2020.','自2020年起，Compaz Finance 一直为社区解决房贷需要。')}</p>
</div></section>
<section class="sec"><div class="wrap founder">
<div class="prose">
<h2>{L('Set up by Lily Liu in 2020','2020年由 Lily Liu 创立')}</h2>
<p>{L('Compaz Finance was established in 2020 by Lily Liu, drawing on her extensive experience in the UK mortgage industry and her fluency in English and Mandarin.','Compaz Finance 于2020年由 Lily Liu 创立。她在英国房贷行业经验丰富，英语和普通话都很流利。')}</p>
<p>{L('Since then the firm has served hundreds of clients across the UK, including homeowners, landlords and property investors, with friendly, sound advice and practical help.','创立至今，公司已为英国各地数百位客户提供服务，包括自住业主、房东和物业投资者，给予亲切、可靠的建议与实际协助。')}</p>
<p>{L('Clients know the firm for diligence, care and, above all, trustworthiness. Each customer is treated as an individual: we listen first and recommend second.','客户认识的 Compaz Finance 细心、负责，最重要的是值得信赖。每位客户都被当作独立的个体：先倾听，再建议。')}</p>
</div>
<ul class="facts">
<li><span>{L('Trust','信赖')}</span><div>{L('The highest standards of integrity in everything we do','一切以最高的诚信标准行事')}</div></li>
<li><span>{L('Diligence','细心')}</span><div>{L('Every document checked, every step followed up','每份文件都核对，每一步都跟进')}</div></li>
<li><span>{L('You first','以您为先')}</span><div>{L('Your needs and goals at the heart of the advice','建议以您的需要和目标为核心')}</div></li>
<li><span>EN · 中文</span><div>{L('Advice in English or Mandarin, whichever you prefer','英语或普通话，任您选择')}</div></li>
</ul>
</div></section>
<section class="sec alt" id="reviews" aria-labelledby="h-rev"><div class="wrap">
<div class="sec-head"><h2 id="h-rev">{L('What clients say','客户评价')}</h2></div>
{reviews()}
</div></section>
{contact_band()}"""

def page_contact():
    opts = "".join(f'<option value="{k}">{L(*n)}</option>' for k, d, n in BEARINGS)
    opts += f'<option value="protect">{L("Life insurance and protection","人寿保险与保障")}</option><option value="other">{L("Something else","其他")}</option>'
    return f"""<section class="page-head"><div class="wrap">
<h1>{L('How can we help you?','我们可以怎样帮您？')}</h1>
<p>{L('Call, email or send a message in English or Chinese. Lily will reply personally.','可以致电、发电邮或留言，中英文皆可。Lily 会亲自回复。')}</p>
</div></section>
<section class="sec"><div class="wrap contact-grid">
<form class="form" id="enquiry" novalidate>
<div><label for="f-name">{L('Your name','您的姓名')}</label><input id="f-name" name="name" autocomplete="name" required><p class="err">{L('Please tell us your name','请填写姓名')}</p></div>
<div><label for="f-phone">{L('Mobile number','手机号码')}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
<div class="full"><label for="f-email">{L('Email address','电邮地址')}</label><input id="f-email" name="email" type="email" autocomplete="email" required><p class="err">{L('Please enter a valid email address','请填写有效的电邮地址')}</p></div>
<div class="full"><label for="f-topic">{L('What is it about?','咨询内容')}</label><select id="f-topic" name="topic">{opts}</select></div>
<div class="full"><label for="f-msg">{L('Message','留言')}</label><textarea id="f-msg" name="message"></textarea></div>
<div class="full"><label class="consent"><input type="checkbox" id="f-ok" required> <span>{L(f'I have read the <a href="{href("privacy")}">customer privacy notice</a> and agree to Compaz Finance Ltd using my details to contact me. They will not be used for marketing.', f'我已阅读<a href="{href("privacy")}">客户隐私声明</a>，同意 Compaz Finance Ltd 使用我的资料与我联系。资料不会用于营销。')}</span></label><p class="err">{L('Please tick to confirm','请勾选确认')}</p></div>
<div class="full"><button class="btn btn-orange" type="submit">{L('Open in my email app','用电邮发送')}</button>
<p class="small" style="margin-top:10px">{L('Nothing is stored on this website. The button opens your own email app with your message filled in, ready to send to '+EMAIL+'.','本网站不会储存任何资料。按下按钮后，会打开您的电邮程序并填好内容，发送至 '+EMAIL+'。')}</p></div>
</form>
<div>
<ul class="ways">
<li><span class="k">{L('Phone','电话')}</span><a href="tel:{PHONE_TEL}">{PHONE_SHOW}</a></li>
<li><span class="k">{L('Email','电邮')}</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><span class="k">{L('Office','办公地址')}</span>37 Hillcrest Road<br>Orpington BR6 9AN</li>
<li><span class="k">{L('Languages','语言')}</span>{L('English and Mandarin','英语、普通话')}</li>
</ul>
<p class="small" style="margin-top:18px">{L('Most advice happens by phone and video call, so you can be anywhere in the UK. Please call before visiting.','大部分咨询通过电话或视频进行，无论您在英国哪里都可以。到访前请先致电预约。')}</p>
</div>
</div></section>"""

def page_privacy():
    return f"""<section class="page-head"><div class="wrap">
<h1>{L('Privacy','隐私')}</h1>
<p>{L('How your personal details are handled.','我们如何处理您的个人资料。')}</p>
</div></section>
<section class="sec"><div class="wrap prose">
<h2>{L('This website','本网站')}</h2>
<p>{L('This concept website stores nothing. The enquiry form and the calculator run entirely in your browser; sending a message opens your own email app, and nothing reaches us until you press send there. There are no tracking cookies or analytics.','本概念网站不储存任何资料。留言表格和计算器完全在您的浏览器中运行；发送留言会打开您自己的电邮程序，您在那里按下发送前，我们收不到任何内容。网站不使用追踪 Cookie 或分析工具。')}</p>
<h2>{L('When you become a client','成为客户后')}</h2>
<p>{L('Arranging a mortgage or insurance means we ask for detailed information about your circumstances, finances and sometimes your health. How we use it, the legal basis, who we share it with and your rights are set out in the Compaz Finance customer privacy notice.','安排房贷或保险时，我们需要了解您的个人情况、财务状况，有时还包括健康信息。我们如何使用这些资料、法律依据、与谁分享，以及您的权利，均载于 Compaz Finance 客户隐私声明。')}</p>
<p><a class="btn btn-ink" href="https://www.compazfinance.co.uk/privacy">{L('Read the full customer privacy notice','阅读完整的客户隐私声明')}</a></p>
<p class="small">{L('Questions about your data: ','资料相关问题：')}<a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>"""

def page_404():
    return f"""<section class="lost"><div class="wrap">
<img src="{asset('img/compass.svg')}" alt="" width="120" height="120">
<h1>{L('Off course','偏离航道了')}</h1>
<p>{L('This page isn’t on the map.','地图上找不到这一页。')}</p>
<p><a class="btn btn-orange" href="{href('index')}">{L('Back to the start','返回首页')}</a></p>
</div></section>"""

META = {
    "index": (("Compaz Finance · Mortgage broker in English and Mandarin", "Compaz Finance · 中英双语房贷经纪"),
              ("Mortgages, buy-to-let, bridging loans and protection from Lily Liu, in English and Mandarin.", "Lily Liu 提供中英双语的房贷、出租房贷、过桥贷款与保障咨询。")),
    "services": (("Mortgages and protection · Compaz Finance", "房贷与保障 · Compaz Finance"),
                 ("First homes, remortgages, buy-to-let, bridging loans and life insurance.", "首套房、转贷、出租房贷、过桥贷款与人寿保险。")),
    "about": (("About Lily Liu · Compaz Finance", "关于 Lily Liu · Compaz Finance"),
              ("Founded in 2020 by Lily Liu. Bilingual mortgage advice for homeowners, landlords and investors.", "2020年由 Lily Liu 创立，为业主、房东和投资者提供双语房贷建议。")),
    "contact": (("Contact · Compaz Finance", "联系 · Compaz Finance"),
                ("Call, email or send a message in English or Chinese.", "致电、电邮或留言，中英文皆可。")),
    "privacy": (("Privacy · Compaz Finance", "隐私 · Compaz Finance"), ("How your personal details are handled.", "我们如何处理您的个人资料。")),
    "404": (("Page not found · Compaz Finance", "找不到页面 · Compaz Finance"), ("Page not found.", "找不到页面。")),
}
BUILD = {"index": page_index, "services": page_services, "about": page_about, "contact": page_contact, "privacy": page_privacy, "404": page_404}

def main():
    global LANG
    for LANG in ("en", "sc"):
        outdir = ROOT if LANG == "en" else os.path.join(ROOT, "sc")
        os.makedirs(outdir, exist_ok=True)
        for p in PAGES:
            t, d = META[p]
            if p == "404" and LANG == "sc":
                continue  # GitHub Pages serves only the root 404.html
            doc = head(p, L(*t), L(*d)) + header(p) + BUILD[p]() + footer()
            if p == "404":  # served at any depth: make local links absolute
                doc = re.sub(r'(href|src)="(?!https?:|tel:|mailto:|#|/)', r'\1="/compazfinance/', doc)
                doc = doc.replace('"/compazfinance/./"', '"/compazfinance/"')
            with open(os.path.join(outdir, p + ".html"), "w", encoding="utf-8") as f:
                f.write(doc)
    print("built", len(PAGES) * 2 - 1, "pages")

if __name__ == "__main__":
    main()
