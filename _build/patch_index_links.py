# -*- coding: utf-8 -*-
"""build_handbook.py 会把相对 .html 链接清成 #，这里在生成后补回真实链接。"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "index.html")

PAIRS = [
    ("03-从零推导-反向传播.html", "反向传播"),
    ("03-从零推导-支持向量机.html", "支持向量机"),
]

def main():
    with open(IDX, encoding="utf-8") as f:
        h = f.read()
    changed = 0
    for fn, _ in PAIRS:
        pat = "<td>%s（与 index.html 同目录）<" % fn
        if pat not in h:
            continue
        rep = ("<td><a href='./%s' target='_blank' rel='noopener'>%s</a>（与 index.html 同目录）<"
               % (fn, fn))
        h = h.replace(pat, rep)
        changed += 1
    with open(IDX, "w", encoding="utf-8") as f:
        f.write(h)
    print("补回链接 %d 处" % changed)

if __name__ == "__main__":
    main()
