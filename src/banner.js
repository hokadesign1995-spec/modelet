(function(){var root=document.getElementById('banSl');if(!root)return;
 var S=[].slice.call(root.querySelectorAll('.ban-s')),dots=document.getElementById('banDots'),a=0,tm=0,paused=false;
 S.forEach(function(s,i){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','اسلاید '+(i+1));b.addEventListener('click',function(){go(i);rs()});dots.appendChild(b)});
 function go(i){a=(i+S.length)%S.length;S.forEach(function(s,k){s.classList.toggle('on',k===a);s.setAttribute('aria-hidden',k===a?'false':'true')});[].forEach.call(dots.children,function(b,k){b.classList.toggle('on',k===a)})}
 function rs(){clearInterval(tm);tm=setInterval(function(){if(!paused&&!document.hidden)go(a+1)},5500)}
 document.getElementById('banPrev').addEventListener('click',function(){go(a+1);rs()});
 document.getElementById('banNext').addEventListener('click',function(){go(a-1);rs()});
 root.addEventListener('mouseenter',function(){paused=true});root.addEventListener('mouseleave',function(){paused=false});
 var sx=null;root.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
 root.addEventListener('touchend',function(e){if(sx==null)return;var d=e.changedTouches[0].clientX-sx;sx=null;if(Math.abs(d)>40){go(a+(d<0?1:-1));rs()}});
 go(0);rs()})();
(function(){[].forEach.call(document.querySelectorAll('#banSl [data-cat]'),function(b){b.addEventListener('click',function(){window.__md.goCat(b.dataset.cat)})})})();
