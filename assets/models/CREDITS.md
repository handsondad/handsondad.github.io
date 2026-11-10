# 3D 角色模型来源

| 文件 | 原始资源 | 作者 | 许可 |
| --- | --- | --- | --- |
| `character.glb` | Ultimate Animated Character Pack · `Casual_Male` | Quaternius（quaternius.com） | CC0 1.0 |

- 与 [Bodyverse](https://handsondad.github.io/bodyverse/) 使用同一个处理后的文件（`bodyverse/public/models/character.glb`）：只保留 Idle、Walk、Run、Jump、Victory 等动作，并用 glTF-Transform 做了 resample、prune、dedup、quantize。
- 首页的小念和爸爸各克隆一份，由 `tools/home-duo/src/home-duo.js` 在运行时设定身高、头身比例、配色、描边、脸红和爸爸的眼镜。
- CC0 不要求署名，这里记录来源是为了方便以后追溯和替换。
