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
* “遇见孩子”品牌标志与社交分享卡由 `python tools/generate_logo.py` 生成：从马善政字体分片取出四个字的轮廓，配色取自首页彩虹标题与小星球底色，输出 `assets/images/logo.svg`（首页使用）、`assets/images/logo.png`（256px 通用）、`assets/images/logo-avatar.png`（字缩小到圆内，供 Chirpy 圆形侧栏头像）、`assets/images/social-preview.png`（`1200×630` 全站社交分享默认图）、根目录 `favicon.ico`，以及覆盖 Chirpy 默认图标的 `assets/img/favicons/`（浏览器标签、iOS 主屏幕、安卓 PWA 图标；安卓 maskable 图标的字限制在中心 80% 安全圆内）。脚本会断言每个字不越出对应形状的安全区。转 PNG 需要本机 Microsoft Edge 或 Chrome 与 Pillow。
* 主页沿用 Bodyverse 的版式：居中彩虹渐变标题、小星球上的小念和爸爸、可点击换句的对话气泡、粉彩描边卡片。三维场景由 `tools/home-duo/` 移植 Bodyverse 的角色装配与星球代码，`npm install && npm run build` 生成 `assets/js/home-duo.js`；角色模型 `assets/models/character.glb`（CC0，来源见同目录 `CREDITS.md`）已裁剪未使用的动作与孤立访问器以压缩体积，并配合同构图透明海报 `assets/images/home-duo-poster.webp` 实现首屏零等待秒开、浏览器空闲加载完成后无缝淡入替换。浏览器不支持 WebGL 或开启省流量时保留高清静态海报版，对话气泡照常可用；减少动态效果时镜头不跟随鼠标、气泡不浮动。
* 主页字体为 Comic Neue／马善政（SIL Open Font License 1.1，授权见 `assets/fonts/`）。`python tools/fetch_landing_fonts.py` 从 Google Fonts 下载按字符范围切好的 WOFF2 分片到 `assets/fonts/landing/`，并生成 `assets/css/landing-fonts.css`；浏览器只下载页面用到的分片，无需连接外部字体服务。脚本会检查首页每个汉字都有字形，修改首页文案后建议重跑。加载期间回退到本机楷体或微软雅黑。
* 博客沿用首页的字体与配色，但只用于标题和导航：`assets/css/jekyll-theme-chirpy.scss` 覆盖 Chirpy 的样式入口，把 `$font-family-heading` 换成首页字体，侧栏站名、导航、顶栏和右栏小标题同样手写，正文与文章摘要仍为主题默认黑体；浅色模式改为首页的奶油底、棕字、橙色链接（深色模式保持主题默认）。字体分片由 `_includes/metadata-hook.html` 引入，与首页共用缓存。升级 Chirpy 时需对照新版主题的同名入口文件。
* `_includes/sidebar.html` 在 Chirpy 侧栏增加“文章”入口（底部 GitHub／邮箱／RSS 图标由 `_data/contact.yml` 配置，文章分享项由 `_data/share.yml` 配置）；`_includes/post-paginator.html` 覆盖主题分页，确保第 1 页返回 `/blog/`，而不是导航主页；`_includes/topbar.html` 去掉文章列表页顶栏的“首页”面包屑，其他页面面包屑的第一项改为“返回”并指向文章列表 `/blog/`；`_layouts/home.html` 为列表卡片加上分类色标并展示右侧配图缩略图（优先取 front matter 的 `image` 或 `thumbnail`，否则自动取正文首幅配图并跳过 `history.svg`，不会在文章顶部重复渲染）；`_layouts/archives.html` 将归档日期改为中文“月·日”顺序。升级 Chirpy 时需核对这些覆盖文件。本地构建使用 `_config.yml`；不要使用切换为其他主题的 `_config.dev.yml` 验收 Chirpy。
* 新增或完善文章前，请先阅读 [`AGENTS.md`](AGENTS.md)：包含来源核查、中文分步图解、短动画、图片授权与验收规范。
* 全站文章的原创教学 SVG 配图统一由 `tools/visuals/` 工具包（零第三方依赖，仅用 Python 标准库）维护，不再按单篇文章堆叠独立脚本：运行 `python tools/visuals.py list` 可查看全部已注册主题（分布在 `algebra_logic`、`geometry_analysis`、`mechanics_sky`、`science_tech` 四个学科模块及共享底座 `core.py`／模板库 `charts.py` 中），运行 `python tools/visuals.py build <主题|all>` 可重新计算生成配图并执行全部数学／物理断言，运行 `python tools/visuals.py audit` 可统一校验全站 SVG 的 XML 合法性、宽高比与 Chirpy 正文字号比例上限。短动画均仅播放一次并响应系统 `prefers-reduced-motion: reduce`。
* 交互实验室位于 `assets/interactive/`（拉普拉斯三体与慢拍 `laplace-lab.html`、蒙日三视图与剖切 `monge-lab.html`、傅里叶热扩散与频谱 `fourier-lab.html`），默认不自动播放且无第三方依赖；对应的数值与几何模型可分别用 `node tools/check_laplace_model.cjs`、`node tools/check_monge_model.cjs`、`node tools/check_fourier_model.cjs` 校验。
* 在 `_posts` 目录下添加 Markdown 文件，参考👉[Jekyll Posts 使用](https://jekyllrb.com/docs/posts/)
* 使用`构建本地测试环境`中的内容进行本地测试
* [`mathjax` 加速地址](https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML)
