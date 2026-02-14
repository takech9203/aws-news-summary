---
name: aws-news-summary
description: AWS What's New、AWS API Changes、Kiro (kiro.dev) の情報を取得し、日本語で詳細な解説レポートを作成するスキル。ユーザーが「AWS新機能」「AWSアップデート」「AWS What's New」「AWS API変更」「AWSニュース」「最新のAWS情報」「Kiroアップデート」「Kiro新機能」などと言った場合に使用する。特定のAWSサービスの最新情報や、期間を指定したAWSアップデートの調査にも対応。Kiro (kiro.dev) のブログやチェンジログの更新情報も同様にレポートを生成する。
---

# AWS News Reporter Skill <!-- omit in toc -->

## 目次

- [目次](#目次)
- [情報ソース](#情報ソース)
- [ワークフロー](#ワークフロー)
  - [0. 現在時刻の確認](#0-現在時刻の確認)
  - [1. RSS フィードから最新情報を取得](#1-rss-フィードから最新情報を取得)
  - [1.1. Kiro アップデートの取得](#11-kiro-アップデートの取得)
  - [2. 期間フィルタリング（デフォルト: 過去3日間）](#2-期間フィルタリングデフォルト-過去3日間)
  - [3. 除外フィルタリング](#3-除外フィルタリング)
  - [4. 重複チェック](#4-重複チェック)
  - [5. 詳細情報の取得](#5-詳細情報の取得)
    - [What's New ページの詳細](#whats-new-ページの詳細)
    - [AWS API Changes の確認（必要に応じて）](#aws-api-changes-の確認必要に応じて)
    - [Kiro アップデートの詳細](#kiro-アップデートの詳細)
  - [6. レポート作成](#6-レポート作成)
  - [7. アーキテクチャ図の作成（必要に応じて）](#7-アーキテクチャ図の作成必要に応じて)
  - [8. AWS Blog リンクの取得（可能な場合）](#8-aws-blog-リンクの取得可能な場合)
- [出力形式](#出力形式)
- [実行例](#実行例)
  - [例1: デフォルト実行（過去1週間のアップデート）](#例1-デフォルト実行過去1週間のアップデート)
  - [例2: 期間指定](#例2-期間指定)
  - [例3: サービス指定](#例3-サービス指定)
  - [例4: Kiro アップデート](#例4-kiro-アップデート)
- [除外サービス](#除外サービス)
- [除外アップデートタイプ](#除外アップデートタイプ)
  - [リージョン拡大のみのアップデート](#リージョン拡大のみのアップデート)
  - [AWS Direct Connect](#aws-direct-connect)
  - [その他](#その他)
- [注意事項](#注意事項)


AWS What's New、AWS API Changes、Kiro (kiro.dev) から最新情報を取得し、構造化されたレポートを作成する。

## 情報ソース

1. **AWS What's New RSS Feed**: https://aws.amazon.com/new/feed/
   - 公式発表、新機能、サービスアップデートの RSS フィード
   - XML 形式

2. **AWS API Changes**: https://awsapichanges.com/
   - API の追加・変更履歴
   - RSS Feed: https://awsapichanges.com/feed/feed.rss
   - 各 API 変更の詳細情報を提供

3. **AWS Blog**: https://aws.amazon.com/blogs/
   - What's New と関連する詳細記事
   - 推奨: aws-knowledge-mcp-server で検索（`topics: ["current_awareness", "general"]`）
   - 補助: RSS Feed（https://aws.amazon.com/blogs/aws/feed/）

4. **AWS Documentation Search**:
   - `mcp__aws-knowledge-mcp-server__aws___search_documentation` を使用
   - 詳細情報の検索、トラブルシューティング、ベストプラクティスの確認に活用

5. **Kiro (kiro.dev)**:
   - Blog: https://kiro.dev/blog/ — 新機能紹介、活用事例などの記事
   - Changelog: https://kiro.dev/changelog/ — バージョンごとの変更履歴
   - HTML ページを curl で取得し、`parse_kiro_updates.py` でパース
   - Kiro は AWS が提供する AI 搭載 IDE

## ワークフロー

### 0. 現在時刻の確認

**重要**: 作業を開始する前に、必ず現在時刻を確認する。

```bash
date "+%Y-%m-%d %H:%M:%S %Z"
```

これにより、ユーザーが指定した期間（例: 「2026年1月」「過去1週間」）が現在の日付から見て適切かどうかを判断できる。

### 1. RSS フィードから最新情報を取得

**重要**: RSS フィードは**1回だけ**取得する。複数回リクエストしない。

**取得方法**: Bash ツールで curl と外部スクリプトを使用する

```bash
# RSS フィードを取得して一時ファイルに保存
curl -L -s "https://aws.amazon.com/new/feed/" > /tmp/aws_news_feed.xml

# パーサースクリプトで JSON に変換（過去7日間）
python3 .claude/skills/aws-news-summary/scripts/parse_aws_news_feed.py --days 7 --feed /tmp/aws_news_feed.xml
```

**パーサースクリプトのオプション:**
- `--days DAYS`: 取得する期間（デフォルト: 7）
- `--feed PATH`: RSS フィードファイルのパス（デフォルト: /tmp/aws_news_feed.xml）

**期間指定の例:**
```bash
# 過去14日間のアイテムを取得
python3 .claude/skills/aws-news-summary/scripts/parse_aws_news_feed.py --days 14
```

- RSS フィードは XML 形式で以下の情報を含む:
  - `<item>`: 各アナウンスメント
  - `<title>`: タイトル
  - `<description>`: 説明（HTML形式）
  - `<pubDate>`: 公開日時（例: "Mon, 29 Dec 2025 15:00:00 GMT"）
  - `<link>`: 詳細ページ URL
  - `<category>`: カテゴリ（サービス名など）
- 取得できたアイテムで処理を続ける（全アイテムが取得できなくても問題なし）

### 1.1. Kiro アップデートの取得

AWS RSS フィードの取得と並行して、Kiro (kiro.dev) のブログとチェンジログからアップデート情報を取得する。

**重要**: Kiro ページも**1回だけ**取得する。複数回リクエストしない。

**取得方法**: Bash ツールで curl と外部スクリプトを使用する

```bash
# Kiro Blog ページを取得
curl -sL "https://kiro.dev/blog/" > /tmp/kiro_blog.html

# Kiro Changelog ページを取得
curl -sL "https://kiro.dev/changelog/" > /tmp/kiro_changelog.html

# Blog エントリをパース（過去7日間）
python3 .claude/skills/aws-news-summary/scripts/parse_kiro_updates.py --source blog --days 7 --feed /tmp/kiro_blog.html

# Changelog エントリをパース（過去7日間）
python3 .claude/skills/aws-news-summary/scripts/parse_kiro_updates.py --source changelog --days 7 --feed /tmp/kiro_changelog.html
```

**パーサースクリプトのオプション:**

- `--source blog|changelog`: パース対象（必須）
- `--days DAYS`: 取得する期間（デフォルト: 7）
- `--feed PATH`: HTML ファイルのパス（指定しない場合は stdin から読み込み）

**出力形式**: JSON（AWS RSS パーサーと同様の構造）

```json
{
  "source": "kiro-blog",
  "total_items": 2,
  "items": [
    {
      "title": "Introducing Claude Opus 4.6 in Kiro",
      "date": "2026-02-05",
      "url": "https://kiro.dev/blog/opus-4-6/",
      "source": "kiro-blog"
    }
  ]
}
```

**Blog と Changelog の使い分け:**

- Blog: 新機能の詳細な紹介記事。レポートのメインソースとして使用
- Changelog: バージョンごとの変更一覧。Blog 記事がない場合や補足情報として使用
- 同じ機能が Blog と Changelog の両方に記載されている場合、Blog を優先してレポートを作成し、Changelog は補足情報として参照

### 2. 期間フィルタリング（デフォルト: 過去3日間）

RSS フィードをパースする際に、指定期間内のアイテムを抽出:
- デフォルト: 過去 3 日間（`--days 3`）- 毎日実行を想定
- ユーザー指定: 「過去1週間」→ `--days 7`、「過去2週間」→ `--days 14` など
- パーサースクリプトの `--days` オプションで期間を変更

### 3. 除外フィルタリング

取得したアイテムから、除外対象を除いたアップデートについてレポートを作成する。
除外対象は「除外サービス」および「除外アップデートタイプ」セクションを参照。

**重要: 除外ルールに該当しない限り、すべてのアップデートを対象とする。**

マイナーなアップデートであっても、Solutions Architect として知っておくべき情報であれば含める。判断に迷った場合は対象とする。除外して後から「知らなかった」となるリスクより、網羅的にカバーする方が価値がある。

### 4. 重複チェック

レポート作成前にプロジェクトルートの `reports/{YYYY}/` ディレクトリを確認:

```
# 既存レポートのファイル名を確認（年別フォルダ）
# 例: Glob(pattern="reports/2025/*.md")
Glob(pattern="reports/{pubDateの年}/*.md")
```

ファイル名形式: `{YYYY}-{MM}-{DD}-{slug}.md`
- 同じ日付・同じ slug のレポートが存在する場合はスキップ

**slug の生成ルール:**
- What's New の URL パスの最後の部分をそのまま使用する
- URL 例: `https://aws.amazon.com/about-aws/whats-new/2026/01/ec2-capacity-manager-spot-interruption-metrics/`
- slug: `ec2-capacity-manager-spot-interruption-metrics`
- **重要**: URL の末尾部分をそのまま使用し、独自に slug を作成しない

**Kiro アップデートの slug 生成ルール:**
- Blog URL のパスから生成する
- URL 例: `https://kiro.dev/blog/opus-4-6/`
- slug: `kiro-opus-4-6`（先頭に `kiro-` を付与）
- Changelog のみの場合: `kiro-changelog-{YYYY-MM-DD}` 形式

### 5. 詳細情報の取得

選定したアップデートについて詳細を取得:

#### What's New ページの詳細
- `mcp__aws-knowledge-mcp-server__aws___read_documentation` で取得
- URL 例: `https://aws.amazon.com/about-aws/whats-new/2026/01/...`

#### AWS API Changes の確認（必要に応じて）

**取得方法**: Bash ツールで curl と外部スクリプトを使用する

```bash
# AWS API Changes RSS フィードを取得
curl -L -s "https://awsapichanges.com/feed/feed.rss" > /tmp/aws_api_changes_feed.xml

# パーサースクリプトで JSON に変換（過去7日間）
python3 .claude/skills/aws-news-summary/scripts/parse_aws_api_changes_feed.py --days 7 --feed /tmp/aws_api_changes_feed.xml

# 特定のサービスの詳細情報を取得（API メソッド名と変更内容を含む）
python3 .claude/skills/aws-news-summary/scripts/parse_aws_api_changes_feed.py --days 30 --service "Bedrock" --details --feed /tmp/aws_api_changes_feed.xml
```

**パーサースクリプトのオプション:**
- `--days DAYS`: 取得する期間（デフォルト: 7）
- `--feed PATH`: RSS フィードファイルのパス（デフォルト: /tmp/aws_api_changes_feed.xml）
- `--service NAME`: サービス名でフィルタリング（部分一致、大文字小文字区別なし）
- `--details`: 各エントリの詳細ページから API メソッド情報を取得

**詳細情報の取得:**
`--details` オプションを使用すると、各 API 変更の詳細ページから以下の情報を取得:
- メソッド名（例: `CreateCapacityProvider`, `DescribeFleets`）
- 変更タイプ（new, updated, removed）
- リクエスト/レスポンスの変更内容

**マッチング方法:**
- What's New のサービス名と API Changes のサービス名を照合
- 同じ日付または近い日付の API 変更を確認
- API 変更がレポートに関連する場合のみ含める

**レポートへの記載:**
- API 変更履歴セクションのサービス名に、awsapichanges.com の該当ページへのリンクを追加する
- URL 形式: `https://awsapichanges.com/archive/changes/{hash}-{service}.html`
- 例: `[ecs](https://awsapichanges.com/archive/changes/d7832c-ecs.html)`
- パーサースクリプトの出力に含まれる `link` フィールドを使用する

#### Kiro アップデートの詳細

Kiro のアップデートについて、Blog 記事の詳細内容を取得する。

**Blog 記事の詳細取得:**

```bash
# Blog 記事の個別ページから詳細テキストを取得
curl -sL "https://kiro.dev/blog/{slug}/" > /tmp/kiro_blog_detail.html

# テキスト抽出（HTML タグを除去して本文を取得）
# sed で HTML タグを除去し、主要なテキストコンテンツを抽出
cat /tmp/kiro_blog_detail.html | sed 's/<[^>]*>//g' | sed '/^$/d' | head -200
```

**代替方法**: WebFetch は使用せず、curl で取得した HTML からテキストを抽出する。Next.js の SPA であるため、サーバーサイドレンダリングされたテキストノードから情報を取得する。

**Changelog の詳細:**

Changelog エントリは `parse_kiro_updates.py` の出力に `description` フィールドが含まれるため、追加の詳細取得は不要。必要に応じて Changelog ページ全体のテキストを参照する。

### 6. レポート作成

`.claude/skills/aws-news-summary/report_template.md` のテンプレートを使用してレポートを作成する。

**インフォグラフィック URL の決定:**

レポート内のインフォグラフィックリンク URL は、環境変数 `INFOGRAPHIC_BASE_URL` から取得する。

```bash
echo "$INFOGRAPHIC_BASE_URL"
```

- CI/CD 環境: GitLab CI/CD Variables または GitHub Repository Variables で設定
- ローカル環境: `export INFOGRAPHIC_BASE_URL=https://your-user.github.io/your-repo` のように設定

テンプレート内の `{INFOGRAPHIC_BASE_URL}` を取得した値で置換し、`{YYYYMMDD}-{slug}.html` と組み合わせて完全な URL を生成する。

**例**: `https://your-user.github.io/your-repo/20260209-amazon-redshift-allocate-extra-compute-for-automatic-optimizations.html`

**出力先**: `reports/{YYYY}/{YYYY}-{MM}-{DD}-{slug}.md` (プロジェクトルートからの相対パス)
- レポートは pubDate の年に対応するフォルダに作成
- フォルダが存在しない場合は新規作成

**Kiro アップデートのレポート:**

Kiro アップデートも AWS アップデートと同じテンプレートとフォーマットでレポートを作成する。以下の点に注意する。

- **サービス名**: 「Kiro」を使用
- **リリース日**: Blog 記事または Changelog の日付を使用
- **参考リンク**: Blog URL、Changelog URL、kiro.dev のドキュメントリンクを含める
- **API 変更履歴セクション**: Kiro には該当しないため省略
- **料金セクション**: 該当する場合のみ記載
- **利用可能リージョンセクション**: Kiro はグローバルサービスのため「グローバル」と記載
- テンプレートの各セクションは、Kiro の文脈に合わせて適宜調整する（不要なセクションは削除）

### 7. アーキテクチャ図の作成（必要に応じて）

以下のようなアップデートの場合、理解を助けるために Mermaid でアーキテクチャ図やシーケンス図を作成する。
**配置場所**: レポートテンプレートの「## アーキテクチャ図」セクション（概要セクションの直後）

**図を作成するケース:**
- 新しいサービス連携やインテグレーション機能
- データフローや処理の流れが重要な機能
- 複数のコンポーネントが関係するアーキテクチャ
- Before/After の比較が有効な機能改善
- セキュリティやネットワーク構成に関する機能

**図の種類:**
- `flowchart`: アーキテクチャ概要、コンポーネント構成
- `sequenceDiagram`: API 呼び出しフロー、処理シーケンス
- `graph`: サービス間の関係性

**絵文字の活用:**

**注意:**
- 図をわかりやすくするために、適切な絵文字を使用する
- 図は必須ではなく、理解を助ける場合にのみ作成する
- シンプルで見やすい図を心がける
- 図には簡潔な説明を添える
- 該当しない場合はセクションごと削除する

### 8. AWS Blog リンクの取得（可能な場合）

アップデートに関連する AWS Blog 記事がある場合、参考リンクに含める。

**推奨方法**: aws-knowledge-mcp-server で検索する

```python
# AWS Blog 記事を検索
mcp__aws-knowledge-mcp-server__aws___search_documentation(
    search_phrase="<サービス名> <機能キーワード> blog",
    topics=["current_awareness", "general"],
    limit=3
)
```

**検索例:**
- "Amazon Bedrock multi-agent collaboration blog"
- "AWS Lambda Durable Functions blog"
- "Amazon EC2 Spot interruption metrics blog"

**マッチング方法:**
- What's New のサービス名と機能キーワードで検索
- 検索結果の `context` (要約) を確認して関連性を判断
- `url` が `aws.amazon.com/blogs/` で始まる記事を優先
- 関連する Blog 記事が見つかった場合のみレポートに含める

**補助方法**: RSS フィード（aws-knowledge-mcp-server で見つからない場合）

```bash
# AWS Blog Atom フィードを取得
curl -L -s "https://aws.amazon.com/blogs/aws/feed/" > /tmp/aws_blog_feed.xml

# パーサースクリプトで JSON に変換（過去7日間）
python3 .claude/skills/aws-news-summary/scripts/parse_aws_blog_feed.py --days 7 --feed /tmp/aws_blog_feed.xml
```

**パーサースクリプトのオプション:**
- `--days DAYS`: 取得する期間（デフォルト: 7）
- `--feed PATH`: Atom フィードファイルのパス（デフォルト: /tmp/aws_blog_feed.xml）

- pubDate が近い記事を手動で確認
- Blog 記事が見つからない場合は省略可

## 出力形式

- 言語: 日本語
- フォーマット: Markdown
- 出力先: `reports/{YYYY}/` (プロジェクトルートからの相対パス)
- ファイル名: `{YYYY}-{MM}-{DD}-{slug}.md`

## 実行例

### 例1: デフォルト実行（過去1週間のアップデート）

ユーザー: 「AWS の最新ニュースをレポートして」

1. AWS What's New RSS フィード取得（curl、1回のみ）
2. 過去 7 日間のアイテムを抽出
3. 除外対象を除外
4. 既存レポートと重複チェック
5. 詳細情報を取得
   - What's New ページ（aws-knowledge-mcp-server）
   - AWS API Changes（curl、必要に応じて）
   - AWS Blog 記事（aws-knowledge-mcp-server で検索）
6. 新規アイテムのみレポート作成

### 例2: 期間指定

ユーザー: 「過去2週間の AWS アップデートをまとめて」

1. AWS What's New RSS フィード取得（curl、1回のみ）
2. 過去 14 日間のアイテムを抽出（`--days 14`）
   ```bash
   python3 .claude/skills/aws-news-summary/scripts/parse_aws_news_feed.py --days 14
   ```
3. 以降同様

### 例3: サービス指定

ユーザー: 「Amazon Bedrock の最新アップデートを教えて」

1. AWS What's New RSS フィード取得（curl、1回のみ）
2. category に "amazon-bedrock" を含むアイテムを抽出
3. AWS API Changes RSS フィードから Bedrock 関連の API 変更を取得
4. 以降同様

### 例4: Kiro アップデート

ユーザー: 「Kiro の最新アップデートを教えて」

1. Kiro Blog / Changelog ページ取得（curl、各 1 回のみ）
2. `parse_kiro_updates.py` でエントリをパース
3. 既存レポートと重複チェック
4. Blog 記事の詳細を curl で取得
5. レポート作成（AWS アップデートと同じテンプレート）

ユーザー: 「AWS と Kiro の最新ニュースをまとめて」

1. AWS What's New RSS フィード取得 + Kiro Blog/Changelog 取得（並行）
2. 両方のアイテムを期間フィルタリング
3. 以降、各アイテムについて同様のワークフローを実行

## 除外サービス

以下のサービスはレポート対象外とする:
- Amazon GameLift (GameLift Streams 含む)

## 除外アップデートタイプ

以下のタイプのアップデートはレポート対象外とする:

### リージョン拡大のみのアップデート
- 中国リージョン (China) のみのサポート追加
- AWS GovCloud (US) のみのサポート追加（**ただし、GovCloud での新機能 GA は対象**）

**重要**: 以下は**対象として含める**:
- 東京リージョンへの新規対応
- 新しいインスタンスタイプのリージョン拡大（例: C8gn、G7e、R8g など）
- 新機能や機能強化を含むアップデートで、リージョン拡大も含まれる場合
- AWS Outposts、Local Zones などのインフラ拡大

### AWS Direct Connect
- AWS Direct Connect ロケーションの日本以外への追加
  - 例: 「AWS Direct Connect announces new location in Hanoi, Vietnam」→ 対象外

### その他
- ドキュメント更新のみのアップデート
- 軽微な UI 変更のみのアップデート

## 注意事項

- **RSS フィードは1回だけ取得する。複数回リクエストしない。**
- **Kiro ページも1回だけ取得する。複数回リクエストしない。**
- **RSS/Atom フィードおよび Kiro ページの取得には Bash ツールで curl を使用する（WebFetch ツールは使用しない）**
- 取得できたアイテムで処理を続ける（全アイテムが取得できなくても問題なし）
- 最新情報を優先（pubDate を確認）
- 公式ドキュメントを情報源として明記
- 推測は避け、確認できた情報のみ記載
- 重複レポートは作成しない（ファイル名で判定）
- Kiro アップデートも AWS アップデートと同じ品質・フォーマットでレポートを作成する
