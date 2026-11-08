# -*- coding: utf-8 -*-
"""支持向量机：从零推导 —— 章节内容"""

SECTIONS = []

def add(sid, title, body):
    SECTIONS.append({"id": sid, "title": title, "body": body})

add("s01", "知识树：从“一条线”到“一个优化问题”", """
<p class="lead">支持向量机（SVM）想做的事，一句话就能说完：<b>把两类点分开，并且让这条分界线离两边都尽量远</b>。难的是怎么把"尽量远"写成一个能算的数学问题。</p>

<div class="box yellow"><span class="box-t">前置知识</span>本课假设你会：四则运算、平方、开方、解一元二次方程、看坐标平面。矩阵、拉格朗日乘子、KKT 这些都会从零补。</p>

<div class="tree">
<div class="tier"><span class="tier-t">根系</span>坐标 · 直线方程 · 距离 · 平方与开方 · 一元二次方程</div>
<div class="tier"><span class="tier-t">第一层</span>向量 · 内积 · 模长（"长度"的向量版）</div>
<div class="tier"><span class="tier-t">第二层</span>点到直线的距离（本课要亲手推出来）</div>
<div class="tier"><span class="tier-t">第三层</span>分类问题 · 标签 ±1 · 函数间隔与几何间隔</div>
<div class="tier"><span class="tier-t">第四层</span>约束优化 · 拉格朗日乘子 · KKT 条件</div>
<div class="tier"><span class="tier-t">主干</span>最大间隔 · 对偶问题 · 支持向量 · 软间隔 · 核技巧</div>
</div>

<p class="note">明确声明本课<b>不涉及</p>：测度论、泛函分析、SMO 的工程实现细节。这些不补也不影响理解主干。</p>
""")

add("s02", "第一层：向量、内积、模长", """
<p class="lead">先把三样工具备齐。它们都只是"把初中的长度概念搬到多个维度"。</p>

<h3>1. 向量</h3>
<p>一个向量就是一串有序的数，写成 $\\mathbf{x}=(x_1,x_2)$ 或竖着写。它有两个解释：一个<b>点</b>（在平面上的位置），或者一个<b>箭头</b>（从原点指向那个点）。两种解释在计算上没区别。</p>

<h3>2. 内积</h3>
<div class="math">$$\\mathbf{w}\\cdot\\mathbf{x}=w_1x_1+w_2x_2$$</div>
<p>对应位置相乘再相加，结果是一个<b>数</b>，不是向量。手算：$\\mathbf{w}=(1,1)$，$\\mathbf{x}=(3,-1)$，内积 $=1\\times3+1\\times(-1)=2$。</p>

<h3>3. 模长</h3>
<div class="math">$$\\|\\mathbf{w}\\|=\\sqrt{\\mathbf{w}\\cdot\\mathbf{w}}=\\sqrt{w_1^2+w_2^2}$$</div>
<p>这就是勾股定理。$\\mathbf{w}=(1,1)$ 的模长是 $\\sqrt{1+1}=\\sqrt2\\approx1.414$。</p>

<h3>4. 内积的几何意义（关键）</h3>
<p>内积等于"一个向量在另一个方向上的投影长度 × 另一个的长度"。这条性质后面解释"为什么 $\\mathbf{w}$ 垂直于分界线"时要用。</p>
<div class="box green"><span class="box-t">记住这个数</span>$\\|\\mathbf{w}\\|=\\sqrt2$ 时，$2/\\|\\mathbf{w}\\|=\\sqrt2\\approx1.414$。这个数字会在 s09 节的算例里反复出现。</div>
""")

add("s03", "第二层：直线方程与“点到直线的距离”（亲手推）", """
<p class="lead">SVM 的分界线在二维是一条直线，在多维是一个超平面。它的方程只有一种写法：$\\mathbf{w}\\cdot\\mathbf{x}+b=0$。</p>

<h3>1. 为什么这个写法能表示直线</h3>
<p>取 $\\mathbf{w}=(1,1)$、$b=-3$，方程是 $x_1+x_2-3=0$。点 $(2,1)$ 代入得 $2+1-3=0$，在线上；点 $(2,2)$ 代入得 $1>0$，在线的一侧；点 $(0,0)$ 代入得 $-3<0$，在另一侧。<b>正负号就代表"在哪一侧"</b>。</p>

<h3>2. $\\mathbf{w}$ 为什么垂直于这条线</h3>
<p>在线上取两个点 $\\mathbf{x}_A$、$\\mathbf{x}_B$，它们都满足 $\\mathbf{w}\\cdot\\mathbf{x}+b=0$，相减得：</p>
<div class="math">$$\\mathbf{w}\\cdot(\\mathbf{x}_A-\\mathbf{x}_B)=0$$</div>
<p>$\\mathbf{x}_A-\\mathbf{x}_B$ 是沿着线的一个方向。内积为 0 说明 $\\mathbf{w}$ 与线的方向垂直。所以 <b>$\\mathbf{w}$ 就是法向量</b>——这也是"$\\mathbf{w}$ 的长度决定间隔"的根源。</p>

<h3>3. 点到直线的距离（推导，不跳步）</h3>
<p>设点 $\\mathbf{x}_0$ 到直线 $\\mathbf{w}\\cdot\\mathbf{x}+b=0$ 的距离是 $d$。做法：从 $\\mathbf{x}_0$ 沿法向走到线上，落点记为 $\\mathbf{x}_1$。</p>
<p>因为走的方向是 $\\mathbf{w}$ 的方向，所以 $\\mathbf{x}_1=\\mathbf{x}_0-t\\mathbf{w}$，其中 $t$ 是某个正数，走的距离就是 $d=t\\|\\mathbf{w}\\|$。</p>
<p>把 $\\mathbf{x}_1$ 代入直线方程：</p>
<div class="math">$$\\mathbf{w}\\cdot(\\mathbf{x}_0-t\\mathbf{w})+b=0$$</div>
<p>展开：$\\mathbf{w}\\cdot\\mathbf{x}_0-t\\,\\mathbf{w}\\cdot\\mathbf{w}+b=0$，即 $\\mathbf{w}\\cdot\\mathbf{x}_0+b=t\\|\\mathbf{w}\\|^2$。</p>
<p>所以 $t=\\dfrac{\\mathbf{w}\\cdot\\mathbf{x}_0+b}{\\|\\mathbf{w}\\|^2}$，代入 $d=t\\|\\mathbf{w}\\|$：</p>
<div class="math">$$d=\\frac{|\\mathbf{w}\\cdot\\mathbf{x}_0+b|}{\\|\\mathbf{w}\\|}$$</div>

<p><b>数值验证：</b>直线 $x_1+x_2-3=0$（$\\mathbf{w}=(1,1)$，$b=-3$），点 $(2,2)$。分子 $=|2+2-3|=1$，分母 $=\\sqrt2$，距离 $=0.707$。用几何看：这条线过 $(3,0)$ 与 $(0,3)$，点 $(2,2)$ 到它的垂直距离确实约 $0.707$，对得上。</p>

<div class="box red"><span class="box-t">这一步是整课的地基</span>后面所有的"间隔"，都是这个距离公式的变形。推不出来就卡死，不要跳过。</div>
""")

add("s04", "第三层：分类问题，以及标签为什么取 +1 和 −1", """
<p class="lead">先明确任务：给一堆点，每个点有坐标和一个类别，要找一个分界线，把两类分开。</p>

<h3>1. 任务形式化</h3>
<p>训练集是 $(\\mathbf{x}_i,y_i)$，$i=1,\\dots,n$。$\\mathbf{x}_i$ 是坐标，$y_i\\in\\{+1,-1\\}$ 是类别。要找 $\\mathbf{w},b$，使得：</p>
<div class="math">$$y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)>0\\quad\\text{对所有 }i$$</div>
<p>读法：如果 $y_i=+1$（正类），要求 $\\mathbf{w}\\cdot\\mathbf{x}_i+b>0$；如果 $y_i=-1$（负类），要求它 $<0$。乘上 $y_i$ 之后，两种情况都变成"大于 0"，一句话就能写完。</p>

<h3>2. 为什么不取 0 和 1</h3>
<p>如果标签取 $\\{0,1\\}$，就要分两种情况写条件：正类要求 $>0$，负类要求 $<0$。写成一个式子需要分段函数，没法直接做优化。</p>
<p>取 $\\pm1$ 之后，$y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)$ 这一个量同时编码了"预测对不对"和"离边界有多远"：</p>
<table class="calc">
<tr><th>情况</th><th>$y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)$</th><th>含义</th></tr>
<tr><td>分对且离得远</td><td>大的正数</td><td>很安全</td></tr>
<tr><td>分对但贴着边界</td><td>接近 0 的正数</td><td>勉强</td></tr>
<tr><td>分错</td><td>负数</td><td>错了，绝对值越大错得越离谱</td></tr>
</table>
<p>这就是 SVM 一个漂亮的设计：<b>用符号表示对错，用大小表示置信度</b>，一个数干两件事。</p>

<div class="box red"><span class="box-t">别以为</p>标签取 $\pm1$ 只是"习惯"。换成 $\{0,1\}$ 整套推导都要重写，而且没有了"距离"这个信息。<b>这是为了后续优化服务的编码选择，不是约定。</div>
""")

add("s05", "函数间隔与几何间隔：同一件事的两种尺度", """
<p class="lead">"离边界多远"有兩種量法，一定要分清，否则后面会以为推导跳步了。</p>

<h3>1. 函数间隔</h3>
<div class="math">$$\\hat{\\gamma}_i=y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)$$</div>
<p>就是上面那个量。它有个致命问题：<b>把 $\\mathbf{w}$ 和 $b$ 同时乘 2，这个值也乘 2，但直线一点没变</b>。</p>

<h3>2. 参数规范化的具体演示</h3>
<p>下面两组参数画的是<b>同一条直线</b>：</p>
<table class="calc">
<tr><th>参数</th><th>方程</th><th>点 $(2,2)$ 处的函数间隔</th><th>几何距离</th></tr>
<tr><td>$\\mathbf{w}=(1,1),b=-3$</td><td>$x_1+x_2-3=0$</td><td>$1$</td><td>$1/\\sqrt2\\approx0.707$</td></tr>
<tr><td>$\\mathbf{w}=(2,2),b=-6$</td><td>$2x_1+2x_2-6=0$</td><td>$2$</td><td>$2/\\sqrt8\\approx0.707$</td></tr>
</table>
<p>函数间隔从 1 变成 2，几何距离不变。所以函数间隔没有几何意义，<b>不能直接拿来比较"哪个分界线更好"</b>。</p>

<h3>3. 几何间隔</h3>
<div class="math">$$\\gamma_i=\\frac{y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)}{\\|\\mathbf{w}\\|}$$</div>
<p>就是距离公式加上符号。它对缩放不变：$\\mathbf{w},b$ 同乘 2，分子分母同时乘 2，结果不变。</p>

<p><b>结论：</b>要比较不同的分界线，必须用几何间隔。而"参数规范化"的意思是：既然缩放不影响几何间隔，那我们就<b>约定</b>让最近点的函数间隔恰好等于 1，用这个约定消掉缩放自由度。</p>
<div class="box green"><span class="box-t">这就是为什么</p>后面会出现 $y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)\\ge1$ 这个约束。它不是凭空来的，是"把尺子固定住"的操作。</div>
""")

add("s06", "主干：最大化间隔，为什么变成最小化 w 的长度", """
<p class="lead">"让分界线离两边都尽量远"这句话，翻译成数学只要三步。</p>

<h3>第 1 步：写出间隔</h3>
<p>规范化之后，最近点的函数间隔是 1，所以最近点的几何距离是 $\\dfrac{1}{\\|\\mathbf{w}\\|}$。两类各有一侧，所以两侧之间的总宽度（叫间隔，margin）是：</p>
<div class="math">$$\\text{margin}=\\frac{2}{\\|\\mathbf{w}\\|}$$</div>

<h3>第 2 步：最大化它</h3>
<p>要 $\\dfrac{2}{\\|\\mathbf{w}\\|}$ 最大，等价于让 $\\|\\mathbf{w}\\|$ <b>最小</b>（分母越小，分数越大）。</p>

<h3>第 3 步：换成好算的形式</h3>
<p>$\\|\\mathbf{w}\\|$ 带根号，求导麻烦。因为最小化和平方是同一件事（都是正数），改成最小化 $\\|\\mathbf{w}\\|^2$；再乘 $\\frac12$ 让求导时系数干净：</p>
<div class="math">$$\\min_{\\mathbf{w},b}\\ \\frac12\\|\\mathbf{w}\\|^2\\quad\\text{s.t.}\\quad y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)\\ge1,\\ i=1,\\dots,n$$</div>

<p>读法：在"所有点都被正确分类且离边界至少 1（函数间隔）"的约束下，让 $\\mathbf{w}$ 的长度尽可能小。</p>

<div class="box red"><span class="box-t">为什么是"最大化间隔"而不是"最小化错误"</p>因为如果只要求分对，会有无穷多条线满足（稍微转一点还是分对）。加"尽量远离两边"这个要求，解才唯一。这是 SVM 与"只要分对就行"的逻辑回归的关键差别：<b>SVM 选的是最安全的那条，不是任意一条。</b></div>

<h3>数值预告</h3>
<p>$\\mathbf{w}=(1,1)$，$\\|\\mathbf{w}\\|=\\sqrt2$，间隔 $=2/\\sqrt2=\\sqrt2\\approx1.414$。s09 节会用完整算例验证这个数。</p>
""")

add("s07", "约束优化与拉格朗日乘子（围栏类比）", """
<p class="lead">现在的问题是"带约束的最小化"。需要一台机器把约束塞进目标函数里，这台机器叫拉格朗日乘子。</p>

<h3>1. 先看一个能画图的例子</h3>
<p>求 $\\min x^2+y^2$，约束 $x+y=2$。</p>
<p>几何上：目标函数的等高线是以原点为圆心的圆，约束是一条直线。圆越小越好，但必须碰到直线。最优时圆与直线<b>相切</p>，此时圆的法向（梯度）与直线的法向平行。</p>
<p>"梯度平行"就是拉格朗日乘子的全部内容：</p>
<div class="math">$$\\nabla f=\\lambda\\nabla g$$</div>
<p>这里 $f=x^2+y^2$，$g=x+y-2$。算出 $\\nabla f=(2x,2y)$，$\\nabla g=(1,1)$，所以 $2x=\\lambda$、$2y=\\lambda$，得 $x=y$。代入约束 $x=y=1$，最小值 $2$。</p>

<h3>2. 围栏类比</h3>
<p>你在草地上想走到最低点，但有一圈围栏不许出去。如果最低点在围栏内，你直接走过去（约束不起作用，$\\lambda=0$）。如果最低点在围栏外，你会<b>贴着围栏</p>停下，此时你往下走的力被围栏的法向力抵消，两个力方向相反、大小成比例——比例系数就是 $\\lambda$。</p>
<div class="box red"><span class="box-t">失效边界</p>围栏类比假设围栏是"硬"的、不能穿。SVM 的软间隔故意把围栏改成"可以挤出去一点，但每次挤要罚款"，那时约束就不再是硬的。</div>

<h3>3. 用到 SVM 上</h3>
<p>目标 $f=\\frac12\\|\\mathbf{w}\\|^2$，有 $n$ 个约束 $g_i=1-y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)\\le0$。每个约束配一个乘子 $\\alpha_i\\ge0$：</p>
<div class="math">$$L(\\mathbf{w},b,\\alpha)=\\frac12\\|\\mathbf{w}\\|^2-\\sum_{i=1}^{n}\\alpha_i\\bigl[y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)-1\\bigr]$$</div>
<p>注意符号：把"$\\ge1$"移项成"$1-\\dots\\le0$"，乘子前面加负号。这是标准写法，目的是让 $\\alpha_i\\ge0$ 时罚项方向正确。</p>
""")

add("s08", "对偶问题：为什么变成“猜下界”", """
<p class="lead">这一步最抽象，但可以用一个生活场景说清：<b>你不知道自己的身高，让两个人分别从上往下猜、从下往上猜，最优值在中间被夹住。</b></p>

<h3>1. 原始问题与对偶</h3>
<p>原始问题：在约束下最小化 $f$。构造 $L$ 之后，对 $\\mathbf{w},b$ 求最小、对 $\\alpha\\ge0$ 求最大，得到对偶问题。</p>
<p>直觉：$L$ 里对每个违反约束的点罚 $\\alpha_i$。$\alpha$ 越大罚越狠，所以 $\alpha$ 想让 $L$ 变大（找最严的罚法）；而 $\\mathbf{w},b$ 想让 $L$ 变小（找最容易满足的解）。<b>一个往上顶，一个往下压，最后夹在同一个值上。</b></p>
<p>对上式分别对 $\\mathbf{w}$ 和 $b$ 求偏导并令其为 0：</p>
<div class="math">$$\\frac{\\partial L}{\\partial\\mathbf{w}}=\\mathbf{w}-\\sum_i\\alpha_iy_i\\mathbf{x}_i=0\\ \\Rightarrow\\ \\mathbf{w}=\\sum_i\\alpha_iy_i\\mathbf{x}_i$$</div>
<div class="math">$$\\frac{\\partial L}{\\partial b}=-\\sum_i\\alpha_iy_i=0\\ \\Rightarrow\\ \\sum_i\\alpha_iy_i=0$$</div>
<p>代回 $L$，得到只含 $\\alpha$ 的问题：</p>
<div class="math">$$\\max_{\\alpha}\\ \\sum_i\\alpha_i-\\frac12\\sum_i\\sum_j\\alpha_i\\alpha_jy_iy_j(\\mathbf{x}_i\\cdot\\mathbf{x}_j)\\quad\\text{s.t.}\\ \\alpha_i\\ge0,\\ \\sum_i\\alpha_iy_i=0$$</div>

<h3>2. n=2 的双重求和，逐项展开</h3>
<p>上面的双重求和 $\sum_i\sum_j$ 让很多人卡住。取 $n=2$，把它写成四项：</p>
<div class="math">$$\\sum_{i=1}^{2}\\sum_{j=1}^{2}\\alpha_i\\alpha_jy_iy_j(\\mathbf{x}_i\\cdot\\mathbf{x}_j)=\\alpha_1^2y_1^2(\\mathbf{x}_1\\cdot\\mathbf{x}_1)+\\alpha_1\\alpha_2y_1y_2(\\mathbf{x}_1\\cdot\\mathbf{x}_2)+\\alpha_2\\alpha_1y_2y_1(\\mathbf{x}_2\\cdot\\mathbf{x}_1)+\\alpha_2^2y_2^2(\\mathbf{x}_2\\cdot\\mathbf{x}_2)$$</div>
<p>注意中间两项是<b>同一个数出现两次</p>（内积对称、$y_1y_2=y_2y_1$），所以可以合并成 $2\\alpha_1\\alpha_2y_1y_2(\\mathbf{x}_1\\cdot\\mathbf{x}_2)$。这就是为什么公式里常写 $\\frac12$——它正好消掉这个 2。</p>

<h3>3. 一个完整的手算（两点、线性核）</h3>
<p>取 $\\mathbf{x}_1=(1,1)$，$y_1=+1$；$\\mathbf{x}_2=(-1,-1)$，$y_2=-1$。先算内积：$\\mathbf{x}_1\\cdot\\mathbf{x}_1=2$，$\\mathbf{x}_2\\cdot\\mathbf{x}_2=2$，$\\mathbf{x}_1\\cdot\\mathbf{x}_2=-2$。</p>
<p>$y_1y_2=-1$，所以那一项系数是 $-1\\times(-2)=+2$。代入：</p>
<div class="math">$$W(\\alpha)=\\alpha_1+\\alpha_2-\\frac12\\bigl[2\\alpha_1^2+2\\alpha_2^2+2\\cdot2\\alpha_1\\alpha_2\\bigr]=\\alpha_1+\\alpha_2-(\\alpha_1+\\alpha_2)^2$$</div>
<p>令 $s=\\alpha_1+\\alpha_2$，则 $W=s-s^2$。这是一个开口向下的抛物线，顶点在 $s=\\frac12$，最大值 $=\\frac12-\\frac14=\\frac14$。</p>
<p>约束 $\\sum\\alpha_iy_i=0$ 就是 $\\alpha_1-\\alpha_2=0$，即 $\\alpha_1=\\alpha_2=\\frac14$。两个都是正数，满足 $\\alpha_i\\ge0$。</p>
<p>回代求 $\\mathbf{w}$：</p>
<div class="math">$$\\mathbf{w}=0.25\\times(+1)\\times(1,1)+0.25\\times(-1)\\times(-1,-1)=(0.5,0.5)$$</div>
<p>$b$ 用"支持向量满足 $y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)=1$"来求：$0.25$ 的 $\\mathbf{w}$ 在 $(1,1)$ 上内积是 $1$，所以 $1\\times(1+b)=1$，得 $b=0$。</p>
<p>间隔 $=2/\\|\\mathbf{w}\\|=2/\\sqrt{0.5}=2/0.707=2.828$。两个点到线的距离各是 $1.414$，加起来正是 $2.828$。数字自洽。</p>
""")

add("s09", "支持向量：为什么只有少数点有用", """
<p class="lead">KKT 条件里有一条叫"互补松弛"，它解释了"为什么大部分训练点可以被删掉"。</p>

<h3>1. 互补松弛条件</h3>
<div class="math">$$\\alpha_i\\bigl[y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)-1\\bigr]=0$$</div>
<p>两个因子相乘为 0，说明至少有一个是 0。分两种情况：</p>
<table class="calc">
<tr><th>情况</th><th>含义</th><th>$\\alpha_i$</th></tr>
<tr><td>点离边界很远，$y_i(\\dots)>1$</td><td>它被分得很安全</td><td>必须为 0，<b>对 $\\mathbf{w}$ 没有贡献</b></td></tr>
<tr><td>点恰好压在边界上，$y_i(\\dots)=1$</td><td>它是"支撑"分界线的点</td><td>可以为正，<b>决定 $\\mathbf{w}$</b></td></tr>
</table>
<p>因为 $\\mathbf{w}=\\sum_i\\alpha_iy_i\\mathbf{x}_i$，$\\alpha_i=0$ 的点直接被消掉。所以最终模型只依赖少数几个"压在边界上"的点——它们叫<b>支持向量</p>，也是 SVM 这个名字的来历。</p>

<h3>2. 这个性质的现实意义</h3>
<p>删掉一个远处的点，模型不变；删掉一个支持向量，模型会变。所以 SVM 对"远离边界的噪声"天然鲁棒，但对"贴边界的错标点"极其敏感——一个错标的点可能把整条边界拉歪。这也是软间隔要解决的问题（下一节）。</p>

<div class="box green"><span class="box-t">一句话</p>SVM 的解是稀疏的：大多数训练样本的权重是 0，模型只由少数关键点构成。</div>
""")

add("s10", "软间隔：当数据不可能完全分开", """
<p class="lead">现实数据常有重叠，硬间隔（要求全部分对）会无解，或者为了一个错点把边界拉得极歪。软间隔的做法是：允许越界，但收费。</p>

<h3>1. 加入松弛变量</h3>
<div class="math">$$y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)\\ge1-\\xi_i,\\qquad \\xi_i\\ge0$$</div>
<p>$\\xi_i$ 读"克西"，表示第 $i$ 个点"越界了多少"。没越界就是 0。</p>
<p>目标变成：</p>
<div class="math">$$\\min\\ \\frac12\\|\\mathbf{w}\\|^2+C\\sum_i\\xi_i$$</div>
<p>$C$ 是惩罚系数：$C$ 大，越界很贵，模型倾向于全分对（容易过拟合）；$C$ 小，允许更多越界，边界更宽（更稳但可能欠拟合）。</p>

<h3>2. 等价的合页损失形式</h3>
<p>把 $\\xi_i$ 消掉，可以写成不带约束的形式：</p>
<div class="math">$$\\min\\ \\frac12\\|\\mathbf{w}\\|^2+C\\sum_i\\max\\bigl(0,\\ 1-y_i(\\mathbf{w}\\cdot\\mathbf{x}_i+b)\\bigr)$$</div>
<p>后面那项叫<b>合页损失</p>（hinge loss）。它的形状像一个合页：分对且离得远（间隔大于 1）时为 0，一点损失都没有；一旦进入间隔区或分错，损失线性增长。</p>

<h3>3. 与逻辑回归的对比</h3>
<table class="calc">
<tr><th></th><th>合页损失（SVM）</th><th>交叉熵（逻辑回归）</th></tr>
<tr><td>分对且很远</td><td>损失恰为 0</td><td>损失很小但永远不为 0</td></tr>
<tr><td>关注点</td><td>只关心"够不够安全"，够了就不管</td><td>所有样本都持续提供梯度</td></tr>
<tr><td>结果</td><td>解稀疏，只由支持向量决定</td><td>所有样本都影响参数</td></tr>
</table>
<p>这个对比解释了"为什么 SVM 在小样本上常常表现好"：它不浪费精力去优化那些已经很安全的点。</p>

<div class="demo">
<div class="demo-t">动手：拖动 C，看边界怎么从"宽而稳"变成"紧而险"</div>
<canvas id="cvsvm" width="420" height="400"></canvas>
<div class="demo-ctl"><label>惩罚系数 C = <span id="c-val">1.00</span></label><input type="range" id="c" min="0" max="100" value="50"><br><span class="axis-note">横轴/纵轴：特征值（0—10）；虚线为间隔边界，实线为分界超平面</span></div>
<div class="demo-note" id="svm-note"></div>
</div>
""")

add("s11", "核技巧：不升维也能算高维内积", """
<p class="lead">如果数据在二维分不开（比如一圈点包着一堆点），办法是映射到更高维。核技巧的价值是：<b>不用真的算高维坐标，只算内积</b>。</p>

<h3>1. 显式升维长什么样</h3>
<p>二维 $(x_1,x_2)$ 映射到三维：</p>
<div class="math">$$\\phi(\\mathbf{x})=(x_1^2,\\ \\sqrt2x_1x_2,\\ x_2^2)$$</div>
<p>取 $\\mathbf{x}=(1,2)$：$\\phi=(1,\\ 2\\sqrt2\\approx2.828,\\ 4)$。原来 2 个数，现在 3 个数。</p>

<h3>2. 关键恒等式</h3>
<p>算两个点映射后的内积：</p>
<div class="math">$$\\phi(\\mathbf{x})\\cdot\\phi(\\mathbf{z})=x_1^2z_1^2+2x_1x_2z_1z_2+x_2^2z_2^2=(\\mathbf{x}\\cdot\\mathbf{z})^2$$</div>
<p>右边验证：$(\\mathbf{x}\\cdot\\mathbf{z})^2=(x_1z_1+x_2z_2)^2=x_1^2z_1^2+2x_1x_2z_1z_2+x_2^2z_2^2$。完全一样。</p>
<p>结论：<b>高维内积可以用低维内积的平方算出来</p>，不需要真的构造 $\\phi$。这个 $(\\mathbf{x}\\cdot\\mathbf{z})^2$ 就叫核函数。</p>

<h3>3. 常用核</h3>
<table class="calc">
<tr><th>名称</th><th>形式</th><th>适用</th></tr>
<tr><td>线性核</td><td>$\\mathbf{x}\\cdot\\mathbf{z}$</td><td>数据本身线性可分，或特征维度已经很高</td></tr>
<tr><td>多项式核</td><td>$(\\mathbf{x}\\cdot\\mathbf{z}+c)^d$</td><td>需要显式的特征交叉</td></tr>
<tr><td>高斯核（RBF）</td><td>$\\exp\\!\\bigl(-\\|\\mathbf{x}-\\mathbf{z}\\|^2/(2\\sigma^2)\\bigr)$</td><td>边界弯曲、样本量中等</td></tr>
</table>
<p>高斯核相当于映射到<b>无限维</p>，永远算不出显式坐标，但内积能算。这就是"核技巧"三个字最值钱的地方。</p>

<div class="box red"><span class="box-t">代价</p>核矩阵是 $n\\times n$，$n=10$ 万时是 100 亿个数，存不下也算不动。所以核方法适合中小样本，大样本要用线性核或近似方法。</div>
""")

add("s12", "VC 维：为什么“能打散几个点”衡量复杂度", """
<p class="lead">这是 SVM 理论部分最容易被讲玄的地方，其实只需要"打散"这一个概念。</p>

<h3>1. 定义</h3>
<p>一个模型族能<b>打散</p>（shatter）$d$ 个点，意思是：这 $d$ 个点的<b>所有</p> $2^d$ 种正负标号组合，模型都能实现。能打散的最大点数，就是这个模型族的 VC 维。</p>

<h3>2. 二维线性分类器：能打散 3 个点</h3>
<p>三个不共线的点，共有 $2^3=8$ 种标号。逐一检查：全正、全负可以（线放到外面）；一个正两个负（3 种）可以；两个正一个负（3 种）可以。8 种都能实现，所以二维线性分类器能打散 3 个点。</p>

<h3>3. 但打散不了 4 个点</h3>
<p>取四个点摆成"X"形（一对在对角、另一对在另一条对角）。让对角的两点为正、另两点为负——这正是异或（XOR）的布局。任何直线都无法把对角的两组分开，所以这一种标号实现不了。</p>
<p>因此二维线性分类器的 VC 维是 3，不是 4。</p>

<h3>4. 这个数字有什么用</h3>
<p>VC 维越大，模型越"能记住"复杂的标号，也越容易过拟合。SVM 的结构风险最小化思路是：<b>在间隔约束下，VC 维可以被间隔大小控制</b>——间隔越大，有效复杂度越低。这就是"最大化间隔"不只是"看起来更安全"，而是有泛化理论支撑的原因。</p>

<div class="box green"><span class="box-t">一句话</p>最大间隔＝在固定模型族的前提下，主动把有效复杂度压低。这是 SVM 与"只要分对"的方法最本质的差别。</div>
""")

add("s13", "完整算例：一组数走完全流程", """
<p class="lead">用一组具体的点，从原始问题走到最终模型，每一步都出数字。</p>

<h3>数据</h3>
<p>两个点：$\\mathbf{x}_1=(1,1)$，$y_1=+1$；$\\mathbf{x}_2=(-1,-1)$，$y_2=-1$。硬间隔、线性核。</p>

<h3>步骤 1：原始问题</h3>
<div class="math">$$\\min\\ \\frac12(w_1^2+w_2^2)\\quad\\text{s.t.}\\ \\begin{cases}+1\\cdot(w_1+w_2+b)\\ge1\\\\ -1\\cdot(-w_1-w_2+b)\\ge1\\end{cases}$$</div>
<p>第二条化简为 $w_1+w_2-b\\ge1$。两式相加得 $2(w_1+w_2)\\ge2$，即 $w_1+w_2\\ge1$。</p>

<h3>步骤 2：最优解</h3>
<p>在 $w_1+w_2=1$ 上让 $w_1^2+w_2^2$ 最小。用"两个数在固定和时，相等则平方和最小"（可由 $(w_1-w_2)^2\\ge0$ 推出）：$w_1=w_2=0.5$。</p>
<p>$\\|\\mathbf{w}\\|=\\sqrt{0.25+0.25}=\\sqrt{0.5}\\approx0.707$。代入约束：$0.5+0.5+b\\ge1$ 且 $0.5+0.5-b\\ge1$，得 $-0\\le b\\le0$，所以 $b=0$。</p>

<h3>步骤 3：间隔</h3>
<div class="math">$$\\text{margin}=\\frac{2}{\\|\\mathbf{w}\\|}=\\frac{2}{0.707}\\approx2.828$$</div>
<p>验证：点 $(1,1)$ 到直线 $0.5x_1+0.5x_2=0$ 的距离 $=\\dfrac{|0.5+0.5|}{\\sqrt{0.5}}=\\dfrac{1}{0.707}=1.414$。两个点各 1.414，合计 2.828，与公式一致。</p>

<h3>步骤 4：对偶验证</h3>
<p>s08 节算过 $\\alpha_1=\\alpha_2=0.25$，回代得 $\\mathbf{w}=(0.5,0.5)$。两条路给出同一个答案，说明对偶推导没错。</p>

<h3>步骤 5：结论</h3>
<p>分界线是 $0.5x_1+0.5x_2=0$，也就是 $x_1+x_2=0$（同乘 2 不改变直线）。两类点在直线的两侧且对称，间隔 2.828。<b>这个答案对不对？</b>凭直觉：两点关于原点对称，最"中立"的分界线就是过原点、垂直于连线的线，即 $x_1+x_2=0$。算出来的结果与直觉一致。</p>
""")

add("s14", "设计动机汇总：六个“为什么”", """
<p class="lead">这一节把前面所有"看起来是规定"的地方，逐一给出理由。想不通这些，会觉得 SVM 是一堆硬凑的符号。</p>

<table class="calc">
<tr><th>设计</th><th>如果不这样做会怎样</th></tr>
<tr><td>标签取 $\\pm1$</td><td>取 $\\{0,1\\}$ 时"对错"与"距离"要分两个量表达，无法用一个式子做优化</td></tr>
<tr><td>约束归一化为 $\\ge1$</td><td>不归一化，$\\mathbf{w}$ 可以任意缩放，间隔没有定义，问题无解</td></tr>
<tr><td>目标用 $\\frac12\\|\\mathbf{w}\\|^2$</td><td>用 $\\|\\mathbf{w}\\|$ 带根号，求导复杂；不乘 $\\frac12$ 则系数是 2，手算易错</td></tr>
<tr><td>最大化间隔而不是最小化错误</td><td>只要求分对时解不唯一，稍微转一点都合法，模型不稳定</td></tr>
<tr><td>对偶而不是直接解原始</td><td>原始问题带 $n$ 个不等式约束，难解；对偶把 $\\mathbf{w}$ 消掉，只剩 $\\alpha$，且能引入核函数</td></tr>
<tr><td>软间隔加 $C$</td><td>硬间隔在数据重叠时无解，或为个别错点牺牲整体间隔</td></tr>
</table>

<div class="box green"><span class="box-t">最后一句</p>SVM 的全部智慧集中在一个转换上：把"找一条好的分界线"变成"在一个凸问题里最小化 $\|\mathbf{w}\|$"。凸问题意味着没有局部最优陷阱，解唯一、可验证。这是它在 1990 年代压制神经网络的技术原因——不是更准，而是<b>有保证</b>。</div>
""")

add("s15", "自测：能独立推出才算过关", """
<p class="lead">六题覆盖本课主干。做不出来就回到对应小节，不要跳。</p>

<div class="quiz">
<p class="q">1.（单选）$\\mathbf{w}=(3,4)$，$\\|\\mathbf{w}\\|=$ ？</p>
<p class="opt">A. 5　B. 7　C. 12　D. 25</p>
<div class="ans"><b>答案：A。</b>$\\sqrt{9+16}=\\sqrt{25}=5$。</p></div>
</div>

<div class="quiz">
<p class="q">2.（填空）直线 $x_1+x_2-3=0$，点 $(2,2)$ 到它的距离是 ？（保留三位小数）</p>
<div class="ans"><b>答案：0.707。</b>分子 $|2+2-3|=1$，分母 $\\sqrt2\\approx1.414$，得 $0.707$。</p></div>
</div>

<div class="quiz">
<p class="q">3.（单选）把 $\\mathbf{w}=(1,1),b=-3$ 换成 $(2,2),b=-6$，下列哪个不变？</p>
<p class="opt">A. 函数间隔　B. 几何间隔　C. 目标函数值　D. 以上都变</p>
<div class="ans"><b>答案：B。</b>几何间隔对缩放不变，因为分子分母同时缩放。</p></div>
</div>

<div class="quiz">
<p class="q">4.（填空）$\\mathbf{w}=(1,1)$ 时，间隔 $2/\\|\\mathbf{w}\\|=$ ？（保留三位小数）</p>
<div class="ans"><b>答案：1.414。</b>$\\|\\mathbf{w}\\|=\\sqrt2\\approx1.414$，$2/1.414=1.414$。</p></div>
</div>

<div class="quiz">
<p class="q">5.（简答）用自己的话说清：为什么 $\\alpha_i=0$ 的点对最终模型没有影响？</p>
<div class="ans"><b>要点：</b>因为 $\\mathbf{w}=\\sum_i\\alpha_iy_i\\mathbf{x}_i$，$\\alpha_i=0$ 时这一项为 0；互补松弛表明这些点是"离边界很远、被分得很安全"的点。</p></div>
</div>

<div class="quiz">
<p class="q">6.（简答）二维线性分类器的 VC 维为什么是 3 而不是 4？</p>
<div class="ans"><b>要点：</b>3 个不共线点的 8 种标号都能用直线实现；4 个点按"对角同号"摆放时（XOR 布局），任何直线都无法实现该标号，故不能打散 4 个点。</p></div>
</div>

<p class="note">对 5 题以上，可以继续学核方法与软间隔；对 3—4 题，重点重读 s05、s06、s08。</p>
""")
