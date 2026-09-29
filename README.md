# DA Brand IP · 品牌 IP 创作室

![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square) ![Styles](https://img.shields.io/badge/Styles-124-8B5CF6?style=flat-square) ![Output](https://img.shields.io/badge/Output-3_Design_Assets-FF4D6D?style=flat-square)

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

`da-brand-ip` 将个人、企业、产品或组织的特点转化为可复用的角色资产。内置 124 种风格，从品牌简报、方向选择、主形象候选到三张正式设计图，再用确认后的角色制作文章和宣传配图。

## 亮点

- 支持真人转译、原创吉祥物、产品拟人、品牌符号角色及已有 IP 规范化。
- 按用途推荐 3—5 种风格；新建角色默认提供 3 张独立候选供选择。
- 正式交付固定为主形象设计卡、三视图、5 动作＋6 表情总览，共三张独立白底图。
- 支持多品牌、多角色、版本保存和 ZIP 导入导出，已确认角色可继续用于内容创作。
- 基础资产默认英文标签；文章和宣传图跟随原文语言，并按发布平台调整。

## 安装到 Codex

下载并解压本项目，在仓库目录运行以下命令。目标目录应尚未安装此 skill；已有安装请先备份，避免混合版本。

```bash
# Run from the downloaded repository directory.
mkdir -p "$HOME/.codex/skills/da-brand-ip"
cp -R SKILL.md agents assets references scripts requirements.txt "$HOME/.codex/skills/da-brand-ip/"
```

安装后可在下一轮对话使用。Windows 用户可将同样的文件和文件夹复制到 `%USERPROFILE%\.codex\skills\da-brand-ip`。需要 Python 3.9+；固定排版脚本依赖 Pillow 和可用的字体文件。图像生成依赖宿主提供的生图能力，脚本本身不生成角色。

## 快速开始

```text
使用 $da-brand-ip，为一家面向年轻人的咖啡品牌设计 IP。
希望温暖、有记忆点，可用于包装和公众号。先推荐角色方向和风格。
```

```text
使用 $da-brand-ip，把附件中的已有角色整理成主形象设计卡、三视图和动作表情总览。
```

```text
使用 $da-brand-ip，用已确认的角色为下面这篇公众号文章设计封面和正文配图：
[粘贴文章全文]
```

## 124 种风格与视觉参考

用当前[风格菜单](references/style-menu.md)中的编号、名称或稳定 ID 选择。以下五张图是用户提供的视觉参考，已压缩为 JPEG；**图内部分名称和编号与当前菜单不一致，不代表 124 种预设的一一对应预览**。选风格请以菜单和对应规则文件为准。点击可查看大图。

[![Style reference sheet 1](assets/previews/1.jpg)](assets/previews/1.jpg)

[![Style reference sheet 2](assets/previews/2.jpg)](assets/previews/2.jpg)

[![Style reference sheet 3](assets/previews/3.jpg)](assets/previews/3.jpg)

[![Style reference sheet 4](assets/previews/4.jpg)](assets/previews/4.jpg)

[![Style reference sheet 5](assets/previews/5.jpg)](assets/previews/5.jpg)

## 工作流程与交付

品牌简报 → 选择方向与风格 → 主形象候选 → 固定角色特征 → 三图交付 → 确认与版本保存 → 内容应用。

| 文件 | 内容 | 比例 |
|---|---|---|
| `01-main.png` | 完整主形象、最多 6 格真实特征、5—7 色色板 | 1:1 |
| `02-turnaround.png` | 正面、侧面、背面 | 3:2 |
| `03-overview.png` | 5 个全身动作与 6 个半身表情 | 4:3 |

角色包另存 `character.json` 和 `manifest.json`。未确认的修订不替换已启用版本；详见[资产包管理](references/package-management.md)。

## 本地开发

```bash
python3 -m pip install -r requirements.txt
python3 scripts/check_release.py
python3 scripts/package_manager.py --help
python3 scripts/compose_board.py --help
```

`package_manager.py` 管理本地角色包；`compose_board.py` 将已有角色图放入固定版式。布局位于 `assets/layouts/`，风格规则位于 `references/styles/`。


## 隐私与素材

用户照片、品牌文件、文章和生成资产保存在独立运行目录，默认 `.da-brand-ip/`，不写入 skill。使用前应拥有输入素材的使用权。无可用生图工具时，skill 提供提示词和规格，并明确说明尚未生成图片。

## 许可证与交流

[MIT License](LICENSE) · Copyright © DAAI。问题反馈欢迎[提交 Issue](https://github.com/daaihq/da-brand-ip/issues)。
