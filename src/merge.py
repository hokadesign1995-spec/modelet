import re,base64,json,glob,os
B='/tmp/claude-0/-home-claude/9d8f67d6-b59b-5c51-9560-f21f5913bddf/scratchpad/build2/'
src=open(B+'src.html',encoding='utf-8').read()
idx=open('/home/claude/modelet/index.html',encoding='utf-8').read()
# --- CSS: story-related rules only
css=src[src.index('<style>')+7:src.index('</style>')]
a=css.index('/* story */');b=css.index('/* sections */')
sc=css[a:b]
sc=sc.replace('html.rm','html.rw-rm')
for o,n in [('.story','.rw-story'),('.stage','.rw-stage'),('.cap','.rw-cap'),('.hud','.rw-hud'),('.prog','.rw-prog'),('.fb','.rw-fb'),('.pill','.rw-pill'),('#gl','#rw-gl'),('.ttl','.rw-ttl'),('.cap .k','.rw-cap .rw-k')]:
    sc=sc.replace(o,n)
sc=sc.replace('.rw-cap .k','.rw-cap .rw-k').replace('.rw-cap .row','.rw-cap .rw-row')
# helper rules that the story relies on
pill='''.rw-pill{height:48px;padding:0 24px;border-radius:99px;border:0;display:inline-flex;align-items:center;gap:9px;font-weight:800;white-space:nowrap;font:inherit;font-weight:800;cursor:pointer;text-decoration:none}
.rw-pill.lime{background:var(--accent);color:var(--on-accent)}
.rw-pill:hover{filter:brightness(1.07)}
.rw-story{--story-fg:#251c3b;color:#251c3b}
.rw-story a{text-decoration:none}
'''
sc=sc.replace('.rw-cap .rw-pill.ghost{color:var(--story-fg)}','.rw-pill.ghost{background:transparent;border:1.5px solid #251c3b;color:#251c3b}')
sc=sc.replace('.hud.tl','.rw-hud.tl').replace('.hud.bl','.rw-hud.bl')
sc=re.sub(r'\.rw-hud\.tl\{top:calc\(88px','.rw-hud.tl{top:calc(88px',sc)
# --- HTML
h=src[src.index('<section class="story"'):src.index('</section>',src.index('<section class="story"'))+10]
for o,n in [('class="story"','class="rw-story"'),('class="stage"','class="rw-stage"'),('id="story"','id="rwStory"'),('id="stage"','id="rwStage"'),('id="gl"','id="rw-gl"'),('class="fb"','class="rw-fb"'),('id="fb"','id="rw-fb"'),('class="hud ','class="rw-hud '),('class="cap','class="rw-cap'),('class="ttl"','class="rw-ttl"'),('class="k"','class="rw-k"'),('class="row"','class="rw-row"'),('class="prog"','class="rw-prog"'),('class="pill lime"','class="rw-pill lime"'),('class="pill ghost"','class="rw-pill ghost"')]:
    h=h.replace(o,n)
h=h.replace('<a class="rw-pill ghost" href="#why">مزایا</a>','<button type="button" class="rw-pill ghost" id="rwMore">ببین چی داریم</button>')
h=re.sub(r'<a class="rw-pill lime" href="https://claude.ai[^"]*" target="_blank" rel="noopener" data-step>Step Inside</a>','<button type="button" class="rw-pill lime" data-step>Step Inside</button>',h)
h=h.replace('id="story"','id="rwStory"')
# --- JS
js=src[src.index("(function(){\n'use strict';"):src.index('</script>')]
# remove nav/modal block
j1=js.index('/* ---------- nav ---------- */');j2=js.index('/* ---------- captions ---------- */')
js=js[:j1]+'''var story=$('#rwStory');
function storyP(){var r=story.getBoundingClientRect(),vh=window.innerHeight,span=Math.max(1,r.height-vh);return clamp(-r.top/span,0,1)}
function navState(){}
var lastFocus=null;
'''+js[j2:]
js=js.replace("html.rm","html.rw-rm").replace("document.documentElement.classList.add('rm')","document.documentElement.classList.add('rw-rm')")
for o,n in [("'.cap'","'.rw-cap'"),("'#gl'","'#rw-gl'"),("'#fb'","'#rw-fb'"),("'#progI'","'#progI'"),("classList.contains('end')","classList.contains('end')")]:
    js=js.replace(o,n)
js=js.replace("$('#fb')","$('#rw-fb')").replace("$$('.cap')","$$('.rw-cap')")
js=js.replace("document.documentElement.setAttribute('dir','rtl');document.documentElement.setAttribute('lang','fa');\n","")
js=js.replace("if(rm&&R){pS=.58","$('#rwMore')&&$('#rwMore').addEventListener('click',function(){var n=document.querySelector('#home > section.sec');if(n)n.scrollIntoView({behavior:'smooth'})});\nif(rm&&R){pS=.58")
D={os.path.basename(f)[:-5]:'data:image/webp;base64,'+base64.b64encode(open(f,'rb').read()).decode() for f in glob.glob('/home/claude/modelet/cut2/*.webp')}
js=js.replace('/*SPRITES*/{}',json.dumps(D),1).replace('/*ASPECT*/{}',open('/home/claude/modelet/cut2/aspect.json').read(),1)

h=open(B+'look.html',encoding='utf-8').read()
js=open(B+'look.js',encoding='utf-8').read()
js=js.replace('/*SPRITES*/{}',json.dumps(D),1).replace('/*ASPECT*/{}',open('/home/claude/modelet/cut2/aspect.json').read(),1)
sc=open(B+'look.css',encoding='utf-8').read()
pill=''

# ---- extra sections (why / how / for / join) from the scroll page, namespaced ab-
ab=src[src.index('<section class="s" id="why"'):src.index('</main>',src.index('<section class="s" id="why"'))]
ab=ab.replace('class="s"','class="ab-s"').replace('class="eyebrow"','class="ab-eyebrow"').replace('class="t"','class="ab-t"').replace('class="lead"','class="ab-lead"')
for o in ['grid3','card','steps','chips']:
    ab=ab.replace('class="%s"'%o,'class="ab-%s"'%o)
ab=ab.replace('class="s band"','class="ab-s ab-band"').replace('class="wrap cta"','class="wrap ab-cta"').replace('class="row"','class="ab-row"')
ab=ab.replace('class="pill lime" id="sellerBtn"','class="ab-pill lime" id="abSeller"')
ab=ab.replace('<a class="pill ghost" href="https://claude.ai/artifact/EgzwHWkqAXJB6L6uB5HwUp" target="_blank" rel="noopener" data-step>Step Inside</a>','<button type="button" class="ab-pill ghost" data-step>فروشگاه مجازی</button>')
ab=ab.replace('<a class="pill ghost" href="https://claude.ai/artifact/EgzwHWkqAXJB6L6uB5HwUp" target="_blank" rel="noopener" data-step>فروشگاه مجازی</a>','<button type="button" class="ab-pill ghost" data-step>فروشگاه مجازی</button>')
ab=ab.replace('<a class="pill ghost" href="https://claude.ai/artifact/EgzwHWkqAXJB6L6uB5HwUp" target="_blank" rel="noopener" data-step>مشاهده فروشگاه‌های مدلت</a>','<button type="button" class="ab-pill ghost" data-step>مشاهده فروشگاه‌های مدلت</button>')
ab=ab.replace('id="why"','id="why"')
abcss=css[css.index('/* sections */'):css.index('footer{')]
for o,n in [('section.s{','section.ab-s{'),('.eyebrow{','.ab-eyebrow{'),('h2.t{','h2.ab-t{'),('.lead{','.ab-lead{'),('.grid3','.ab-grid3'),('.card','.ab-card'),('.steps','.ab-steps'),('.chips','.ab-chips'),('.band','.ab-band'),('.cta','.ab-cta'),('.cta .row','.ab-cta .ab-row')]:
    abcss=abcss.replace(o,n)
abcss=abcss.replace('.ab-cta .row','.ab-cta .ab-row').replace('.ab-band .pill.ghost{color:#fff}','.ab-band .ab-pill.ghost{color:#fff}')
abcss+="""
.ab-s{color:var(--fg)}
.ab-band{background:#251c3b;color:#fff}
.ab-s .ab-card{display:block}
.ab-pill{height:46px;padding:0 24px;border-radius:99px;border:0;display:inline-flex;align-items:center;gap:9px;font:inherit;font-weight:800;white-space:nowrap;cursor:pointer;text-decoration:none;color:inherit}
.ab-pill.lime{background:#89e06c;color:#10200a}
.ab-pill.ghost{background:transparent;border:1.5px solid currentColor}
.ab-pill:hover{filter:brightness(1.07)}
.ab-ph2{border:1.5px dashed var(--line);border-radius:12px;padding:12px 14px;color:var(--muted);font-size:14px;margin-top:14px}
.ab-scrim{position:fixed;inset:0;background:rgba(14,8,28,.6);z-index:90;display:grid;place-items:center;padding:16px}
.ab-modal{background:var(--surface);color:var(--fg);border-radius:22px;max-width:520px;width:100%;padding:28px 26px;position:relative}
.ab-modal h3{margin:0 0 8px;font-size:24px;font-weight:800}
.ab-modal ul{padding-inline-start:20px;color:var(--muted)}
.ab-modal .abx{position:absolute;top:12px;inset-inline-start:12px;width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer;font-size:18px}
"""
abjs="""(function(){var b=document.getElementById('abSeller');if(!b)return;
function close(){var r=document.getElementById('abRoot');if(r)r.remove();b.focus()}
b.addEventListener('click',function(){var r=document.createElement('div');r.id='abRoot';
r.innerHTML='<div class="ab-scrim"><div class="ab-modal" role="dialog" aria-modal="true" aria-label="همکاری با مدلت"><button class="abx" aria-label="بستن">✕</button><h3>همکاری با مدلت</h3><p style="color:var(--muted);margin:0 0 10px">برای فروشندگان و برندها، مسیر کار این است:</p><ul><li>قرارداد و هماهنگی تأمین کالا با تیم مدلت</li><li>ثبت کالا و عکس‌ها در مارکت‌پلیس</li><li>مدلت سفارش، پرداخت، ارسال و پشتیبانی را مدیریت می‌کند</li><li>کمیسیون از فروش در توافق اولیه مشخص می‌شود</li></ul><div class="ab-ph2">اطلاعات تماس مدلت (ایمیل و شماره) را بفرست تا همین‌جا بگذارم.</div></div></div>';
document.body.appendChild(r);r.querySelector('.abx').addEventListener('click',close);r.firstChild.addEventListener('click',function(e){if(e.target===r.firstChild)close()});r.querySelector('.abx').focus()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')close()})})();
"""
mk="    </section>\\n  </main>\\n"

abjs+="""(function(){var r=document.documentElement,b=document.getElementById('themeBtn');if(!b)return;
var t='light';try{t=localStorage.getItem('modelet-theme')||'light'}catch(e){}
function set(v){t=v;r.setAttribute('data-theme',v);r.style.colorScheme=v;var dark=v==='dark';
 document.getElementById('icoSun').style.display=dark?'':'none';document.getElementById('icoMoon').style.display=dark?'none':'';
 b.setAttribute('aria-label',dark?'تم روشن':'تم تیره');b.title=dark?'تم روشن':'تم تیره';
 try{localStorage.setItem('modelet-theme',v)}catch(e){}}
set(t);b.addEventListener('click',function(){set(t==='dark'?'light':'dark')})})();
"""
def sec(h,i):
    a=h.rfind('<section',0,h.index('id="%s"'%i));b=h.index('</section>',a)+10;return h[a:b]
S={k:sec(ab,k) for k in ['why','how','for','join']}
ab_home=S['join']
ab_about=''.join(S[k].replace('id="why"','id="why2"').replace('id="whyT"','id="whyT2"').replace('aria-labelledby="whyT"','aria-labelledby="whyT2"') if k=='why' else S[k] for k in ['why','how','for'])
ab_about=ab_about
for _a,_b in [('به دنیای محصولات برندهای معتبر ایرانی با قیمت\u200cهای ویژه خوش آمدید. مدلت فرصتی است برای انتخاب محصولات برندهای باکیفیت جایی که اصالت، کیفیت، استایل و قیمت مناسب در کنار هم قرار می\u200cگیرند.', 'اصالت، کیفیت، استایل و قیمت مناسب؛ همه در کنار هم.'), ('برندهای معتبر، قیمت\u200cهای ویژه', 'برندهای معتبر، قیمت ویژه'), ('محصولات باکیفیت از برندهای منتخب ایرانی، با فرصت\u200cهایی ویژه برای خریدی هوشمندانه\u200cتر.', 'محصولات باکیفیت برندهای منتخب ایرانی.'), ('تنوعی برای هر سلیقه', 'تنوع برای هر سلیقه'), ('مجموعه\u200cای متنوع از پوشاک زنانه، مردانه، بچگانه و اکسسوری از برندهای منتخب.', 'پوشاک زنانه، مردانه، بچگانه و اکسسوری.'), ('تجربه خریدی مطمئن و آسان', 'خرید مطمئن و آسان'), ('از انتخاب محصول تا دریافت سفارش، همراه شما هستیم تا خریدی آسان، شفاف و مطمئن را تجربه کنید.', 'از انتخاب تا دریافت سفارش، شفاف و مطمئن.'), ('پرداخت آسان و منعطف', 'پرداخت آسان'), ('انتخاب و خرید آسان با امکان استفاده از روش\u200cهای پرداخت متنوع و اعتبار خرید.', 'روش\u200cهای پرداخت متنوع و اعتبار خرید.'), ('بسته\u200cبندی با سلیقه شما', 'بسته\u200cبندی هدیه'), ('سفارش خود را با بسته\u200cبندی ویژه و امکان آماده\u200cسازی برای هدیه، به انتخاب خود دریافت کنید.', 'بسته\u200cبندی ویژه و آماده\u200cسازی برای هدیه.'), ('در صورت عدم رضایت از محصول، امکان بازگشت یا تعویض مطابق با شرایط فروشگاه فراهم است.', 'طبق شرایط فروشگاه و مدلت.')]:
    assert _a in ab_about,_a[:20]
    ab_about=ab_about.replace(_a,_b)
about_main='<main id="about" hidden>\n<div class="wrap" style="padding-top:18px"><div class="crumbs"><button data-go="home">خانه</button> / <span>درباره ما</span></div><h1 style="margin:14px 0 0;font-size:clamp(28px,4vw,44px);font-weight:800">درباره مدلت</h1></div>\n'+ab_about+'\n</main>\n'
sale_html=open(B+'sale.html',encoding='utf-8').read()
ab=ab_home
# insert into index
out=idx.replace('</style>',sc+pill+abcss+'</style>',1)
assert '<!--LOOK-->' in out and '<!--SALE-->' in out
out=out.replace('<!--LOOK-->',h,1)
out=out.replace('<!--SALE-->',sale_html,1)
out=out.replace('    </section>\n  </main>\n','    </section>\n\n'+ab+'  </main>\n',1)
out=out.replace('  <main id="style" hidden>',about_main+'  <main id="style" hidden>',1)
assert 'id="about"' in out
assert 'id="why2"' in out
js=js+'\n'+abjs
# script before the main script
out=out.replace('<script>\n','<script>\n'+js+'\n</script>\n<script>\n',1) if False else out.replace('</script>','</script>\n<script>\n'+js+'\n</script>',1) if False else out
i=out.rindex('</script>')
out=out[:i]+'</script>\n<script>\n'+js+'\n'+out[i:]
open('/home/claude/modelet/home.html','w',encoding='utf-8').write(out)
print(len(out))
