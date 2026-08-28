# AWS Glue - AWS Glue 5.1 が AWS European Sovereign Cloud リージョンで利用可能に

**リリース日**: 2026 年 8 月 26 日
**サービス**: AWS Glue
**機能**: AWS Glue 5.1 の AWS European Sovereign Cloud リージョンでの提供開始

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260826-aws-glue-5-1-european-sovereign-cloud.html)

## 概要

AWS Glue 5.1 が AWS European Sovereign Cloud リージョンで利用可能になりました。AWS Glue は、複数のソースからのデータの検出、準備、移動、統合を簡素化するサーバーレスでスケーラブルなデータ統合サービスです。AWS European Sovereign Cloud は、完全に欧州連合 (EU) 域内に配置された独立したクラウドであり、ソブリンティ (主権) 要件を持つ組織を支援するために構築されています。

Glue 5.1 はコアエンジンを Apache Spark 3.5.6、Python 3.11、Scala 2.12.18 にアップグレードし、パフォーマンスとセキュリティを強化しています。また、Apache Hudi 1.0.2、Apache Iceberg 1.10.0、Delta Lake 3.3.2 といったオープンテーブルフォーマットライブラリの更新に加え、Apache Iceberg フォーマットバージョン 3.0 のサポートや、AWS Lake Formation のきめ細かなアクセス制御の書き込み操作 (DML/DDL) への拡張が含まれます。

**アップデート前の課題**

- AWS European Sovereign Cloud リージョンでは Glue 5.1 が利用できず、最新のエンジンバージョンやライブラリを使用できなかった
- Apache Iceberg フォーマットバージョン 3.0 や Lake Formation の書き込みアクセス制御など、Glue 5.1 の新機能を EU ソブリンティ要件下で活用できなかった

**アップデート後の改善**

- AWS European Sovereign Cloud リージョンで Glue 5.1 のジョブを実行できるようになった
- EU 域内にデータを保持しながら、Spark 3.5.6 ベースの最新データ統合機能と強化されたセキュリティ機能を活用できるようになった

## サービスアップデートの詳細

### 主要機能

1. **コアエンジンのアップグレード**
   - Apache Spark 3.5.6、Python 3.11、Scala 2.12.18 を採用
   - パフォーマンスとセキュリティの強化

2. **オープンテーブルフォーマットライブラリの更新**
   - Apache Hudi 1.0.2、Apache Iceberg 1.10.0、Delta Lake 3.3.2 をサポート

3. **Apache Iceberg フォーマットバージョン 3.0 サポート**
   - デフォルトカラム値
   - マージオンリードテーブルの削除ベクトル
   - マルチ引数変換
   - 行リネージ追跡

4. **Lake Formation きめ細かなアクセス制御の書き込み対応**
   - Spark DataFrames および Spark SQL の書き込み操作 (DML/DDL) に対するきめ細かなアクセス制御 (以前は読み取り操作のみ)
   - Apache Hudi および Delta Lake テーブルに対する Apache Spark でのフルテーブルアクセス制御

## 技術仕様

### エンジンバージョン

| コンポーネント | Glue 5.1 |
|---------------|----------|
| Apache Spark | 3.5.6 |
| Python | 3.11 |
| Scala | 2.12.18 |
| Apache Hudi | 1.0.2 |
| Apache Iceberg | 1.10.0 |
| Delta Lake | 3.3.2 |

## 設定方法

### 前提条件

1. AWS European Sovereign Cloud リージョンのアカウントを利用していること
2. AWS Glue へのアクセス権限があること

### 手順

#### ステップ 1: Glue 5.1 ジョブの作成

```bash
aws glue create-job \
  --name "my-glue-job" \
  --role "arn:aws:iam::123456789012:role/GlueServiceRole" \
  --command '{"Name":"glueetl","ScriptLocation":"s3://my-bucket/scripts/my-script.py","PythonVersion":"3"}' \
  --glue-version "5.1"
```

`--glue-version "5.1"` を指定して Glue ジョブを作成します。AWS APIs、AWS CLI、AWS SDK、AWS Glue Studio のいずれからでも利用を開始できます。

#### ステップ 2: 既存ジョブのアップグレード

既存ジョブの Glue バージョンを 5.1 に変更し、スクリプトの互換性 (特に Python 3.11 とライブラリの依存関係) を確認します。

## メリット

### ビジネス面

- **ソブリンティ要件との両立**: EU 域内に完全に配置されたクラウドで最新のデータ統合機能を利用できる
- **コンプライアンス対応**: データレジデンシー要件を満たしながら、規制の厳しい業界のデータ基盤を最新化できる

### 技術面

- **パフォーマンス向上**: Spark 3.5.6 と最新ライブラリによる処理速度とセキュリティの改善
- **Iceberg 3.0 の活用**: 削除ベクトルや行リネージ追跡など、データレイクの効率化と監査性向上に役立つ機能を利用できる
- **データガバナンス強化**: Lake Formation による書き込み操作を含むきめ細かなアクセス制御を適用できる

## デメリット・制約事項

### 考慮すべき点

- 既存の Glue ジョブを 5.1 へ移行する際は、Python 3.11 やライブラリバージョンとの互換性確認が必要
- Iceberg フォーマットバージョン 3.0 は、連携するすべてのツールでサポートされているとは限らない

## ユースケース

### ユースケース: EU ソブリンティ要件下でのデータレイク構築

**シナリオ**: 欧州の公共機関や規制業界の企業が、データを EU 域内に保持しながら Iceberg ベースのデータレイクを構築、運用したい。

**効果**: AWS European Sovereign Cloud 上で Glue 5.1 の ETL ジョブを実行し、Iceberg 3.0 と Lake Formation の書き込みアクセス制御を組み合わせることで、ソブリンティ要件とデータガバナンスを両立したデータ基盤を実現できる。

## 料金

AWS Glue の標準料金が適用されます。リージョンによって料金が異なる場合があるため、詳細は [AWS Glue 料金ページ](https://aws.amazon.com/glue/pricing/) を参照してください。

## 利用可能リージョン

今回のアップデートにより、AWS European Sovereign Cloud リージョンで AWS Glue 5.1 が利用可能になりました。Glue 5.1 は商用リージョンでも順次拡大されており、利用可能リージョンの一覧は [AWS Glue ドキュメント](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html) を参照してください。

## 関連サービス・機能

- **AWS Lake Formation**: データレイクのきめ細かなアクセス制御とガバナンスを提供する
- **Apache Iceberg / Apache Hudi / Delta Lake**: Glue 5.1 がサポートするオープンテーブルフォーマット
- **AWS European Sovereign Cloud**: EU 域内に完全に配置された独立したクラウドで、ソブリンティ要件への対応を支援する

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260826-aws-glue-5-1-european-sovereign-cloud.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/08/aws-glue-5-1-european-sovereign-cloud)
- [AWS Blog - Introducing AWS Glue 5.1 for Apache Spark](https://aws.amazon.com/blogs/big-data/introducing-aws-glue-5-1-for-apache-spark/)
- [AWS Glue プロダクトページ](https://aws.amazon.com/glue/)
- [AWS Glue ドキュメント](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html)

## まとめ

AWS Glue 5.1 が AWS European Sovereign Cloud リージョンに拡大され、EU のソブリンティ要件を持つ組織でも Spark 3.5.6、Iceberg 3.0、Lake Formation 書き込みアクセス制御といった最新のデータ統合機能を利用できるようになりました。AWS European Sovereign Cloud でデータ基盤を運用する組織は、Glue 5.1 へのアップグレードを検討することを推奨します。
