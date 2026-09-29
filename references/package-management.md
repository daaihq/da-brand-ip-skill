# 多品牌资产包与跨端恢复

用户资产放在可写运行目录，绝不放在Skill目录。Codex默认项目 `.da-brand-ip/`；ChatGPT按宿主持久化规则保存并保留实际引用。不会凭记忆恢复已丢失的文件。

结构：`brands/<brand-id>/characters/<character-id>/v001/` 下为 `manifest.json`、`character.json`、`01-main.png`、`02-turnaround.png`、`03-overview.png`。草稿递增v002等，不覆盖旧版；同品牌角色目录有active.json，运行根目录current.json记录当前明确选择。

## 角色规范字段

`character.json` 包含 brand_id、brand_name、entity_type、character_id、character_name、style_id、identity（完整身份文字）、palette（色板列表）、allowed_changes、forbidden_changes、actions（恰好5个标签／描述）、expressions（恰好6个）。可添加品牌简报、标签文本、来源说明与语种。

ID使用小写ASCII字母、数字、短横线或下划线，名称字段可用中文。entity_type从personal/company/brand/product/school/community/nonprofit/organization/event选择。style_id保留原表ID；定制风格以custom-开头并将完整规则写入角色规范。

## 脚本操作

以下SCRIPT替换为本Skill实际目录内scripts/package_manager.py，ROOT替换为运行目录。引用含空格路径时加引号。

```bash
python SCRIPT register --root ROOT --spec character.json --main 01-main.png --turnaround 02-turnaround.png --overview 03-overview.png
python SCRIPT confirm --root ROOT --brand example --character mascot --version v001 --confirmation '用户实际确认语句或已有授权' --visual-reviewed
python SCRIPT list --root ROOT
python SCRIPT resolve --root ROOT --brand example --character mascot
python SCRIPT activate --root ROOT --brand example --character mascot --version v001
python SCRIPT export --root ROOT --brand example --character mascot --out /path/brand-character.zip
python SCRIPT import --root OTHER_ROOT --archive /path/brand-character.zip
```

register只有三图真实存在且比例符合时成功。confirm前人工查看三图并核对规范；脚本的格式、尺寸、哈希检查不是视觉一致性验证。记录真实用户确认，不伪造。已有明确完成授权可直接完成验证和确认，不重复提问。

resolve与activate只接受已确认版本。新草稿不会更改active；修订未通过时旧角色仍可用于宣传。多个品牌不明确时先询问，不能因最近目录时间而猜客户。

导出仅包含已确认版本的五个必要文件，不包含客户原始照片、文章、候选或私钥。用户要求导出时才创建ZIP。导入验证哈希与结构，以本地新草稿版本保存，绝不覆盖或静默激活。若用户已明确授权启用该导入包，校验后直接确认，不必重复询问。

平台不支持脚本时建立相同字段的索引与文件关系；说明无法执行的校验，不能伪造路径、哈希或版本。不同客户端的Skill安装是独立事项；资产包可迁移，不宣称自动同步。

## v2设计卡字段与兼容

新建包明确设置layout_version=2。除原有字段外，signature_details为1—6个对象，含英文label和description（可中文）及可选slot（0—5）；color_palette为5—7个对象，含英文role、六位HEX值hex及可选slot（0—6）。palette原列表继续作为简要色板，须与color_palette一致；图中展示以color_palette为准。中文原角色名可保留在资料字段，另记录english_display_name，图中只用已确认英文名。

slot确定后跨版本保持对应位置，不随元素缺失自动挪位。没有服装时选真实结构特征，没有皮肤／头发／金属时替换用途标签。不得为凑色块改变人物实际配色；必要时从已有材质明暗与中性色中选取。

已存在v1包仍可读取、导入和使用；不能把旧图或旧目录自动改成v2。用户要求升级时创建新版本并制作设计卡，再确认。导入的旧包明确保留layout_version=1；新增注册默认v2且须提供v2字段。角色包只有三张正式图；如果第一张是设计卡，后续生图应仅使用左侧主体识别区，不把配色板、细节格、文字带入应用。

## 风格菜单重排兼容

124种菜单采用新编号；旧100种编号使用 style-number-map.json。保存与复用以稳定风格ID、角色规范、已确认图及包内提示词为准。来源更新不自动改变旧角色风格；同ID有用户新提示词时，新建角色优先新版，旧角色需要用户要求升级后另建版本，不覆盖旧包。
