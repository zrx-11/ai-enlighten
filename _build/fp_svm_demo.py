# -*- coding: utf-8 -*-
"""支持向量机页的 Canvas 演示：构建时用线性 SVM 解出一族软间隔解，嵌进页面供滑块插值。"""
import json

POINTS = [
    (2.0, 2.0, 1), (2.5, 3.0, 1), (4.0, 3.5, 1),
    (3.5, 2.5, -1), (6.0, 6.0, -1), (7.0, 5.0, -1),
]

CS = [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 80.0]

def _solve_sklearn():
    import numpy as np
    from sklearn.svm import SVC
    X = np.array([[p[0], p[1]] for p in POINTS], float)
    y = np.array([p[2] for p in POINTS])
    out = []
    for c in CS:
        m = SVC(kernel="linear", C=c)
        m.fit(X, y)
        w = m.coef_[0]
        out.append({"C": c, "w": [round(float(w[0]), 4), round(float(w[1]), 4)],
                    "b": round(float(m.intercept_[0]), 4)})
    return out

def _solve_gd():
    out = []
    for c in CS:
        w1, w2, b = 0.0, 0.0, 0.0
        lr = 0.003 / max(c, 0.1)
        for _ in range(40000):
            g1, g2, gb = w1, w2, 0.0
            for x1, x2, y in POINTS:
                if y * (w1 * x1 + w2 * x2 + b) < 1:
                    g1 -= c * y * x1
                    g2 -= c * y * x2
                    gb -= c * y
            w1 -= lr * g1
            w2 -= lr * g2
            b -= lr * gb
        out.append({"C": c, "w": [round(w1, 4), round(w2, 4)], "b": round(b, 4)})
    return out

try:
    SOLUTIONS = _solve_sklearn()
except Exception:
    SOLUTIONS = _solve_gd()

DEMO_JS = r"""
(function(){
  var cv = document.getElementById('cvsvm');
  if(!cv) return;
  var ctx = cv.getContext('2d');
  var slider = document.getElementById('c');
  var lab = document.getElementById('c-val');
  var note = document.getElementById('svm-note');
  var SOL = __SOL__;
  var PTS = __PTS__;

  function Cof(v){ return 0.01 * Math.pow(10, v/50); }
  function lerp(a, b, t){ return a + (b-a)*t; }

  function model(C){
    if(C <= SOL[0].C) return SOL[0];
    if(C >= SOL[SOL.length-1].C) return SOL[SOL.length-1];
    for(var i=0;i<SOL.length-1;i++){
      if(C >= SOL[i].C && C <= SOL[i+1].C){
        var t = (Math.log(C)-Math.log(SOL[i].C))/(Math.log(SOL[i+1].C)-Math.log(SOL[i].C));
        return {w:[lerp(SOL[i].w[0],SOL[i+1].w[0],t), lerp(SOL[i].w[1],SOL[i+1].w[1],t)],
                b: lerp(SOL[i].b,SOL[i+1].b,t)};
      }
    }
    return SOL[0];
  }

  function draw(C){
    var W = cv.width, H = cv.height;
    ctx.clearRect(0,0,W,H);
    var pad = 44, side = Math.min(W-pad*2, H-pad*2);
    var ox = (W - side)/2, oy = H - pad;
    function X(v){ return ox + side*(v/10); }
    function Y(v){ return oy - side*(v/10); }

    ctx.strokeStyle='#e0dacb'; ctx.lineWidth=1;
    for(var i=0;i<=10;i+=2){
      ctx.beginPath(); ctx.moveTo(X(i),Y(0)); ctx.lineTo(X(i),Y(10)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(X(0),Y(i)); ctx.lineTo(X(10),Y(i)); ctx.stroke();
    }
    ctx.fillStyle='#6c777f'; ctx.font='13px sans-serif';
    ctx.fillText('x1', X(10)-2, oy+16);
    ctx.fillText('x2', ox-24, Y(10)+2);

    var m = model(C);
    var w1=m.w[0], w2=m.w[1], b=m.b;
    var n = Math.sqrt(w1*w1+w2*w2) || 1e-9;

    function lineAt(offset, style, dash){
      ctx.strokeStyle=style; ctx.lineWidth=2; ctx.setLineDash(dash||[]);
      ctx.beginPath();
      var first=true;
      for(var t=0;t<=1.0001;t+=0.01){
        var x1=t*10;
        if(Math.abs(w2)<1e-9) continue;
        var x2=(offset-b-w1*x1)/w2;
        if(x2<-1||x2>11){ first=true; continue; }
        var px=X(x1), py=Y(x2);
        if(first){ctx.moveTo(px,py); first=false;} else {ctx.lineTo(px,py);}
      }
      ctx.stroke(); ctx.setLineDash([]);
    }
    lineAt(0,'#b4483c',[]);
    lineAt(1,'#2a6b52',[6,4]);
    lineAt(-1,'#2a6b52',[6,4]);

    var viol=0, err=0;
    PTS.forEach(function(p){
      var v=p[2]*(w1*p[0]+w2*p[1]+b);
      if(v<1) viol++;
      if(v<0) err++;
      ctx.beginPath(); ctx.arc(X(p[0]),Y(p[1]), v<1?8:6, 0, 6.28);
      ctx.fillStyle = p[2]>0 ? '#a8442f' : '#2f5b8a';
      ctx.globalAlpha = v<1?1:0.55; ctx.fill(); ctx.globalAlpha=1;
      if(v<1){
        ctx.strokeStyle='#1c2024'; ctx.lineWidth=1.4;
        ctx.beginPath(); ctx.arc(X(p[0]),Y(p[1]),9,0,6.28); ctx.stroke();
      }
    });

    note.textContent = 'C = '+C.toFixed(2)+'｜‖w‖ = '+n.toFixed(3)
      +'｜几何间隔 2/‖w‖ = '+(2/n).toFixed(3)
      +'｜越界点 '+viol+' 个，分错 '+err+' 个（红=正类，蓝=负类，空心圈=越界）';
    lab.textContent = C.toFixed(2);
  }

  slider.addEventListener('input', function(){ draw(Cof(parseInt(slider.value,10))); });
  draw(1.0);
})();
"""

DEMO_JS = (DEMO_JS
           .replace("__SOL__", json.dumps(SOLUTIONS))
           .replace("__PTS__", json.dumps(POINTS)))
