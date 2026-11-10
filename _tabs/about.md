---
layout: page
icon: fas fa-info-circle
order: 5
---

**Hands-on Dad（实践奶爸）** 是一个专为奶爸打造的育儿宝库。

我是奶爸 Liang。这里记录孩子的成长、我当爸爸的心路历程，也收着我和孩子一起探索世界时找到的答案。陪孩子长大的过程中，我自己也在重新学习一遍：

> 💡 **育儿即育己。** 孩子像一面镜子，照见我们的优点，也照见我们的不足。

## 这里有什么

- 📝 **文章**：目前共 {{ site.posts.size }} 篇，分科学、亲子时间、个人感悟三条主线。[从文章列表开始 →](/blog/)
- 🎮 **亲子探索项目**：{{ site.data.projects.experiences.size }} 个打开浏览器就能和孩子一起玩的小站。
- 🌱 **好内容收藏**：给大人看的育儿与学习资源整理。

## 三条阅读主线

### 🔬 科学

数学、物理、化学和技术里的“为什么”。通常从一位科学家遇到的具体难题讲起，配原创分步图，必要时加一段短动画。

- [帕斯卡怎样把一场赌局变成概率论？]({% post_url 2026-11-04-帕斯卡怎样把一场赌局变成概率论 %})
- [神秘的摆线：为什么绕远路，反而先到？]({% post_url 2026-11-07-摆线为什么绕远路反而先到 %})
- [傅里叶怎样把温度拆成波？]({% post_url 2026-11-10-傅里叶怎样把温度拆成波 %})

[全部科学文章 →](/categories/%E7%A7%91%E5%AD%A6/)

### 🧒 亲子时间

和孩子一起认识世界：飞行、光合作用、地球为什么适合生命，还有一组值得收藏的亲子网站。

- [如何能实现飞行]({% post_url 2024-10-10-如何能实现飞行 %})
- [可视化理解光合作用]({% post_url 2025-01-03-可视化理解光合作用 %})
- [为什么地球能孕育生命]({% post_url 2024-12-10-为什么地球能孕育生命 %})

[全部亲子时间 →](/categories/%E4%BA%B2%E5%AD%90%E6%97%B6%E9%97%B4/)

### 💭 个人感悟

从准父母到新手奶爸，写情绪、观察和自己的变化。

- [蓦然回首 - 准父母的那些事]({% post_url 2023-08-15-蓦然回首 %})
- [进入孩子的视角]({% post_url 2024-03-01-进入孩子的视角 %})
- [感受和认识自己的情绪]({% post_url 2024-04-15-感受和认识自己的情绪 %})

[全部个人感悟 →](/categories/%E4%B8%AA%E4%BA%BA%E6%84%9F%E6%82%9F/)

## 文章是怎样写的

1. **从一个具体问题出发**，而不是从定义出发。
2. **先举能算、能画的例子**，再给公式；符号、单位和适用条件都会解释。
3. **难的步骤配原创分步图**；只有变化过程本身值得看时才加动画，并保留静态版本。
4. **关键年份、定理和数据标出处**，文末附参考资料；比喻、近似和简化模型会明确标出。

如果发现哪里写错了，欢迎告诉我，确认后会尽快更正。

## 亲子探索项目

每个小站都可以直接在浏览器里打开，适合大人和孩子坐在一起玩：
{% for project in site.data.projects.experiences %}{% unless project.hidden %}
- {{ project.icon }} **[{{ project.title }}]({{ project.url }})**（{{ project.kind }}）：{{ project.description }}{% endunless %}{% endfor %}

## 好内容收藏
{% for project in site.data.projects.collections %}{% unless project.hidden %}
- {{ project.icon }} **[{{ project.title }}]({{ project.url }})**：{{ project.description }}{% if project.notice %}（{{ project.notice }}）{% endif %}{% endunless %}{% endfor %}

这些项目的代码都在 [GitHub @handsondad](https://github.com/handsondad) 上，包括这个博客本身。那里还有两个更早的仓库：给孩子的 AI 小实验 [Kids AI Lab](https://github.com/handsondad/kids-ai-lab)，以及记录“奶爸升级之路”的 [Dadventures](https://github.com/handsondad/dadventures)。

## 联系我

有问题、建议，想一起做项目，或者孩子提了一个好问题，都欢迎来信：

- 📧 邮箱：liang@handsondad.com
- 🐙 GitHub：[@handsondad](https://github.com/handsondad)
- 🐦 Twitter：[@handsondad](https://twitter.com/handsondad)

> **Hands-on Dad**
>
> 用实践的态度，做一个用心的奶爸。❤️
