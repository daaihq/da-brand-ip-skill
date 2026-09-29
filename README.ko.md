# DA Brand IP · 브랜드 캐릭터 스튜디오

![Skill](https://img.shields.io/badge/Skill-Codex-111111?style=flat-square) ![Styles](https://img.shields.io/badge/Styles-124-8B5CF6?style=flat-square) ![Output](https://img.shields.io/badge/Output-3_Design_Assets-FF4D6D?style=flat-square)

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

`da-brand-ip`는 개인, 기업, 제품, 조직의 특징을 재사용할 수 있는 캐릭터 자산으로 만드는 스킬입니다. 124가지 스타일을 바탕으로 브랜드 브리프, 방향 선택, 캐릭터 후보, 디자인 시트 3장, 콘텐츠 이미지 제작까지 안내합니다.

## 주요 기능

- 인물 사진의 캐릭터화, 오리지널 마스코트, 제품 의인화, 기존 캐릭터 정리를 지원합니다.
- 용도에 맞는 스타일 3~5가지를 추천하고, 신규 제작 시 기본적으로 개별 후보 이미지 3장을 만듭니다.
- 메인 디자인 카드, 3면도, 동작 5개와 표정 6개를 담은 시트를 흰 배경의 독립 파일로 제공합니다.
- 여러 브랜드와 캐릭터의 버전을 관리하고, 확정된 패키지를 ZIP으로 내보내거나 가져옵니다.
- 기본 자산의 라벨은 영어를 사용하며, 기사와 홍보 이미지는 원문 언어와 게시 플랫폼에 맞춥니다.

## Codex에 설치

저장소를 다운로드하고 압축을 푼 뒤 루트 폴더에서 다음 명령을 실행하세요. 기존 설치가 있다면 먼저 백업하여 버전이 섞이지 않도록 하세요.

```bash
# Run from the downloaded repository directory.
mkdir -p "$HOME/.codex/skills/da-brand-ip"
cp -R SKILL.md agents assets references scripts requirements.txt "$HOME/.codex/skills/da-brand-ip/"
```

설치 후 다음 대화 턴부터 사용할 수 있습니다. Windows에서는 같은 파일과 폴더를 `%USERPROFILE%\.codex\skills\da-brand-ip`에 복사하세요. 로컬 도구는 Python 3.9+가 필요하며 고정 레이아웃에는 Pillow와 적절한 글꼴 파일이 필요합니다. 캐릭터 생성에는 호스트의 이미지 생성 기능을 사용합니다.

## 빠른 시작

```text
$da-brand-ip로 젊은 고객을 위한 커피 브랜드 캐릭터를 만들어 주세요.
따뜻하고 기억하기 쉬우며 포장과 SNS에 활용할 수 있으면 좋겠습니다.
먼저 캐릭터 방향과 스타일을 추천해 주세요.
```

```text
$da-brand-ip로 첨부한 기존 캐릭터의 디자인 카드, 3면도,
동작과 표정 모음 시트를 만들어 주세요.
```

```text
$da-brand-ip로 확정된 캐릭터를 활용해 블로그 글의 이미지를 만들어 주세요.
게시 플랫폼: 회사 웹사이트. 글 전문: [본문 붙여넣기]
```

## 124가지 스타일과 시각 참고 자료

현재 [스타일 메뉴](references/style-menu.md)의 번호, 이름 또는 고정 ID로 선택하세요. 아래 5장은 제공된 참고 이미지를 JPEG로 압축한 것입니다. **이미지 안의 일부 이름과 번호는 현재 메뉴와 다르며, 124가지 프리셋과 일대일로 대응하는 미리보기가 아닙니다.** 선택 시 메뉴와 개별 스타일 규칙을 기준으로 삼으세요. 클릭하면 크게 볼 수 있습니다.

[![Style reference sheet 1](assets/previews/1.jpg)](assets/previews/1.jpg)

[![Style reference sheet 2](assets/previews/2.jpg)](assets/previews/2.jpg)

[![Style reference sheet 3](assets/previews/3.jpg)](assets/previews/3.jpg)

[![Style reference sheet 4](assets/previews/4.jpg)](assets/previews/4.jpg)

[![Style reference sheet 5](assets/previews/5.jpg)](assets/previews/5.jpg)

## 작업 흐름과 결과물

브리프 → 방향과 스타일 → 후보 → 정체성 확정 → 시트 3장 → 확인 및 버전 저장 → 콘텐츠 활용.

| 파일 | 내용 | 비율 |
|---|---|---|
| `01-main.png` | 전신 캐릭터, 최대 6개 특징 슬롯, 5~7색 팔레트 | 1:1 |
| `02-turnaround.png` | 정면, 측면, 후면 | 3:2 |
| `03-overview.png` | 전신 동작 5개와 반신 표정 6개 | 4:3 |

패키지에는 `character.json`과 `manifest.json`도 저장됩니다. 확인되지 않은 수정본은 활성 버전을 교체하지 않습니다. [패키지 관리](references/package-management.md)를 참고하세요.

## 로컬 개발

```bash
python3 -m pip install -r requirements.txt
python3 scripts/check_release.py
python3 scripts/package_manager.py --help
python3 scripts/compose_board.py --help
```

`package_manager.py`는 로컬 패키지를 관리하고 `compose_board.py`는 기존 이미지를 고정 레이아웃에 배치합니다. 레이아웃은 `assets/layouts/`, 스타일 규칙은 `references/styles/`에 있습니다. 스킬 본문과 운영 참고 문서는 현재 중국어입니다.


## 개인정보와 소재

사용자 사진, 브랜드 자료, 기사, 생성물은 스킬 내부가 아닌 별도 작업 폴더에 저장하며 기본 경로는 `.da-brand-ip/`입니다. 사용 권한이 있는 소재를 이용하세요. 이미지 도구가 없으면 프롬프트와 사양을 제공하고 이미지가 생성되지 않았음을 알립니다.

## 라이선스와 문의

[MIT License](LICENSE) · Copyright © DAAI. [Issues](https://github.com/daaihq/da-brand-ip-skill/issues)로 의견을 보내 주세요.
