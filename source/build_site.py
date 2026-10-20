import re, os, shutil
guides=[('plunge-pool-guide.html','plunge-pool','Plunge-Pool-Welcome-Guide.pdf'),
        ('green-pool-guide.html','green-pool','Green-Pool-Recovery-Guide.pdf'),
        ('heat-pump-guide.html','heat-pump','Heat-Pump-Owners-Guide.pdf')]
navcss='''
.guide-nav { display: flex; justify-content: space-between; gap: 12px; margin-bottom: 14px; }
.guide-nav a { color: #FFFFFF; font-weight: 500; text-underline-offset: 3px; min-height: 44px; display: inline-flex; align-items: center; }
.guide-nav a:focus-visible { outline: 3px solid #F7C935; outline-offset: 3px; }
a.phone { text-decoration: none; display: inline-block; }
@media print { .guide-nav { display: none; } }
'''
os.chdir('/home/claude')
for src,slug,pdf in guides:
    s=open(src).read()
    i=s.index('</style>')+len('</style>')
    head,body=s[:i],s[i:]
    head=head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','').replace('</style>',navcss+'</style>')
    nav=f'<nav class="guide-nav" aria-label="Guide"><a href="/">All guides</a><a href="/pdf/{pdf}">Download PDF</a></nav>\n    '
    assert body.count('<div class="cover-top">')==1
    body=body.replace('<div class="cover-top">',nav+'<div class="cover-top">',1)
    body=body.replace('<div class="phone">(07) 5356 9448</div>','<a class="phone" href="tel:+61753569448">(07) 5356 9448</a>')
    html=('<!doctype html>\n<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
          '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<meta name="theme-color" content="#2878B8">\n'
          + head.strip() + '\n</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n')
    os.makedirs(f'guides-site/{slug}',exist_ok=True)
    open(f'guides-site/{slug}/index.html','w').write(html)
    shutil.copy(pdf, f'guides-site/pdf/{pdf}')
shutil.copy('guides-site-src/index-body.html','guides-site/index.html')
shutil.copy('assets/swimart-logo.png','guides-site/swimart-logo.png')
print('built')
