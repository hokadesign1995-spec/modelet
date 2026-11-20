(function(){
var SP=/*SPRITES*/{},AS=/*ASPECT*/{},M=window.__md;
var tr=document.getElementById('lkTrack');if(!tr||!M)return;
var LOOKS=[['purple','ست بنفش نرم',[101,102]],['grayman','ست روزمره',[103,104,105]],['blackcoat','کت مشکی شهری',[106,107]],['maroon','ست پاییزی',[108]],['younggray','استایل خاکستری',[109,110,111]],['navydrape','شب سرمه‌ای',[112]]];
var N=LOOKS.length,act=0,hov=false,vis=true,timer=0,fav={};
var stage=document.getElementById('lkStage'),row=document.getElementById('lkRow'),seg=document.getElementById('lkSeg'),ring=document.getElementById('lkRing');
var els=LOOKS.map(function(L,i){var d=document.createElement('div');d.className='lk2-m';
 var im=new Image();im.src=SP[L[0]];im.alt=L[1];im.draggable=false;d.appendChild(im);
 d.addEventListener('click',function(){if(i!==act){go(i);restart()}});row.appendChild(d);return d});
LOOKS.forEach(function(L,i){var b=document.createElement('button');b.setAttribute('aria-label',L[1]);b.addEventListener('click',function(){go(i);restart()});seg.appendChild(b)});
var HEART='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.2-9.3C1.7 8 3.6 5 6.8 5c2 0 3.7 1.1 5.2 3 1.5-1.9 3.2-3 5.2-3 3.2 0 5.1 3 4 6.2-1.7 4.7-9.2 9.3-9.2 9.3z"/></svg>';
var STEP=[0,.2,.36,.49,.59],SC=[1,.66,.52,.42,.34],BL=[0,4,7,9,11],OP=[1,.92,.72,.5,.3];
function layout(){var W=stage.clientWidth,Hh=stage.clientHeight,mob=W<861,rowH=row.clientHeight||Hh;
 var colW=mob?0:212,span=W-colW,ax=mob?W*.4:colW+span*.3,mh=mob?rowH*.9:rowH*.86;
 els.forEach(function(e,i){var L=LOOKS[i],k=(i-act+N)%N,w=mh*(AS[L[0]]||.27);
  e.style.height=mh+'px';e.style.width=w+'px';e.style.bottom=mob?'4%':'8%';
  var x,s,b,o,z;
  if(k<5){x=mob?ax+W*.6*STEP[k]*1.5:ax+span*STEP[k];s=SC[k];b=BL[k];o=OP[k];z=10-k}
  else if(k===N-1){x=ax-span*.18;s=1.04;b=6;o=0;z=1}
  else{x=ax+span*.7;s=.28;b=12;o=0;z=1}
  e.style.transform='translateX('+(x-w/2).toFixed(1)+'px) scale('+s+')';e.style.filter=b?'blur('+b+'px)':'none';e.style.opacity=o;e.style.zIndex=z;e.style.pointerEvents=o<.2?'none':'auto'})}
function render(){var L=LOOKS[act],list=document.getElementById('lkList');
 document.getElementById('lkNo').textContent='ست '+M.fa(('0'+(act+1)).slice(-2));document.getElementById('lkName').textContent=L[1];
 var tot=0;list.innerHTML=L[2].map(function(id,k){var p=M.byId(id);tot+=p.price;
  return '<div class="lk2-it" style="animation-delay:'+(k*.08)+'s" data-id="'+id+'"><button class="th" aria-label="'+p.name+'">'+M.art(p)+'</button><h4>'+p.name+'</h4><div class="p">'+M.money(p.price)+'</div><button class="hr'+(fav[id]?' on':'')+'" aria-label="علاقه‌مندی">'+HEART+'</button><button class="pl" aria-label="افزودن به سبد">+</button></div>'}).join('');
 list.querySelectorAll('.lk2-it').forEach(function(it){var id=+it.dataset.id;
  it.querySelector('.th').addEventListener('click',function(){M.openModal(id)});
  it.querySelector('.hr').addEventListener('click',function(){fav[id]=!fav[id];this.classList.toggle('on',!!fav[id])});
  it.querySelector('.pl').addEventListener('click',function(){M.addToCart(id,M.byId(id).sizes[0])})});
 document.getElementById('lkSave').textContent=L[2].length>1?'هر '+M.fa(L[2].length)+' قطعه با ۱۰٪ تخفیف':'با ۱۰٪ تخفیف ست';
 document.getElementById('lkOld').textContent=M.money(tot);document.getElementById('lkNew').textContent=M.money(Math.round(tot*.9/1000)*1000);
 [].forEach.call(seg.children,function(b,i){b.classList.toggle('on',i===act)})}
function go(i){act=(i+N)%N;layout();render()}
function restart(){clearInterval(timer);timer=setInterval(function(){if(!hov&&vis&&!document.hidden)go(act+1)},3800)}
document.getElementById('lkPrev').addEventListener('click',function(){go(act-1);restart()});
document.getElementById('lkNext').addEventListener('click',function(){go(act+1);restart()});
document.getElementById('lkAll').addEventListener('click',function(){LOOKS[act][2].forEach(function(id){M.addToCart(id,M.byId(id).sizes[0])})});
stage.addEventListener('mouseenter',function(){hov=true});stage.addEventListener('mouseleave',function(){hov=false;stage.classList.remove('ring')});
var fine=window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches;
if(fine){stage.addEventListener('mousemove',function(e){var r=stage.getBoundingClientRect();stage.classList.add('ring');ring.style.transform='translate('+(e.clientX-r.left)+'px,'+(e.clientY-r.top)+'px)';ring.classList.toggle('big',!!(e.target.closest&&e.target.closest('button,.lk2-m')))})}
var tx=0;stage.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});stage.addEventListener('touchend',function(e){var d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50){go(act+(d<0?1:-1));restart()}},{passive:true});
if('IntersectionObserver' in window)new IntersectionObserver(function(en){vis=en[0].isIntersecting}).observe(tr);
window.addEventListener('resize',layout);
layout();render();restart();
setTimeout(layout,300);
})();
