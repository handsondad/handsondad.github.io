# 3D 角色模型来源

| 文件 | 原始资源 | 作者 | 许可 |
| --- | --- | --- | --- |
| `character.glb` | Ultimate Animated Character Pack · `Casual_Male` | Quaternius（quaternius.com） | CC0 1.0 |

- 源自 [Bodyverse](https://handsondad.github.io/bodyverse/) 处理后的文件，并进一步针对首页裁剪：仅保留实际使用的 `Idle`、`Jump`、`Victory` 三个动作与对应访问器，剔除未引用的动作轨道并压缩 JSON，体积从 712 KB 降至约 320 KB；同时提取同视角首帧透明图 `assets/images/home-duo-poster.webp`（约 30 KB）供首页瞬时首屏显示，后台空闲加载完成后平滑切换至实时 3D。
- 首页的小念和爸爸各克隆一份，由 `tools/home-duo/src/home-duo.js` 在运行时设定身高、头身比例、配色、描边、脸红和爸爸的眼镜。
- CC0 不要求署名，这里记录来源是为了方便以后追溯和替换。
