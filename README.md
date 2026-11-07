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
* 在 `_posts` 目录下添加 Markdown 文件，参考👉[Jekyll Posts 使用](https://jekyllrb.com/docs/posts/)
* 使用`构建本地测试环境`中的内容进行本地测试
* [`mathjax` 加速地址](https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML)
