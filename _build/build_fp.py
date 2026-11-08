#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把章节内容 + 内联 KaTeX 组装成单文件交互式 HTML。"""
import base64, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KATEX = os.path.join(HERE, "katex", "dist")

def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def katex_css():
    css = read(os.path.join(KATEX, "katex.min.css"))
    fdir = os.path.join(KATEX, "fonts")
    for fn in sorted(os.listdir(fdir)):
        if not fn.endswith(".woff2"):
            continue
        b64 = base64.b64encode(open(os.path.join(fdir, fn), "rb").read()).decode()
        data = "data:font/woff2;base64,%s" % b64
        css = css.replace("url(fonts/%s)" % fn, "url(%s)" % data)
        css = css.replace('url("fonts/%s")' % fn, "url(%s)" % data)
        css = css.replace("url('fonts/%s')" % fn, "url(%s)" % data)
    return css

def clean(html):
    # 修掉内容里 <span class="box-t">x</p> 这类错配
    html = re.sub(r'(<span class="box-t">[^<]*)</p>', r'\1</span>', html)
    html = re.sub(r'(<b>[^<]*)</p>', r'\1</b>', html)
    # 矩阵行分隔：单反斜杠 \[2pt] 修正为 \\
    html = html.replace("\\[2pt]", "\\\\[2pt]")
    # 未闭合的 <b> 在段落结尾
    html = re.sub(r'(<b>)([^<]{1,40})\n', r'\1\2</b>\n', html)
    return html

CSS = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.75;color:#1c2024;background:#fbfaf7}
#topbar{position:fixed;top:0;left:0;right:0;height:52px;display:flex;align-items:center;gap:8px;padding:0 10px;background:#1f272e;color:#f2efe6;z-index:30}
#topbar button{background:#33414b;color:#f2efe6;border:0;border-radius:8px;padding:7px 10px;font-size:14px;min-width:38px}
#topbar .now{flex:1;font-size:13px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;opacity:.92}
#main{padding:64px 14px 80px;max-width:820px;margin:0 auto}
.chap{display:none}
.chap.on{display:block}
.breadcrumb{font-size:12px;color:#6c777f;margin-bottom:6px;letter-spacing:.02em}
.breadcrumb b{color:#2a6b52}
h1{font-size:22px;line-height:1.4;margin:2px 0 14px;font-weight:700}
h3{font-size:16px;margin:22px 0 8px;color:#24485c;border-left:3px solid #2a6b52;padding-left:8px}
p{margin:0 0 12px;overflow-wrap:break-word}
.lead{font-size:15.5px;color:#33414b;background:#fff;border-left:4px solid #2a6b52;padding:10px 12px;border-radius:0 6px 6px 0}
.box{margin:14px 0;padding:10px 12px;border-radius:8px;font-size:14.5px;line-height:1.7}
.box-t{display:inline-block;font-weight:700;margin-right:6px;font-size:12px;padding:1px 6px;border-radius:4px;color:#fff;background:#2a6b52}
.box.yellow{background:#fdf7e3;border-left:4px solid #d8a72a}
.box.yellow .box-t{background:#d8a72a}
.box.green{background:#eef6ef;border-left:4px solid #2a6b52}
.box.red{background:#fbeceb;border-left:4px solid #b4483c}
.box.red .box-t{background:#b4483c}
.tree{margin:14px 0}
.tier{margin:0 0 6px;padding:7px 10px;background:#fff;border:1px solid #e3ded2;border-radius:6px;font-size:14px}
.tier-t{display:inline-block;min-width:66px;font-weight:700;color:#2a6b52;font-size:12px}
.math{overflow-x:auto;overflow-y:hidden;margin:10px 0;padding:2px 0;-webkit-overflow-scrolling:touch}
@media(max-width:767px){.math .katex-display{font-size:.86em}.math{font-size:.93em}}
.note{font-size:13.5px;color:#5a6670;background:#f3f1ea;padding:8px 10px;border-radius:6px}
table.calc{width:100%;border-collapse:collapse;font-size:12.8px;margin:12px 0}
table.calc.num{display:block;overflow-x:auto}
table.calc.num th,table.calc.num td{white-space:nowrap}
table.calc th,table.calc td{border:1px solid #ded8cb;padding:6px 8px;text-align:left;white-space:normal;word-break:break-word}
table.calc th{background:#f1efe7;font-weight:700}
.chapter-nav{display:flex;gap:10px;justify-content:space-between;margin:28px 0 0;padding-top:14px;border-top:1px dashed #d7d1c4}
.chapter-nav button{flex:1;padding:10px;font-size:14px;background:#fff;border:1px solid #cfc9bb;border-radius:8px;color:#24485c}
.chapter-nav button:disabled{opacity:.4}
.demo{margin:16px 0;padding:12px;background:#fff;border:1px solid #e3ded2;border-radius:10px}
.demo-t{font-weight:700;font-size:14px;margin-bottom:8px;color:#24485c}
.demo canvas{width:100%;height:auto;display:block;background:#fcfbf6;border-radius:6px;touch-action:none}
.demo-ctl{margin-top:10px;font-size:13px}
.demo-ctl input[type=range]{width:100%;margin:8px 0 2px}
.axis-note{color:#6c777f;font-size:12px}
.demo-note{margin-top:6px;font-size:13px;color:#33414b}
.quiz{margin:14px 0;padding:10px 12px;background:#fff;border:1px solid #e3ded2;border-radius:8px;font-size:14px}
.quiz .q{font-weight:600;margin-bottom:6px}
.quiz .opt{color:#33414b;margin-bottom:8px}
.quiz .ans{display:none;background:#f1f6f1;border-left:3px solid #2a6b52;padding:8px 10px;border-radius:0 6px 6px 0;font-size:13.5px}
.quiz.open .ans{display:block}
.quiz button.rev{margin-top:6px;background:#eee9dc;border:0;border-radius:6px;padding:6px 10px;font-size:13px}
#scrim{position:fixed;inset:0;background:rgba(20,26,30,.45);display:none;z-index:40}
#sidebar{position:fixed;top:0;left:0;bottom:0;width:80%;max-width:330px;background:#f6f3ea;z-index:41;transform:translateX(-102%);transition:transform .22s;overflow-y:auto;padding:14px}
#sidebar.on{transform:none}
.sb-title{font-size:12px;color:#6c777f;letter-spacing:.08em;margin:6px 0 10px;text-transform:uppercase}
#toc a{display:block;padding:9px 10px;margin-bottom:4px;background:#fff;border-radius:7px;color:#24485c;text-decoration:none;font-size:14px;border:1px solid #e6e0d3}
#toc a.cur{background:#2a6b52;color:#fff;border-color:#2a6b52}
@media(min-width:768px){
 body{font-size:16.5px}
 #topbar{left:300px}
 #topbar .now{font-size:14px}
 #sidebar{width:300px;transform:none;max-width:none;border-right:1px solid #e3ded2}
 #scrim{display:none!important}
 #main{margin:0 20px 0 320px;max-width:860px;padding-top:70px}
 #topbar .menu{display:none}
 h1{font-size:26px}
}
"""

JS = """
(function(){
  var CH = __ORDER__;
  var cur = 0;
  var bar = document.getElementById('topbar');
  var nowEl = bar.querySelector('.now');
  var sidebar = document.getElementById('sidebar');
  var scrim = document.getElementById('scrim');

  function sec(i){ return document.getElementById(CH[i]); }

  function render(el, tries){
    if(!el) return;
    if(window.renderMathInElement){
      try{ renderMathInElement(el, {delimiters:[
        {left:'$$',right:'$$',display:true},
        {left:'$',right:'$',display:false}
      ], throwOnError:false}); }catch(e){}
      return;
    }
    tries = (tries||0) + 1;
    if(tries < 40){ setTimeout(function(){ render(el, tries); }, 200); }
  }

  function show(i){
    if(i < 0 || i >= CH.length) return;
    var old = sec(cur); if(old) old.classList.remove('on');
    cur = i;
    var el = sec(cur);
    el.classList.add('on');
    nowEl.textContent = el.getAttribute('data-title');
    var links = document.querySelectorAll('#toc a');
    for(var k=0;k<links.length;k++){
      links[k].classList.toggle('cur', k===i);
    }
    var prev = el.querySelector('.chapter-nav .prev');
    var next = el.querySelector('.chapter-nav .next');
    if(prev) prev.disabled = (cur===0);
    if(next) next.disabled = (cur===CH.length-1);
    render(el, 0);
    window.scrollTo(0,0);
    closeSb();
  }

  function openSb(){ sidebar.classList.add('on'); scrim.style.display='block'; }
  function closeSb(){ sidebar.classList.remove('on'); scrim.style.display='none'; }

  document.addEventListener('click', function(ev){
    var t = ev.target;
    if(t.closest('.menu')){ openSb(); return; }
    if(t.closest('.prev-top')){ show(cur-1); return; }
    if(t.closest('.next-top')){ show(cur+1); return; }
    if(t === scrim){ closeSb(); return; }
    var a = t.closest('#toc a');
    if(a){ ev.preventDefault(); show(parseInt(a.getAttribute('data-i'),10)); return; }
    var q = t.closest('.quiz');
    if(q && t.tagName === 'BUTTON'){ q.classList.toggle('open'); return; }
    // 章节内导航用 querySelector 在所属 chapter 里找按钮
    var nb = t.closest('.chapter-nav button');
    if(nb){
      var chap = nb.closest('.chap');
      var idx = CH.indexOf(chap.id);
      if(nb.classList.contains('prev')) show(idx-1); else show(idx+1);
      return;
    }
  });
  document.addEventListener('keydown', function(ev){
    if(ev.key==='ArrowLeft') show(cur-1);
    if(ev.key==='ArrowRight') show(cur+1);
    if(ev.key==='Escape') closeSb();
  });

  // 初次：先把所有章节都渲染一遍（含隐藏的），再显示第一章
  CH.forEach(function(id){ render(document.getElementById(id), 0); });
  show(0);
  __DEMO__
})();
"""

def build(name, subtitle, sections, demos="", order_hint=""):
    items, toc = [], []
    for i, s in enumerate(sections):
        body = clean(s["body"])
        items.append(
            '<section class="chap" id="%s" data-title="%s">\n'
            '<div class="breadcrumb">%s · 从零推导 / <b>%s</b></div>\n'
            '<h1>%s</h1>\n%s\n'
            '<div class="chapter-nav"><button class="prev">← 上一章</button>'
            '<button class="next">下一章 →</button></div>\n'
            '</section>' % (s["id"], s["title"], name, s["title"], s["title"], body)
        )
        toc.append('<a href="#%s" data-i="%d">%s</a>' % (s["id"], i, s["title"]))

    order = json.dumps([s["id"] for s in sections], ensure_ascii=False)
    js = JS.replace("__ORDER__", order).replace("__DEMO__", demos)
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s · 从零推导</title>
<style>%s
%s
</style>
</head>
<body>
<header id="topbar">
  <button class="menu" aria-label="目录">☰</button>
  <button class="prev-top" aria-label="上一章">←</button>
  <div class="now">加载中…</div>
  <button class="next-top" aria-label="下一章">→</button>
</header>
<div id="scrim"></div>
<aside id="sidebar">
  <div class="sb-title">%s · 目录</div>
  <nav id="toc">%s</nav>
</aside>
<main id="main">
%s
</main>
<script>%s</script>
<script>%s</script>
<script>%s</script>
</body>
</html>""" % (
        name, CSS, katex_css(),
        name, "\n".join(toc), "\n".join(items),
        read(os.path.join(KATEX, "katex.min.js")),
        read(os.path.join(KATEX, "contrib", "auto-render.min.js")),
        js,
    )
    return html


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "bp"
    if which == "bp":
        sys.path.insert(0, HERE)
        import fp_bp_sections as M
        import fp_bp_demo as D
        html = build("反向传播", "", M.SECTIONS, D.DEMO_JS)
        out = os.path.join(os.path.dirname(HERE), "03-从零推导-反向传播.html")
    else:
        sys.path.insert(0, HERE)
        import fp_svm_sections as M
        import fp_svm_demo as D
        html = build("支持向量机", "", M.SECTIONS, D.DEMO_JS)
        out = os.path.join(os.path.dirname(HERE), "03-从零推导-支持向量机.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("写出", out, "%.0f KB" % (os.path.getsize(out) / 1024))

if __name__ == "__main__":
    main()
