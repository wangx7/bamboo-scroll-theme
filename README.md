# 水墨主题 (Shuimo Theme)

一款根植于东方美学的 VS Code 主题集合，以「意象留白」与「长时护眼」为核心设计理念。

---

## 主题

### 水墨·丹青
> 案上微寒展玉宣，毫端深浅化孤云。
> 丹青点染千行句，不惹红尘扰寸心。

以宣纸质感的淡雅色调为底，深浅墨色区分代码层级，营造如观古画般的宁静体验。

### 水墨·竹韵
> 幽篁斜抱半窗风，碎叶交筛落翠空。
> 敲罢繁星织夜雨，绿荫长护眼瞳中。

以青竹为底色，搭配浓墨与黛绿文字。精心调优的对比度，适合长时间沉浸式开发。

### 水墨·世界
> 大千一墨化鸿蒙，万象森罗指掌中。
> 代码纵横经纬里，山河入眼夜朦胧。

以宣纸暖白为底，墨色层次分明，营造开阔而沉静的编码空间。

---

## 背景

为达到极致体验，建议搭配背景图片。可使用 [Background](https://marketplace.visualstudio.com/items?itemName=Katsute.code-background) 扩展，参考壁纸见 [backgrounds 目录](https://github.com/wangx7/shuimo-theme/tree/main/backgrounds)。

---

## 推荐搭配

水墨主题已为以下扩展预设配色，安装后即可获得一致的视觉体验。

### Error Lens

错误 / 警告 / 提示的行内高亮已与主题色板对齐：朱砂红表错误、赭石表警告、墨蓝表信息、灰表提示。无需额外配置。

### Better Comments

将以下配置复制到 `settings.json`，让注释按语义着色，与水墨色板保持一致：

```jsonc
"betterComments.tags": [
  { "tag": "!",     "color": "#983029", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": true,  "italic": false },
  { "tag": "?",     "color": "#20526F", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": false, "italic": true  },
  { "tag": "TODO",  "color": "#8B4E3D", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": true,  "italic": false },
  { "tag": "*",     "color": "#4F5B67", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": false, "italic": true  },
  { "tag": "//",    "color": "#5B6E7D", "strikethrough": true,  "underline": false, "backgroundColor": "transparent", "bold": false, "italic": false }
]
```

| 标签 | 语义 | 颜色 | 字体 |
|---|---|---|---|
| `!` | 警示 | 朱砂红 | 粗体 |
| `?` | 疑问 | 墨蓝 | 斜体 |
| `TODO` | 待办 | 赭石 | 粗体 |
| `*` | 强调 | 描述墨 | 斜体 |
| `//` | 弃用 | 灰 | 删除线 |

### Todo Tree / TODO Highlight

注释中的 `TODO` / `FIXME` / `XXX` / `HACK` / `NOTE` 关键字已通过 tokenColors 着色：`TODO` 朱砂红粗体、`FIXME`/`XXX` 赭石粗体、`HACK` 墨蓝斜体、`NOTE` 墨蓝斜体。

---

## 安装

VS Code 扩展市场搜索 `水墨 Theme` 安装。

🔗 [GitHub 仓库](https://github.com/wangx7/shuimo-theme)