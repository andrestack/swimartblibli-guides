import re, sys
from playwright.sync_api import sync_playwright
src = open('/home/claude/stain-guide.html').read()
fd = '/tmp/claude-0/-home-claude/8403b610-bfcd-5d5a-b91b-c57549736438/scratchpad/fonts/package/files'
faces = ''.join(f'@font-face{{font-family:"Ubuntu";font-weight:{w};src:url("file://{fd}/ubuntu-latin-{w}-normal.woff2") format("woff2");}}' for w in (400,500,700))
src = re.sub(r'<link[^>]*fonts\.g[^>]*>\n?', '', src)
html = f'<!doctype html><html><head><meta charset="utf-8"><style>{faces}</style>{src}</head></html>'
open('/home/claude/print-stain.html','w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto('file:///home/claude/print-stain.html'); pg.wait_for_timeout(600)
    pg.emulate_media(media='print')
    pg.pdf(path='/home/claude/Pool-Stain-Guide.pdf', format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
