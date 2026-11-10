## 简单介绍
Thank you for reading my blog. I will share more about becoming a hands-on dad at [handsondad.github.io](https://handsondad.github.io)

## 本地构建
* 在 GitHub 发布自己的站点，参考👉[GitHub Pages介绍](https://pages.github.com/)
* 安装 Jekyll，参考👉[使用 Jekyll 设置 GitHub Pages 站点](https://docs.github.com/cn/pages/setting-up-a-github-pages-site-with-jekyll)
    ```bash
    # 安装 Ruby和开发工具Devkit 

    # 安装 Jekyll
    gem install jekyll bundler

    # 测试
    jekyll -v
    ``` 
* 构建本地测试环境，参考[使用 Jekyll 构建本地测试环境](https://docs.github.com/cn/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)
    ```bash
    # 使用Gemfile安装环境依赖
    bundle install
    
    # 启动本地服务
    bundle exec jekyll serve

    # 浏览器查看4000端口服务
    ```

**注意：** 
* 如果您使用的是 Ruby 3.0 和 Jekyll 4.2.x 或更早版本，则需要在运行 bundle install 之前，将 webrick gem 添加到项目的 Gemfile 中
* 如果项目中缺少 Gemfile，使用 `bundle init` 命令生成 

## 使用说明
* 网站根目录的 `index.html` 是独立的项目导航主页；原有 Chirpy 文章列表位于 `/blog/`，分页路径为 `/blog/page2/` 等，文章永久链接不变。
* 主页项目卡片统一在 `_data/projects.yml` 维护，`experiences` 是亲子探索项目，`collections` 是资源收藏。`notice` 可在卡片上提示站点暂不可用，恢复后移除；确实要暂时下架某张卡片时可设 `hidden: true`；主页样式位于 `assets/css/landing.css`。
* “遇见孩子”品牌标志由 `python tools/generate_logo.py` 生成：从马善政字体分片取出四个字的轮廓，配色取自首页彩虹标题与小星球底色，输出 `assets/images/logo.svg`（首页使用）、`assets/images/logo.png`（256px 通用）、`assets/images/logo-avatar.png`（字缩小到圆内，供 Chirpy 圆形侧栏头像）、根目录 `favicon.ico`，以及覆盖 Chirpy 默认图标的 `assets/img/favicons/`（浏览器标签、iOS 主屏幕、安卓 PWA 图标；安卓 maskable 图标的字限制在中心 80% 安全圆内）。脚本会断言每个字不越出对应形状的安全区。转 PNG 需要本机 Microsoft Edge 或 Chrome 与 Pillow。
* 主页沿用 Bodyverse 的版式：居中彩虹渐变标题、小星球上的小念和爸爸、可点击换句的对话气泡、粉彩描边卡片。三维场景由 `tools/home-duo/` 移植 Bodyverse 的角色装配与星球代码，`npm install && npm run build` 生成 `assets/js/home-duo.js`；角色模型 `assets/models/character.glb` 为 CC0，来源见同目录 `CREDITS.md`。浏览器不支持 WebGL 或开启省流量时只显示平面版，对话气泡照常可用；减少动态效果时镜头不跟随鼠标、气泡不浮动。
* 主页字体为 Comic Neue／马善政（SIL Open Font License 1.1，授权见 `assets/fonts/`）。`python tools/fetch_landing_fonts.py` 从 Google Fonts 下载按字符范围切好的 WOFF2 分片到 `assets/fonts/landing/`，并生成 `assets/css/landing-fonts.css`；浏览器只下载页面用到的分片，无需连接外部字体服务。脚本会检查首页每个汉字都有字形，修改首页文案后建议重跑。加载期间回退到本机楷体或微软雅黑。
* 博客沿用首页的字体与配色，但只用于标题和导航：`assets/css/jekyll-theme-chirpy.scss` 覆盖 Chirpy 的样式入口，把 `$font-family-heading` 换成首页字体，侧栏站名、导航、顶栏和右栏小标题同样手写，正文与文章摘要仍为主题默认黑体；浅色模式改为首页的奶油底、棕字、橙色链接（深色模式保持主题默认）。字体分片由 `_includes/metadata-hook.html` 引入，与首页共用缓存。升级 Chirpy 时需对照新版主题的同名入口文件。
* `_includes/sidebar.html` 在 Chirpy 侧栏增加“文章”入口；`_includes/post-paginator.html` 覆盖主题分页，确保第 1 页返回 `/blog/`，而不是导航主页；`_includes/topbar.html` 去掉文章列表页顶栏的“首页”面包屑，其他页面面包屑的第一项改为“返回”并指向文章列表 `/blog/`。升级 Chirpy 时需核对这三个覆盖文件。本地构建使用 `_config.yml`；不要使用切换为其他主题的 `_config.dev.yml` 验收 Chirpy。
* 新增或完善文章前，请先阅读 [`AGENTS.md`](AGENTS.md)：包含来源核查、中文分步图解、短动画、图片授权与验收规范。
* 最近文章的六幅补充图可用 `python tools/generate_recent_post_visuals.py` 重新生成；脚本仅使用 Python 标准库，并核对比例换算、平方不等式、切线长度与注意力权重。
* 历史文章的原创图可用 `python tools/generate_archive_visuals.py` 重新生成；脚本仅使用标准库，核对历法周期差、碳收支和字符编码，生成的短动画支持减少动态效果。目录导读图与随笔提醒卡保持静态，不表示医学评估或因果模型。
* 重点科普的十二幅机制图可用 `python tools/generate_deep_science_visuals.py` 重新生成；脚本校验碳与电子收支、ATP近似账、太阳辐射比例、时间换算、逻辑门和玩具CPU执行。图中描线仅引导阅读，不模拟真实生物速率或处理器周期。
* 周期表文章的五幅原创图可用 `python tools/generate_periodic_table_visuals.py` 重新生成；脚本核对第四周期的18个元素、氧化物电荷收支与轨道容量，短表局部按俄罗斯2026年官方化学示例卷的位置重绘。
* 美元文字文章的五幅原创静态图可用 `python tools/generate_dollar_visuals.py` 重新生成；脚本核对十三条盾纹、格言字母数与罗马数字1776，图为位置和历史关系示意，不是纸币或国玺的精确复制件。
* 开普勒与牛顿文章的七幅原创图可用 `python tools/generate_kepler_newton_visuals.py` 重新生成；脚本核对等时面积、周期比例、速度Verlet轨道收敛与理想地火转移时间，唯一的轨道动画按开普勒方程计时，播放一次并支持减少动态效果。
* 微积分与引力文章的六幅原创图可用 `python tools/generate_calculus_gravity_visuals.py` 重新生成；脚本核对地月尺度、轨道高度引力、向量方向、分段逃逸功与不同初速度的圆锥曲线，圆周运动动画播放一次并支持减少动态效果。
* 微积分入门文章的八幅原创图可用 `python tools/generate_calculus_foundations_visuals.py` 重新生成；脚本核对差商、自由落体、矩形上下界、二项式近似、气体偏导与热方程的初始和边界条件，割线演示播放一次并保留静态路线。
* 墨卡托与地图文章的八幅原创静态图可用 `python tools/generate_mercator_visuals.py` 重新生成；脚本核对球面投影倍率、大圆与恒向线长度、三角测量、山丘等高线、比例尺换算与瓦片层级。肖像的作者、馆藏来源与许可另列在文章末尾。
* 尺规作图文章的八幅分步图可用 `python tools/generate_compass_visuals.py` 重新生成；脚本核对等长与角平分、正多边形闭合、几何平均数、平行分线，以及外接圆共圆和内切圆相切。虚线表示辅助线，构造步骤不依赖动画。
* 计算器历史文章的八幅原创静态图可用 `python tools/generate_calculator_visuals.py` 重新生成；脚本核对十进制与二进制进位、阶梯鼓选齿、滑架乘法、对数刻度、函数采样和数值表示。另有一张依 CC BY-SA 4.0 转载的开源复刻界面，作者、原文件与许可见正文。
* 织布机文章的八幅原创图可用 `python tools/generate_loom_visuals.py` 重新生成；脚本核对平纹、斜纹、缎纹组织，卡片选择与64个交织点的对应，以及教学组织的循环浮长。逐纬动画播放一次并保留完整结果，支持减少动态效果；机构图为概念示意，不是制造图。
* 摆线文章的八幅原创图可用 `python tools/generate_cycloid_visuals.py` 重新生成；脚本核对同端点竞速积分、等时解析运动与能量、弧长关系、完整单摆周期，以及摆线挡板的切向和绳长约束。三幅短动画播放一次并支持减少动态效果，下滑演示按统一物理时间放慢四倍。
* 悬链线文章的九幅原创图可用 `python tools/generate_catenary_visuals.py` 重新生成；脚本校验链条静力平衡、等弧长取点与斜率、双曲余弦、抛物线近似、索力和教学温升模型。三幅教学动画展示受力、链段累积与温升弧垂，全跨和局部放大同步，播放一次并响应减少动态效果，不可作为工程设计或安全距离依据。
* 分析力学文章的八幅原创图可用 `python tools/generate_analytical_mechanics_visuals.py` 重新生成；脚本核对非线性单摆周期与能量、关键帧插值、约束几何、驻定作用量的非极小反例、谐振相图和轨道有效势能。三幅短动画分别同步单摆与能量、强调候选曲线、同步直线运动与相空间，播放一次并支持减少动态效果。
* 变分法文章的八幅原创图可用 `python tools/generate_variations_visuals.py` 重新生成；脚本核对泛函评分与弧长、第一变分、局部扰动积分、边界几何、折射时间和角度、链长与自由落体作用量。一次短演示只改变候选函数家族，不模拟真实运动，保留全部静态比较并支持减少动态效果。
* 拉普拉斯与天体力学文章的六幅原创图可用 `python tools/generate_laplace_visuals.py` 重新生成；脚本核对三体模型、步长收敛、质心、慢相位与真空引力势。`assets/interactive/laplace-lab.html` 提供可暂停、重播、调参数的三体与慢拍两个实验，默认不自动播放，无第三方依赖；`node tools/check_laplace_model.cjs` 检查实际使用的 JavaScript 模型。模型采用人造初值，不是精密星历或长期稳定性证明。
* 蒙日与机械制图文章的八幅原创图可用 `python tools/generate_monge_visuals.py` 重新生成；脚本核对正投影、台阶尺寸、真长、轴套断面与间隙区间。`assets/interactive/monge-lab.html` 可旋转相机、对照同一角点的三视图、改变台阶与剖切位置；`node tools/check_monge_model.cjs` 检查模型拓扑与几何。默认不自动播放，静态图独立可读；教学图不是完整制造文件。
* 傅里叶文章的八幅原创图可用 `python tools/generate_fourier_visuals.py` 生成；`assets/interactive/fourier-lab.html` 提供绝热环热扩散动画和实际 DFT／低通／逆变换实验。`node tools/check_fourier_model.cjs` 核对热方程、周期性、均温守恒、Parseval 关系、幅相、单边归一化、泄漏与混叠。默认不自动播放，减少动态效果时改为分步；热参数为教学设定，不是材料实测，直接 DFT 不冒称 FFT。
* 在 `_posts` 目录下添加 Markdown 文件，参考👉[Jekyll Posts 使用](https://jekyllrb.com/docs/posts/)
* 使用`构建本地测试环境`中的内容进行本地测试
* [`mathjax` 加速地址](https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML)
