# Amazon RDS および Aurora - 追加リージョンでの R8g、M8g データベースインスタンス対応

**リリース日**: 2026 年 7 月 15 日
**サービス**: Amazon RDS, Amazon Aurora
**機能**: 追加 AWS リージョンでの R8g および M8g データベースインスタンスのサポート

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260715-amazon-rds-aurora-r8g-m8g-regions.html)
<!-- INFOGRAPHIC_BASE_URL は環境変数から取得 -->

## 概要

AWS Graviton4 ベースの R8g データベースインスタンスが、Amazon Aurora (MySQL および PostgreSQL 互換) および Amazon RDS for PostgreSQL、MySQL、MariaDB において、追加の AWS リージョンで一般提供されました。対象リージョンは、アジアパシフィック (ハイデラバード、メルボルン、マレーシア)、ヨーロッパ (ロンドン、パリ、チューリッヒ)、AWS GovCloud (US-East)、南米 (サンパウロ)、メキシコ (中部) です。

さらに、AWS Graviton4 ベースの M8g データベースインスタンスが、Amazon RDS for PostgreSQL、MySQL、MariaDB において、米国西部 (北カリフォルニア)、アジアパシフィック (ムンバイ、シドニー、香港、ソウル、マレーシア、シンガポール)、カナダ西部 (カルガリー)、ヨーロッパ (チューリッヒ、ミラノ、パリ)、南米 (サンパウロ)、アフリカ (ケープタウン) でサポートされるようになりました。

AWS Graviton4 ベースのインスタンスは、同等サイズの Graviton3 ベースのインスタンスと比較して、データベースエンジン、バージョン、ワークロードに応じて、最大 40% のパフォーマンス向上と最大 29% の価格/パフォーマンス向上を提供します。R8g はメモリ最適化インスタンス、M8g は汎用インスタンスであり、ワークロードの特性に合わせて選択できます。

**アップデート前の課題**

- 上記リージョンでは、最新の Graviton4 ベースの R8g または M8g インスタンスを利用できませんでした
- これらのリージョンでデータベースを運用する組織は、旧世代のインスタンスを選択する必要がありました
- 最新のハードウェアを使用したパフォーマンス向上とコスト効率の改善が地域的に制限されていました

**アップデート後の改善**

- 追加された多数のリージョンで R8g (Aurora および RDS) インスタンスを利用できるようになりました
- 追加された多数のリージョンで M8g (RDS) インスタンスを利用できるようになりました
- 対象リージョンでも最大 40% のパフォーマンス向上と最大 29% の価格/パフォーマンス向上を享受できるようになりました

## サービスアップデートの詳細

### 主要機能

1. **AWS Graviton4 ベースの R8g インスタンス (メモリ最適化)**
   - AWS Nitro System 上に構築
   - 24xlarge および 48xlarge サイズを導入し、最大 192 vCPU に対応
   - 8:1 のメモリ対 vCPU 比率と DDR5 メモリ
   - 最大 50Gbps の強化されたネットワーク帯域幅
   - 最大 40Gbps の Amazon EBS への帯域幅
   - Amazon Aurora (MySQL/PostgreSQL 互換) および Amazon RDS for PostgreSQL、MySQL、MariaDB で利用可能

2. **AWS Graviton4 ベースの M8g インスタンス (汎用)**
   - Amazon RDS for PostgreSQL、MySQL、MariaDB で利用可能
   - 汎用ワークロード向けにバランスの取れたコンピューティングとメモリを提供
   - 今回のアップデートで多数のリージョンに拡大

3. **パフォーマンスとコスト効率の向上**
   - 同等サイズの Graviton3 ベースのインスタンスと比較して、最大 40% のパフォーマンス向上
   - 同等サイズの Graviton3 ベースのインスタンスと比較して、最大 29% の価格/パフォーマンス向上
   - データベースエンジン、バージョン、ワークロードに応じて異なります

## 技術仕様

### R8g インスタンスの新規サポートリージョン

| データベース | 新規サポートリージョン |
|-------------|------------------------|
| Amazon Aurora MySQL 互換 | アジアパシフィック (ハイデラバード、メルボルン、マレーシア)、ヨーロッパ (ロンドン、パリ、チューリッヒ)、AWS GovCloud (US-East)、南米 (サンパウロ)、メキシコ (中部) |
| Amazon Aurora PostgreSQL 互換 | 同上 |
| Amazon RDS for PostgreSQL | 同上 |
| Amazon RDS for MySQL | 同上 |
| Amazon RDS for MariaDB | 同上 |

### M8g インスタンスの新規サポートリージョン

| データベース | 新規サポートリージョン |
|-------------|------------------------|
| Amazon RDS for PostgreSQL | 米国西部 (北カリフォルニア)、アジアパシフィック (ムンバイ、シドニー、香港、ソウル、マレーシア、シンガポール)、カナダ西部 (カルガリー)、ヨーロッパ (チューリッヒ、ミラノ、パリ)、南米 (サンパウロ)、アフリカ (ケープタウン) |
| Amazon RDS for MySQL | 同上 |
| Amazon RDS for MariaDB | 同上 |

### R8g インスタンスの仕様

| インスタンスサイズ | vCPU | メモリ (GiB) | ネットワーク帯域幅 (Gbps) | EBS 帯域幅 (Gbps) |
|-------------------|------|-------------|--------------------------|---------------------|
| r8g.large | 2 | 16 | 最大 12.5 | 最大 10 |
| r8g.xlarge | 4 | 32 | 最大 12.5 | 最大 10 |
| r8g.2xlarge | 8 | 64 | 最大 15 | 最大 10 |
| r8g.4xlarge | 16 | 128 | 最大 15 | 最大 10 |
| r8g.8xlarge | 32 | 256 | 12.5 | 10 |
| r8g.12xlarge | 48 | 384 | 20 | 15 |
| r8g.16xlarge | 64 | 512 | 25 | 20 |
| r8g.24xlarge | 96 | 768 | 37.5 | 30 |
| r8g.48xlarge | 192 | 1536 | 50 | 40 |

### インスタンスファミリーの比較

| 項目 | R8g (メモリ最適化) | M8g (汎用) |
|------|--------------------|------------|
| メモリ対 vCPU 比率 | 8:1 | 4:1 |
| 対象サービス | Aurora, RDS | RDS |
| 適したワークロード | メモリ集約型 (インメモリキャッシュ、大規模データセット) | バランス型 (Web アプリケーション、中規模データベース) |
| プロセッサ | AWS Graviton4 | AWS Graviton4 |

## 設定方法

### 前提条件

1. Amazon Aurora または RDS インスタンスが作成されているか、新規作成を予定していること
2. 適切な IAM 権限があること
3. サポートされるデータベースエンジンバージョンを使用していること

### 手順

#### ステップ 1: 新しいインスタンスの起動 (コンソールを使用)

1. Amazon RDS Management Console にアクセス
2. [データベースの作成] をクリック
3. データベースエンジン (Aurora MySQL、Aurora PostgreSQL、RDS MySQL、RDS PostgreSQL、RDS MariaDB) を選択
4. インスタンスクラスで、R8g の場合は [メモリ最適化クラス]、M8g の場合は [汎用クラス] を選択
5. R8g または M8g インスタンスを選択
6. その他の設定を行い、[データベースの作成] をクリック

#### ステップ 2: 新しいインスタンスの起動 (AWS CLI を使用)

```bash
# RDS for PostgreSQL で M8g インスタンスを起動 (ロンドンリージョン)
aws rds create-db-instance \
  --db-instance-identifier my-postgres-instance \
  --engine postgres \
  --db-instance-class db.m8g.2xlarge \
  --master-username admin \
  --master-user-password MyPassword123 \
  --allocated-storage 100 \
  --region eu-west-2
```

このコマンドは、ロンドンリージョンで M8g.2xlarge インスタンスを使用する RDS for PostgreSQL インスタンスを作成します。

#### ステップ 3: 既存のインスタンスのアップグレード

```bash
# 既存の RDS インスタンスを R8g にアップグレード
aws rds modify-db-instance \
  --db-instance-identifier my-existing-instance \
  --db-instance-class db.r8g.4xlarge \
  --apply-immediately
```

このコマンドは、既存のインスタンスを R8g.4xlarge にアップグレードします。`--apply-immediately` フラグを使用すると、変更が即座に適用されます。

#### ステップ 4: パフォーマンスの確認

```bash
# CloudWatch メトリクスを使用してパフォーマンスを確認
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=my-postgres-instance \
  --start-time 2026-07-15T00:00:00Z \
  --end-time 2026-07-16T00:00:00Z \
  --period 3600 \
  --statistics Average
```

このコマンドは、過去 24 時間の CPU 使用率の平均を取得します。

## メリット

### ビジネス面

- **コスト効率の向上**: 最大 29% の価格/パフォーマンス向上により、対象リージョンでコストを削減できます
- **地理的な選択肢の拡大**: データレジデンシー要件やレイテンシ要件に応じて、より多くのリージョンで最新インスタンスを選択できます
- **ワークロード最適化**: R8g (メモリ最適化) と M8g (汎用) を使い分けることで、ワークロードに最適なコスト構成を選べます

### 技術面

- **最新ハードウェア**: AWS Graviton4 プロセッサと DDR5 メモリを使用
- **高帯域幅**: R8g では最大 50Gbps のネットワーク帯域幅と最大 40Gbps の EBS 帯域幅
- **大規模スケール**: R8g は 48xlarge (192 vCPU、1536 GiB メモリ) までスケールアップ可能
- **互換性**: 既存の Aurora および RDS ワークロードと完全に互換性があります

## デメリット・制約事項

### 制限事項

- すべてのデータベースエンジンバージョンで R8g および M8g インスタンスがサポートされているわけではありません
- M8g は Amazon RDS でのみ利用可能で、Amazon Aurora では対象外です
- 一部のリージョンでは、特定のインスタンスサイズが利用できない場合があります
- Graviton ベースのインスタンスは、ARM64 アーキテクチャを使用します

### 考慮すべき点

- データベースエンジンバージョンが R8g または M8g インスタンスをサポートしているか確認してください
- アプリケーションが ARM64 アーキテクチャと互換性があることを確認してください
- パフォーマンステストを実施して、ワークロードに適したインスタンスファミリーとサイズを選択してください

## ユースケース

### ユースケース 1: メモリ集約型ワークロードの高性能化

**シナリオ**: ヨーロッパ (ロンドン) リージョンで、大規模データセットを扱うメモリ集約型の Aurora PostgreSQL ワークロードを R8g インスタンスに移行する。

**実装例**:
1. 現在のインスタンスのパフォーマンスとメモリ使用状況を測定
2. R8g インスタンス (8:1 のメモリ比率) にアップグレード
3. パフォーマンスとコストを再評価

**効果**: メモリ集約型ワークロードで最大 40% のパフォーマンス向上と最大 29% の価格/パフォーマンス向上を実現できます。

### ユースケース 2: 汎用ワークロードのコスト最適化

**シナリオ**: アジアパシフィック (シドニー) リージョンで運用する RDS for MySQL の Web アプリケーションバックエンドを、汎用の M8g インスタンスに移行する。

**実装例**:
1. 現行の汎用インスタンスから M8g インスタンスへ変更
2. CloudWatch でパフォーマンスとコストを比較
3. 適切なインスタンスサイズを選定

**効果**: バランス型のワークロードで最新の Graviton4 による価格/パフォーマンス改善を得られます。

### ユースケース 3: リージョン展開に伴うデータベース基盤の刷新

**シナリオ**: メキシコ (中部) や南米 (サンパウロ) での事業拡大に伴い、新規に構築するデータベースで最新の R8g インスタンスを採用する。

**実装例**:
1. 対象リージョンで Aurora または RDS を新規構築
2. R8g インスタンスを選択して高性能なデータベース基盤を整備
3. 必要に応じてリードレプリカやマルチ AZ 構成を追加

**効果**: 地域の顧客に対して、低レイテンシで高性能かつコスト効率の高いデータベースサービスを提供できます。

## 料金

R8g および M8g インスタンスの料金は、インスタンスサイズ、データベースエンジン、リージョンによって異なります。AWS Graviton4 ベースのインスタンスは、同等サイズの Graviton3 ベースのインスタンスと比較して、最大 29% の価格/パフォーマンス向上を提供します。

詳細については、[Amazon RDS Pricing](https://aws.amazon.com/rds/pricing/) および [Amazon Aurora Pricing](https://aws.amazon.com/rds/aurora/pricing/) を参照してください。

## 利用可能リージョン

今回のアップデートで追加された新規サポートリージョンは以下のとおりです。

**R8g (Aurora および RDS)**

- アジアパシフィック (ハイデラバード、メルボルン、マレーシア)
- ヨーロッパ (ロンドン、パリ、チューリッヒ)
- AWS GovCloud (US-East)
- 南米 (サンパウロ)
- メキシコ (中部)

**M8g (RDS)**

- 米国西部 (北カリフォルニア)
- アジアパシフィック (ムンバイ、シドニー、香港、ソウル、マレーシア、シンガポール)
- カナダ西部 (カルガリー)
- ヨーロッパ (チューリッヒ、ミラノ、パリ)
- 南米 (サンパウロ)
- アフリカ (ケープタウン)

これらのリージョンに加えて、R8g および M8g は既存の対応リージョンでも引き続き利用可能です。最新の対応状況については公式ドキュメントを参照してください。

## 関連サービス・機能

- **Amazon Aurora**: 高性能でスケーラブルなクラウドネイティブデータベース
- **Amazon RDS**: マネージドリレーショナルデータベースサービス
- **AWS Graviton4**: AWS が設計した最新世代の ARM ベースプロセッサ
- **AWS Nitro System**: R8g インスタンスの基盤となる次世代仮想化基盤
- **Amazon CloudWatch**: データベースパフォーマンスを監視するサービス

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260715-amazon-rds-aurora-r8g-m8g-regions.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/7/amazon-rds-aurora-r8g-m8g-regions/)
- [Amazon Aurora Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.DBInstanceClass.SupportAurora.html)
- [Amazon RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.Support.html)
- [Amazon RDS Pricing](https://aws.amazon.com/rds/pricing/)

## まとめ

Amazon RDS および Aurora が追加リージョンで R8g および M8g データベースインスタンスをサポートしたことで、より多くの地域で最新の AWS Graviton4 ベースのインスタンスを活用できるようになりました。R8g はメモリ集約型、M8g は汎用ワークロードに適しており、最大 40% のパフォーマンス向上と最大 29% の価格/パフォーマンス向上を提供します。対象リージョンでデータベースを運用する組織は、ワークロードの特性に応じてこれらのインスタンスへの移行を検討することをお勧めします。
