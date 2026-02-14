# AWS News Summary <!-- omit in toc -->

[English](README-en.md) | **日本語**

AWS What's New と AWS API Changes の情報を取得し、日本語で詳細な解説レポートを作成する Claude Agent SDK スキル。


- [アーキテクチャ](#アーキテクチャ)
  - [システム概要 (ハイレベル)](#システム概要-ハイレベル)
  - [システム概要 (詳細版)](#システム概要-詳細版)
  - [シーケンス図](#シーケンス図)
  - [シーケンス図 (Phase 2 詳細: Subagent 内部処理)](#シーケンス図-phase-2-詳細-subagent-内部処理)
- [プロジェクト構造](#プロジェクト構造)
- [MCP サーバー](#mcp-サーバー)
- [実行方法](#実行方法)
  - [CI/CD での実行 (Claude Agent SDK)](#cicd-での実行-claude-agent-sdk)
  - [ローカル開発](#ローカル開発)
- [情報ソース](#情報ソース)
- [出力](#出力)
- [参考資料](#参考資料)
  - [Claude Agent SDK](#claude-agent-sdk)
  - [CI/CD セットアップ](#cicd-セットアップ)
- [ライセンス](#ライセンス)


## アーキテクチャ

このスキルは Claude Agent SDK を使用し、GitHub Actions または GitLab CI からスケジュール実行される。`run.py` が 2 フェーズのオーケストレーターとして動作し、Phase 1 で Bedrock API 経由で Claude を呼び出して SKILL.md の定義に従い日本語レポートを自動生成し、Phase 2 では `AgentDefinition` で定義した `infographic-generator` subagent を Task ツール経由で並列に起動し、インフォグラフィックを生成する。

### システム概要 (ハイレベル)

```mermaid
flowchart TD
    Trigger["⏰ CI/CD Scheduled Trigger"]
    SDK["🐍 run.py (Claude Agent SDK)"]

    Trigger --> SDK

    subgraph Phase1["Phase 1: レポート生成"]
        direction TB
        Skill["📋 awsnews-summary Skill"]

        subgraph Collect["データ収集"]
            direction LR
            Bash["💻 Bash (curl)"]
            Feeds["📡 RSS/Atom Feeds"]
            Parse["🐍 Parse XML"]
            MCP["📚 MCP Server<br/>(AWS Docs)"]
            Bash --> Feeds --> Parse
            Bash ~~~ MCP
        end

        Filter["🔍 Filter & Check"]
        Generate["📝 Generate Report"]
        Reports["📁 reports/"]

        Skill --> Collect
        Parse --> Filter
        MCP --> Filter
        Filter --> Generate
        Generate --> Reports
    end

    subgraph Phase2["Phase 2: インフォグラフィック生成"]
        direction TB
        InfSkill["🎨 creating-infographic Skill"]
        Infographic["📊 infographic/"]
        InfSkill --> Infographic
    end

    SDK --> Phase1
    Reports -.->|"Subagent 並列実行<br/>(Task ツール経由)"| Phase2

    classDef ci fill:#F3E5F5,stroke:#CE93D8,stroke-width:2px,color:#6A1B9A
    classDef sdk fill:#E1BEE7,stroke:#CE93D8,stroke-width:2px,color:#6A1B9A
    classDef agent fill:#E8EAF6,stroke:#9FA8DA,stroke-width:2px,color:#283593
    classDef bash fill:#FFF3E0,stroke:#FFB74D,stroke-width:2px,color:#E65100
    classDef sources fill:#E3F2FD,stroke:#90CAF9,stroke-width:2px,color:#1565C0
    classDef mcp fill:#FFF8E1,stroke:#FFE082,stroke-width:2px,color:#F57F17
    classDef process fill:#FFECB3,stroke:#FFD54F,stroke-width:2px,color:#F57C00
    classDef output fill:#E8F5E9,stroke:#A5D6A7,stroke-width:2px,color:#2E7D32
    classDef frame fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666

    class Trigger ci
    class SDK sdk
    class Skill,InfSkill agent
    class Bash bash
    class Feeds sources
    class MCP mcp
    class Parse,Filter,Generate process
    class Reports,Infographic output
    class Phase1,Phase2,Collect frame
```

**全体フロー:**

このスキルは CI/CD から定期実行され、`run.py` が 2 フェーズで処理を行います。

1. **Phase 1 - レポート生成**: RSS/Atom フィードと AWS ドキュメントから情報を取得し、テンプレートベースで構造化された日本語レポートを作成 (awsnews-summary スキル)
2. **Phase 2 - インフォグラフィック生成**: メインエージェントが `AgentDefinition` で定義された `infographic-generator` subagent を Task ツール経由で並列に起動し、各レポートの HTML インフォグラフィックを生成 (creating-infographic スキル)

### システム概要 (詳細版)

以下は実際の技術的な実装とデータフローを詳細に表現した図です。

```mermaid
flowchart TB
    subgraph CI["CI/CD Environment"]
        Trigger["⏰ Scheduled Trigger<br/>(Daily 06:00 JST / 21:00 UTC)"]
        SDK["Claude Agent SDK<br/>(run.py)"]
    end

    subgraph Claude["Claude Agent"]
        Agent["🤖 Claude<br/>(Bedrock API)"]
        SkillDef["📋 SKILL.md<br/>(Instructions)"]
        Template["📄 report_template.md"]
    end

    Bash["💻 Bash Tool<br/>(curl commands)"]
    Scripts["🐍 Python Scripts"]

    subgraph External["External Data Sources"]
        Feeds["📡 RSS/Atom Feeds<br/>• AWS What's New (RSS)<br/>• AWS API Changes (RSS)<br/>• AWS Blog (Atom)"]
        Docs["📚 AWS Documentation<br/>(HTML/Markdown)"]
    end

    subgraph TempStorage["Temporary Storage (/tmp/)"]
        XMLNews["aws_news_feed.xml"]
        XMLAPI["aws_api_changes_feed.xml"]
        XMLBlog["aws_blog_feed.xml"]
    end

    subgraph Parsers["Parser Scripts"]
        ParseNews["parse_aws_news_feed.py<br/>📥 Input: XML<br/>📤 Output: JSON"]
        ParseAPI["parse_aws_api_changes_feed.py<br/>📥 Input: XML<br/>📤 Output: JSON"]
        ParseBlog["parse_aws_blog_feed.py<br/>📥 Input: XML<br/>📤 Output: JSON"]
    end

    subgraph MCP["MCP Server"]
        AWSKnowledge["aws-knowledge-mcp-server<br/>🔍 search_documentation<br/>📖 read_documentation"]
    end

    subgraph Processing["Claude Processing"]
        JSON1["📊 JSON Data<br/>(What's New items)"]
        JSON2["📊 JSON Data<br/>(API Changes)"]
        JSON3["📊 JSON Data<br/>(Blog posts)"]
        Filter["🔍 Filter & Prioritize<br/>(Period, Exclusions)"]
        Check["✅ Duplicate Check<br/>(Existing reports)"]
        Enrich["📝 Enrich Details<br/>(Docs, Blog links)"]
        Generate["📄 Generate Report<br/>(Template-based)"]
    end

    subgraph Output["Output Storage"]
        Reports["reports/{YYYY}/<br/>{date}-{slug}.md"]
        Infographic["infographic/<br/>{YYYYMMDD}-{slug}.html"]
        Git["📤 Git Commit & Push"]
    end

    %% Flow
    Trigger --> SDK
    SDK --> Agent
    Agent --> SkillDef
    
    %% Data Collection Flow
    SkillDef -->|"1. Execute curl"| Bash
    Bash -->|"HTTP GET"| Feeds
    
    Feeds -->|"XML Response"| Bash
    Bash -->|"Save XML"| XMLNews
    Bash -->|"Save XML"| XMLAPI
    Bash -->|"Save XML"| XMLBlog
    
    %% Parsing Flow
    SkillDef -->|"2. Execute python"| Scripts
    Scripts -->|"Run"| ParseNews
    Scripts -->|"Run"| ParseAPI
    Scripts -->|"Run"| ParseBlog
    
    XMLNews -->|"Read XML"| ParseNews
    ParseNews -->|"stdout JSON"| JSON1
    
    XMLAPI -->|"Read XML"| ParseAPI
    ParseAPI -->|"stdout JSON"| JSON2
    
    XMLBlog -->|"Read XML"| ParseBlog
    ParseBlog -->|"stdout JSON"| JSON3
    
    %% Processing Flow
    JSON1 --> Filter
    JSON2 --> Filter
    JSON3 --> Filter
    
    Filter --> Check
    Check -->|"New items only"| Enrich
    
    %% MCP Integration
    SkillDef -->|"3. Call MCP tools"| AWSKnowledge
    AWSKnowledge -->|"HTTP Request"| Docs
    Docs -->|"Markdown"| Enrich
    
    %% Report Generation
    Enrich --> Generate
    Template --> Generate
    Generate --> Reports
    Reports --> Git
    Reports -.->|"Phase 2<br/>(subagent 並列実行)"| Infographic
    Infographic --> Git
    
    %% Styling
    classDef ci fill:#F3E5F5,stroke:#CE93D8,stroke-width:2px,color:#6A1B9A
    classDef claude fill:#E8EAF6,stroke:#9FA8DA,stroke-width:2px,color:#283593
    classDef tools fill:#FFF3E0,stroke:#FFB74D,stroke-width:2px,color:#E65100
    classDef external fill:#E3F2FD,stroke:#90CAF9,stroke-width:2px,color:#1565C0
    classDef temp fill:#F5F5F5,stroke:#BDBDBD,stroke-width:2px,color:#424242
    classDef parsers fill:#FFF9C4,stroke:#FFF176,stroke-width:2px,color:#F57F17
    classDef mcp fill:#FFF8E1,stroke:#FFE082,stroke-width:2px,color:#F57F17
    classDef process fill:#FFECB3,stroke:#FFD54F,stroke-width:2px,color:#F57C00
    classDef output fill:#E8F5E9,stroke:#A5D6A7,stroke-width:2px,color:#2E7D32
    classDef data fill:#E1F5FE,stroke:#81D4FA,stroke-width:2px,color:#01579B
    classDef frame fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    
    class Trigger,SDK ci
    class Agent,SkillDef,Template claude
    class Bash,Scripts tools
    class Feeds,Docs external
    class XMLNews,XMLAPI,XMLBlog temp
    class ParseNews,ParseAPI,ParseBlog parsers
    class AWSKnowledge mcp
    class Filter,Check,Enrich,Generate process
    class JSON1,JSON2,JSON3 data
    class Reports,Git output
    class CI,Claude,External,TempStorage,Parsers,MCP,Processing,Output frame
```

**技術的な実装詳細:**

1. **データ収集フェーズ**
   - Claude Agent SDK が提供する Bash Tool 経由で `curl` コマンドを実行
   - RSS/Atom フィードを XML として `/tmp/` ディレクトリに保存
   - 3 つのフィード (What's New, API Changes, Blog) を並行取得

2. **パース処理フェーズ**
   - Python パーサースクリプト (`parse_*.py`) を実行
   - 各スクリプトが `/tmp/*.xml` を読み込み
   - 期間フィルタリングを適用し、JSON を stdout に出力

3. **詳細取得フェーズ**
   - MCP サーバー (`aws-knowledge-mcp-server`) 経由で追加情報を取得
   - `read_documentation`: What's New の詳細ページを Markdown で取得
   - `search_documentation`: 関連 Blog 記事を検索

4. **レポート生成フェーズ (Phase 1)**
   - 既存レポートとの重複チェック
   - テンプレート (`report_template.md`) ベースでレポート作成
   - `reports/{YYYY}/{date}-{slug}.md` に保存し Git にコミット

5. **インフォグラフィック生成フェーズ (Phase 2)**
   - `run.py` が 1 つの `query()` 呼び出しでオーケストレーターエージェントを起動
   - `AgentDefinition` で定義した `infographic-generator` subagent を Task ツール経由で並列に起動
   - 各 subagent が独立したコンテキストで `creating-infographic` スキルを使用して HTML インフォグラフィックを生成
   - `infographic/{YYYYMMDD}-{slug}.html` に保存

### シーケンス図

以下は、CI/CD パイプラインから run.py が Claude Agent SDK を実行し、2 フェーズでレポートとインフォグラフィックを生成する全体フローを示す。Phase 1 では awsnews-summary スキルを使用してレポートを生成し、Phase 2 では `AgentDefinition` で定義した `infographic-generator` subagent を Task ツール経由で並列に起動してインフォグラフィックを生成する。各フェーズのコンテキストが分離されることで、コンテキスト枯渇による生成漏れを防止する。

```mermaid
sequenceDiagram
    participant CI as ⏰ CI/CD<br/>(GitLab CI)
    participant RunPy as 🐍 run.py<br/>(Orchestrator)
    participant SDK as Claude Agent SDK
    participant LLM as 🤖 Claude<br/>(Bedrock API)
    participant Bash as 💻 Bash Tool
    participant Scripts as 🐍 Parser Scripts
    participant MCP as 📚 MCP Server<br/>(aws-knowledge)
    participant FS as 📁 File System

    Note over CI,FS: 初期化

    CI->>RunPy: python run.py --debug
    RunPy->>RunPy: AWS 認証情報検証 (STS)
    RunPy->>RunPy: モデル選択<br/>(Primary / Fallback)

    Note over CI,FS: Phase 1: レポート生成 (awsnews-summary スキル)

    activate RunPy
    RunPy->>SDK: run_skill(prompt)
    activate SDK

    SDK->>LLM: Request (prompt + tools)
    activate LLM
    LLM-->>SDK: Response (tool_use: Skill=awsnews-summary)
    deactivate LLM

    rect rgb(255, 255, 255)
        Note over SDK,Scripts: Step 0-1: データ収集
        SDK->>Bash: date (現在時刻確認)
        Bash-->>SDK: 日時
        SDK->>LLM: Request (Bash 結果)
        activate LLM
        LLM-->>SDK: Response (tool_use: Bash)
        deactivate LLM
        SDK->>Bash: curl AWS What's New RSS
        Bash-->>SDK: /tmp/aws_news_feed.xml
        SDK->>LLM: Request (Bash 結果)
        activate LLM
        LLM-->>SDK: Response (tool_use: Bash)
        deactivate LLM
        SDK->>Scripts: parse_aws_news_feed.py --days N
        Scripts-->>SDK: JSON (フィルタ済みアイテム)
    end

    SDK->>LLM: Request (パース結果)
    activate LLM
    LLM-->>SDK: Response (tool_use: Glob)
    deactivate LLM

    rect rgb(255, 255, 255)
        Note over SDK,MCP: Step 2-4: フィルタリング & 重複チェック
        SDK->>FS: Glob(reports/{YYYY}/*.md)
        FS-->>SDK: 既存レポート一覧
        SDK->>LLM: Request (Glob 結果)
        activate LLM
        LLM-->>SDK: Response (重複判定 + tool_use)
        deactivate LLM
    end

    rect rgb(240, 255, 240)
        Note over SDK,MCP: Step 5-8: 詳細取得 & レポート生成
        loop 新規アイテムごと
            SDK->>LLM: Request (次のアイテム処理)
            activate LLM
            LLM-->>SDK: Response (tool_use: MCP read)
            deactivate LLM
            SDK->>MCP: read_documentation(URL)
            MCP-->>SDK: Markdown (詳細)
            SDK->>LLM: Request (MCP 結果)
            activate LLM
            LLM-->>SDK: Response (tool_use: MCP search)
            deactivate LLM
            SDK->>MCP: search_documentation(keyword)
            MCP-->>SDK: Blog 検索結果
            SDK->>LLM: Request (検索結果)
            activate LLM
            LLM-->>SDK: Response (tool_use: Write)
            deactivate LLM
            SDK->>FS: Write reports/{YYYY}/{date}-{slug}.md
        end
    end

    SDK-->>RunPy: 新規レポートパス一覧を返却
    deactivate SDK

    Note over CI,FS: Phase 2: インフォグラフィック生成 (subagent 並列実行)

    rect rgb(248, 240, 255)
        RunPy->>SDK: generate_infographics()<br/>query(orchestrator_prompt,<br/>agents={infographic-generator: AgentDefinition(...)})
        activate SDK
        SDK->>LLM: Request (タスク一覧 + AgentDefinition)
        activate LLM
        LLM-->>SDK: Response (tool_use: Task × N 並列)
        deactivate LLM

        par レポート A の subagent
            SDK->>LLM: Subagent: レポート A のインフォグラフィック生成
            activate LLM
            LLM->>FS: Read report A
            LLM->>FS: Write infographic A
            LLM-->>SDK: Subagent 完了
            deactivate LLM
        and レポート B の subagent
            SDK->>LLM: Subagent: レポート B のインフォグラフィック生成
            activate LLM
            LLM->>FS: Read report B
            LLM->>FS: Write infographic B
            LLM-->>SDK: Subagent 完了
            deactivate LLM
        and レポート C の subagent
            SDK->>LLM: Subagent: レポート C のインフォグラフィック生成
            activate LLM
            LLM->>FS: Read report C
            LLM->>FS: Write infographic C
            LLM-->>SDK: Subagent 完了
            deactivate LLM
        end

        SDK-->>RunPy: 生成結果サマリー
        deactivate SDK
    end

    deactivate RunPy

    Note over CI,FS: 完了 & コミット

    RunPy-->>CI: Exit

    CI->>CI: インデックス更新<br/>(reports/index.md,<br/>infographic/index.html)
    CI->>CI: git add & commit & push<br/>(一括コミット)
```

### シーケンス図 (Phase 2 詳細: Subagent 内部処理)

以下は、Phase 2 における subagent の内部処理フローの詳細を示す。`run.py` が 1 つの `query()` 呼び出しでオーケストレーターエージェントを起動し、`AgentDefinition` で定義された `infographic-generator` subagent を Task ツール経由で並列に起動する。各 subagent は独立したコンテキストでレポートを読み込み、creating-infographic スキルを使用して HTML インフォグラフィックを生成する。

```mermaid
sequenceDiagram
    participant RunPy as 🐍 run.py
    participant SDK as Claude Agent SDK
    participant Orch as 🤖 Orchestrator Agent<br/>(メインエージェント)
    participant Sub as 🎨 infographic-generator<br/>(Subagent)
    participant FS as 📁 File System

    Note over RunPy,FS: Phase 2 開始: generate_infographics()

    RunPy->>RunPy: 対象レポートのフィルタリング<br/>(既存インフォグラフィックをスキップ)

    RunPy->>SDK: query(<br/>  prompt=orchestrator_prompt,<br/>  options=ClaudeAgentOptions(<br/>    allowed_tools=[..., "Task"],<br/>    agents={"infographic-generator":<br/>      AgentDefinition(<br/>        description="...",<br/>        prompt=subagent_prompt,<br/>        tools=["Skill","Read","Write",...]<br/>      )}<br/>  )<br/>)
    activate SDK

    SDK->>Orch: プロンプト + AgentDefinition 送信
    activate Orch

    Note over Orch: タスク一覧を解析し<br/>各レポートを subagent に委譲

    Orch->>SDK: tool_use: Task<br/>(infographic-generator,<br/>report_1 の処理指示)
    Orch->>SDK: tool_use: Task<br/>(infographic-generator,<br/>report_2 の処理指示)
    Orch->>SDK: tool_use: Task<br/>(infographic-generator,<br/>report_3 の処理指示)

    Note over SDK,Sub: 各 Task が独立した subagent として並列実行

    par Subagent 1: report_1
        SDK->>Sub: report_1 の処理開始
        activate Sub
        Sub->>FS: Read reports/2026/2026-02-10-xxx.md
        FS-->>Sub: レポート内容
        Sub->>Sub: Skill(creating-infographic)<br/>+ テーマ (awsnews.md) 読み込み
        Sub->>Sub: HTML インフォグラフィック生成
        Sub->>FS: Write infographic/20260210-xxx.html
        Sub-->>SDK: 完了 (成功)
        deactivate Sub
    and Subagent 2: report_2
        SDK->>Sub: report_2 の処理開始
        activate Sub
        Sub->>FS: Read reports/2026/2026-02-10-yyy.md
        FS-->>Sub: レポート内容
        Sub->>Sub: Skill(creating-infographic)<br/>+ テーマ (awsnews.md) 読み込み
        Sub->>Sub: HTML インフォグラフィック生成
        Sub->>FS: Write infographic/20260210-yyy.html
        Sub-->>SDK: 完了 (成功)
        deactivate Sub
    and Subagent 3: report_3
        SDK->>Sub: report_3 の処理開始
        activate Sub
        Sub->>FS: Read reports/2026/2026-02-10-zzz.md
        FS-->>Sub: レポート内容
        Sub->>Sub: Skill(creating-infographic)<br/>+ テーマ (awsnews.md) 読み込み
        Sub->>Sub: HTML インフォグラフィック生成
        Sub->>FS: Write infographic/20260210-zzz.html
        Sub-->>SDK: 完了 (成功)
        deactivate Sub
    end

    SDK-->>Orch: 全 subagent の結果
    Orch-->>SDK: 結果サマリー (N/M 成功)
    deactivate Orch

    SDK-->>RunPy: ResultMessage (生成結果)
    deactivate SDK

    RunPy->>RunPy: 生成されたファイルの存在確認
    RunPy->>RunPy: サマリー出力<br/>(Infographic Summary: N/M created)
```

## プロジェクト構造

```
awsnews-summary/
├── .claude/                           # Claude Code 設定
│   ├── settings.json                  # 権限と MCP 設定
│   └── skills/
│       ├── awsnews-summary/           # スキル定義 (レポート生成)
│       │   ├── SKILL.md               # スキル指示
│       │   ├── report_template.md     # レポートテンプレート
│       │   └── scripts/               # パーサースクリプト
│       │       ├── parse_aws_news_feed.py        # AWS What's New パーサー
│       │       ├── parse_aws_api_changes_feed.py # AWS API Changes パーサー
│       │       ├── parse_aws_blog_feed.py        # AWS Blog パーサー
│       │       └── parse_kiro_updates.py         # Kiro Updates パーサー
│       └── creating-infographic/      # スキル定義 (インフォグラフィック生成)
│           ├── SKILL.md               # スキル指示
│           └── themes/                # テーマ定義
├── .github/workflows/                 # GitHub Actions
├── .gitlab-ci.yml                     # GitLab CI パイプライン
├── .mcp.json                          # MCP サーバー設定
├── reports/                           # 生成されたレポート (年別)
│   ├── 2025/
│   └── 2026/
├── infographic/                       # 生成されたインフォグラフィック (HTML)
├── docs/                              # ドキュメント
│   ├── SETUP.md                       # CI/CD セットアップガイド (日本語)
│   └── SETUP-en.md                    # CI/CD セットアップガイド (英語)
├── CLAUDE.md                          # Claude Code 指示
├── README.md                          # 日本語ドキュメント
├── README-en.md                       # 英語ドキュメント
├── requirements.txt                   # Python 依存関係
└── run.py                             # CI/CD エントリポイント (2 フェーズオーケストレーター)
```

**注意**: スキルはプロジェクトレベル (`.claude/skills/`) で定義されている。これは、ユーザーレベルのスキル (`~/.claude/skills/`) が利用できない CI/CD 環境でも動作することを保証するため。`run.py` が Phase 1 (レポート生成) と Phase 2 (subagent 並列インフォグラフィック生成) をオーケストレーションする。

## MCP サーバー

このプロジェクトでは `.mcp.json` で設定された以下の MCP サーバーを使用する。

| サーバー | タイプ | 用途 |
|----------|--------|------|
| `aws-knowledge-mcp-server` | HTTP | AWS ドキュメント検索、ドキュメント読み込み、AWS Blog 検索 |

**注意**: RSS/Atom フィードの取得には MCP サーバーではなく、curl コマンドと外部 Python パーサースクリプト (scripts/) を使用している。これにより、RSS/Atom フィードのパース処理をスキル外で管理し、保守性を向上させている。

MCP 設定は Claude Agent SDK の `setting_sources=["project"]` により自動的に読み込まれる。

## 実行方法

### CI/CD での実行 (Claude Agent SDK)

このスキルは Claude Agent SDK を使用して GitHub Actions または GitLab CI から自動実行される。

**セットアップ手順**: CI/CD 環境での実行には、AWS IAM OIDC プロバイダー、IAM ロール、CI/CD 変数の設定が必要です。詳細な手順は以下のドキュメントを参照してください。

📖 **[CI/CD セットアップガイド (docs/SETUP.md)](docs/SETUP.md)**

セットアップガイドには以下の内容が含まれます。

- AWS IAM OIDC プロバイダーと IAM ロールの作成 (自動化スクリプト付き)
- GitHub Actions / GitLab CI 変数の設定
- トラブルシューティング

**GitHub Actions**:
```yaml
# .github/workflows/awsnews-summary.yml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ vars.AWS_ROLE_ARN }}
    aws-region: ${{ vars.AWS_REGION }}

- name: Run AWS News Summary
  run: python run.py
```

**GitLab CI**:
```yaml
# .gitlab-ci.yml
aws_news_summary:
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com
  script:
    - python run.py
```

### ローカル開発

**Claude Code CLI を使用**:
```bash
cd ~/.claude/skills/awsnews-summary
claude "AWS の最新ニュースをレポートして"
```

**run.py を使用**:
```bash
cd ~/.claude/skills/awsnews-summary
pip install -r requirements.txt

# デフォルトプロンプト (過去 1 週間)
python run.py

# カスタムプロンプト - 特定のサービスに絞る
python run.py "Run the awsnews-summary skill for Amazon Bedrock updates"

# カスタムプロンプト - 特定の期間を指定
python run.py "Run the awsnews-summary skill for AWS updates from the past 2 weeks"

# カスタムプロンプト - 特定の月を指定（実行時の現在日時が自動的に含まれます）
python run.py "Run the awsnews-summary skill for AWS updates launched in January 2026"
```

**注意**:
- `run.py` は Bedrock アクセス用の AWS 認証情報が設定されている必要がある
- プロンプトには「Run the awsnews-summary skill」を含めることで、スキルが確実に呼び出されます
- 実行時の現在日時が自動的にプロンプトに追加されるため、期間指定が正確に処理されます

## 情報ソース

| ソース | URL | フォーマット | 取得方法 |
|--------|-----|--------------|----------|
| AWS What's New | https://aws.amazon.com/new/feed/ | RSS/XML | curl + parse_aws_news_feed.py |
| AWS API Changes | https://awsapichanges.com/feed/feed.rss | RSS/XML | curl + parse_aws_api_changes_feed.py |
| AWS Blog | https://aws.amazon.com/blogs/aws/feed/ | Atom/XML | curl + parse_aws_blog_feed.py (補助) |
| AWS Blog | - | - | aws-knowledge-mcp-server search (推奨) |
| AWS Documentation | - | Markdown | aws-knowledge-mcp-server read_documentation |
| Kiro Blog | https://kiro.dev/blog/ | HTML | curl + parse_kiro_updates.py |
| Kiro Changelog | https://kiro.dev/changelog/ | HTML | curl + parse_kiro_updates.py |

## 出力

レポートとインフォグラフィックの 2 種類の成果物を生成する。

- **レポート**: 日本語 Markdown、`reports/{YYYY}/{YYYY}-{MM}-{DD}-{slug}.md`
- **インフォグラフィック**: HTML、`infographic/{YYYYMMDD}-{slug}.html`

## 参考資料

### Claude Agent SDK
- [Claude Agent SDK - Skills](https://platform.claude.com/docs/en/agent-sdk/skills) - SDK のエージェントスキル
- [Claude Agent SDK - Subagents](https://platform.claude.com/docs/en/agent-sdk/subagents) - SDK の Subagent (並列実行)
- [Claude Agent SDK - MCP](https://platform.claude.com/docs/en/agent-sdk/mcp) - SDK の MCP
- [Claude Agent SDK - Python](https://platform.claude.com/docs/en/agent-sdk/python) - Python SDK リファレンス
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - 概念的な概要
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) - 作成ガイドライン
- [Claude Code Skills](https://code.claude.com/docs/en/skills) - スキル完全ガイド

### CI/CD セットアップ
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) - GitHub Actions で AWS 認証情報を設定するための公式アクション
- [GitHub Actions: AWS での OpenID Connect の設定](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [GitLab CI: AWS での OpenID Connect の設定](https://docs.gitlab.com/ci/cloud_services/aws/)

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照。
