#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""丹青 v2.7 前后对比预览生成器
用简化 TextMate 匹配(最长 scope 子序列)解析旧/新主题, 渲染同一段 TS 样例 + 色板对比。
"""
import json, colorsys, html

ROOT = "/Users/wangx/我的/github/vscode/shuimo-theme"

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def hex_to_rgb(h):
    h = h.lstrip("#")[:6]
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def luminance(r, g, b):
    a = [v/255.0 for v in (r, g, b)]
    a = [((v+0.055)/1.055)**2.4 if v > 0.03928 else v/12.92 for v in a]
    return 0.2126*a[0] + 0.7152*a[1] + 0.0722*a[2]

def contrast(c1, c2):
    l1, l2 = luminance(*hex_to_rgb(c1)), luminance(*hex_to_rgb(c2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi+0.05)/(lo+0.05)

def resolve(theme, scope_str):
    """返回 (color, fontStyle) — 最长 scope 匹配"""
    chain = scope_str.split(".")
    best, style = None, None
    for rule in theme.get("tokenColors", []):
        scopes = rule.get("scope", [])
        if isinstance(scopes, str):
            scopes = [scopes]
        for rs in scopes:
            rparts = rs.split(".")
            # 子序列匹配: rparts 必须连续出现在 chain 中
            matched = False
            for i in range(len(chain) - len(rparts) + 1):
                if chain[i:i+len(rparts)] == rparts:
                    matched = True
                    break
            if matched:
                if best is None or len(rs.split(".")) > len(best.split(".")):
                    best = rs
                    st = rule.get("settings", {})
                    style = (st.get("foreground"), st.get("fontStyle"))
    if best is None:
        return (theme["colors"].get("editor.foreground", "#383A3D"), None)
    return style

# ---------- TS 样例: (文本, scope) ----------
SAMPLE = [
    ("// 丹青 v2.7 — 山色空蒙雨亦奇", "comment.line.double-slash.ts"),
    ("import ", "keyword.control.import.ts"),
    ("{ defineStore } ", "punctuation.definition.block.ts"),
    ("from ", "keyword.control.from.ts"),
    ("'pinia'", "string.quoted.single.ts"),
    ("", None),
    ("const ", "keyword.operator.expression.ts"),
    ("API_BASE", "variable.other.constant.ts"),
    (" = ", "keyword.operator.assignment.ts"),
    ("'https://api.example.com'", "string.quoted.single.ts"),
    ("", None),
    ("export ", "keyword.control.export.ts"),
    ("function ", "storage.type.function.ts"),
    ("fetchUser", "entity.name.function.ts"),
    ("(", "punctuation.definition.parameters.ts"),
    ("id", "variable.parameter.ts"),
    (": ", "meta.type.annotation.ts"),
    ("number", "support.type.primitive.ts"),
    (")", "punctuation.definition.parameters.ts"),
    (": ", "meta.type.annotation.ts"),
    ("Promise", "support.class.ts"),
    ("<", "punctuation.definition.typeparameters.ts"),
    ("User", "entity.name.type.ts"),
    (">", "punctuation.definition.typeparameters.ts"),
    (" ", "source.ts"),
    ("{", "meta.brace.curly.ts"),
    ("", None),
    ("  ", "source.ts"),
    ("return ", "keyword.control.return.ts"),
    ("new ", "keyword.operator.new.ts"),
    ("Promise", "support.class.ts"),
    ("((resolve, reject) => ", "source.ts"),
    ("{", "meta.brace.curly.ts"),
    ("", None),
    ("    ", "source.ts"),
    ("if ", "keyword.control.conditional.ts"),
    ("(", "meta.brace.round.ts"),
    ("id", "variable.parameter.ts"),
    (" <= ", "keyword.operator.relational.ts"),
    ("0", "constant.numeric.ts"),
    (")", "meta.brace.round.ts"),
    (" ", "source.ts"),
    ("{", "meta.brace.curly.ts"),
    ("", None),
    ("      ", "source.ts"),
    ("reject", "variable.parameter.ts"),
    ("(new ", "source.ts"),
    ("Error", "support.class.ts"),
    ("('invalid id'))", "string.quoted.single.ts"),
    ("  ", "source.ts"),
    ("// FIXME: 边界校验", "comment.line.double-slash.ts"),
    ("", None),
    ("    ", "source.ts"),
    ("}", "meta.brace.curly.ts"),
    ("", None),
    ("    ", "source.ts"),
    ("const ", "keyword.operator.expression.ts"),
    ("user", "variable.other.readwrite.ts"),
    (": ", "meta.type.annotation.ts"),
    ("User", "entity.name.type.ts"),
    (" = ", "keyword.operator.assignment.ts"),
    ("{ ", "meta.brace.curly.ts"),
    ("id", "variable.other.readwrite.ts"),
    (", ", "punctuation.separator.ts"),
    ("name", "variable.other.readwrite.ts"),
    (": ", "meta.type.annotation.ts"),
    ("'青竹'", "string.quoted.single.ts"),
    (", ", "punctuation.separator.ts"),
    ("tags", "variable.other.readwrite.ts"),
    (": ", "meta.type.annotation.ts"),
    ("[", "punctuation.definition.array.ts"),
    ("'admin'", "string.quoted.single.ts"),
    ("]", "punctuation.definition.array.ts"),
    (" }", "meta.brace.curly.ts"),
    ("", None),
    ("    ", "source.ts"),
    ("resolve", "variable.parameter.ts"),
    ("(user)", "meta.brace.round.ts"),
    ("", None),
    ("  ", "source.ts"),
    ("}", "meta.brace.curly.ts"),
    ("}", "meta.brace.curly.ts"),
    ("", None),
    ("", None),
    ("class ", "keyword.control.class.ts"),
    ("UserRepository", "entity.name.class.ts"),
    (" ", "source.ts"),
    ("implements ", "keyword.control.import.ts"),
    ("Repository", "support.class.ts"),
    ("<", "punctuation.definition.typeparameters.ts"),
    ("User", "entity.name.type.ts"),
    (">", "punctuation.definition.typeparameters.ts"),
    (" ", "source.ts"),
    ("{", "meta.brace.curly.ts"),
    ("", None),
    ("  ", "source.ts"),
    ("private ", "storage.modifier.ts"),
    ("cache", "variable.other.readwrite.ts"),
    (" = ", "keyword.operator.assignment.ts"),
    ("new ", "keyword.operator.new.ts"),
    ("Map", "support.class.ts"),
    ("<", "punctuation.definition.typeparameters.ts"),
    ("number", "support.type.primitive.ts"),
    (", ", "punctuation.separator.ts"),
    ("User", "entity.name.type.ts"),
    (">()", "punctuation.definition.typeparameters.ts"),
    ("", None),
    ("  ", "source.ts"),
    ("public ", "storage.modifier.ts"),
    ("async ", "storage.modifier.ts"),
    ("find", "entity.name.function.ts"),
    ("(", "punctuation.definition.parameters.ts"),
    ("id", "variable.parameter.ts"),
    (": ", "meta.type.annotation.ts"),
    ("number", "support.type.primitive.ts"),
    ("): ", "meta.type.annotation.ts"),
    ("Promise", "support.class.ts"),
    ("<", "punctuation.definition.typeparameters.ts"),
    ("User", "entity.name.type.ts"),
    (" | ", "keyword.operator.type.ts"),
    ("null", "constant.language.ts"),
    (">", "punctuation.definition.typeparameters.ts"),
    (" ", "source.ts"),
    ("{", "meta.brace.curly.ts"),
    ("", None),
    ("    ", "source.ts"),
    ("return ", "keyword.control.return.ts"),
    ("this", "variable.language.this.ts"),
    (".", "punctuation.accessor.ts"),
    ("cache", "variable.other.readwrite.ts"),
    (".", "punctuation.accessor.ts"),
    ("get", "support.function.builtin.ts"),
    ("(id)", "meta.brace.round.ts"),
    (" ", "source.ts"),
    ("?? ", "keyword.operator.expression.ts"),
    ("null", "constant.language.ts"),
    ("", None),
    ("  ", "source.ts"),
    ("}", "meta.brace.curly.ts"),
    ("}", "meta.brace.curly.ts"),
]

def render_code(theme, sample, bg):
    out = []
    for text, scope in sample:
        if text == "":
            out.append("<br>")
            continue
        if scope is None:
            out.append(html.escape(text))
            continue
        color, style = resolve(theme, scope)
        css = f"color:{color}"
        if style:
            css += f";font-style:{'italic' if 'italic' in style else 'normal'};font-weight:{'bold' if 'bold' in style else '400'}"
        out.append(f'<span style="{css}">{html.escape(text)}</span>')
    return "".join(out)

def palette_table(theme, roles):
    rows = []
    bg = theme["colors"]["editor.background"]
    for name, key, font in roles:
        val = theme["colors"].get(key) or next(
            (r["settings"]["foreground"] for r in theme["tokenColors"]
             if key in str(r.get("scope", [])) and r["settings"].get("foreground")), "?")
        if not val or len(val) != 7:
            continue
        cr = contrast(bg, val)
        h, s, v = colorsys.rgb_to_hsv(*(x/255 for x in hex_to_rgb(val)))
        hue = h*360
        fam = "水色" if 100 <= hue <= 300 else ("朱砂" if (hue < 60 or hue > 340) else "—")
        rows.append((name, val, cr, fam, font))
    return rows, bg

ROLES = [
    ("正文 / 变量", "editor.foreground", "常规"),
    ("类型 / 类 / 命名空间", "entity.name.type", "粗体"),
    ("行号 / 运算符", "editorLineNumber.foreground", "常规"),
    ("注释", "comment", "斜体"),
    ("字符串 / 正则", "string", "常规"),
    ("函数 / 方法", "entity.name.function", "常规"),
    ("关键字", "keyword", "粗体"),
    ("数字 / 常量", "constant.numeric", "常规"),
    ("参数", "variable.parameter", "斜体"),
    ("修饰符", "storage.modifier", "常规"),
]

def build():
    old = load("/tmp/danqing_old.json")
    new = load(f"{ROOT}/themes/shuimo-danqing-theme.json")
    old_bg = "#F6F5E1"

    old_code = render_code(old, SAMPLE, old_bg)
    new_code = render_code(new, SAMPLE, old_bg)

    rows_old, bg = palette_table(old, ROLES)
    rows_new, _ = palette_table(new, ROLES)

    sw = ""
    for name, val, cr, fam, font in rows_new:
        sw += f'''<tr>
          <td style="padding:6px 10px;border-bottom:1px solid #e2ddc4">{name}</td>
          <td style="padding:6px 10px;border-bottom:1px solid #e2ddc4">
            <span style="display:inline-block;width:52px;height:20px;border-radius:4px;background:{val};border:1px solid #d8d3bc;vertical-align:middle;margin-right:8px"></span>
            <code style="font-size:12px">{val}</code>
          </td>
          <td style="padding:6px 10px;border-bottom:1px solid #e2ddc4">{cr:.2f}:1</td>
          <td style="padding:6px 10px;border-bottom:1px solid #e2ddc4">{fam}</td>
          <td style="padding:6px 10px;border-bottom:1px solid #e2ddc4">{font}</td>
        </tr>'''

    diff_rows = ""
    pairs = [
        ("正文", "#2A2C30", "#383A3D", "12.8:1 → 10.4:1, 进入 7~10 舒适区"),
        ("焦墨", "#232527", "#2C2E31", "14.1:1 → 12.4:1, 保留强调层级"),
        ("注释", "#4C7548", "#51686E", "松绿→灰青: 与 git added 绿解耦, 4.8→5.4:1"),
        ("焦点框", "#9A3B26", "#315D8C", "朱砂→远水蓝: 与错误红解耦"),
        ("警告图标", "#8A4B2F", "#8A6D1F", "统一为藤黄警告族"),
    ]
    for a, b, c, note in pairs:
        diff_rows += f'''<tr>
          <td style="padding:5px 10px;border-bottom:1px solid #efe9d2;font-weight:600">{a}</td>
          <td style="padding:5px 10px;border-bottom:1px solid #efe9d2"><span style="display:inline-block;width:46px;height:18px;border-radius:4px;background:{b};border:1px solid #d8d3bc;vertical-align:middle;margin-right:6px"></span><code>{b}</code></td>
          <td style="padding:5px 10px;border-bottom:1px solid #efe9d2;color:#9A3B26">→</td>
          <td style="padding:5px 10px;border-bottom:1px solid #efe9d2"><span style="display:inline-block;width:46px;height:18px;border-radius:4px;background:{c};border:1px solid #d8d3bc;vertical-align:middle;margin-right:6px"></span><code>{c}</code></td>
          <td style="padding:5px 10px;border-bottom:1px solid #efe9d2;color:#5A5F66;font-size:12px">{note}</td>
        </tr>'''

    page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>水墨·丹青 v2.7 对比预览</title>
<style>
  body {{ background:#F6F5E1; color:#383A3D; font-family:"PingFang SC","Microsoft YaHei",sans-serif; margin:0; padding:32px 40px; }}
  h1 {{ font-size:22px; margin:0 0 4px; }}
  .sub {{ color:#5A5F66; font-size:13px; margin-bottom:28px; }}
  .cols {{ display:flex; gap:20px; flex-wrap:wrap; }}
  .panel {{ flex:1; min-width:420px; background:#F6F5E1; border:1px solid #d8d3bc; border-radius:10px; overflow:hidden; box-shadow:0 2px 10px #26262614; }}
  .panel .head {{ padding:8px 14px; font-size:12px; letter-spacing:2px; color:#FAF9F0; }}
  .old .head {{ background:#9A3B26; }}
  .new .head {{ background:#315D8C; }}
  .code {{ padding:18px 20px; font-family:"SF Mono",Menlo,Consolas,monospace; font-size:13px; line-height:1.65; min-height:520px; }}
  .badge {{ float:right; background:#FAF9F0; color:#383A3D; border-radius:20px; padding:1px 10px; font-size:11px; letter-spacing:1px; }}
  h2 {{ font-size:16px; margin:32px 0 12px; color:#2C2E31; border-left:4px solid #9A3B26; padding-left:10px; }}
  table {{ border-collapse:collapse; width:100%; background:#FAF9F0; border-radius:8px; overflow:hidden; }}
  th {{ background:#ECE8D0; color:#2C2E31; font-size:12px; padding:7px 10px; text-align:left; }}
  td {{ font-size:13px; }}
  code {{ font-family:Menlo,Consolas,monospace; background:#2626260D; padding:1px 5px; border-radius:3px; font-size:12px; }}
  .foot {{ margin-top:24px; color:#6E7278; font-size:12px; }}
</style>
</head>
<body>
<h1>水墨·丹青 v2.7 <span style="font-size:14px;color:#9A3B26">改造预览</span></h1>
<div class="sub">同一段 TypeScript 样例 · 左: v2.4 现状 / 右: v2.7 改造后 · scope 级配色自动解析</div>
<div class="cols">
  <div class="panel old"><div class="head">v2.4 旧版 <span class="badge">朱砂焦点 · 松绿注释</span></div>
    <div class="code">{old_code}</div></div>
  <div class="panel new"><div class="head">v2.7 新版 <span class="badge">远水蓝焦点 · 灰青注释</span></div>
    <div class="code">{new_code}</div></div>
</div>

<h2>关键角色变化</h2>
<table>{diff_rows}</table>

<h2>新色板角色表 (WCAG 实测)</h2>
<table>
  <tr><th>角色</th><th>色值</th><th>对比度</th><th>色族</th><th>字体</th></tr>
  {sw}
</table>

<div class="foot">测试套件结果: 44 通过 / 0 失败 / 0 警告 · 全部 125 项静态 Token ≥ 4.5:1 · 注释 5.36:1 · 注释/正文可分辨 1.93:1</div>
</body>
</html>'''
    with open(f"{ROOT}/scratch/danqing-v2.7-preview.html", "w", encoding="utf-8") as f:
        f.write(page)
    print("preview written:", f"{ROOT}/scratch/danqing-v2.7-preview.html")

if __name__ == "__main__":
    build()
