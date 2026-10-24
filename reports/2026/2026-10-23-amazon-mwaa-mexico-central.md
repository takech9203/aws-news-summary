# Amazon MWAA - Mexico (Central) リージョンで Provisioned 環境が利用可能に

**リリース日**: 2026 年 10 月 23 日
**サービス**: Amazon Managed Workflows for Apache Airflow (Amazon MWAA)
**機能**: Mexico (Central) リージョン (mx-central-1) での Provisioned 環境の提供開始

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261023-amazon-mwaa-mexico-central.html)

## 概要

Amazon Managed Workflows for Apache Airflow (Amazon MWAA) の Provisioned 環境が、Mexico (Central) リージョン (mx-central-1) で利用可能になりました。Amazon MWAA は Apache Airflow 向けのマネージドオーケストレーションサービスで、クラウド上でエンドツーエンドのデータパイプラインを大規模にセットアップ・実行する作業を簡素化します。

同リージョンでは MWAA Serverless がすでに提供されており、今回のアップデートにより Provisioned 環境も選択できるようになりました。環境は AWS マネジメントコンソール、AWS CLI、AWS SDK、AWS CloudFormation から作成できます。

**アップデート前の課題**

- Mexico (Central) リージョンでは MWAA の Provisioned 環境を作成できず、利用形態は Serverless に限られていた
- メキシコ国内にデータソースやエンドユーザーを持つ場合でも、Provisioned 環境は他リージョンで実行する必要があり、レイテンシやデータレジデンシーの面で制約があった

**アップデート後の改善**

- Mexico (Central) リージョンで Provisioned 環境の Apache Airflow ワークフローを実行可能になった
- データソースやエンドユーザーの近くでワークフローを実行でき、レイテンシを低減できる
- メキシコ国内のデータレジデンシー要件への対応に役立つ
- 同一リージョン内で Serverless と Provisioned の両方の利用形態を選択できるようになった

## サービスアップデートの詳細

### 主要機能

1. **Provisioned 環境の提供開始**
   - Mexico (Central) リージョン (mx-central-1) で MWAA Provisioned 環境を作成可能
   - AWS マネジメントコンソール、AWS CLI、AWS SDK、AWS CloudFormation に対応

2. **Serverless との併用**
   - 同リージョンでは MWAA Serverless がすでに提供済み
   - ワークロードの特性に応じて Provisioned と Serverless を使い分け可能

## 設定方法

### 前提条件

1. AWS アカウントと Mexico (Central) リージョン (mx-central-1) へのアクセス
2. DAG を配置する Amazon S3 バケットなど、MWAA 環境作成に必要なリソース

### 手順

#### ステップ 1: 環境の作成

```bash
aws mwaa create-environment \
  --region mx-central-1 \
  --name my-mwaa-environment \
  --source-bucket-arn arn:aws:s3:::my-dag-bucket \
  --dag-s3-path dags \
  --execution-role-arn arn:aws:iam::123456789012:role/my-mwaa-role \
  --network-configuration SubnetIds=subnet-xxxx,subnet-yyyy,SecurityGroupIds=sg-zzzz
```

AWS CLI でリージョンに `mx-central-1` を指定し、MWAA 環境を作成します。コンソール、SDK、CloudFormation からも同様に作成できます。

## メリット

### ビジネス面

- **データレジデンシー要件への対応**: メキシコ国内でワークフローを実行でき、データ所在地に関する要件への対応に役立つ
- **ユーザー体験の向上**: エンドユーザーの近くで実行することでレイテンシを低減できる

### 技術面

- **レイテンシの低減**: データソースの近くでワークフローを実行できる
- **利用形態の選択肢拡大**: 同一リージョン内で Serverless と Provisioned を使い分けられる

## デメリット・制約事項

### 考慮すべき点

- 既存の他リージョン環境を移行する場合は、DAG や接続情報、依存リソースの移行計画が必要
- リージョンごとの料金は料金ページで確認が必要

## 利用可能リージョン

今回のアップデートにより、Mexico (Central) リージョン (mx-central-1) で Provisioned 環境が利用可能になりました。対応リージョンの一覧は [公式ドキュメント](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html#regions-mwaa) を参照してください。

## 関連サービス・機能

- **Apache Airflow**: MWAA のベースとなるオープンソースのワークフローオーケストレーションツール
- **Amazon S3**: DAG ファイルや依存関係の配置先
- **AWS CloudFormation**: MWAA 環境の IaC による作成・管理

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261023-amazon-mwaa-mexico-central.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/10/amazon-mwaa-mexico-central/)
- [Amazon MWAA 製品ページ](https://aws.amazon.com/managed-workflows-for-apache-airflow/)
- [対応リージョン一覧 (ドキュメント)](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html#regions-mwaa)

## まとめ

Amazon MWAA の Provisioned 環境が Mexico (Central) リージョンで利用可能になり、Serverless と合わせて同リージョンでの利用形態の選択肢が揃いました。メキシコ国内にデータソースやエンドユーザーを持つワークロードでは、レイテンシ低減とデータレジデンシー要件対応の観点から、同リージョンでの環境作成を検討してください。
