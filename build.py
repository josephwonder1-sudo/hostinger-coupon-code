#!/usr/bin/env python3
"""Builds README.md (GitHub) and docs/ (GitHub Pages) from article.md.
Edit article.md, then run:  python3 build.py   (needs: pip install markdown)
[[CTA1]]..[[CTA4]] in article.md become buttons. All use the exact affiliate URL.
"""
import html, json, pathlib, re
from urllib.parse import quote
import markdown

AFF = "https://www.hostg.xyz/aff_c?offer_id=6&aff_id=180675"   # locked - do not edit
CTAS = {
    "CTA1": "🎁 CLAIM YOUR DISCOUNT",
    "CTA2": "GET THE OFFER",
    "CTA3": "ACTIVATE YOUR OFFER",
    "CTA4": "CLAIM YOUR OFFER NOW",
}
SEO_TITLE = "Working Hostinger Promo Codes BF & Coupons/Up to 85% off"
META_DESC = ("Hostinger coupon code for Black Friday 2026: up to 85% off web hosting from $1.99/mo. "
             "No promo code needed, free domain, 30-day money-back. Claim your deal.")
SITE = "https://josephwonder1-sudo.github.io/hostinger-coupon-code/"
REPO = "https://github.com/josephwonder1-sudo/hostinger-coupon-code"
LASTMOD = "2026-11-10"

root = pathlib.Path(__file__).parent
src = (root / "article.md").read_text()

# ---------- README.md (GitHub-flavoured markdown) ----------
def md_button(label):
    badge = quote(label.replace("-", "--").replace("_", "__"), safe="")
    return (f"<p align=\"center\"><a href=\"{AFF}\"><img alt=\"{label}\" "
            f"src=\"https://img.shields.io/badge/{badge}-000000?style=for-the-badge\"></a><br>"
            f"<a href=\"{AFF}\"><b>{label} →</b></a></p>")

readme = src
for k, label in CTAS.items():
    readme = readme.replace(f"[[{k}]]", md_button(label))
readme += f"\n🌐 Web version: {SITE}\n"
(root / "README.md").write_text(readme)

# ---------- docs/index.html ----------
body_md = src.split("\n", 1)[1]            # H1 is rendered separately
placeholder = {k: f"CTAPLACEHOLDER{k}" for k in CTAS}
for k, p in placeholder.items():
    body_md = body_md.replace(f"[[{k}]]", p)
body = markdown.markdown(body_md, extensions=["tables"])
for k, p in placeholder.items():
    btn = (f'<div class="cta"><a class="btn" href="{html.escape(AFF)}" '
           f'rel="sponsored nofollow noopener" target="_blank">{CTAS[k]}</a></div>')
    body = body.replace(f"<p>{p}</p>", btn)

# FAQ schema built from the FAQ section's H3 questions and their answers
faq_part = src.split("## Frequently Asked Questions", 1)[1].split("\n## ", 1)[0]
faqs = re.findall(r"### (.+?)\n(.+?)(?=\n### |\Z)", faq_part, re.S)
schema = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q.strip(),
                          "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\*\*", "", a).strip()}}
                         for q, a in faqs]}
h1 = src.splitlines()[0][2:]
e = html.escape
page = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(SEO_TITLE)}</title>
<meta name="description" content="{e(META_DESC)}">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(SEO_TITLE)}">
<meta property="og:description" content="{e(META_DESC)}">
<meta property="og:url" content="{SITE}">
<meta property="article:modified_time" content="{LASTMOD}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:#111;font:18px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:28px 20px 72px}}
h1{{font-size:2.2rem;line-height:1.2;margin:.3em 0 .4em}}
h2{{font-size:1.55rem;margin:2em 0 .6em;padding-bottom:.25em;border-bottom:2px solid #111}}
h3{{font-size:1.2rem;margin:1.6em 0 .4em}}
p,li{{margin:.5em 0}}
a{{color:#673de6}}
em{{color:#555}}
blockquote{{margin:1.2em 0;padding:14px 20px;border:2px solid #111;background:#f6f4ff}}
blockquote p{{margin:.2em 0}}
table{{width:100%;border-collapse:collapse;margin:1em 0;font-size:.95rem}}
th,td{{border:1px solid #ccc;padding:9px 11px;text-align:left;vertical-align:top}}
th{{background:#111;color:#fff}}
tr:nth-child(even) td{{background:#fafafa}}
.table-wrap{{overflow-x:auto}}
.cta{{text-align:center;margin:28px 0}}
.btn{{display:inline-block;background:#673de6;color:#fff;text-decoration:none;font-weight:800;letter-spacing:.02em;
     padding:16px 34px;font-size:1.15rem;border-radius:6px;box-shadow:0 4px 0 #3b1fa8}}
.btn:hover{{background:#5025d1}}
.meta{{color:#555;font-size:.9rem}}
footer{{margin-top:48px;border-top:1px solid #ddd;padding-top:16px;font-size:.85rem;color:#555}}
@media (max-width:600px){{h1{{font-size:1.7rem}} .btn{{display:block}}}}
</style>
</head>
<body>
<main>
<p class="meta">Last verified {LASTMOD}</p>
<h1>{e(h1)}</h1>
{body}
<footer><p><a href="{REPO}">Source on GitHub</a></p></footer>
</main>
</body>
</html>
"""
page = page.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
d = root / "docs"; d.mkdir(exist_ok=True)
(d / "index.html").write_text(page)
(d / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
(d / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"  <url><loc>{SITE}</loc><lastmod>{LASTMOD}</lastmod><changefreq>weekly</changefreq></url>\n</urlset>\n")
(d / ".nojekyll").write_text("")
print(f"built README.md + docs/ ({len(faqs)} FAQ entries)")
