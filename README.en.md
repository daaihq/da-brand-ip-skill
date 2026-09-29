# DA Brand IP · Character Design Studio

![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square) ![Styles](https://img.shields.io/badge/Styles-124-8B5CF6?style=flat-square) ![Output](https://img.shields.io/badge/Output-3_Design_Assets-FF4D6D?style=flat-square)

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

`da-brand-ip` turns the identity of a person, company, product, or organization into reusable character assets. It includes 124 styles and guides you from a brand brief and concept selection to three design sheets and subsequent editorial or promotional images.

## Highlights

- Create portrait-inspired characters, original mascots, personified products, or standardized versions of existing characters.
- Receive 3–5 style recommendations and, by default, three separate initial character candidates.
- Deliver a character design card, a turnaround, and an overview with 5 poses and 6 expressions.
- Manage multiple brands, characters, and versions; import or export confirmed packages as ZIP files.
- Use English labels for base assets; match editorial and promotional text to the source language and publishing platform.

## Install in Codex

Download and extract this repository, then run the following from its root. Back up an existing installation before copying to avoid mixing versions.

```bash
# Run from the downloaded repository directory.
mkdir -p "$HOME/.codex/skills/da-brand-ip"
cp -R SKILL.md agents assets references scripts requirements.txt "$HOME/.codex/skills/da-brand-ip/"
```

The skill is available on your next turn. On Windows, copy the same files and folders to `%USERPROFILE%\.codex\skills\da-brand-ip`. Local helpers require Python 3.9+; layout composition also needs Pillow and a suitable font file. Character generation requires the host's image generation capability.

## Quick start

```text
Use $da-brand-ip to design a mascot for a coffee brand aimed at young adults.
It should feel warm and memorable, and work on packaging and social media.
Start by recommending character concepts and styles.
```

```text
Use $da-brand-ip to turn this existing character into a design card, turnaround,
and pose/expression overview.
```

```text
Use $da-brand-ip and my confirmed character to illustrate this blog article.
Publishing platform: my website. Full article: [paste text]
```

## 124 styles and visual references

Choose by number, name, or stable ID in the current [style menu](references/style-menu.md). The five supplied reference sheets below have been compressed to JPEG. **Some embedded names and numbers differ from the current menu; these are not a one-to-one preview of all 124 presets.** Use the menu and individual style files as the authority. Click a sheet to enlarge it.

[![Style reference sheet 1](assets/previews/1.jpg)](assets/previews/1.jpg)

[![Style reference sheet 2](assets/previews/2.jpg)](assets/previews/2.jpg)

[![Style reference sheet 3](assets/previews/3.jpg)](assets/previews/3.jpg)

[![Style reference sheet 4](assets/previews/4.jpg)](assets/previews/4.jpg)

[![Style reference sheet 5](assets/previews/5.jpg)](assets/previews/5.jpg)

## Workflow and deliverables

Brief → concept and style → character candidates → fixed identity → three design sheets → confirmation and version storage → content applications.

| File | Contents | Ratio |
|---|---|---|
| `01-main.png` | Full character, up to 6 detail slots, 5–7 palette colors | 1:1 |
| `02-turnaround.png` | Front, side, and back views | 3:2 |
| `03-overview.png` | 5 full-body poses and 6 half-body expressions | 4:3 |

Packages also contain `character.json` and `manifest.json`. Unconfirmed revisions do not replace the active version. See [package management](references/package-management.md).

## Local development

```bash
python3 -m pip install -r requirements.txt
python3 scripts/check_release.py
python3 scripts/package_manager.py --help
python3 scripts/compose_board.py --help
```

`package_manager.py` manages local character packages. `compose_board.py` places existing artwork into fixed layouts. Layouts live in `assets/layouts/`; style rules live in `references/styles/`. Operational skill references are currently written in Chinese.


## Privacy and media

User photos, brand files, articles, and generated assets belong in a separate runtime directory, normally `.da-brand-ip/`, never inside the skill. Use source material you have permission to use. If image tools are unavailable, the skill supplies prompts and specifications and states that no images were generated.

## License and feedback

[MIT License](LICENSE) · Copyright © DAAI. For feedback, [open an issue](https://github.com/daaihq/da-brand-ip-skill/issues).
