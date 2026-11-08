# -*- coding: utf-8 -*-
"""反向传播页的 Canvas 演示 JS"""

DEMO_JS = r"""
(function(){
  var cv = document.getElementById('cvbp');
  if(!cv) return;
  var ctx = cv.getContext('2d');
  var slider = document.getElementById('eta');
  var lab = document.getElementById('eta-val');
  var note = document.getElementById('bp-note');

  function sim(eta, steps){
    var w = 2.0, x = 1.0, y = 3.0, hist = [];
    for(var k=0;k<steps;k++){
      var pred = w*x;
      var loss = 0.5*Math.pow(pred-y,2);
      hist.push({w:w, loss:loss});
      var g = (pred - y) * x;
      w = w - eta*g;
      if(!isFinite(w) || Math.abs(w) > 500) { hist.push({w:w,loss:NaN}); break; }
    }
    return hist;
  }

  function draw(eta){
    var hist = sim(eta, 30);
    var W = cv.width, H = cv.height;
    ctx.clearRect(0,0,W,H);
    var padL=56, padR=18, padT=20, padB=40;
    var plotW = W-padL-padR, plotH = H-padT-padB;

    ctx.strokeStyle='#e0dacb'; ctx.lineWidth=1;
    for(var i=0;i<=5;i++){
      var y = padT + plotH*i/5;
      ctx.beginPath(); ctx.moveTo(padL,y); ctx.lineTo(W-padR,y); ctx.stroke();
    }
    for(var j=0;j<=6;j++){
      var xx = padL + plotW*j/6;
      ctx.beginPath(); ctx.moveTo(xx,padT); ctx.lineTo(xx,H-padB); ctx.stroke();
    }
    ctx.fillStyle='#5a6670'; ctx.font='13px sans-serif';
    ctx.fillText('损失', 6, padT+12);
    ctx.fillText('0.5', 26, padT+8);
    ctx.fillText('0', 34, padT+plotH+4);
    ctx.fillText('轮次 0', padL-6, H-12);
    ctx.fillText('30', W-padR-14, H-12);
    ctx.fillText('w 起点 2.0，目标 3.0', padL+4, H-12);

    var maxLoss = 0.5;
    ctx.strokeStyle='#2a6b52'; ctx.lineWidth=2; ctx.beginPath();
    for(var k=0;k<hist.length;k++){
      var L = hist[k].loss;
      if(!isFinite(L) || L > 3) break;
      var px = padL + plotW * (k/30);
      var py = padT + plotH * (1 - Math.min(1, L/maxLoss*0.9));
      if(k===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
    }
    ctx.stroke();
    ctx.fillStyle='#2a6b52';
    for(var k2=0;k2<hist.length;k2+=5){
      var L2 = hist[k2].loss; if(!isFinite(L2) || L2>3) break;
      var px2 = padL + plotW*(k2/30);
      var py2 = padT + plotH*(1 - Math.min(1, L2/maxLoss*0.9));
      ctx.beginPath(); ctx.arc(px2,py2,3,0,6.28); ctx.fill();
    }

    var last = hist[hist.length-1];
    var txt;
    if(eta > 2.0){
      txt = '学习率 ' + eta.toFixed(2) + ' 过大：w 来回越过目标，损失震荡不下降。';
    } else if(isFinite(last.loss)) {
      txt = '第 ' + (hist.length-1) + ' 轮：w = ' + last.w.toFixed(3) + '，损失 = ' + last.loss.toFixed(4) + '。';
      if(last.w > 2.99 && last.w < 3.01) txt += ' 已基本收敛。';
    } else {
      txt = '学习率 ' + eta.toFixed(2) + ' 过大，数值发散。';
    }
    note.textContent = txt;
    lab.textContent = eta.toFixed(2);
  }

  slider.addEventListener('input', function(){
    draw(parseInt(slider.value,10)/100);
  });
  draw(0.10);
})();
"""
