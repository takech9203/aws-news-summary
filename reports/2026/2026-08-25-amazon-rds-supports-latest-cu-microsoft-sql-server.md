# Amazon RDS for SQL Server - 最新累積更新プログラム CU のサポート (SQL Server 2025 CU6)

**リリース日**: 2026 年 8 月 25 日
**サービス**: Amazon RDS for SQL Server
**機能**: SQL Server 2025 CU6 (KB5093421) のサポート

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260825-amazon-rds-supports-latest-cu-microsoft-sql-server.html)

## 概要

Amazon RDS for SQL Server が、Microsoft SQL Server 2025 の最新累積更新プログラム CU6 (KB5093421) のサポートを開始しました。この累積更新プログラムには、Microsoft が提供するセキュリティ修正、パフォーマンス改善、バグ修正が含まれています。RDS のマイナーバージョンとしては 17.00.4055.5.v1 が提供されます。

AWS は、Amazon RDS Management Console、AWS SDK、または AWS CLI を使用してデータベースインスタンスをアップグレードし、この更新プログラムを適用することを推奨しています。CU6 に含まれる修正と改善の詳細は、Microsoft の KB5093421 のドキュメントで確認できます。

**アップデート前の課題**

- SQL Server 2025 の最新のセキュリティ修正とバグ修正が RDS で適用できなかった
- CU5 以前のバージョンに含まれる既知の問題が残存していた
- Microsoft が推奨する最新ビルドと RDS で利用可能なビルドに差分があった

**アップデート後の改善**

- CU6 (KB5093421) のセキュリティ修正とバグ修正が RDS 上で適用可能になった
- マイナーバージョン 17.00.4055.5.v1 へのアップグレードにより、Microsoft が推奨する最新の安定バージョンを利用できるようになった
- AWS Management Console、SDK、CLI から簡単にアップグレードできる

## サービスアップデートの詳細

### 主要機能

1. **SQL Server 2025 CU6 のサポート**
   - 累積更新プログラム CU6 (KB5093421) を RDS for SQL Server で利用可能
   - RDS マイナーバージョン 17.00.4055.5.v1 として提供
   - Microsoft が提供するセキュリティ修正、パフォーマンス改善、バグ修正を含む

2. **簡単なアップグレードプロセス**
   - AWS Management Console から数クリックでアップグレード可能
   - AWS CLI/SDK を使用した自動化されたアップグレードをサポート
   - メンテナンスウィンドウ中の自動適用にも対応

## 技術仕様

### サポートされるバージョン

| SQL Server バージョン | CU | RDS マイナーバージョン | KB 番号 |
|----------------------|-----|----------------------|---------|
| SQL Server 2025 | CU6 | 17.00.4055.5.v1 | KB5093421 |

### アップグレード方法

```bash
# AWS CLI を使用した RDS インスタンスのアップグレード
aws rds modify-db-instance \
  --db-instance-identifier mydbinstance \
  --engine-version 17.00.4055.5.v1 \
  --apply-immediately
```

## 設定方法

### 前提条件

1. Amazon RDS for SQL Server 2025 のインスタンスが稼働している
2. AWS Management Console へのアクセス権限、または AWS CLI/SDK の設定
3. アップグレード前のバックアップ (推奨)

### 手順

#### ステップ 1: バックアップの作成

```bash
# 手動スナップショットを作成
aws rds create-db-snapshot \
  --db-instance-identifier mydbinstance \
  --db-snapshot-identifier mydbinstance-pre-cu6-snapshot
```

アップグレード前に、データベースの手動スナップショットを作成します。万が一の場合に備えたロールバック手段を確保します。

#### ステップ 2: 利用可能なエンジンバージョンの確認

```bash
# アップグレード可能なバージョンを確認
aws rds describe-db-engine-versions \
  --engine sqlserver-se \
  --engine-version 17.00 \
  --query 'DBEngineVersions[].EngineVersion'
```

現在のエディション (例: Standard Edition の場合は sqlserver-se) で利用可能な SQL Server 2025 のエンジンバージョンを確認します。

#### ステップ 3: AWS Management Console からアップグレード

1. AWS Management Console を開き、Amazon RDS サービスに移動
2. ナビゲーションペインで「データベース」を選択
3. アップグレードするデータベースインスタンスを選択
4. 「変更」ボタンをクリック
5. 「DB エンジンのバージョン」セクションで 17.00.4055.5.v1 を選択
6. 「すぐに適用」または「次のメンテナンスウィンドウ中に適用」を選択
7. 「データベースの変更」をクリック

AWS Management Console を使用して、数クリックでアップグレードを実行します。

#### ステップ 4: アップグレードの確認

```bash
# アップグレードの進行状況を確認
aws rds describe-db-instances \
  --db-instance-identifier mydbinstance \
  --query 'DBInstances[0].[EngineVersion,DBInstanceStatus]'
```

アップグレードが完了したら、データベースに接続してバージョンを確認し、アプリケーションが正常に動作することをテストします。

## メリット

### ビジネス面

- **セキュリティリスクの軽減**: 最新のセキュリティ修正を適用し、潜在的な脆弱性を修正
- **コンプライアンスの維持**: 最新パッチの適用により、業界標準とコンプライアンス要件を満たす
- **システムの安定性向上**: バグ修正により、予期しない障害のリスクを低減

### 技術面

- **パフォーマンス改善**: CU6 に含まれるパフォーマンス最適化を利用可能
- **バグ修正**: 既知のバグが修正され、SQL Server 2025 の安定性が向上
- **簡単なアップグレード**: AWS Management Console または CLI から数ステップでアップグレード可能

## デメリット・制約事項

### 制限事項

- アップグレード中は、データベースインスタンスが一時的に利用不可になる (Multi-AZ 構成では影響を軽減可能)
- ダウングレードは直接サポートされていない (スナップショットからの復元が必要)
- 今回のアップデートの対象は SQL Server 2025 のみ

### 考慮すべき点

- アップグレード前に、テスト環境で互換性を確認することを推奨
- ビジネスに影響の少ない時間帯にアップグレードを計画
- アップグレード後にクエリプランが変更される可能性があるため、パフォーマンスの監視を推奨

## ユースケース

### ユースケース 1: 本番環境のセキュリティ強化

**シナリオ**: 本番環境の Amazon RDS for SQL Server 2025 インスタンスに最新のセキュリティ修正を適用したい。

**実装例**:
```bash
# メンテナンスウィンドウ中にアップグレードを予約
aws rds modify-db-instance \
  --db-instance-identifier prod-sqlserver \
  --engine-version 17.00.4055.5.v1 \
  --no-apply-immediately
```

**効果**: メンテナンスウィンドウ中にセキュリティ修正が適用され、ビジネスへの影響を最小限に抑えながらセキュリティを向上させます。

### ユースケース 2: 開発環境での事前検証

**シナリオ**: CU6 のアップグレードを本番環境に適用する前に、開発環境で互換性を検証したい。

**実装例**:
```bash
# 開発環境を即座にアップグレード
aws rds modify-db-instance \
  --db-instance-identifier dev-sqlserver \
  --engine-version 17.00.4055.5.v1 \
  --apply-immediately
```

**効果**: 開発環境で事前にアップグレードを検証し、アプリケーションの互換性やパフォーマンスへの影響を本番適用前に確認できます。

## 料金

SQL Server のバージョンアップグレード自体に追加料金はかかりません。Amazon RDS for SQL Server の標準的な料金体系が適用されます。

| 項目 | 説明 |
|------|------|
| インスタンス時間 | DB インスタンスの稼働時間に基づいて課金 |
| ストレージ | プロビジョニングされたストレージ容量に基づいて課金 |
| バックアップ | 自動バックアップと手動スナップショットのストレージに対して課金 |

## 利用可能リージョン

Amazon RDS for SQL Server が利用可能なすべての AWS リージョンで提供されています。

## 関連サービス・機能

- **Amazon RDS Automated Backups**: アップグレード前のバックアップを自動作成
- **Amazon RDS Blue/Green Deployments**: 本番環境への影響を抑えたアップグレード検証に活用可能
- **Amazon RDS Performance Insights**: アップグレード後のパフォーマンスを監視
- **Amazon CloudWatch**: RDS インスタンスのメトリクスを監視し、アップグレード後の動作を確認

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260825-amazon-rds-supports-latest-cu-microsoft-sql-server.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/08/amazon-rds-supports-latest-cu-microsoft-sql-server/)
- [ドキュメント: Upgrades of the Microsoft SQL Server DB engine](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.SQLServer.html)
- [ドキュメント: Microsoft SQL Server versions on Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/SQLServer.Concepts.General.VersionSupport.html)
- [Microsoft KB5093421 - SQL Server 2025 CU6](https://learn.microsoft.com/en-us/troubleshoot/sql/releases/sqlserver-2025/cumulativeupdate6)
- [料金ページ](https://aws.amazon.com/rds/sqlserver/pricing/)

## まとめ

Amazon RDS for SQL Server が SQL Server 2025 の最新累積更新プログラム CU6 (KB5093421) のサポートを開始し、マイナーバージョン 17.00.4055.5.v1 として利用可能になりました。このアップデートには Microsoft が提供するセキュリティ修正とバグ修正が含まれており、SQL Server 2025 を利用するすべての RDS ユーザーにアップグレードが推奨されます。テスト環境での事前検証を行った上で、メンテナンスウィンドウを活用した計画的な適用を推奨します。
