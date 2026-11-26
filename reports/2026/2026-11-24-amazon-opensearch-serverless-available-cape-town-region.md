# Amazon OpenSearch Serverless - アフリカ (ケープタウン) リージョンで利用可能に

**リリース日**: 2026年11月24日
**サービス**: Amazon OpenSearch Serverless
**機能**: アフリカ (ケープタウン) リージョンへの提供拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261124-amazon-opensearch-serverless-available-cape-town-region.html)

## 概要

AWS は、次世代 Amazon OpenSearch Serverless がアフリカ (ケープタウン) リージョン (af-south-1) で利用可能になったことを発表した。OpenSearch Serverless は、数秒でリソースをプロビジョニングできるフルマネージドの検索・ベクトル・分析エンジンであり、需要に合わせて自動的にスケールし、未使用時には Scale-to-zero によってコンピュートコストをゼロまで縮小できる。

今回の提供拡大により、ケープタウンリージョンを利用する顧客は、クラスターのプロビジョニングや管理を行うことなく、エージェント型 AI、検索、オブザーバビリティのワークロードを実行できるようになった。コンピュートとストレージが完全に分離されているため、低トラフィック時にはコンピュートを縮小してコストを削減しつつ、トラフィックスパイクへの即時対応能力を維持できる。Scale-to-zero と使用量ベースの課金により、ピーク負荷に合わせてクラスターをプロビジョニングする場合と比較して最大 60% のコスト削減が可能となる。

**アップデート前の課題**

- アフリカ (ケープタウン) リージョンでは OpenSearch Serverless を利用できず、検索やベクトル検索のワークロードには OpenSearch クラスターのプロビジョニングと管理が必要だった
- データレジデンシー要件によりアフリカ域内でのデータ保管が必要な場合、サーバーレスの検索基盤という選択肢がなかった
- アフリカの顧客が OpenSearch Serverless を利用するには他リージョンへのアクセスが必要で、レイテンシが増大していた

**アップデート後の改善**

- ケープタウンリージョンでクラスター管理不要の検索・ベクトル・分析エンジンを利用できるようになった
- アフリカ域内にデータを保持したまま、エージェント型 AI、検索、オブザーバビリティのワークロードをサーバーレスで実行できるようになった
- アフリカのエンドユーザーに近い場所で処理することで、低レイテンシなアクセスが可能になった
- Scale-to-zero と使用量ベースの課金により、同リージョンでも最大 60% のコスト削減が可能になった

## サービスアップデートの詳細

### 主要機能

1. **次世代 OpenSearch Serverless の提供**
   - 数秒でのリソースプロビジョニングと即時オートスケーリング
   - 未使用時は Scale-to-zero によりコンピュートコストがゼロになる
   - 使用量ベースの課金 (実際に消費したコンピュートのみ支払い)

2. **クラスター管理不要のワークロード実行**
   - エージェント型 AI、検索、オブザーバビリティのワークロードに対応
   - クラスターのプロビジョニング、パッチ適用、キャパシティプランニングが不要

3. **コンピュートとストレージの分離**
   - コンピュートはストレージから独立してスケール
   - 低トラフィック期間のコスト削減とトラフィックスパイクへの即応性を両立
   - ピーク負荷に合わせたクラスタープロビジョニングと比較して最大 60% のコスト削減

## 技術仕様

### リージョン情報

| 項目 | 詳細 |
|------|------|
| リージョン名 | アフリカ (ケープタウン) |
| リージョンコード | af-south-1 |
| 提供サービス | 次世代 Amazon OpenSearch Serverless |
| 主な対象ワークロード | エージェント型 AI、検索、オブザーバビリティ |

### コレクションタイプ

| コレクションタイプ | 用途 |
|------|------|
| SEARCH | 全文検索、ログ分析 |
| VECTORSEARCH | RAG、セマンティック検索、AI エージェント |

## 設定方法

### 前提条件

1. AWS アカウントと適切な IAM 権限 (`aoss:*` 関連ポリシー)
2. 暗号化ポリシーとネットワークポリシーの設定
3. AWS CLI または AWS マネジメントコンソールでケープタウンリージョンを選択可能なこと

### 手順

#### ステップ 1: ケープタウンリージョンでコレクショングループを作成

```bash
aws opensearchserverless create-collection-group \
  --region af-south-1 \
  --name "my-group" \
  --generation "NEXTGEN" \
  --capacity-limits '{
    "maxIndexingCapacityInOCU": 10,
    "maxSearchCapacityInOCU": 10,
    "minIndexingCapacityInOCU": 0,
    "minSearchCapacityInOCU": 0
  }'
```

`--region af-south-1` を指定してケープタウンリージョンにコレクショングループを作成する。最小キャパシティを 0 に設定することで Scale-to-zero が有効になる。

#### ステップ 2: コレクションの作成

```bash
aws opensearchserverless create-collection \
  --region af-south-1 \
  --name "my-collection" \
  --type "VECTORSEARCH" \
  --collection-group-name "my-group"
```

コレクショングループに紐づけてコレクションを作成する。ベクトル検索用途では `VECTORSEARCH`、全文検索用途では `SEARCH` を指定する。

#### ステップ 3: コレクションの状態確認

```bash
aws opensearchserverless batch-get-collection \
  --region af-south-1 \
  --names "my-collection"
```

コレクションのステータスとエンドポイントを確認する。`ACTIVE` になればデータの取り込みと検索が可能になる。

## メリット

### ビジネス面

- **データレジデンシー対応**: アフリカ域内にデータを保持する必要がある規制要件や社内ポリシーに対応できる
- **コスト最適化**: Scale-to-zero と使用量ベース課金により、ピーク負荷プロビジョニング比で最大 60% のコスト削減が可能
- **運用負荷の軽減**: クラスター管理が不要になり、キャパシティプランニングやパッチ適用の工数を削減できる

### 技術面

- **低レイテンシ**: アフリカのエンドユーザーに近いリージョンで検索処理を実行できる
- **即時スケーリング**: 数秒でのプロビジョニングと自動スケーリングにより、予測不可能なワークロードに対応できる
- **コンピュート/ストレージ分離**: それぞれ独立したスケーリングにより最適なリソース配分を実現できる

## デメリット・制約事項

### 制限事項

- 本アップデートはリージョン拡大であり、新機能の追加はない
- 利用可能な機能の詳細 (コレクションタイプなど) はリージョンごとに異なる場合があるため、公式ドキュメントでの確認が必要

### 考慮すべき点

- Scale-to-zero 後の初回リクエストにはコールドスタートによるレイテンシが発生する可能性がある
- 他リージョンで既に稼働中のワークロードを移行する場合は、データ移行とネットワーク構成の計画が必要
- 料金はリージョンによって異なるため、料金ページでケープタウンリージョンの単価を確認すべき

## ユースケース

### ユースケース 1: アフリカ域内向け AI エージェントの RAG バックエンド

**シナリオ**: アフリカの顧客向けに AI エージェントを提供しており、ナレッジベースのデータを域内に保持しつつ、低レイテンシなベクトル検索を実現したい場合。

**実装例**:
```bash
aws opensearchserverless create-collection \
  --region af-south-1 \
  --name "agent-knowledge-base" \
  --type "VECTORSEARCH" \
  --collection-group-name "agent-rag-group"
```

**効果**: データレジデンシー要件を満たしながら、エンドユーザーに近い場所で低レイテンシの RAG を実現できる。トラフィックの少ない時間帯は Scale-to-zero によりコストが発生しない。

### ユースケース 2: ケープタウンリージョンのログ分析・オブザーバビリティ基盤

**シナリオ**: ケープタウンリージョンで稼働するアプリケーションのログを、同一リージョン内で検索・分析したい場合。

**実装例**:
```bash
aws opensearchserverless create-collection \
  --region af-south-1 \
  --name "app-logs" \
  --type "SEARCH" \
  --collection-group-name "log-analytics-group"
```

**効果**: ログデータをリージョン外に転送することなく分析でき、転送コストとレイテンシを削減できる。クラスター管理が不要なため、運用負荷も最小限に抑えられる。

### ユースケース 3: トラフィック変動の大きい検索サービス

**シナリオ**: 日中と夜間でトラフィックが大きく変動する EC サイトの商品検索を、ケープタウンリージョンで運用する場合。

**実装例**:
```bash
aws opensearchserverless create-collection-group \
  --region af-south-1 \
  --name "ecommerce-search-group" \
  --generation "NEXTGEN" \
  --capacity-limits '{
    "maxIndexingCapacityInOCU": 20,
    "maxSearchCapacityInOCU": 20,
    "minIndexingCapacityInOCU": 0,
    "minSearchCapacityInOCU": 0
  }'
```

**効果**: ピーク時には自動スケーリングで即座に対応し、トラフィックの少ない時間帯はコンピュートを縮小してコストを削減できる。ピーク負荷に合わせたプロビジョニングと比較して最大 60% のコスト削減が可能。

## 料金

OpenSearch Serverless は使用量ベースの課金モデルを採用しており、実際に消費したコンピュートに対してのみ課金される。Scale-to-zero により未使用時のコンピュートコストは発生しない。

ケープタウンリージョンの具体的な単価は [Amazon OpenSearch Service 料金ページ](https://aws.amazon.com/opensearch-service/pricing/) を参照。

## 利用可能リージョン

本アップデートにより、アフリカ (ケープタウン) リージョン (af-south-1) で次世代 Amazon OpenSearch Serverless が利用可能になった。利用可能なリージョンの完全なリストは [AWS Regional Services List](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html) を参照。

## 関連サービス・機能

- **Amazon OpenSearch Service**: マネージド型の OpenSearch クラスター。サーバーレスではなくプロビジョニング型の選択肢
- **Amazon Bedrock**: AI エージェント構築プラットフォーム。OpenSearch Serverless をナレッジベースとして統合可能
- **Amazon VPC**: リソースベースエンドポイントにより標準 VPC API で OpenSearch Serverless に接続可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261124-amazon-opensearch-serverless-available-cape-town-region.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-opensearch-serverless-available-cape-town-region/)
- [技術ドキュメント (OpenSearch Serverless デベロッパーガイド)](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)
- [料金ページ](https://aws.amazon.com/opensearch-service/pricing/)
- [AWS Regional Services List](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html)
- [次世代 OpenSearch Serverless GA レポート (2026 年 5 月)](./2026-05-28-amazon-opensearch-serverless-next-generation-generally-available.md)

## まとめ

次世代 Amazon OpenSearch Serverless がアフリカ (ケープタウン) リージョンで利用可能になり、アフリカ域内でのデータレジデンシー要件を満たしながら、クラスター管理不要の検索・ベクトル・分析基盤を構築できるようになった。同リージョンで AI エージェント、検索、オブザーバビリティのワークロードを運用している、または計画している組織は、Scale-to-zero による最大 60% のコスト削減効果を含めて導入を検討することを推奨する。
