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
* 在 `_posts` 目录下添加 Markdown 文件，参考👉[Jekyll Posts 使用](https://jekyllrb.com/docs/posts/)
* 使用`构建本地测试环境`中的内容进行本地测试
* [`mathjax` 加速地址](https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML)
