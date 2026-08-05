# Amazon Keyspaces - カナダ西部 (カルガリー) リージョン拡大

**リリース日**: 2026 年 8 月 5 日
**サービス**: Amazon Keyspaces (for Apache Cassandra)
**機能**: カナダ西部 (カルガリー) リージョン (ca-west-1) での利用開始

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260805-amazon-keyspaces-apache-cassandra-canada-west.html)

## 概要

Amazon Keyspaces (for Apache Cassandra) が、カナダ西部 (カルガリー) リージョン (ca-west-1) で利用可能になった。これにより、カナダのユーザーは Apache Cassandra 互換のアプリケーションをより低いレイテンシーで実行しながら、データをカナダ国内のリージョンに保持できるようになった。

Amazon Keyspaces は、スケーラブルで高可用性を備えたフルマネージドの Apache Cassandra 互換データベースサービスである。サーバーレスモデルを採用しており、サーバーのプロビジョニング、パッチ適用、管理は不要で、使用したリソースに対してのみ課金される。開発者は使い慣れた Cassandra Query Language (CQL) を使用して、自前の Cassandra クラスターを運用することなく、毎秒数千リクエストを処理するアプリケーションを構築できる。

**アップデート前の課題**

- カナダのユーザーは、カナダ (中部) リージョン (ca-central-1) のみが国内の選択肢であり、カナダ西部のユーザーにはレイテンシーが発生していた
- カナダ国内でのマルチリージョン構成 (レプリケーションや DR) を Amazon Keyspaces で組むことができなかった
- カナダ西部で稼働する他の AWS ワークロードと同一リージョンで Cassandra 互換データベースを利用できなかった

**アップデート後の改善**

- カナダ西部のユーザーが地理的に近いカルガリーリージョンで Amazon Keyspaces を利用でき、レイテンシーが低減された
- データレジデンシー要件を満たしながら、カナダ国内 2 リージョンでの構成が可能になった
- カナダ国内でのディザスタリカバリや高可用性アーキテクチャの選択肢が広がった

## サービスアップデートの詳細

### 主要機能

1. **フルマネージド Cassandra 互換データベース**
   - サーバーレスアーキテクチャにより、インフラストラクチャの管理が不要
   - Cassandra Query Language (CQL) を使用したアクセス
   - 既存の Cassandra アプリケーションコードおよびドライバーとの互換性

2. **サーバーレスによる自動スケーリング**
   - アプリケーションのトラフィックに応じてテーブルが自動的にスケールアップ・ダウン
   - 事実上無制限のスループットとストレージ
   - 使用したリソースに対してのみ課金

3. **カナダ国内でのデータレジデンシー**
   - データをカナダ西部 (カルガリー) リージョン内に保持可能
   - カナダの規制要件やデータ主権要件への対応が容易に

## 技術仕様

### エンドポイント情報

| 項目 | 詳細 |
|------|------|
| リージョン名 | カナダ西部 (カルガリー) |
| リージョンコード | ca-west-1 |
| エンドポイント | cassandra.ca-west-1.amazonaws.com |

### 接続プロトコル

| アクセス方法 | ポート | プロトコル |
|------|------|------|
| cqlsh / Cassandra ドライバー | 9142 | TLS |
| AWS CLI | 443 | HTTPS |
| AWS SDK | 443 | HTTPS |

## 設定方法

### 前提条件

1. AWS アカウントでカナダ西部 (カルガリー) リージョンが有効化されていること
2. IAM ユーザーまたはロールに Amazon Keyspaces へのアクセス権限が設定されていること
3. TLS 接続用の Amazon Trust Services ルート CA 証明書が準備されていること

### 手順

#### ステップ 1: キースペースの作成

```bash
aws keyspaces create-keyspace \
    --keyspace-name my_keyspace \
    --region ca-west-1
```

カナダ西部 (カルガリー) リージョンに新しいキースペースを作成する。

#### ステップ 2: テーブルの作成

```bash
aws keyspaces create-table \
    --keyspace-name my_keyspace \
    --table-name my_table \
    --schema-definition '{
        "allColumns": [
            {"name": "id", "type": "uuid"},
            {"name": "name", "type": "text"},
            {"name": "created_at", "type": "timestamp"}
        ],
        "partitionKeys": [{"name": "id"}]
    }' \
    --region ca-west-1
```

作成したキースペース内にテーブルを定義する。スキーマは CQL のデータ型に対応している。

#### ステップ 3: cqlsh での接続

```bash
cqlsh cassandra.ca-west-1.amazonaws.com 9142 \
    --ssl \
    --auth-provider "PlainTextAuthProvider" \
    -u "ServiceUserName" \
    -p "ServicePassword"
```

TLS を使用してカルガリーリージョンの Amazon Keyspaces エンドポイントに接続する。サービス固有の認証情報は IAM コンソールから生成できる。

## メリット

### ビジネス面

- **データレジデンシーコンプライアンス**: データをカナダ国内に保持でき、規制産業や公共部門での採用障壁が解消される
- **低レイテンシーアクセス**: カナダ西部のユーザーに地理的に近いリージョンからのアクセスにより、エンドユーザー体験が向上する
- **事業継続性の強化**: カナダ国内 2 リージョン (ca-central-1 と ca-west-1) での構成が可能になり、DR 対策の選択肢が広がる

### 技術面

- **サーバーレスの運用負荷軽減**: 新リージョンでもインフラストラクチャ管理不要のサーバーレスモデルが適用される
- **既存アプリケーションの互換性**: CQL および既存の Cassandra ドライバーをそのまま利用でき、移行コストが低い
- **カナダ国内での高可用性構成**: ca-central-1 との組み合わせにより、国内完結型の冗長構成を検討できる

## デメリット・制約事項

### 制限事項

- 新リージョンの初期段階では、他のリージョンと比較して一部の AWS サービスとの連携や機能が制限される可能性がある
- カルガリーリージョンの料金は他のリージョンと異なる場合がある (リージョン別料金を確認すること)

### 考慮すべき点

- マルチリージョンレプリケーションなど、特定機能のカルガリーリージョンでの対応状況は公式ドキュメントで事前に確認すること
- 既存の ca-central-1 ワークロードとの併用時は、リージョン間のデータ転送料金を考慮すること

## ユースケース

### ユースケース 1: カナダ西部の企業によるデータレジデンシー対応

**シナリオ**: カナダ西部に拠点を持つ金融・公共系の組織が、データをカナダ国内に保持しながら低レイテンシーで Cassandra 互換データベースを利用したい。

**実装例**:
```sql
CREATE KEYSPACE regulated_data
    WITH REPLICATION = {'class': 'SingleRegionStrategy'}
    AND TAGS = {'environment': 'production', 'residency': 'canada'};
```

**効果**: データレジデンシー要件を満たしつつ、カナダ西部のユーザーへ低レイテンシーでサービスを提供できる。

### ユースケース 2: 既存 Cassandra クラスターのマネージドサービスへの移行

**シナリオ**: カナダ西部で自己管理の Cassandra クラスターを運用している企業が、運用負荷を削減するためにマネージドサービスへ移行したい。

**実装例**:
```bash
# 既存の CQL アプリケーションの接続先を変更するのみ
cqlsh cassandra.ca-west-1.amazonaws.com 9142 --ssl
```

**効果**: 既存の CQL コードとドライバーを流用しながら、クラスター運用 (プロビジョニング、パッチ適用、スケーリング) から解放される。

### ユースケース 3: カナダ国内 2 リージョンでの DR 構成

**シナリオ**: ca-central-1 で稼働中のワークロードについて、カナダ国内で完結するディザスタリカバリ構成を検討している。

**実装例**:
```bash
# カルガリーリージョンに DR 用のキースペース・テーブルを構築し、
# アプリケーションレイヤーまたはレプリケーション機能でデータを同期する
aws keyspaces create-keyspace \
    --keyspace-name dr_keyspace \
    --region ca-west-1
```

**効果**: データをカナダ国外に出すことなく、リージョン障害に備えた冗長構成を実現できる。

## 料金

Amazon Keyspaces はサーバーレスモデルを採用しており、使用したリソースに対してのみ課金される。

### 料金体系

| 項目 | 説明 |
|------|------|
| オンデマンド読み取り | Read Request Units (RRU): 4 KB あたり 1 RRU |
| オンデマンド書き込み | Write Request Units (WRU): 1 KB あたり 1 WRU |
| プロビジョンド読み取り | Read Capacity Units (RCU): 4 KB/秒あたり 1 RCU |
| プロビジョンド書き込み | Write Capacity Units (WCU): 1 KB/秒あたり 1 WCU |
| ストレージ | 使用量に応じた GB 単位の課金 |

カルガリーリージョンの具体的な単価は [料金ページ](https://aws.amazon.com/keyspaces/pricing/) を参照。

## 利用可能リージョン

今回の拡大により、カナダ西部 (カルガリー) リージョン (ca-west-1) で Amazon Keyspaces が利用可能になった。

**カナダ国内の利用可能リージョン:**
- カナダ (中部) - ca-central-1
- カナダ西部 (カルガリー) - ca-west-1 **[NEW]**

利用可能なリージョンの全リストは [サービスエンドポイント一覧](https://docs.aws.amazon.com/keyspaces/latest/devguide/programmatic.endpoints.html) を参照。

## 関連サービス・機能

- **Amazon DynamoDB**: 同じくフルマネージドの NoSQL データベースだが、Cassandra 互換性が不要な場合の選択肢
- **AWS Database Migration Service (DMS)**: 既存の Cassandra クラスターから Amazon Keyspaces への移行をサポート
- **AWS PrivateLink**: VPC 内からのプライベート接続によるセキュアなアクセス

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260805-amazon-keyspaces-apache-cassandra-canada-west.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-keyspaces-apache-cassandra-canada-west/)
- [Amazon Keyspaces ドキュメント](https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html)
- [サービスエンドポイント一覧](https://docs.aws.amazon.com/keyspaces/latest/devguide/programmatic.endpoints.html)
- [料金ページ](https://aws.amazon.com/keyspaces/pricing/)

## まとめ

Amazon Keyspaces のカナダ西部 (カルガリー) リージョンへの拡大は、カナダ国内でのデータレジデンシー要件を持つ企業や、カナダ西部での低レイテンシーアクセスを必要とするワークロードに価値をもたらす。カナダ国内 2 リージョン構成による DR や高可用性アーキテクチャの検討も可能になったため、ca-central-1 で稼働中の Cassandra 互換ワークロードを持つユーザーは、カルガリーリージョンの活用を検討することを推奨する。
