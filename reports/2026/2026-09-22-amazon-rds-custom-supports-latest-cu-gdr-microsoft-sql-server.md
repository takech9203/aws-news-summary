# Amazon RDS Custom - Microsoft SQL Server の最新 CU のサポート

**リリース日**: 2026 年 9 月 22 日
**サービス**: Amazon RDS Custom for SQL Server
**機能**: Microsoft SQL Server 向け最新 Cumulative Update (CU) のサポート

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260922-amazon-rds-custom-supports-latest-cu-gdr-microsoft-sql-server.html)

## 概要

Amazon RDS Custom for SQL Server が、Microsoft SQL Server の最新の Cumulative Update (CU) をサポートしました。今回のリリースでは、SQL Server 2022 向けの CU26 (KB5093420、RDS バージョン 16.00.4265.3.v1) が利用可能になります。

RDS Custom は OS やデータベース環境へのアクセスを必要とするレガシーアプリケーションやサードパーティ製アプリケーション、カスタマイズが必要なワークロード向けのマネージドサービスです。今回のアップデートにより、こうした環境でも Microsoft の最新の不具合修正や改善を、AWS が検証済みのエンジンバージョンとして適用できます。アップデートの適用は、Amazon RDS マネジメントコンソール、AWS SDK、AWS CLI のいずれからでも実行できます。

**アップデート前の課題**

このアップデート以前に存在していた課題や制限は以下のとおりです。

- SQL Server 2022 CU26 に含まれる不具合修正や改善を RDS Custom for SQL Server で利用できなかった
- Microsoft の最新 CU を適用するには、AWS がサポートするエンジンバージョンの提供を待つ必要があった

**アップデート後の改善**

今回のアップデートにより可能になったことは以下のとおりです。

- SQL Server 2022 CU26 を含む新しいエンジンバージョン 16.00.4265.3.v1 へアップグレードできるようになった
- コンソール、AWS SDK、AWS CLI から最新 CU をマネージドな手順で適用できるようになった

## サービスアップデートの詳細

### 主要機能

1. **SQL Server 2022 CU26 のサポート**
   - Microsoft KB5093420 に対応
   - RDS エンジンバージョン: 16.00.4265.3.v1
   - CU26 までの累積的な不具合修正と改善を含む

2. **複数の適用手段**
   - Amazon RDS マネジメントコンソール、AWS SDK、AWS CLI からアップグレードを実行可能
   - 即時適用、またはメンテナンスウィンドウでの適用を選択可能

## 技術仕様

### 対応バージョン

| SQL Server バージョン | 更新プログラム | Microsoft KB | RDS エンジンバージョン |
|------|------|------|------|
| SQL Server 2022 | CU26 | KB5093420 | 16.00.4265.3.v1 |

### アップグレード方式

| 項目 | 詳細 |
|------|------|
| RPEV | AWS が提供するエンジンバージョン。直接アップグレード可能 |
| CEV | カスタムエンジンバージョン。対象 CU を含む CEV を新規作成し、インスタンスを新 CEV に変更する 2 段階の手順が必要 |
| Multi-AZ | ローリングアップグレードを実行。ダウンタイムはフェイルオーバーに要する時間のみ |

## 設定方法

### 前提条件

1. Amazon RDS Custom for SQL Server の DB インスタンスが稼働していること
2. アップグレード先のエンジンバージョンが現在のバージョン以降であること (アップグレードは不可逆)
3. CEV を使用している場合は、対象の CU を含む新しい CEV を事前に作成すること

### 手順

#### ステップ 1: アップグレード可能なターゲットバージョンの確認

```bash
aws rds describe-db-engine-versions \
    --engine custom-sqlserver-se \
    --engine-version 16.00.4262.2.v1 \
    --query "DBEngineVersions[*].ValidUpgradeTarget[*].{EngineVersion:EngineVersion}" \
    --output table
```

現在のエンジンバージョンからアップグレード可能なターゲットバージョンの一覧を表形式で表示します。`--engine` にはエディションに応じて `custom-sqlserver-se`、`custom-sqlserver-ee`、`custom-sqlserver-web` などを指定します。

#### ステップ 2: DB インスタンスのエンジンバージョン変更

```bash
aws rds modify-db-instance \
    --db-instance-identifier my-custom-sqlserver-instance \
    --engine-version 16.00.4265.3.v1 \
    --no-apply-immediately
```

DB インスタンスのエンジンバージョンを SQL Server 2022 CU26 に対応する新バージョンに変更します。`--no-apply-immediately` を指定すると次回のメンテナンスウィンドウで適用され、`--apply-immediately` を指定すると即時に適用されます。

## メリット

### ビジネス面

- **運用リスクの低減**: AWS が検証したエンジンバージョンとして提供されるため、独自パッチ適用に伴う障害リスクを抑えられる
- **サポート継続性の確保**: Microsoft の最新更新プログラムに追随することで、既知の不具合による業務影響を回避できる

### 技術面

- **マネージドなアップグレード手順**: コンソール、AWS CLI、AWS SDK から一貫した手順でアップグレードを実行できる
- **累積修正の一括適用**: CU は累積的な更新であるため、過去の修正を含めて一度に適用できる

## デメリット・制約事項

### 制限事項

- アップグレードは不可逆であり、以前のバージョンへのダウングレードはできない
- CEV を使用している場合、稼働中のインスタンスへ CU をインプレース適用することはサポートされない
- 今回の対象は SQL Server 2022 のみで、他のバージョン向けの新しい CU は含まれない

### 考慮すべき点

- 後方互換性の問題を避けるため、本番環境への適用前に非本番環境でアプリケーションのテストを実施することが推奨される
- Single-AZ 構成ではアップグレード中にダウンタイムが発生するため、メンテナンスウィンドウでの適用を検討する

## 料金

今回のアップデートによる追加料金はありません。Amazon RDS Custom for SQL Server の通常料金 (インスタンス、ストレージ、ライセンスなど) が適用されます。詳細は [Amazon RDS Custom の料金ページ](https://aws.amazon.com/rds/custom/pricing/) を参照してください。

## 利用可能リージョン

公式発表ではリージョンに関する記載はありません。Amazon RDS Custom for SQL Server が利用可能なリージョンについては、[AWS リージョン別サービス一覧](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) を参照してください。

## 関連サービス・機能

- **Amazon RDS for SQL Server**: OS アクセスが不要な標準的なワークロード向けのフルマネージド SQL Server。同様に CU 更新が順次提供される
- **Amazon RDS Custom for Oracle**: OS / データベースレベルのカスタマイズが必要な Oracle ワークロード向けの同種のサービス

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260922-amazon-rds-custom-supports-latest-cu-gdr-microsoft-sql-server.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-rds-custom-supports-latest-cu-gdr-microsoft-sql-server/)
- [ドキュメント: Upgrading an Amazon RDS Custom for SQL Server DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-upgrading-sqlserver.html)
- [Amazon RDS Custom 製品ページ](https://aws.amazon.com/rds/custom/)
- [Microsoft KB5093420 (SQL Server 2022 CU26)](https://support.microsoft.com/en-us/servicing/sql/sql-server-2022/cumulative-update/kb5093420-cu26)

## まとめ

Amazon RDS Custom for SQL Server で SQL Server 2022 CU26 (RDS バージョン 16.00.4265.3.v1) が利用可能になりました。Microsoft の最新の不具合修正を取り込むため、非本番環境での検証を経て計画的にアップグレードすることを推奨します。CEV を利用している場合は、インプレース適用を避け、新しい CEV を作成して切り替える手順に従ってください。
