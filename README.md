# 水墨主题 (Shuimo Theme)

一款根植于东方美学的 VS Code 主题集合，以「意象留白」与「长时护眼」为核心设计理念。

---

## 主题

### 水墨·世界

> 大千一墨化鸿蒙，万象森罗指掌中。
> 代码纵横经纬里，山河入眼夜朦胧。

以宣纸暖白 `#F6F5E1` 为底，遵循「墨为主，色为辅，计白当黑，惜墨如金」：

| 角色 | 色名 | 色值 | 字体 |
|---|---|---|---|
| 正文 / 变量 | 浓墨 | `#2A2C30` | 常规 |
| 类型 / 类 / 命名空间 | 焦墨 | `#232527` | 粗体 |
| 属性 / 参数 / 数字 / 常量 | 重墨 | `#3A3E43` | 常规 / 斜体 |
| 标点 / 运算符 / 装饰器 | 淡墨 | `#4A4F56` | 常规 / 斜体 |
| 行号 / Inlay / Ghost Text | 清墨 | `#5A5F66` | 常规 |
| 注释 | 水汽灰青 | `#626E74` | 斜体 |
| 字符串 / 正则 | 潭水青 | `#2B6E64` | 常规 |
| 函数 / 方法 / 链接 | 远水蓝 | `#4A6A8A` | 声明粗体 |
| 关键字 / 错误 / 当前焦点 | 朱砂 | `#8F3D2D` | 控制流粗体 |

**v2.4 水色长用版：**

- 编辑区只保留「一池水色 + 一点朱砂」，其余全部由五色墨承担。
- 注释与正文可分辨性 `2.67:1`，与纸面背景对比度 `4.76:1`，不再和内容粘连。
- 全部静态语法 Token 达到 WCAG 2.1 AA（含注释在内均 `>= 4.5:1`）。
- 选择区、当前行、词高亮改为中性墨色 wash；查找命中、焦点、活动标签只留朱砂一点。
- 语义高亮 36 项，覆盖 C#、PHP、Ruby、Kotlin、Swift、Lua、Dockerfile 与 JSX/TSX。
- 终端 ANSI、Git/SCM、Diff 作为功能色例外区，使用低饱和水色与朱砂。

### 水墨·竹韵

> 幽篁斜抱半窗风，碎叶交筛落翠空。
> 敲罢繁星织夜雨，绿荫长护眼瞳中。

以青竹为底色，搭配浓墨与黛绿文字。精心调优的对比度，适合长时间沉浸式开发。

---

## 背景

为达到极致体验，建议搭配背景图片。可使用 [Background](https://marketplace.visualstudio.com/items?itemName=Katsute.code-background) 扩展，参考壁纸见 [backgrounds 目录](https://github.com/wangx7/shuimo-theme/tree/main/backgrounds)。

---

## 推荐搭配

水墨主题已为以下扩展预设配色，安装后即可获得一致的视觉体验。

### Error Lens

错误 / 警告 / 提示的行内高亮已与主题色板对齐：朱砂表错误、赭沙表警告、远水蓝表信息、淡墨表提示。无需额外配置。

### Better Comments

将以下配置复制到 `settings.json`，让注释按语义着色，与水墨色板保持一致：

```jsonc
"betterComments.tags": [
  { "tag": "!",     "color": "#8F3D2D", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": true,  "italic": false },
  { "tag": "?",     "color": "#4A6A8A", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": false, "italic": true  },
  { "tag": "TODO",  "color": "#3A3E43", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": true,  "italic": false },
  { "tag": "*",     "color": "#5A5F66", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": false, "italic": true  },
  { "tag": "//",    "color": "#626E74", "strikethrough": true,  "underline": false, "backgroundColor": "transparent", "bold": false, "italic": false }
]
```

| 标签 | 语义 | 颜色 | 字体 |
|---|---|---|---|
| `!` | 警示 | 朱砂红 | 粗体 |
| `?` | 疑问 | 远水蓝 | 斜体 |
| `TODO` | 待办 | 重墨 | 粗体 |
| `*` | 强调 | 淡墨 | 斜体 |
| `//` | 弃用 | 水汽灰青 | 删除线 |

### Todo Tree / TODO Highlight

注释中的 `TODO` / `FIXME` / `XXX` / `HACK` / `NOTE` 关键字已通过 tokenColors 着色：`TODO` 朱砂粗体、`FIXME`/`XXX` 重墨、`HACK`/`NOTE` 远水蓝斜体。

---

## 安装

VS Code 扩展市场搜索 `水墨 Theme` 安装。

🔗 [GitHub 仓库](https://github.com/wangx7/shuimo-theme)