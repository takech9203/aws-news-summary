# AWS Glue Schema Registry - 3 つの新リージョンで利用可能に

**リリース日**: 2026年4月3日
**サービス**: AWS Glue
**機能**: AWS Glue Schema Registry のリージョン拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260403-aws-gsr-3-more-regions.html)

## 概要

AWS Glue Schema Registry が、アジアパシフィック (ジャカルタ)、ヨーロッパ (スペイン)、ヨーロッパ (チューリッヒ) の 3 つの新しいリージョンで利用可能になりました。AWS Glue Schema Registry は、AWS Glue のサーバーレスかつ無料の機能であり、Apache Avro、JSON、Protobuf スキーマ形式を使用してストリーミングデータの進化を検証・制御できます。

Schema Registry は、データストリーミングシステムにおけるデカップルされたアプリケーション間のデータフォーマットと構造を管理するための一元化されたリポジトリとして機能します。これにより、データ検証ロジックやチーム間の調整を排除し、ストリーミングデータの品質を向上させ、下流アプリケーションの障害を削減できます。

**アップデート前の課題**

- ジャカルタ、スペイン、チューリッヒリージョンで AWS Glue Schema Registry が利用できなかった
- これらのリージョンのユーザーは、他のリージョンの Schema Registry を使用する必要があり、レイテンシーやデータレジデンシーの面で課題があった
- リージョン間通信によるストリーミングデータ処理のパフォーマンス低下が懸念されていた

**アップデート後の改善**

- 3 つの新リージョンでローカルに Schema Registry を利用可能になった
- ヨーロッパおよび東南アジアのデータレジデンシー要件に対応しやすくなった
- ローカルリージョンでのスキーマ管理により、ストリーミングデータ処理のレイテンシーが改善

## サービスアップデートの詳細

### AWS Glue Schema Registry の主要機能

1. **スキーマの一元管理**
   - Apache Avro、JSON、Protobuf スキーマ形式をサポート
   - デカップルされたプロデューサーとコンシューマー間のデータ互換性を保証
   - スキーマのバージョニングと進化ルールの管理が可能

2. **ストリーミングデータの品質管理**
   - データ検証ロジックをアプリケーションコードから分離
   - スキーマ互換性チェックによるデータ品質の自動検証
   - 下流アプリケーションの障害を未然に防止

3. **幅広いサービス連携**
   - Apache Kafka / Amazon Managed Streaming for Apache Kafka (Amazon MSK)
   - Amazon Kinesis Data Streams
   - Amazon Kinesis Data Analytics for Apache Flink
   - AWS Lambda
   - C# および Java アプリケーションとの統合 (Apache ライセンスのシリアライザー/デシリアライザー経由)

## 技術仕様

### サポートされるスキーマ形式

| スキーマ形式 | 説明 |
|-------------|------|
| Apache Avro | バイナリシリアライゼーション形式。コンパクトで高速なデータ交換に最適 |
| JSON Schema | JSON ドキュメントの構造を定義。REST API やイベント駆動型アーキテクチャで広く使用 |
| Protocol Buffers (Protobuf) | Google 開発のバイナリ形式。高効率なシリアライゼーションと言語間互換性を提供 |

### 新規対応リージョン

| リージョン名 | リージョンコード |
|-------------|----------------|
| アジアパシフィック (ジャカルタ) | ap-southeast-3 |
| ヨーロッパ (スペイン) | eu-south-2 |
| ヨーロッパ (チューリッヒ) | eu-central-2 |

### API 変更履歴

直近 7 日間で AWS Glue に関連する API 変更は検出されませんでした。今回のアップデートはリージョン拡大であり、新しい API の追加や既存 API の変更は含まれていません。

## 設定方法

### 前提条件

1. AWS アカウントが上記の新リージョンで有効化されていること
2. AWS Glue へのアクセス権限を持つ IAM ロールまたはユーザーが設定されていること
3. ストリーミングデータのプロデューサーまたはコンシューマーアプリケーションが存在すること

### 手順

#### ステップ 1: Schema Registry の作成

```bash
aws glue create-registry \
  --registry-name my-schema-registry \
  --region ap-southeast-3
```

ジャカルタリージョンに新しい Schema Registry を作成します。`--region` パラメータで対象リージョンを指定します。

#### ステップ 2: スキーマの登録

```bash
aws glue create-schema \
  --registry-id RegistryName=my-schema-registry \
  --schema-name my-avro-schema \
  --data-format AVRO \
  --compatibility BACKWARD \
  --schema-definition '{"type":"record","name":"User","fields":[{"name":"name","type":"string"},{"name":"age","type":"int"}]}' \
  --region ap-southeast-3
```

Avro 形式のスキーマを登録します。`--compatibility` でスキーマの進化ルール (BACKWARD、FORWARD、FULL など) を指定できます。

#### ステップ 3: アプリケーションからの利用

```java
// Java アプリケーションでの Schema Registry 統合例 (Amazon MSK)
GlueSchemaRegistryKafkaSerializer serializer =
    new GlueSchemaRegistryKafkaSerializer();

Properties props = new Properties();
props.put("region", "ap-southeast-3");
props.put("schemaAutoRegistrationEnabled", "true");
props.put("dataFormat", "AVRO");
```

Java アプリケーションでシリアライザーを設定し、Schema Registry と連携します。リージョンを新規対応リージョンに指定します。

## メリット

### ビジネス面

- **データレジデンシー要件への対応**: EU (スペイン、チューリッヒ) および東南アジア (ジャカルタ) のデータ主権規制に対応可能
- **コスト削減**: リージョン間データ転送が不要になり、ネットワークコストを削減
- **グローバル展開の加速**: これらのリージョンで既に稼働しているストリーミングワークロードに Schema Registry をローカルに追加可能

### 技術面

- **低レイテンシー**: ローカルリージョンでのスキーマ検証により、ストリーミング処理のレイテンシーを削減
- **無料機能**: Schema Registry は AWS Glue の無料機能であり、追加コストなしで利用可能
- **サーバーレス**: インフラストラクチャの管理不要で、スキーマ管理に集中可能

## デメリット・制約事項

### 制限事項

- Schema Registry のスキーマ数やバージョン数にはサービスクォータの上限がある
- C# および Java 以外の言語向けのネイティブシリアライザー/デシリアライザーは提供されていない
- リージョン間でのスキーマの自動レプリケーション機能は提供されていない

### 考慮すべき点

- 既存のリージョンから新リージョンへのスキーマ移行は手動で行う必要がある
- 複数リージョンにまたがるストリーミングアーキテクチャでは、各リージョンの Schema Registry でスキーマの一貫性を維持する運用が必要

## ユースケース

### ユースケース 1: インドネシアのデータストリーミング基盤

**シナリオ**: インドネシア国内で IoT デバイスからのストリーミングデータを Amazon MSK で収集し、データ品質を担保したい

**効果**: ジャカルタリージョンの Schema Registry でスキーマを管理することで、インドネシア国内にデータを保持しながら低レイテンシーでストリーミングデータの品質を保証

### ユースケース 2: EU データ保護規制への対応

**シナリオ**: スペインまたはスイスの顧客データを処理するイベント駆動型アプリケーションで、GDPR やスイスのデータ保護法に準拠する必要がある

**効果**: ヨーロッパリージョンの Schema Registry を使用することで、データを EU 域内に保持しつつスキーマ管理を一元化

### ユースケース 3: マルチリージョンストリーミングアーキテクチャ

**シナリオ**: グローバルに分散した Kafka クラスタで、各リージョンのプロデューサーとコンシューマー間のデータ互換性を確保したい

**効果**: 各リージョンにローカル Schema Registry を配置し、スキーマのバージョニングと互換性チェックをローカルで実行することでレイテンシーを最小化

## 料金

AWS Glue Schema Registry は AWS Glue の無料機能です。Schema Registry 自体の使用に追加料金はかかりません。ただし、関連する AWS サービス (Amazon MSK、Kinesis Data Streams など) の利用料金は別途発生します。

## 利用可能リージョン

今回のアップデートにより、以下の 3 リージョンが新たに追加されました。

- アジアパシフィック (ジャカルタ) - ap-southeast-3
- ヨーロッパ (スペイン) - eu-south-2
- ヨーロッパ (チューリッヒ) - eu-central-2

AWS Glue Schema Registry が利用可能な全リージョンの一覧は [AWS Regional Services List](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) を参照してください。

## 関連サービス・機能

- **Amazon Managed Streaming for Apache Kafka (Amazon MSK)**: Schema Registry と連携してスキーマ管理付きの Kafka ストリーミングを実現
- **Amazon Kinesis Data Streams**: リアルタイムデータストリーミングサービスとして Schema Registry のスキーマ検証と統合
- **AWS Glue Data Catalog**: データレイクのメタデータ管理。Schema Registry と組み合わせてデータガバナンスを強化
- **AWS Lambda**: Schema Registry のスキーマを使用してイベント駆動型処理のデータ検証を実装

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260403-aws-gsr-3-more-regions.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/04/aws-gsr-3-more-regions/)
- [AWS Glue Schema Registry ドキュメント](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)
- [AWS Glue 料金ページ](https://aws.amazon.com/glue/pricing/)
- [AWS Regional Services List](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/)

## まとめ

AWS Glue Schema Registry がジャカルタ、スペイン、チューリッヒの 3 リージョンに拡大されたことで、東南アジアおよびヨーロッパのユーザーがローカルリージョンでストリーミングデータのスキーマ管理を行えるようになりました。Schema Registry は AWS Glue の無料機能であるため、追加コストなしでデータ品質の向上とデータレジデンシー要件への対応が可能です。対象リージョンで Amazon MSK や Kinesis Data Streams を利用している場合は、Schema Registry の活用を検討することを推奨します。
