import re, base64
def uri(p, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(p,'rb').read()).decode()
LOGO = uri('assets/swimart-logo.png', 'image/png')
SHOP = '''    <div class="shop">
      <div><span class="lbl">Visit us</span><span>1/311 David Low Way<br>Bli Bli QLD 4560</span></div>
      <div><span class="lbl">Shop hours</span><span>Mon–Fri 9:00 am – 4:30 pm<br>Sat 8:30 am – 12:30 pm</span></div>
    </div>
'''
CSS = '''main { background: var(--white); padding-bottom: 48px; }
.cover-top { display: flex; justify-content: flex-end; }
.logo { display: block; height: auto; max-width: 100%; }
.cover-top .logo { width: 132px; }
.foot-logo { width: 150px; }
.shop { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 40px; width: 100%; max-width: 560px; margin-top: 6px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,.3); }
.shop div { display: grid; gap: 2px; }
.shop span { color: #E6F1FA; }
.shop .lbl { color: var(--sun); font-weight: 700; }
'''
for f in ['plunge-pool-guide.html','green-pool-guide.html','heat-pump-guide.html']:
    s = open(f).read()
    # page ground is blue so the footer runs to the bottom edge; content sits on white
    s = s.replace('body { margin: 0; background: var(--white);', 'body { margin: 0; background: var(--swim);', 1)
    s = re.sub(r'^\.brand \{[^\n]*\}\n', '', s, count=1, flags=re.M)
    s = s.replace('footer { background: var(--swim); color: var(--white); margin-top: 48px; }',
                  CSS + 'footer { background: var(--swim); color: var(--white); }', 1)
    s = s.replace('footer .wrap { padding-block: 36px 40px; display: grid; gap: 10px; }',
                  'footer .wrap { padding-block: 36px 44px; display: grid; gap: 12px; justify-items: center; text-align: center; }', 1)
    s = s.replace('footer p { color: #E6F1FA; max-width: 60ch; }', 'footer p { color: #E6F1FA; max-width: 60ch; margin-inline: auto; }', 1)
    # print: white page ground, spacing moves from footer margin to main padding
    s, n = re.subn(r'  footer \{ margin-top: (\d+mm);', r'  body { background: var(--white); }\n  main { padding-bottom: \1; }\n  .cover-top .logo { width: 34mm; }\n  .foot-logo { width: 30mm; }\n  .shop { padding-top: 3mm; gap: 2mm 10mm; }\n  footer { margin-top: 0;', s, count=1)
    assert n == 1, f
    # header logo top right
    s = s.replace('    <div class="brand">Swimart Bli Bli</div>\n',
                  f'    <div class="cover-top"><img class="logo" src="{LOGO}" alt="Swimart Bli Bli" width="202" height="100"></div>\n', 1)
    # footer: logo under the heading, address and hours at the end
    s, n = re.subn(r'(<footer>\n  <div class="wrap">\n    <h2>Need a hand\?</h2>\n)(.*?)(  </div>\n</footer>)',
                   lambda m: m.group(1) + f'    <img class="logo foot-logo" src="{LOGO}" alt="Swimart Bli Bli" width="202" height="100">\n' + m.group(2) + SHOP + m.group(3),
                   s, count=1, flags=re.S)
    assert n == 1, f
    if f.startswith('green'):
        s = re.sub(r'^\.(water|light \.water|mid \.water|dark \.water)[^\n]*\n', '', s, flags=re.M)
        s = re.sub(r'^\.shade \{[^\n]*\}\n', '.shade { border-radius: 16px; overflow: hidden; background-color: var(--deep); background-size: cover; background-position: center; display: grid; align-content: end; padding: 120px 10px 10px; }\n'
                   + ''.join(f'.shade.{k} {{ background-image: url("{uri(f"assets/pool-{k}.jpg", "image/jpeg")}"); }}\n' for k in ('light','mid','dark')), s, count=1, flags=re.M)
        s = s.replace('.shade .body { padding: 14px 16px 16px; display: grid; gap: 6px; align-content: start; }',
                      '.shade .body { padding: 14px 16px 16px; display: grid; gap: 6px; align-content: start; background: rgba(255,255,255,.93); border-radius: 11px; }', 1)
        s = s.replace('  .water { height: 70px; }', '  .shade { padding-top: 26mm; }', 1)
        s = s.replace('        <div class="water" aria-hidden="true"></div>\n', '')
        assert 'class="water"' not in s and '.water' not in s
    open(f, 'w').write(s)
    print('patched', f, len(s))
