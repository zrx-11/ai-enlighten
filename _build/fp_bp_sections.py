# -*- coding: utf-8 -*-
"""反向传播：从零推导 —— 章节内容"""

SECTIONS = []

def add(sid, title, body):
    SECTIONS.append({"id": sid, "title": title, "body": body})

add("s01", "知识树：这一课要爬的台阶", """
<p class="lead">这份产物只讲一件事：<b>一个神经网络怎么知道自己的参数该往哪边改</b>。为了回答它，我们需要爬五层台阶。看不懂某一层，就往回退一层。</p>

<div class="box yellow"><span class="box-t">前置知识</span>本课从"一个数的加减乘除"开始，不假设你会微积分、矩阵、编程。凡是第一次出现的符号，我都会先用白话解释它是什么、怎么读。</div>

<div class="tree">
<div class="tier"><span class="tier-t">根系</span>加减乘除 · 负数 · 平方 · 大小比较 · 分数</div>
<div class="tier"><span class="tier-t">第一层</span>函数与图像 · 斜率 · 导数（"变化有多快"）</div>
<div class="tier"><span class="tier-t">第二层</span>导数四则法则 · 链式法则（本课的核心工具）</div>
<div class="tier"><span class="tier-t">第三层</span>多元函数 · 偏导 · 梯度（"往哪个方向下坡最快"）</div>
<div class="tier"><span class="tier-t">第四层</span>神经元 · 激活函数 · 损失函数</div>
<div class="tier"><span class="tier-t">主干</span>计算图 · 反向传播 · 梯度下降 · 一次完整训练</div>
</div>

<p class="note">不补就卡死的地方有三个：链式法则、偏导、矩阵乘法。其余（比如极限的严格定义、泰勒展开）本课用不到，直接跳过。</p>
""")

add("s02", "第一层：斜率是什么，导数是什么", """
<p class="lead">先建立唯一一个直觉：<b>导数就是"此刻的变化速度"</b>。它不是新东西，就是你开车时仪表盘上那个数。</p>

<h3>1. 一句严格定义</h3>
<p>函数 $f(x)$ 在点 $x_0$ 处的导数，记作 $f'(x_0)$，定义为：当 $x$ 在 $x_0$ 附近变化一点点 $\Delta x$ 时，$f$ 的变化量 $\Delta f$ 与 $\Delta x$ 的比值的极限：</p>
<div class="math">$$f'(x_0)=\\lim_{\\Delta x\\to 0}\\frac{f(x_0+\\Delta x)-f(x_0)}{\\Delta x}$$</div>
<p>符号解释：$\Delta$ 读"德尔塔"，表示"一小段变化量"；$\lim$ 读"极限"，表示"让 $\Delta x$ 无限接近 0 时，这个比值趋近的那个数"。</p>

<h3>2. 生活类比</h3>
<p>你开车走了 100 公里，用了 2 小时，平均速度是 50 公里/小时。但仪表盘显示的是<b>此刻</b>的速度。平均速度是"一段路的斜率"，仪表盘速度是"一个瞬间的斜率"。导数就是那个瞬间的斜率。</p>
<div class="box red"><span class="box-t">类比的失效边界</span>车速有上限、有惯性，而数学函数的导数可以是任意大、也可以不存在（比如在尖角处）。不要把"车不能瞬间从 0 到 100"套到函数上。</p>

<h3>3. 手算三个例子（不跳步）</h3>
<p><b>例 1：</b>$f(x)=3x$。取 $x_0=2$，$\Delta x=0.1$：</p>
<div class="math">$$\\frac{f(2.1)-f(2)}{0.1}=\\frac{6.3-6}{0.1}=3$$</div>
<p>换 $\Delta x=0.01$，结果还是 3。所以 $f'(2)=3$。直观看：这条直线每往前走 1，就上升 3，斜率恒为 3。</p>

<p><b>例 2：</b>$f(x)=x^2$。取 $x_0=1$：</p>
<div class="math">$$\\frac{(1+\\Delta x)^2-1^2}{\\Delta x}=\\frac{1+2\\Delta x+(\\Delta x)^2-1}{\\Delta x}=2+\\Delta x$$</div>
<p>让 $\Delta x\\to 0$，结果是 2。所以 $(x^2)'=2x$，在 $x=1$ 处等于 2。</p>

<p><b>例 3：</b>$f(x)=5$（常数）。无论 $x$ 怎么变，$f$ 都不变，所以 $\Delta f=0$，导数为 0。</p>

<div class="box green"><span class="box-t">后续应用</span>反向传播里每一层都在问"我这点参数变一点，损失变多少"，问的就是导数。第 s04 节把它推广到多个变量。</div>
""")

add("s03", "第二层：链式法则——整门课最重要的一步", """
<p class="lead">如果只能记住一个公式，就记这个：<b>复合函数的变化率，等于外层变化率乘内层变化率</b>。</p>

<h3>1. 先看一个"算得动"的例子</h3>
<p>设 $y=(3x+1)^2$，求 $x=2$ 时的导数。</p>
<p>做法一（展开）：$y=9x^2+6x+1$，导数是 $18x+6$，代入 $x=2$ 得 42。</p>
<p>做法二（链式）：把它看成两层。内层 $u=3x+1$，外层 $y=u^2$。</p>
<ul>
<li>外层对 $u$ 的变化率：$\\dfrac{dy}{du}=2u$，在 $u=7$ 时是 14。</li>
<li>内层对 $x$ 的变化率：$\\dfrac{du}{dx}=3$。</li>
<li>相乘：$14\\times 3=42$。</li>
</ul>
<p>两种做法结果一致，说明链式法则不是新规则，只是"分步骤求导"。</p>

<h3>2. 为什么是"乘"而不是"加"</h3>
<p>用比例解释：$x$ 变 1，$u$ 变 3 倍；$u$ 变 1，$y$ 变 $2u$ 倍。那么 $x$ 变 1，$y$ 先被放大 3 倍、再被放大 $2u$ 倍，总的放大倍数是 $3\\times 2u$。倍数是连乘的，所以变化率连乘。</p>

<div class="box red"><span class="box-t">这里最容易错</span>很多人会把两层的变化率相加。记住：<b>放大的倍数是乘的</b>。$x$ 变 1%，$u$ 变 3%，$y$ 变 3% 的 14 倍，不是 17%。</div>

<h3>3. 三层嵌套也照办</h3>
<div class="math">$$\\frac{d}{dx}f(g(h(x)))=f'(g(h(x)))\\cdot g'(h(x))\\cdot h'(x)$$</div>
<p>读法："最外层导数（自变量是内层的输出）乘中间层导数乘最内层导数"。层数再多，就是继续往后乘。</p>

<h3>4. 一个具体算例（后面会用到）</h3>
<p>设 $L=(wx-y)^2$，$w=2$，$x=1$，$y=3$。求 $L$ 对 $w$ 的导数。</p>
<p>把 $w$ 当自变量：内层 $u=wx-y=2-3=-1$，外层 $L=u^2$。</p>
<ul>
<li>$\\dfrac{dL}{du}=2u=-2$</li>
<li>$\\dfrac{du}{dw}=x=1$</li>
<li>相乘：$(-2)\\times 1=-2$</li>
</ul>
<p>含义：$w$ 增大一点，损失会减小。所以要让损失变小，$w$ 应该往<b>增大</b>的方向走。这个判断会在 s08 节变成更新公式。</p>
""")

add("s04", "第三层：多个变量，偏导与梯度", """
<p class="lead">神经网络里参数不是一个，是成千上万个。所以要问"损失对<b>某一个</b>参数的变化率"，这就是偏导。</p>

<h3>1. 偏导：把其他变量当常数</h3>
<p>$f(w,b)=w^2+3b$。求对 $w$ 的偏导，记作 $\\dfrac{\\partial f}{\\partial w}$。$\\partial$ 读"偏"，含义是"只让 $w$ 变，$b$ 冻结"。</p>
<div class="math">$$\\frac{\\partial f}{\\partial w}=2w,\\qquad \\frac{\\partial f}{\\partial b}=3$$</div>
<p>做法就是：求 $w$ 的导数时把 $3b$ 看成常数（导数为 0）；求 $b$ 的导数时把 $w^2$ 看成常数。</p>

<h3>2. 梯度：把偏导排成一个向量</h3>
<p>把所有偏导按参数顺序排成一列，就叫<b>梯度</b>，记作 $\\nabla f$（读"纳布拉 f"）：</p>
<div class="math">$$\\nabla f=\\begin{bmatrix}\\dfrac{\\partial f}{\\partial w}\\\\[2pt]\\dfrac{\\partial f}{\\partial b}\\end{bmatrix}=\\begin{bmatrix}2w\\\\3\\end{bmatrix}$$</div>
<p>梯度的方向是"函数上升最快的方向"，它的长度是"上升有多快"。所以<b>反着梯度走，就是下降最快的方向</b>。</p>

<h3>3. 类比：山坡</h3>
<p>你站在山坡上，想知道往哪走下降最快。你不用看整座山，只需要感受脚下哪个方向最陡。梯度就是那个"最陡的上坡方向"的箭头，取负号就是下坡。</p>
<div class="box red"><span class="box-t">失效边界</span>这个类比只在"坡面光滑、没有坑"时成立。真实损失函数有很多局部低点，按梯度走只能保证走到<b>附近</b>的最低点，不保证是全局最低。</p>

<h3>4. 梯度下降的更新式</h3>
<div class="math">$$w\\leftarrow w-\\eta\\frac{\\partial L}{\\partial w}$$</div>
<p>$\\eta$ 读"伊塔"，叫学习率，控制每步走多大。负号表示"往梯度的反方向走"。</p>
<p>注意这个式子的含义：梯度是正的，说明增大 $w$ 会让损失上升，所以 $w$ 要减小；梯度是负的，$w$ 要增大。负号自动处理了这个逻辑，不用你判断。</p>
""")

add("s05", "第四层前半：神经元与激活函数", """
<p class="lead">有了导数工具，现在看要给它喂什么。一个神经元只做两件事：<b>加权求和</b>，然后<b>过一道非线性</b>。</p>

<h3>1. 加权求和</h3>
<div class="math">$$z=w_1x_1+w_2x_2+\\cdots+w_nx_n+b=\\mathbf{w}^\\top\\mathbf{x}+b$$</div>
<p>$\mathbf{w}$ 和 $\mathbf{x}$ 是向量（一串数），$\\mathbf{w}^\\top\\mathbf{x}$ 就是对应位置相乘再相加，结果是一个数。$b$ 叫偏置，是一个可以平移的常数。</p>

<h3>2. 手算一个具体值</h3>
<p>$\mathbf{x}=(1,2)$，$\mathbf{w}=(0.5,-1)$，$b=0.5$：</p>
<div class="math">$$z=0.5\\times 1+(-1)\\times 2+0.5=0.5-2+0.5=-1$$</div>

<h3>3. 为什么必须加非线性</h3>
<p>如果不加，两层网络等价于一层：设第一层 $z_1=W_1x$，第二层 $z_2=W_2z_1=W_2W_1x$。两个矩阵相乘还是矩阵，所以整个网络等于一个线性变换。堆一百层也没有增加任何表达能力。</p>
<div class="box red"><span class="box-t">别以为</span>"层数多就更强"——层数多只在<b>每层之间插入了非线性</b>的前提下才更强。这是 1969 年《感知机》一书指出的核心问题，也是深度学习的设计前提。</div>

<h3>4. 两个常用激活函数</h3>
<p><b>Sigmoid：</b></p>
<div class="math">$$\\sigma(z)=\\frac{1}{1+e^{-z}},\\qquad \\sigma'(z)=\\sigma(z)\\bigl(1-\\sigma(z)\\bigr)$$</div>
<p>它把任意实数压到 (0,1) 之间，可以当概率看。导数有一个很漂亮的封闭形式，所以手算方便。</p>
<p><b>ReLU：</b>$\\mathrm{ReLU}(z)=\\max(0,z)$。导数是：$z>0$ 时为 1，$z<0$ 时为 0。简单，而且不会让梯度越乘越小（这是 s10 节要讲的关键）。</p>

<p class="note">记住 Sigmoid 的两个端点值：$\\sigma(0)=0.5$，$\\sigma(1)\\approx 0.731$，$\\sigma(-1)\\approx 0.269$。后面算例要用。</p>
""")

add("s06", "第四层后半：损失函数——“错了多少”要能被计算", """
<p class="lead">训练需要一个分数，告诉你现在错得多离谱。这个分数必须<b>可导</b>，否则没法用梯度。</p>

<h3>1. 平方损失（回归问题）</h3>
<div class="math">$$L=\\frac12(\\hat{y}-y)^2$$</div>
<p>$\\hat{y}$ 读"y hat"，表示预测值；$y$ 是真实值。前面的 $\\frac12$ 是为了求导时把 2 消掉，纯粹为了手算干净，不改变最优解的位置。</p>
<p>对 $\\hat{y}$ 求导：</p>
<div class="math">$$\\frac{\\partial L}{\\partial \\hat{y}}=\\hat{y}-y$$</div>
<p>含义直白：预测比真实大多少，梯度就是多少。预测准了梯度为 0，不再调整。</p>

<h3>2. 交叉熵（分类问题）</h3>
<div class="math">$$L=-\\log p_y$$</div>
<p>$p_y$ 是模型给"正确类别"的概率。预测得越自信且正确，$p_y$ 越接近 1，$-\\log p_y$ 越接近 0；预测错得越离谱，损失越大。</p>
<p>为什么不用平方损失做分类？因为平方损失配合 Sigmoid 时，错得很离谱的地方梯度反而很小（Sigmoid 两端太平），学得极慢。交叉熵没有这个问题。</p>

<div class="box green"><span class="box-t">设计动机</span>损失函数不是"随便找个能算差距的东西"。它决定了梯度的形状，也就决定了学得快还是学得慢。<b>同一件事，换个损失函数，训练速度可能差十倍。</b></div>
""")

add("s07", "主干第一步：计算图——把求导变成“往回传”", """
<p class="lead">反向传播的核心不是数学新发现，而是<b>工程组织方式</b>：把前向计算拆成一个个小步骤，记住每一步的输入，然后从结果往回，逐步用链式法则乘。</p>

<h3>1. 一个最小的计算图</h3>
<p>取 $L=(wx-y)^2$，$w=2$，$x=1$，$y=3$。把它拆成四个节点：</p>
<div class="math">$$u=wx\\ \\Rightarrow\\ v=u-y\\ \\Rightarrow\\ L=v^2$$</div>
<p>数值：$u=2$，$v=-1$，$L=1$。</p>

<h3>2. 反向：从 $L$ 往回乘</h3>
<table class="calc">
<tr><th>步骤</th><th>节点</th><th>局部导数</th><th>累乘得到</th></tr>
<tr><td>①</td><td>$L=v^2$</td><td>$\\dfrac{\\partial L}{\\partial v}=2v=-2$</td><td>$\\dfrac{\\partial L}{\\partial v}=-2$</td></tr>
<tr><td>②</td><td>$v=u-y$</td><td>$\\dfrac{\\partial v}{\\partial u}=1$</td><td>$\\dfrac{\\partial L}{\\partial u}=-2\\times 1=-2$</td></tr>
<tr><td>③</td><td>$u=wx$</td><td>$\\dfrac{\\partial u}{\\partial w}=x=1$</td><td>$\\dfrac{\\partial L}{\\partial w}=-2\\times 1=-2$</td></tr>
</table>
<p>结论：$\\dfrac{\\partial L}{\\partial w}=-2$。梯度为负，说明增大 $w$ 会降低损失，所以 $w$ 应该增大。这和 s03 节手算的结果一致——但这次是"机械化流程"，任何复杂网络都能照这个流程走。</p>

<h3>3. 为什么要"记住中间值"</h3>
<p>注意第 ① 步用到 $v=-1$，这是前向时算出来存下的。反向时必须能拿到前向的中间结果，否则算不了局部导数。这就是深度学习框架要保存 activation 的原因，也是显存占用的主要来源。</p>

<div class="box red"><span class="box-t">常见误解</span>别以为反向传播是"另一种求导公式"。它就是链式法则，只是组织成了一个可以自动执行的流程。<b>数学上没有任何新东西，工程上价值巨大。</b></div>
""")

add("s08", "主干第二步：一次完整的参数更新（手算到底）", """
<p class="lead">现在把前面所有零件装起来，走一整圈：前向算损失，反向算梯度，更新参数。</p>

<h3>设定</h3>
<p>单神经元，无激活（$\\hat y=wx$），平方损失。$x=1$，$y=3$，初始 $w=2$，学习率 $\\eta=0.1$。</p>

<h3>第 1 轮</h3>
<p><b>前向</b>：$\\hat y=2\\times 1=2$，损失 $L=\\frac12(2-3)^2=0.5$。</p>
<p><b>反向</b>：</p>
<div class="math">$$\frac{\partial L}{\partial \hat y}=\hat y-y=-1,\qquad \frac{\partial \hat y}{\partial w}=x=1$$</div>
<div class="math">$$\frac{\partial L}{\partial w}=\frac{\partial L}{\partial \hat y}\cdot\frac{\partial \hat y}{\partial w}=-1\times1=-1$$</div>
<p><b>更新</b>：$w\\leftarrow 2-0.1\\times(-1)=2.1$。</p>

<h3>第 2 轮</h3>
<p>前向：$\\hat y=2.1$，$L=\\frac12(2.1-3)^2=0.405$。</p>
<p>梯度：$\\dfrac{\\partial L}{\\partial w}=(2.1-3)\\times 1=-0.9$。</p>
<p>更新：$w\\leftarrow 2.1-0.1\\times(-0.9)=2.19$。</p>

<h3>第 3 轮</h3>
<p>$\\hat y=2.19$，$L=\\frac12(0.81)^2=0.328$，梯度 $-0.81$，$w\\leftarrow 2.271$。</p>

<table class="calc">
<tr><th>轮</th><th>$w$</th><th>$\\hat y$</th><th>损失</th><th>梯度</th></tr>
<tr><td>0</td><td>2.000</td><td>2.000</td><td>0.500</td><td>−1.000</td></tr>
<tr><td>1</td><td>2.100</td><td>2.100</td><td>0.405</td><td>−0.900</td></tr>
<tr><td>2</td><td>2.190</td><td>2.190</td><td>0.328</td><td>−0.810</td></tr>
<tr><td>3</td><td>2.271</td><td>2.271</td><td>0.266</td><td>−0.729</td></tr>
</table>

<p>看这张表：每轮 $w$ 增加的量是上一轮的 0.9 倍，损失是上一轮的 0.81 倍。它会一直逼近 $w=3$，但永远不到。这就是学习率 0.1 决定的收敛速度——<b>学习率越大，逼近越快，但太大就会越过目标来回震荡</b>。</p>

<div class="demo">
<div class="demo-t">动手：拖动滑块改变学习率，看损失怎么下降</div>
<canvas id="cvbp" width="420" height="300"></canvas>
<div class="demo-ctl"><label>学习率 η = <span id="eta-val">0.10</span></label><input type="range" id="eta" min="1" max="200" value="10"><br><span class="axis-note">横轴：训练轮次（0—30）；纵轴：损失值（0—0.5）</span></div>
<div class="demo-note" id="bp-note"></div>
</div>
""")

add("s09", "主干第三步：两层网络，矩阵怎么写、转置为什么出现", """
<p class="lead">一层搞懂了，两层只是把"数"换成"一排数"。唯一新的东西是<b>维度对齐</b>和<b>转置</b>。</p>

<h3>1. 前向</h3>
<p>输入是一行两个数 $\\mathbf{x}=[x_1,x_2]$。第一层有 3 个神经元，权重矩阵 $W_1$ 是 $3\\times 2$（3 行 2 列：每行是一个神经元的权重）。</p>
<div class="math">$$\\mathbf{z}_1=W_1\\mathbf{x}+\\mathbf{b}_1,\\qquad \\mathbf{a}_1=\\sigma(\\mathbf{z}_1)$$</div>
<p>维度检查：$(3\\times2)\\cdot(2\\times1)=(3\\times1)$，得到一个 3 个数的向量。这就是"左边列数必须等于右边行数"的规则。</p>

<h3>2. 手算一个 2×2 的例子</h3>
<p>$W_1=\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}$，$\\mathbf{x}=\\begin{bmatrix}1\\\\1\\end{bmatrix}$：</p>
<div class="math">$$W_1\\mathbf{x}=\\begin{bmatrix}1\\times1+2\\times1\\\\3\\times1+4\\times1\\end{bmatrix}=\\begin{bmatrix}3\\\\7\\end{bmatrix}$$</div>
<p>记法：结果第 1 个数＝矩阵第 1 行与向量逐项相乘再相加；第 2 个数用第 2 行。</p>

<h3>3. 反向时为什么出现转置</h3>
<p>前向是 $W\\mathbf{x}$，把"输入"变成"输出"。反向要反过来：把"输出的梯度"变回"输入的梯度"，乘的必须是 $W^\\top$。</p>
<div class="math">$$\\frac{\\partial L}{\\partial \\mathbf{x}}=W^\\top\\frac{\\partial L}{\\partial \\mathbf{z}}$$</div>
<p>转置就是把矩阵的行列互换。$\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}^\\top=\\begin{bmatrix}1&3\\\\2&4\\end{bmatrix}$。</p>
<p><b>为什么要转置：</b>前向时 $z_1=w_{11}x_1+w_{12}x_2$。所以 $x_1$ 通过 $w_{11}$ 影响 $z_1$、通过 $w_{21}$ 影响 $z_2$。要把 $z$ 的梯度加回 $x_1$，必须用<b>第一列</b>的系数，也就是转置后的第一行。行列互换不是数学技巧，是"把每个输入收到的贡献收拢起来"。</p>

<h3>4. 权重梯度</h3>
<div class="math">$$\\frac{\\partial L}{\\partial W}=\\frac{\\partial L}{\\partial \\mathbf{z}}\\,\\mathbf{x}^\\top$$</div>
<p>维度检查：$(3\\times1)\\cdot(1\\times2)=(3\\times2)$，和 $W$ 的形状一致，可以直接相减更新。</p>

<div class="box yellow"><span class="box-t">卡点提醒</span>如果这里跟不上，回去看 s05 的加权求和手算，再回来看维度。矩阵乘法不是新东西，它就是"很多个加权求和并排做"。</div>
""")

add("s10", "梯度消失：为什么深网络曾经训不动", """
<p class="lead">反向传播在 1986 年就被发表，但直到 2012 年才真正赢。原因之一就在这一节。</p>

<h3>1. 连乘的代价</h3>
<p>一个 10 层网络，每层往回传都要乘一次权重和一个激活导数。如果每次乘的因子平均是 0.5：</p>
<div class="math">$$0.5^{10}\\approx 0.001,\\qquad 0.5^{20}\\approx 0.000001$$</div>
<p>传到第一层时，梯度几乎为 0，参数基本不动。<b>不是算错了，是信息在传递中被衰减光了。</b></p>

<h3>2. Sigmoid 为什么加剧这个问题</h3>
<p>$\\sigma'(z)=\\sigma(z)(1-\\sigma(z))$。它的最大值是 0.25（在 $z=0$ 处）。也就是说，<b>每经过一个 Sigmoid，梯度至少被压到四分之一</b>。10 层就是 $0.25^{10}\\approx 9.5\\times10^{-7}$。</p>

<h3>3. 三个解法</h3>
<table class="calc">
<tr><th>解法</th><th>机制</th><th>代价</th></tr>
<tr><td>ReLU</td><td>正区间导数为 1，不衰减</td><td>负区间导数为 0，可能出现"死神经元"</td></tr>
<tr><td>残差连接</td><td>$y=x+F(x)$，梯度有一条直通的加法路径</td><td>需要网络结构配合</td></tr>
<tr><td>批归一化</td><td>把每层输入拉回稳定分布</td><td>增加计算与实现复杂度</td></tr>
</table>
<p>残差连接值得多说一句：因为 $y=x+F(x)$，所以 $\\dfrac{\\partial y}{\\partial x}=1+\\dfrac{\\partial F}{\\partial x}$。那个"1"保证了梯度至少能原样传回去一层，不会被压没。这就是 ResNet 能堆到上百层的原因。</p>

<div class="box red"><span class="box-t">别以为</span>"梯度消失只是理论问题"。它是 1990 年代神经网络被 SVM 压制的实际原因之一：深网络训不动，浅网络又表达力不够。</div>
""")

add("s11", "设计动机：为什么这样设计，而不是那样", """
<p class="lead">这一节回答四类"学习者不问但会想"的问题。想不通这些，会觉得整套体系是硬凑的。</p>

<h3>Q1：为什么损失前面要加 $\\frac12$？</h3>
<p>因为 $(\\frac12u^2)'=u$，求导时那个 2 正好消掉，手算干净。最优解的位置不变，只是损失的数值差一倍。工程上无所谓，教学上很重要——它让梯度等于"预测减真实"，一眼能看懂。</p>

<h3>Q2：为什么更新是"减"梯度，不是"加"？</h3>
<p>梯度指向上升最快的方向。我们要损失变小，所以要往反方向走。<b>减号不是规定，是定义的直接后果。</b></p>

<h3>Q3：学习率为什么不能取很大？</h3>
<p>用 s08 的例子：目标 $w=3$，起始 $w=2$，如果 $\\eta=2$，第一轮 $w=2-2\\times(-1)=4$，越过目标到了另一侧；第二轮梯度变成 $+1$，$w=4-2\\times1=2$，又回去了。<b>来回震荡，永远不收敛。</b>稳定条件是 $\\eta$ 小于"损失曲率"的倒数，具体值取决于问题。</p>

<h3>Q4：为什么不能一次算出最优解，非要一步步走？</h3>
<p>线性回归可以（有闭式解），但多层网络的损失关于参数是<b>非凸</b>的，没有公式解。只能迭代。而且实际参数可能有上亿个，即便有公式也要解巨型方程，算不动。</p>

<div class="box green"><span class="box-t">小结一句</span>反向传播＝链式法则的机械化；梯度下降＝按梯度反方向小步走；两者合起来，就是"深度学习能训练"的全部秘密。剩下的都是工程细节。</div>
""")

add("s12", "自测：能独立推出才算过关", """
<p class="lead">合上前面，试着在纸上做完这 6 题。做不出来就回到对应小节。</p>

<div class="quiz" data-ans="b">
<p class="q">1.（单选）$f(x)=(2x+1)^2$ 在 $x=1$ 处的导数是？</p>
<p class="opt">A. 6　B. 12　C. 18　D. 24</p>
<div class="ans"><b>答案：B。</b>内层 $u=3$，外层导数 $2u=6$，内层导数 2，相乘得 12。</div>
</div>

<div class="quiz" data-ans="a">
<p class="q">2.（单选）梯度下降中 $w\\leftarrow w-\\eta\\frac{\\partial L}{\\partial w}$，若 $\\frac{\\partial L}{\\partial w}=0.5$，则 $w$ 会？</p>
<p class="opt">A. 减小　B. 增大　C. 不变　D. 无法判断</p>
<div class="ans"><b>答案：A。</b>梯度为正说明增大 $w$ 会让损失上升，所以要减小。</p></div>
</div>

<div class="quiz" data-ans="c">
<p class="q">3.（单选）两层网络若两层之间不加非线性激活，整体等价于？</p>
<p class="opt">A. 一个更深的网络　B. 一个非线性函数　C. 一层线性变换　D. 无法训练</p>
<div class="ans"><b>答案：C。</b>$W_2(W_1x)=(W_2W_1)x$，矩阵乘积仍是矩阵。</p></div>
</div>

<div class="quiz" data-ans="0.9">
<p class="q">4.（填空）$x=1$、$y=3$、$w=2$，平方损失取 $\\frac12(\\hat y-y)^2$。此时 $\\frac{\\partial L}{\\partial w}=$ ？</p>
<div class="ans"><b>答案：−1。</b>$\\hat y=2$，$\\partial L/\\partial\\hat y=-1$，$\\partial\\hat y/\\partial w=x=1$，相乘得 −1。</p></div>
</div>

<div class="quiz" data-ans="0.1">
<p class="q">5.（填空）2×2 矩阵 $W=\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}$，向量 $[1,1]^\\top$，$W\\mathbf{x}$ 的第二个分量是？</p>
<div class="ans"><b>答案：7。</b>用第二行：$3\\times1+4\\times1=7$。</p></div>
</div>

<div class="quiz" data-ans="b">
<p class="q">6.（简答）用自己的话说清：为什么残差连接 $y=x+F(x)$ 能缓解梯度消失？</p>
<div class="ans"><b>要点：</b>求导得 $\\partial y/\\partial x=1+\\partial F/\\partial x$，那个常数 1 保证梯度至少原样传回一层，不会被连乘压到 0。</p></div>
</div>

<p class="note">六题里对五题以上，可以进入下一个课题（支持向量机）。三到四题，重读 s03、s04、s08。</p>
""")
