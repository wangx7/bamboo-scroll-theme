#!/usr/bin/env python3
"""
水墨主题 (Shuimo Theme) 全场景深度测试套件
全面覆盖 12 大 UI 子系统、全语言语法高亮、WCAG 2.1 护眼对比度、终端 ANSI 表现与扩展协同
"""

import json
import os
import re
import sys
import argparse
import colorsys

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 8:
        hex_str = hex_str[:6]
    elif len(hex_str) == 4:
        hex_str = hex_str[:3]
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def luminance(r, g, b):
    a = [v / 255.0 for v in [r, g, b]]
    a = [((v + 0.055) / 1.055) ** 2.4 if v > 0.03928 else v / 12.92 for v in a]
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def contrast_ratio(hex1, hex2):
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    l1 = luminance(r1, g1, b1)
    l2 = luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

HEX_REGEX = re.compile(r'^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$')

SUBSYSTEMS = {
    "1. 基础纸面与全景无界 (Base & Window)": [
        ("editor.background", True),
        ("foreground", True),
        ("selection.background", True),
        ("focusBorder", True),
        ("sideBar.background", True),
        ("activityBar.background", True),
        ("statusBar.background", True)
    ],
    "2. 编辑器交互与光标水晕 (Editor Interaction)": [
        ("editor.selectionBackground", True),
        ("editor.selectionHighlightBackground", True),
        ("editor.wordHighlightBackground", True),
        ("editor.wordHighlightStrongBackground", True),
        ("editor.findMatchBackground", True),
        ("editor.findMatchHighlightBackground", True),
        ("editor.lineHighlightBackground", True),
        ("editorCursor.foreground", True)
    ],
    "3. 彩虹括号与缩进参考 (Brackets & Guides)": [
        ("editorBracketHighlight.foreground1", True),
        ("editorBracketHighlight.foreground2", True),
        ("editorBracketHighlight.foreground3", True),
        ("editorBracketHighlight.foreground4", True),
        ("editorBracketHighlight.foreground5", True),
        ("editorBracketHighlight.foreground6", True),
        ("editorBracketMatch.background", True),
        ("editorBracketPairGuide.activeBackground1", True)
    ],
    "4. 辅助阅读与吸顶行 (Sticky Scroll & Inlays)": [
        ("editorStickyScroll.background", True),
        ("editorStickyScrollHover.background", True),
        ("editorInlayHint.background", True),
        ("editorInlayHint.foreground", True),
        ("editorInlayHint.parameterForeground", True),
        ("editorInlayHint.typeForeground", True)
    ],
    "5. 诊断波浪线与 ErrorLens 协同 (Diagnostics)": [
        ("editorError.foreground", True),
        ("editorWarning.foreground", True),
        ("editorInfo.foreground", True),
        ("errorLens.errorBackground", True),
        ("errorLens.warningBackground", True),
        ("errorLens.infoBackground", True)
    ],
    "6. 智能浮层与弹窗 (IntelliSense & Widgets)": [
        ("editorSuggestWidget.background", True),
        ("editorSuggestWidget.selectedBackground", True),
        ("editorHoverWidget.background", True),
        ("peekViewEditor.background", True),
        ("quickInput.background", True)
    ],
    "7. 标签与窗口分屏 (Tabs & Editor Groups)": [
        ("tab.activeBackground", True),
        ("tab.activeForeground", True),
        ("tab.inactiveBackground", True),
        ("tab.inactiveForeground", True),
        ("editorGroupHeader.tabsBackground", True),
        ("editorGroup.border", True)
    ],
    "8. 资源管理与 Git 状态 (Explorer & SCM)": [
        ("sideBarTitle.foreground", True),
        ("breadcrumb.background", True),
        ("breadcrumb.foreground", True),
        ("gitDecoration.addedResourceForeground", True),
        ("gitDecoration.modifiedResourceForeground", True),
        ("gitDecoration.deletedResourceForeground", True),
        ("gitDecoration.untrackedResourceForeground", True),
        ("gitDecoration.conflictingResourceForeground", True)
    ],
    "9. 版本比对与三路合并 (Diff Editor & Merge)": [
        ("diffEditor.insertedTextBackground", True),
        ("diffEditor.removedTextBackground", True),
        ("diffEditor.unchangedRegionBackground", True),
        ("merge.currentHeaderBackground", True),
        ("merge.incomingHeaderBackground", True)
    ],
    "10. 终端控制台与 16 色 ANSI (Terminal)": [
        ("terminal.background", True),
        ("terminal.foreground", True),
        ("terminal.ansiBlack", True),
        ("terminal.ansiRed", True),
        ("terminal.ansiGreen", True),
        ("terminal.ansiYellow", True),
        ("terminal.ansiBlue", True),
        ("terminal.ansiMagenta", True),
        ("terminal.ansiCyan", True),
        ("terminal.ansiWhite", True),
        ("terminal.ansiBrightWhite", True)
    ],
    "11. 状态栏与命令中心 (StatusBar & CommandCenter)": [
        ("statusBar.background", True),
        ("statusBar.foreground", True),
        ("statusBar.debuggingBackground", True),
        ("commandCenter.background", True),
        ("commandCenter.foreground", True)
    ],
    "12. 现代 AI 与国画矿彩符号 (AI Chat & Symbols)": [
        ("chat.requestBackground", True),
        ("inlineChat.background", True),
        ("symbolIcon.classForeground", True),
        ("symbolIcon.functionForeground", True),
        ("symbolIcon.variableForeground", True),
        ("symbolIcon.propertyForeground", True),
        ("symbolIcon.interfaceForeground", True),
        ("symbolIcon.methodForeground", True)
    ]
}

class ThemeTester:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def assert_true(self, condition, msg):
        if condition:
            self.passed += 1
            print(f"    \033[32m✔\033[0m {msg}")
        else:
            self.failed += 1
            print(f"    \033[31m✘ FAIL:\033[0m {msg}")

    def warn(self, msg):
        self.warnings += 1
        print(f"    \033[33m▲ WARN:\033[0m {msg}")

    def run(self, target=None):
        print("\033[1;34m========================================================\033[0m")
        print("\033[1;34m        水墨主题 (Shuimo Theme) 全场景深度测试套件       \033[0m")
        print("\033[1;34m========================================================\033[0m\n")

        self.test_package_manifest()

        if target in (None, 'all', 'wuzheng'):
            # 水墨·无争：v2.5 生理学优化版，主背景已从 #F6F5E1 调整为 #F5F1DE
            self.test_theme_deep('themes/shuimo-wuzheng-theme.json', label='水墨·无争', is_light=True,
                                 editor_bg_expected='#F5F1DE', check_unity=False)

        if target in (None, 'all', 'danqing'):
            # 水墨·丹青：承「世界」之无界融通理念，全画布同色
            self.test_theme_deep('themes/shuimo-danqing-theme.json', label='水墨·丹青', is_light=True,
                                 editor_bg_expected='#F6F5E1', check_unity=True)

        if target in (None, 'all', 'zhuyun'):
            self.test_theme_deep('themes/shuimo-zhuyun-theme.json', label='水墨·竹韵', is_light=False,
                                 check_unity=True)

        self.test_showcase_files()

        print("\n\033[1;34m========================================================\033[0m")
        if self.failed == 0:
            print(f"\033[1;32m🎉 全场景测试全部通过! (通过: {self.passed}, 失败: 0, 提示: {self.warnings})\033[0m")
            print("\033[1;34m========================================================\033[0m")
            return 0
        else:
            print(f"\033[1;31m❌ 测试未通过! (通过: {self.passed}, 失败: {self.failed}, 提示: {self.warnings})\033[0m")
            print("\033[1;34m========================================================\033[0m")
            return 1

    def test_package_manifest(self):
        print("\033[1m[模块 1] 测试扩展元数据与清单配置 (package.json)\033[0m")
        pkg_path = os.path.join(self.root_dir, 'package.json')
        self.assert_true(os.path.exists(pkg_path), "package.json 文件存在")
        
        with open(pkg_path, 'r', encoding='utf-8') as f:
            pkg = json.load(f)

        self.assert_true('contributes' in pkg and 'themes' in pkg['contributes'], "package.json 包含 contributes.themes 贡献点")
        themes = pkg['contributes']['themes']
        self.assert_true(len(themes) >= 2, f"声明了 {len(themes)} 款官方主题")

        for t in themes:
            label = t.get('label')
            path = t.get('path')
            full_path = os.path.join(self.root_dir, path)
            self.assert_true(os.path.exists(full_path), f"主题 '{label}' 文件真实存在: {path}")

    def test_theme_deep(self, rel_path, label, is_light=True, editor_bg_expected=None, check_unity=False):
        print(f"\n\033[1m[模块 2] 深度测试主题: {label} ({rel_path})\033[0m")
        file_path = os.path.join(self.root_dir, rel_path)
        self.assert_true(os.path.exists(file_path), f"文件 {rel_path} 存在")

        with open(file_path, 'r', encoding='utf-8') as f:
            theme = json.load(f)

        colors = theme.get('colors', {})
        token_colors = theme.get('tokenColors', [])
        sem_colors = theme.get('semanticTokenColors', {})

        print(f"\n  \033[1;36m▶ 验证 12 大 UI 子系统覆盖度与完整性:\033[0m")
        for sub_name, keys in SUBSYSTEMS.items():
            missing_keys = [k for k, req in keys if req and k not in colors]
            if not missing_keys:
                self.assert_true(True, f"{sub_name} (全部 {len(keys)} 项已配置)")
            else:
                if is_light:
                    self.assert_true(False, f"{sub_name} (缺少: {', '.join(missing_keys)})")
                else:
                    self.warn(f"{sub_name} (缺少: {', '.join(missing_keys)})")

        print(f"\n  \033[1;36m▶ 验证色值格式与基础纸面特性:\033[0m")
        invalid_hexes = [f"{k}: {v}" for k, v in colors.items() if isinstance(v, str) and not HEX_REGEX.match(v)]
        self.assert_true(len(invalid_hexes) == 0, f"所有 UI 色值均为标准 Hex 格式 (共 {len(colors)} 项)")

        editor_bg = colors.get('editor.background')
        self.assert_true(editor_bg is not None, f"主画布背景已定义: {editor_bg}")

        if is_light:
            self.assert_true(editor_bg == editor_bg_expected, f"主画布背景已精准设定为暖纸宣色 ({editor_bg})")
            if check_unity:
                # 校验无界一体感
                sidebar_bg = colors.get('sideBar.background')
                activity_bg = colors.get('activityBar.background')
                status_bg = colors.get('statusBar.background')
                self.assert_true(sidebar_bg == editor_bg and activity_bg == editor_bg and status_bg == editor_bg, "秋水共长天一色: 侧边栏/活动栏/状态栏与编辑器无界融通")

        print(f"\n  \033[1;36m▶ 验证终端 ANSI 16 色与白字可见性:\033[0m")
        term_bg = colors.get('terminal.background', editor_bg)
        ansi_white = colors.get('terminal.ansiWhite')
        ansi_bwhite = colors.get('terminal.ansiBrightWhite')
        if term_bg and ansi_white:
            cr_white = contrast_ratio(term_bg, ansi_white)
            if is_light:
                self.assert_true(cr_white >= 3.0, f"终端 ANSI White 对比度 {cr_white:.2f}:1 (>= 3.0:1, 无白字隐形)")
            else:
                self.assert_true(cr_white >= 2.0, f"终端 ANSI White 对比度 {cr_white:.2f}:1")
        if term_bg and ansi_bwhite:
            cr_bwhite = contrast_ratio(term_bg, ansi_bwhite)
            self.assert_true(cr_bwhite >= 3.0, f"终端 ANSI BrightWhite 对比度 {cr_bwhite:.2f}:1")

        print(f"\n  \033[1;36m▶ 验证语法 Token 护眼对比度 (WCAG 2.1 AAA/AA):\033[0m")
        if editor_bg and is_light:
            checked_tokens = 0
            pass_tokens = 0
            for tc in token_colors:
                fg = tc.get('settings', {}).get('foreground')
                if fg and len(fg) == 7:
                    cr = contrast_ratio(editor_bg, fg)
                    checked_tokens += 1
                    if cr >= 4.5:
                        pass_tokens += 1
            self.assert_true(pass_tokens == checked_tokens, f"全静态语法 Token 满足长时护眼对比度规范 (含注释在内全部 >= 4.5:1 WCAG AA) ({pass_tokens}/{checked_tokens} 项通过)")

            editor_fg = colors.get('editor.foreground')
            comment_rule = next((tc for tc in token_colors if 'comment' in str(tc.get('scope', [])) and tc.get('settings', {}).get('foreground')), None)
            if editor_fg and comment_rule:
                comment_fg = comment_rule['settings']['foreground']
                cr_comment = contrast_ratio(editor_bg, comment_fg)
                cr_comment_code = contrast_ratio(comment_fg, editor_fg)
                self.assert_true(cr_comment >= 4.5, f"注释与纸面背景对比度 {cr_comment:.2f}:1 (>= 4.5:1)")
                # 注释/正文可分辨性: 正文进入 7~10:1 舒适区后, 与注释 AA(4.5:1) 的明度空间
                # 在数学上互斥于 2.3:1 (上限约 2.2:1)。1.9:1 + 斜体足以与内容区分。
                self.assert_true(cr_comment_code >= 1.9, f"注释与正文可分辨性 {cr_comment_code:.2f}:1 (>= 1.9:1, 注释不再与内容粘连)")

            # 水色约束：编辑区有色 token 只允许「水色系 + 朱砂」两族
            token_fgs = []
            for tc in token_colors:
                fg = tc.get('settings', {}).get('foreground')
                if fg and len(fg) == 7 and fg not in token_fgs:
                    token_fgs.append(fg)
            water_count = 0
            cinnabar_count = 0
            other_color = []
            for fg in token_fgs:
                r, g, b = hex_to_rgb(fg)
                h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
                if s >= 0.20:
                    hue = h * 360.0
                    # 水色系 = 绿→青→蓝→紫完整冷色带 (hue 100~300):
                    # 潭水青(#1F6E5C≈165°)/松绿(#4C7548≈115°)/远水蓝(#3A6680≈203°)/紫毫(#6F5E8A≈263°)
                    if 100.0 <= hue <= 300.0:
                        water_count += 1
                    elif hue < 60.0 or hue > 340.0:
                        cinnabar_count += 1
                    else:
                        other_color.append(f"{fg}(hue={hue:.0f},sat={s:.2f})")
            self.assert_true(water_count > 0, f"编辑区保留水色系 token ({water_count} 种水色)")
            self.assert_true(cinnabar_count > 0, f"编辑区保留朱砂 token ({cinnabar_count} 种朱砂)")
            self.assert_true(len(other_color) == 0, f"编辑区无非水色/非朱砂的有彩色: {', '.join(other_color) if other_color else '无'}")

        print(f"\n  \033[1;36m▶ 验证现代特性与语义高亮 (Semantic Highlighting):\033[0m")
        self.assert_true(theme.get('semanticHighlighting') is True, "已开启 semanticHighlighting: true")
        self.assert_true(len(sem_colors) >= 20, f"已定义 {len(sem_colors)} 项语义高亮规则")
        self.assert_true('keyword' in sem_colors and 'function' in sem_colors and 'class' in sem_colors, "核心语义规则 (keyword/function/class) 完备")

    def test_showcase_files(self):
        print(f"\n\033[1m[模块 3] 验证多语言与多场景视觉测试样例库 (tests/showcase/)\033[0m")
        showcase_dir = os.path.join(self.root_dir, 'tests/showcase')
        self.assert_true(os.path.exists(showcase_dir), "tests/showcase 目录存在")

        expected_files = [
            ("demo.vue", "Vue 3 SFC (PascalCase 组件 / 指令 / TS Setup)"),
            ("demo.ts", "TypeScript (泛型 / 接口 / 装饰器 / 枚举)"),
            ("demo.py", "Python (类 / f-string / 装饰器 / 异常)"),
            ("demo.go", "Go (结构体 / 接口 / 协程 / Struct Tags)"),
            ("demo.rs", "Rust (生命周期 / Traits / 模式匹配 / 宏)"),
            ("demo.sql", "SQL (关键字 / 聚合查询 / 数据库定义)"),
            ("demo.json", "JSON (数据结构 / Schema / 键值对)"),
            ("demo_comments.ts", "注释全覆盖 (Better Comments / Todo Tree / JSDoc)"),
            ("demo.md", "Markdown (H1-H6 阶梯墨色 / 引用 / 代码块 / 表格)")
        ]

        for fname, desc in expected_files:
            fpath = os.path.join(showcase_dir, fname)
            exists = os.path.exists(fpath)
            self.assert_true(exists, f"样例文件存在: {fname:18s} -> {desc}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="水墨主题全场景测试套件")
    parser.add_argument('--wuzheng', action='store_true', help="仅测试「水墨·无争」")
    parser.add_argument('--danqing', action='store_true', help="仅测试「水墨·丹青」")
    parser.add_argument('--zhuyun', action='store_true', help="仅测试「水墨·竹韵」")
    args = parser.parse_args()

    target = 'all'
    if args.wuzheng:
        target = 'wuzheng'
    elif args.danqing:
        target = 'danqing'
    elif args.zhuyun:
        target = 'zhuyun'

    tester = ThemeTester()
    sys.exit(tester.run(target=target))
