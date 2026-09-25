# Amazon RDS for MySQL - Extended Support マイナーバージョン 5.7.44-rds.20260902 および 8.0.46-rds.20260908 のリリース

**リリース日**: 2026 年 9 月 24 日
**サービス**: Amazon RDS for MySQL
**機能**: Amazon RDS Extended Support マイナーバージョン (5.7.44-rds.20260902 / 8.0.46-rds.20260908)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260924-amazon-rds-mysql-extended-support-minor-5744-8046-rds.html)

## 概要

Amazon RDS for MySQL が、Amazon RDS Extended Support のマイナーバージョン 5.7.44-rds.20260902 および 8.0.46-rds.20260908 をリリースしました。Amazon RDS Extended Support は、メジャーバージョンの標準サポート終了日以降も、重大な CVE (Common Vulnerabilities and Exposures) およびバグに対する修正を最大 3 年間提供するプログラムです。

今回のリリースにより、MySQL 5.7 系および 8.0 系を Extended Support で利用しているユーザーは、最新のセキュリティ修正とバグ修正を含むマイナーバージョンへ更新できます。標準サポートが終了したバージョンを利用し続けざるを得ないワークロードでも、セキュリティリスクを抑えながら運用を継続できます。

なお、より新しいメジャーバージョンへの移行手段として、Amazon RDS Blue/Green Deployments、インプレースアップグレード、スナップショットからの復元が利用可能です。外部の MySQL ソースからの MySQL 8.4 への移行には AWS Database Migration Service (AWS DMS) を利用できます。

**アップデート前の課題**

- 標準サポートが終了した MySQL 5.7 / 8.0 を利用する環境では、新たに公開される重大な CVE やバグへの対応手段が限られていた
- アプリケーション側の制約などで最新メジャーバージョンへすぐに移行できない場合、脆弱性を抱えたまま運用を続けるリスクがあった

**アップデート後の改善**

- Extended Support 対象の 5.7 系 / 8.0 系それぞれに、重大な CVE およびバグ修正を含む新しいマイナーバージョンが提供された
- マイナーバージョン更新により、メジャーバージョン移行の準備期間中もセキュリティを維持した運用が可能になった
- Blue/Green Deployments やインプレースアップグレードなど、複数のアップグレード手段が引き続き利用できる

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Current["🗄️ 現在の環境"]
        direction LR
        V57["MySQL 5.7 系<br/>Extended Support"]
        V80["MySQL 8.0 系<br/>Extended Support"]
        V57 ~~~ V80
    end

    subgraph MinorUpdate["🔄 マイナーバージョン更新"]
        direction LR
        M57["5.7.44-rds.20260902<br/>重大な CVE / バグ修正"]
        M80["8.0.46-rds.20260908<br/>重大な CVE / バグ修正"]
        M57 ~~~ M80
    end

    subgraph MajorUpgrade["⬆️ メジャーバージョン移行の選択肢"]
        direction LR
        BG["🔵🟢 Blue/Green<br/>Deployments"]
        IP["⚙️ インプレース<br/>アップグレード"]
        SS["📸 スナップショット<br/>からの復元"]
        BG ~~~ IP ~~~ SS
    end

    Ext{{"🌐 外部 MySQL ソース"}}
    Target["🆕 MySQL 8.4 など<br/>標準サポート対象バージョン"]
    DMS["🚚 AWS DMS"]

    V57 --> M57
    V80 --> M80
    M57 -.-> MajorUpgrade
    M80 -.-> MajorUpgrade
    MajorUpgrade --> Target
    Ext --> DMS
    DMS --> Target

    classDef layer fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef current fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#5D4037
    classDef minor fill:#E8F1FF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef path fill:#FFFFFF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef target fill:#E9F7EC,stroke:#66BB6A,stroke-width:2px,color:#33691E
    classDef external fill:#F3E5F5,stroke:#7B61FF,stroke-width:2px,color:#333333

    class Current,MajorUpgrade layer
    class V57,V80 current
    class M57,M80,MinorUpdate minor
    class BG,IP,SS path
    class Target target
    class Ext,DMS external
```

Extended Support 環境の各バージョンを新しいマイナーバージョンへ更新する流れと、メジャーバージョン移行の選択肢を示しています。マイナーバージョン更新でセキュリティを維持しつつ、Blue/Green Deployments などを利用して標準サポート対象バージョンへ計画的に移行できます。

## サービスアップデートの詳細

### 主要機能

1. **MySQL 5.7 系向け Extended Support マイナーバージョン 5.7.44-rds.20260902**
   - MySQL 5.7 系の Extended Support 利用環境向けの新しいマイナーバージョン
   - 重大な CVE およびバグに対する修正を含む
   - RDS マネジメントコンソールまたは AWS CLI から適用可能

2. **MySQL 8.0 系向け Extended Support マイナーバージョン 8.0.46-rds.20260908**
   - MySQL 8.0 系の Extended Support 利用環境向けの新しいマイナーバージョン
   - 重大な CVE およびバグに対する修正を含む
   - RDS マネジメントコンソールまたは AWS CLI から適用可能

3. **メジャーバージョン移行手段の提供**
   - Amazon RDS Blue/Green Deployments によるダウンタイムを最小化した移行
   - インプレースアップグレードによる直接的なバージョン更新
   - スナップショットからの復元によるアップグレード
   - 外部 MySQL ソースからの MySQL 8.4 への移行には AWS DMS を利用可能

## 技術仕様

### リリースされたバージョン

| 項目 | 詳細 |
|------|------|
| 対象エンジン | Amazon RDS for MySQL |
| 5.7 系バージョン | 5.7.44-rds.20260902 |
| 8.0 系バージョン | 8.0.46-rds.20260908 |
| 提供プログラム | Amazon RDS Extended Support |
| 修正内容 | 重大な CVE およびバグの修正 |
| 適用方法 | RDS マネジメントコンソール、AWS CLI |

### Amazon RDS Extended Support の概要

| 項目 | 詳細 |
|------|------|
| 目的 | 標準サポート終了後のメジャーバージョンに対する継続的な修正提供 |
| 提供期間 | 標準サポート終了日から最大 3 年間 |
| 提供内容 | 重大な CVE の修正、バグ修正 |
| 課金 | Extended Support 利用分は追加料金が発生 (詳細は料金ページを参照) |

## 設定方法

### 前提条件

1. Amazon RDS for MySQL 5.7 系または 8.0 系の DB インスタンスを利用していること
2. Extended Support が有効になっていること
3. マイナーバージョン更新に伴う短時間の停止を許容できるメンテナンスウィンドウを確保していること

### 手順

#### ステップ 1: 利用可能なバージョンの確認

```bash
aws rds describe-db-engine-versions \
    --engine mysql \
    --query 'DBEngineVersions[?contains(EngineVersion, `rds.2026`)].EngineVersion'
```

RDS for MySQL で利用可能なエンジンバージョンの一覧から、今回リリースされた Extended Support マイナーバージョンが選択可能かを確認します。

#### ステップ 2: マイナーバージョンの適用

```bash
aws rds modify-db-instance \
    --db-instance-identifier my-mysql-instance \
    --engine-version 8.0.46 \
    --apply-immediately
```

対象の DB インスタンスのエンジンバージョンを新しいマイナーバージョンに変更します。`--apply-immediately` を指定すると即時適用され、指定しない場合は次回のメンテナンスウィンドウで適用されます。5.7 系の場合はエンジンバージョンに 5.7.44 系の該当バージョンを指定します。

#### ステップ 3: 適用状況の確認

```bash
aws rds describe-db-instances \
    --db-instance-identifier my-mysql-instance \
    --query 'DBInstances[0].{Status:DBInstanceStatus,Version:EngineVersion}'
```

DB インスタンスのステータスとエンジンバージョンを確認し、更新が正常に完了したことを検証します。

## メリット

### ビジネス面

- **セキュリティリスクの低減**: 標準サポート終了後のバージョンでも重大な CVE への修正が提供され、コンプライアンス要件への対応を継続できる
- **移行計画の柔軟性**: 最大 3 年間の Extended Support 期間を活用し、アプリケーション改修やテストを含む計画的なメジャーバージョン移行が可能
- **運用継続性の確保**: 既存アプリケーションを変更せずにセキュリティ修正のみを適用できる

### 技術面

- **マイナーバージョン更新の容易さ**: メジャーバージョンアップグレードと比べて互換性リスクが小さく、適用のハードルが低い
- **複数の移行パスの提供**: Blue/Green Deployments、インプレースアップグレード、スナップショット復元と、要件に応じた移行手段を選択できる
- **外部ソースからの移行支援**: AWS DMS により外部 MySQL ソースから MySQL 8.4 への移行が可能

## デメリット・制約事項

### 制限事項

- Extended Support の提供期間は標準サポート終了日から最大 3 年間であり、恒久的な解決策ではない
- Extended Support の利用には追加料金が発生する (料金はリージョンおよびバージョンにより異なる)
- 個別の CVE 番号や具体的なバグ修正の一覧は今回の発表には記載されていない

### 考慮すべき点

- Extended Support はあくまで移行までの猶予期間と位置付け、標準サポート対象バージョン (MySQL 8.4 など) への移行計画を早期に策定することが推奨される
- マイナーバージョン更新時には短時間のダウンタイムが発生する可能性があるため、メンテナンスウィンドウの調整が必要
- 適用前にステージング環境での動作確認を行うことが望ましい

## ユースケース

### ユースケース 1: レガシーアプリケーションのセキュリティ維持

**シナリオ**: MySQL 5.7 に依存するレガシーアプリケーションを運用しており、すぐにはメジャーバージョンアップグレードができないが、セキュリティ要件は満たす必要がある。

**実装例**:
```bash
aws rds modify-db-instance \
    --db-instance-identifier legacy-app-db \
    --engine-version 5.7.44 \
    --no-apply-immediately
```

**効果**: 次回メンテナンスウィンドウで最新の CVE 修正を適用し、アプリケーションを変更することなくセキュリティ基準を維持できる。

### ユースケース 2: Blue/Green Deployments を利用した MySQL 8.0 から 8.4 への計画的移行

**シナリオ**: MySQL 8.0 の Extended Support を利用中だが、コスト最適化のため標準サポート対象バージョンへの移行を計画している。移行時のダウンタイムは最小限に抑えたい。

**実装例**:
```bash
aws rds create-blue-green-deployment \
    --blue-green-deployment-name mysql80-to-84 \
    --source arn:aws:rds:ap-northeast-1:123456789012:db:prod-mysql \
    --target-engine-version 8.4
```

**効果**: 本番環境 (Blue) を稼働させたまま新バージョン環境 (Green) を構築・検証し、切り替え時のダウンタイムを最小化してメジャーバージョン移行を実現できる。

### ユースケース 3: 外部 MySQL 環境からの AWS 移行

**シナリオ**: オンプレミスで稼働する MySQL データベースを AWS に移行し、あわせて MySQL 8.4 へバージョンアップしたい。

**実装例**:
```bash
aws dms create-replication-task \
    --replication-task-identifier onprem-to-rds-mysql84 \
    --source-endpoint-arn <オンプレミス MySQL のエンドポイント ARN> \
    --target-endpoint-arn <RDS for MySQL 8.4 のエンドポイント ARN> \
    --migration-type full-load-and-cdc \
    --table-mappings file://table-mappings.json
```

**効果**: AWS DMS のフルロードと CDC (変更データキャプチャ) により、稼働中の外部データベースから最小限の停止時間で RDS for MySQL 8.4 へ移行できる。

## 料金

Amazon RDS Extended Support の利用には、通常のインスタンス料金に加えて追加料金が発生します。料金はリージョン、エンジンバージョン、vCPU 数などにより異なります。具体的な料金は [Amazon RDS for MySQL 料金ページ](https://aws.amazon.com/rds/mysql/pricing/) を参照してください。

## 利用可能リージョン

リージョンごとの提供状況は [Amazon RDS for MySQL 料金ページ](https://aws.amazon.com/rds/mysql/pricing/) で確認できます。

## 関連サービス・機能

- **Amazon RDS Blue/Green Deployments**: 本番環境に影響を与えずにステージング環境を作成し、ダウンタイムを最小化してバージョンアップグレードを実施できる機能
- **AWS Database Migration Service (AWS DMS)**: 外部 MySQL ソースから MySQL 8.4 への移行を支援するマネージドな移行サービス
- **Amazon Aurora MySQL**: 同様に Extended Support を提供する MySQL 互換のマネージドデータベース。移行先の選択肢の 1 つ

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260924-amazon-rds-mysql-extended-support-minor-5744-8046-rds.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-rds-mysql-extended-support-minor-5744-8046-rds/)
- [Amazon RDS for MySQL 製品ページ](https://aws.amazon.com/rds/mysql/)
- [Amazon RDS Extended Support ユーザーガイド](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html)
- [Amazon RDS Blue/Green Deployments ドキュメント](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments.html)
- [MySQL DB エンジンのアップグレード手順](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.html)
- [AWS Database Migration Service](https://aws.amazon.com/dms/)
- [Amazon RDS for MySQL 料金ページ](https://aws.amazon.com/rds/mysql/pricing/)

## まとめ

Amazon RDS for MySQL の Extended Support マイナーバージョン 5.7.44-rds.20260902 および 8.0.46-rds.20260908 のリリースにより、標準サポート終了後のバージョンでも重大な CVE とバグの修正を適用できます。Extended Support 環境を利用中の場合は、早期にマイナーバージョン更新を適用してセキュリティを維持することを推奨します。あわせて、Extended Support は最大 3 年間の時限的なプログラムであるため、Blue/Green Deployments などを活用した標準サポート対象バージョンへの移行計画も並行して進めることが重要です。
