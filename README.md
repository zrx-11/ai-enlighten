# AI 点化学习系统 · 使用与部署

两本书 → 一套能直接开学的知识库：总入口 `index.html`、每本书一份单书伴侣、Markdown 知识库，另加两份从零推导交互页。全部离线可用，不需要服务器。

## 先打开哪一页

双击 `index.html`。它是唯一的入口：顶部切换两本书与四篇跨书总览，左侧按书导航（路径 / 章节 / 概念 / 测验 / 卡片 / 术语 / 模式 / 速查），搜索覆盖全部书，学习进度保存在浏览器本地。

## 目录

| 路径 | 是什么 |
|---|---|
| `index.html` | 总学习手册，单文件，统一入口（591 KB） |
| `index.md` | 上一页的 Markdown 版导航 |
| `.nojekyll` | 关闭 Jekyll，让中文目录名与 `_` 开头目录原样托管 |
| `00-跨书总览/` | 推荐顺序、跨书概念映射、综合检验、从零推导说明（4 篇） |
| `01-人工智能导论模型与算法/` | 吴飞《人工智能导论：模型与算法》知识库 + 伴侣 HTML + manifest |
| `02-人工智能简史/` | 尼克《人工智能简史》知识库 + 伴侣 HTML + manifest |
| `03-从零推导-反向传播.html` | 单文件交互页，12 章，从导数一路推到反向传播 |
| `03-从零推导-支持向量机.html` | 单文件交互页，15 章，从点到直线距离推到对偶与核 |
| `_build/` | 构建脚本、章节正文源、KaTeX 素材、验证报告、截图 |
| `_work/` | 两本书的原始抽取文本与页面读图素材 |

## 怎么学

1. 先看 `00-跨书总览/README.md` 的推荐顺序：简史打底（知道问题怎么来的），导论加压（知道方法怎么算）。
2. 每章先读"一句话核心"，再读零基础讲解，最后做自测题；答错看解析，不通过就别进下一章。
3. 学到导论 4.6 和 6.2.3 时，打开对应的从零推导页，把公式亲手推一遍。
4. 抽认卡按"次日 / 3 天 / 7 天"复习；术语表用搜索框过滤。
5. 跨书复习看 `跨书概念映射表.md`：同一个概念在两本书里的口径常常不一样。

## 部署到 GitHub Pages

```bash
# 1. 新建仓库，把本目录全部文件放进仓库根
git init
git add .
git commit -m "AI 点化学习系统"
git branch -M main
git remote add origin git@github.com:<你的账号>/<仓库名>.git
git push -u origin main
```

2. 仓库 Settings → Pages → Source 选 `Deploy from a branch`，分支 `main`，目录 `/ (root)`，保存。
3. 等 1–2 分钟，访问 `https://<你的账号>.github.io/<仓库名>/`。

注意事项：
- `.nojekyll` 必须在仓库根，否则 `_build/`、`_work/` 会被 Jekyll 忽略，中文目录名也可能 404。
- 所有 HTML 都是单文件、无外部依赖，Pages 只做静态托管即可。
- 若页面空白，先看浏览器控制台；常见原因是仓库名带空格或中文，建议用纯英文仓库名。

## 重新构建

```bash
# 单书伴侣
python3 ~/.doubao/agent_mode/workspace/.user_skills/book-enlighten/scripts/build_companion.py \
  --manifest "01-人工智能导论模型与算法/manifest.json" \
  --out "01-人工智能导论模型与算法/ai-models-algorithms学习伴侣.html"

# 总入口
python3 ~/.doubao/agent_mode/workspace/.user_skills/book-enlighten/scripts/build_handbook.py \
  --root . --order "01,02" --cross-dir "00-跨书总览"
python3 _build/patch_index_links.py   # 把总览页里指向两份从零推导页的链接补回真实地址

# 两份从零推导页
cd _build && python3 build_fp.py bp && python3 build_fp.py svm
```

改内容只改 `_build/*_data.py`（书）或 `_build/fp_*_sections.py`（从零推导），重跑对应脚本，结果幂等。

## 自检

```bash
python3 ~/.doubao/agent_mode/workspace/.user_skills/book-enlighten/scripts/verify_handbook.py \
  --index index.html --chromium /usr/local/bin/chromium

python3 ~/.doubao/agent_mode/workspace/.user_skills/doubao-first-principles-derivation/scripts/check_render.py \
  "03-从零推导-反向传播.html"
```

当前结论：总入口 25/25 通过；两份从零推导页静态检查 0 处公式裸 `<`、全部章节通过、390px 无横向溢出。

## 已知边界

- 导论 PDF 是纯扫描件（358 页无文字层）。本套知识库按官方目录的 9 章结构写主干精讲，关键公式页（SVM、EM、A\*、因果）读图核对过；没有做 358 页逐页 OCR，因此原书的习题、附录 7 个设计实验未逐题覆盖。
- 简史 PDF 有文字层，16 章全文抽取后重组成 11 个主题章，内容覆盖全书。
- 从零推导页的数值都是自拟教学数据，正文已标注；SVM 页的 C 滑块在 12 个离线解之间插值，不是实时求解。
- 全部内容的版权归原作者与出版社，本套产物仅供个人学习使用，不要公开分发原书内容。
