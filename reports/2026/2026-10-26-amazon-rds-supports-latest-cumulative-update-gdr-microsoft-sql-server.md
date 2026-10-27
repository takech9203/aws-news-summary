# Amazon RDS for SQL Server - 最新 CU と GDR アップデートのサポート

**リリース日**: 2026年10月26日
**サービス**: Amazon RDS for SQL Server
**機能**: Microsoft SQL Server の累積更新プログラム (CU) と一般配布リリース (GDR) のサポート

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261026-amazon-rds-supports-latest-cumulative-update-gdr-microsoft-sql-server.html)

## 概要

Amazon RDS for SQL Server が、Microsoft SQL Server の最新の累積更新プログラム (CU) と一般配布リリース (GDR) アップデートのサポートを開始しました。今回のリリースでは、SQL Server 2017 から SQL Server 2025 までの 4 つのメジャーバージョンに対して、Microsoft が提供する最新のセキュリティ修正とバグ修正を適用した新しい RDS エンジンバージョンが利用可能になります。

**サポート対象のアップデート:**

- SQL Server 2017 CU31+GDR KB5122774 (RDS バージョン 14.00.3550.4.v1)
- SQL Server 2019 CU32+GDR KB5122772 (RDS バージョン 15.00.4490.9.v1)
- SQL Server 2022 CU27 KB5104824 (RDS バージョン 16.00.4295.3.v1)
- SQL Server 2025 CU9 KB5122048 (RDS バージョン 17.00.5005.3.v1)

AWS は、Amazon RDS マネジメントコンソール、AWS SDK、または CLI を使用してデータベースインスタンスをアップグレードし、これらのアップデートを適用することを推奨しています。各アップデートに含まれる修正と改善の詳細は、Microsoft の各 KB 記事を参照してください。

**アップデート前の課題**

- 最新の CU/GDR に含まれるセキュリティ修正が RDS 上の SQL Server に未適用で、脆弱性リスクが残っていた
- CU に含まれるバグ修正やパフォーマンス改善を RDS 環境で利用できなかった
- オンプレミスの SQL Server と RDS 上の SQL Server でパッチレベルに差分が生じ、互換性検証やコンプライアンス対応が難しかった

**アップデート後の改善**

- 最新の GDR アップデートにより、Microsoft が公開したセキュリティ修正を RDS 上でも適用可能になった
- SQL Server 2017/2019/2022/2025 の各バージョンで最新 CU のバグ修正と改善を利用できるようになった
- RDS マネジメントコンソール、AWS SDK、CLI から簡単にエンジンバージョンをアップグレードできる

## サービスアップデートの詳細

### 主要機能

1. **最新 GDR セキュリティアップデートのサポート**
   - SQL Server 2017 (CU31+GDR) と SQL Server 2019 (CU32+GDR) に GDR アップデートを提供
   - Microsoft のセキュリティリリースに追随したパッチ適用が可能
   - 修正内容の詳細は各 KB 記事 (KB5122774、KB5122772) を参照

2. **最新 CU のサポート**
   - SQL Server 2022 CU27 (KB5104824) と SQL Server 2025 CU9 (KB5122048) をサポート
   - 累積更新プログラムに含まれるバグ修正、パフォーマンス改善を利用可能
   - SQL Server 2025 についても継続的に最新 CU へ追随

3. **簡単なアップグレードプロセス**
   - Amazon RDS マネジメントコンソールから数クリックでアップグレード
   - AWS CLI/SDK を使用した自動化されたアップグレードにも対応
   - メンテナンスウィンドウ中の適用を選択して、業務影響を最小化可能

## 技術仕様

### サポートされる SQL Server バージョン

| SQL Server バージョン | CU/GDR | KB 番号 | RDS バージョン |
|----------------------|--------|---------|---------------|
| SQL Server 2017 | CU31+GDR | KB5122774 | 14.00.3550.4.v1 |
| SQL Server 2019 | CU32+GDR | KB5122772 | 15.00.4490.9.v1 |
| SQL Server 2022 | CU27 | KB5104824 | 16.00.4295.3.v1 |
| SQL Server 2025 | CU9 | KB5122048 | 17.00.5005.3.v1 |

### アップグレード方法

```bash
# AWS CLI を使用した RDS インスタンスのアップグレード (SQL Server 2022 の例)
aws rds modify-db-instance \
  --db-instance-identifier mydbinstance \
  --engine-version 16.00.4295.3.v1 \
  --apply-immediately
```

`modify-db-instance` コマンドで `--engine-version` に新しい RDS バージョンを指定することで、DB エンジンのマイナーバージョンアップグレードを実行します。`--apply-immediately` を指定すると即時適用され、指定しない場合は次のメンテナンスウィンドウで適用されます。

## 設定方法

### 前提条件

1. Amazon RDS for SQL Server のインスタンスが稼働している
2. AWS マネジメントコンソールへのアクセス権限、または AWS CLI/SDK の設定
3. アップグレード前のバックアップ (推奨)

### 手順

#### ステップ1: バックアップの作成

```bash
# 手動スナップショットを作成
aws rds create-db-snapshot \
  --db-instance-identifier mydbinstance \
  --db-snapshot-identifier mydbinstance-pre-upgrade-snapshot
```

アップグレード前に手動スナップショットを作成し、万が一問題が発生した場合に復元できるようにします。

#### ステップ2: エンジンバージョンのアップグレード

```bash
# メンテナンスウィンドウ中に適用する場合
aws rds modify-db-instance \
  --db-instance-identifier mydbinstance \
  --engine-version 16.00.4295.3.v1 \
  --no-apply-immediately
```

対象バージョンに応じた RDS バージョン (14.00.3550.4.v1 / 15.00.4490.9.v1 / 16.00.4295.3.v1 / 17.00.5005.3.v1) を指定してアップグレードを実行します。`--no-apply-immediately` を指定すると、次のメンテナンスウィンドウで適用されます。マネジメントコンソールの場合は、対象インスタンスを選択して [変更] から DB エンジンバージョンを選択します。

#### ステップ3: アップグレードの確認

```bash
# エンジンバージョンとステータスを確認
aws rds describe-db-instances \
  --db-instance-identifier mydbinstance \
  --query 'DBInstances[0].[EngineVersion,DBInstanceStatus]'
```

アップグレードの進行状況と完了後のエンジンバージョンを確認します。完了後はアプリケーションからの接続と主要機能の動作を確認してください。

## メリット

### ビジネス面

- **セキュリティリスクの軽減**: GDR アップデートにより Microsoft が公開した最新のセキュリティ修正を適用し、脆弱性リスクを低減
- **コンプライアンスの維持**: 最新パッチの適用により、セキュリティ基準やコンプライアンス要件への対応を維持
- **ビジネス継続性**: 既知のバグが修正された安定バージョンにより、予期しない障害リスクを低減

### 技術面

- **バグ修正とパフォーマンス改善**: CU に含まれる修正と最適化を利用可能
- **運用の容易さ**: マネジメントコンソール、AWS SDK、CLI から簡単にアップグレード可能
- **幅広いバージョンカバレッジ**: SQL Server 2017 から最新の SQL Server 2025 まで 4 バージョンを同時にサポート

## デメリット・制約事項

### 制限事項

- アップグレード中はデータベースインスタンスが一時的に利用不可になる
- エンジンバージョンのダウングレードは直接サポートされていない (スナップショットからの復元が必要)
- 今回の発表では RDS Custom for SQL Server は対象として記載されていない

### 考慮すべき点

- アップグレード前にテスト環境で互換性を確認することを推奨
- 業務影響の少ない時間帯 (メンテナンスウィンドウ) での適用を計画
- CU 適用後にクエリプランが変化する可能性があるため、アップグレード後のパフォーマンス監視を推奨

## ユースケース

### ユースケース1: 本番環境への計画的なセキュリティパッチ適用

**シナリオ**: 本番環境の Amazon RDS for SQL Server 2019 に GDR セキュリティアップデートを適用し、業務影響を最小化したい。

**実装例**:
```bash
# 1. 事前にスナップショットを作成
aws rds create-db-snapshot \
  --db-instance-identifier prod-sqlserver \
  --db-snapshot-identifier prod-sqlserver-pre-upgrade

# 2. メンテナンスウィンドウ中にアップグレード
aws rds modify-db-instance \
  --db-instance-identifier prod-sqlserver \
  --engine-version 15.00.4490.9.v1 \
  --no-apply-immediately
```

**効果**: メンテナンスウィンドウ中にセキュリティパッチが適用され、業務時間への影響を抑えながらセキュリティリスクを軽減できます。

### ユースケース2: 開発・テスト環境での事前互換性検証

**シナリオ**: 本番適用前に、開発環境で SQL Server 2022 CU27 との互換性を検証したい。

**実装例**:
```bash
# 開発環境を即時アップグレード
aws rds modify-db-instance \
  --db-instance-identifier dev-sqlserver \
  --engine-version 16.00.4295.3.v1 \
  --apply-immediately

# アプリケーションのテストスイートを実行して互換性を確認
```

**効果**: クエリプランの変化やアプリケーション互換性の問題を本番適用前に検出でき、安全なロールアウト計画を立てられます。

### ユースケース3: SQL Server 2025 環境の最新化

**シナリオ**: 最新の SQL Server 2025 を RDS で利用しており、CU9 で提供される修正を早期に取り込みたい。

**実装例**:
```bash
aws rds modify-db-instance \
  --db-instance-identifier sql2025-instance \
  --engine-version 17.00.5005.3.v1 \
  --apply-immediately
```

**効果**: 最新メジャーバージョンでも継続的に CU を適用でき、新機能利用と安定運用を両立できます。

## 料金

SQL Server エンジンバージョンのアップグレード自体に追加料金はかかりません。Amazon RDS for SQL Server の標準的な料金体系が適用されます。

- **インスタンス時間**: 使用した DB インスタンスの時間数に基づいて課金
- **ストレージ**: プロビジョニングされたストレージ容量に基づいて課金
- **バックアップ**: 自動バックアップと手動スナップショットのストレージに対して課金

最新の料金については、[Amazon RDS for SQL Server 料金ページ](https://aws.amazon.com/rds/sqlserver/pricing/)を参照してください。

## 利用可能リージョン

公式発表には特定のリージョンの記載はありません。利用可能なリージョンとエンジンバージョンの詳細は、[AWS リージョン別サービス一覧](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/)および RDS ユーザーガイドを参照してください。

## 関連サービス・機能

- **Amazon RDS 自動バックアップ**: アップグレード前の復元ポイントを確保し、万が一の場合に復元可能
- **Amazon RDS Performance Insights**: アップグレード後のパフォーマンスを監視し、クエリプランの変化を確認
- **Amazon CloudWatch**: RDS インスタンスのメトリクスを監視し、アップグレード後の動作を確認
- **Amazon RDS Blue/Green Deployments**: 本番環境への影響を最小化したアップグレード手法として活用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261026-amazon-rds-supports-latest-cumulative-update-gdr-microsoft-sql-server.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/10/amazon-rds-supports-latest-cumulative-update-gdr-microsoft-sql-server/)
- [ドキュメント: Upgrading the Microsoft SQL Server DB engine](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.SQLServer.html)
- [Amazon RDS for SQL Server 製品ページ](https://aws.amazon.com/rds/sqlserver/)
- [Microsoft KB5122774 (SQL Server 2017 CU31+GDR)](https://support.microsoft.com/help/5122774)
- [Microsoft KB5122772 (SQL Server 2019 CU32+GDR)](https://support.microsoft.com/help/5122772)
- [Microsoft KB5104824 (SQL Server 2022 CU27)](https://support.microsoft.com/help/5104824)
- [Microsoft KB5122048 (SQL Server 2025 CU9)](https://support.microsoft.com/help/5122048)
- [料金ページ](https://aws.amazon.com/rds/sqlserver/pricing/)

## まとめ

Amazon RDS for SQL Server が、SQL Server 2017/2019/2022/2025 の 4 バージョンに対する最新の CU と GDR アップデートをサポートしました。GDR にはセキュリティ修正が含まれるため、RDS for SQL Server を利用しているすべてのユーザーは、テスト環境での互換性確認とバックアップ取得のうえ、早期のアップグレード適用を推奨します。アップグレードは RDS マネジメントコンソール、AWS SDK、CLI から簡単に実行できます。
