# Amazon EC2 - C7i インスタンスが欧州 (ミラノ) およびカナダ西部 (カルガリー) リージョンで利用可能に

**リリース日**: 2026 年 7 月 31 日
**サービス**: Amazon EC2
**機能**: C7i インスタンスの Europe (Milan) および Canada West (Calgary) リージョンへの拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260731-amazon-ec2-c7i-instances-mxp-yyc-region.html)

## 概要

Amazon EC2 C7i インスタンスが、欧州 (ミラノ) およびカナダ西部 (カルガリー) リージョンで利用可能になりました。C7i は、AWS 専用のカスタム第 4 世代 Intel Xeon Scalable プロセッサ (コードネーム Sapphire Rapids) を搭載したコンピューティング最適化インスタンスで、他のクラウドプロバイダーが使用する同等の x86 ベース Intel プロセッサと比較して最大 15% 優れたパフォーマンスを提供します。

C7i インスタンスは、前世代の C6i インスタンスと比較して最大 15% 優れた価格パフォーマンスを実現します。最大 48xlarge までの大きなサイズに加え、metal-24xl と metal-48xl の 2 つのベアメタルサイズを提供し、バッチ処理、分散分析、広告配信、動画エンコーディングなどのコンピューティング集約型ワークロードに最適です。

**アップデート前の課題**

- C7i インスタンスが欧州 (ミラノ) およびカナダ西部 (カルガリー) リージョンで利用できなかった
- これらのリージョンのお客様は、第 4 世代 Intel Xeon Scalable プロセッサの性能を活用できなかった
- コンピューティング集約型ワークロードで、データレジデンシー要件を満たしながら最新のコンピューティング最適化インスタンスを利用することが難しかった

**アップデート後の改善**

- 欧州 (ミラノ) およびカナダ西部 (カルガリー) リージョンで C7i インスタンスを直接起動できるようになった
- C6i インスタンスからの移行で最大 15% の価格パフォーマンス改善を実現できる
- 最大 48xlarge および 2 つのベアメタルサイズにより、大規模なコンピューティング集約型ワークロードを両リージョンで実行可能になった

## サービスアップデートの詳細

### 主要機能

1. **C7i インスタンス**
   - C6i と比較して最大 15% 優れた価格パフォーマンス
   - 最大 48xlarge までのサイズと、metal-24xl / metal-48xl の 2 つのベアメタルサイズを提供
   - 継続的な高 CPU 使用率が必要なワークロードに最適
   - バッチ処理、分散分析、広告配信、動画エンコーディングに適している

2. **カスタム第 4 世代 Intel Xeon Scalable プロセッサ**
   - コードネーム Sapphire Rapids
   - AWS 専用のカスタムプロセッサ
   - 他のクラウドプロバイダーが使用する同等の x86 ベース Intel プロセッサと比較して最大 15% 優れたパフォーマンス

3. **内蔵 Intel アクセラレータ (ベアメタルサイズ)**
   - **Data Streaming Accelerator (DSA)**: データストリーミング操作を効率化
   - **In-Memory Analytics Accelerator (IAA)**: インメモリ分析を高速化
   - **QuickAssist Technology (QAT)**: 暗号化と圧縮処理を高速化
   - データ操作の効率的なオフロードと高速化により、ワークロードのパフォーマンスを向上

## 技術仕様

### C7i インスタンスサイズ

| インスタンスサイズ | vCPU | メモリ (GiB) |
|-------------------|------|-------------|
| c7i.large | 2 | 4 |
| c7i.xlarge | 4 | 8 |
| c7i.2xlarge | 8 | 16 |
| c7i.4xlarge | 16 | 32 |
| c7i.8xlarge | 32 | 64 |
| c7i.12xlarge | 48 | 96 |
| c7i.16xlarge | 64 | 128 |
| c7i.24xlarge | 96 | 192 |
| c7i.48xlarge | 192 | 384 |
| c7i.metal-24xl | 96 | 192 |
| c7i.metal-48xl | 192 | 384 |

### パフォーマンス比較

| 指標 | 内容 |
|------|------|
| 価格パフォーマンス | C6i 比で最大 15% 向上 |
| プロセッサ性能 | 同等の x86 ベース Intel プロセッサ比で最大 15% 向上 |

## 設定方法

### 前提条件

1. AWS アカウントと欧州 (ミラノ) またはカナダ西部 (カルガリー) リージョンへのアクセス権限
2. C7i インスタンスタイプのサービスクォータ確認
3. 適切な VPC およびサブネット設定

### 手順

#### ステップ 1: C7i インスタンスの起動

```bash
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type c7i.4xlarge \
  --region eu-south-1 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx \
  --key-name my-key-pair
```

欧州 (ミラノ) リージョン (eu-south-1) で C7i インスタンスを起動するコマンドです。カナダ西部 (カルガリー) の場合は `--region ca-west-1` を指定します。

#### ステップ 2: 利用可能なインスタンスタイプの確認

```bash
aws ec2 describe-instance-types \
  --filters "Name=instance-type,Values=c7i.*" \
  --region ca-west-1 \
  --query "InstanceTypes[].{Type:InstanceType,vCPU:VCpuInfo.DefaultVCpus,Memory:MemoryInfo.SizeInMiB}" \
  --output table
```

カルガリーリージョンで利用可能な C7i インスタンスタイプとスペックを一覧表示するコマンドです。

## メリット

### ビジネス面

- **コスト効率の向上**: C6i と比較して最大 15% 優れた価格パフォーマンスにより、コンピューティングコストを削減
- **リージョン拡大**: 欧州 (ミラノ) およびカナダ西部 (カルガリー) リージョンでの提供により、データレジデンシー要件を満たしながら最新インスタンスを利用可能
- **柔軟なサイジング**: 最大 48xlarge と 2 つのベアメタルサイズにより、ワークロードに最適なサイズを選択可能

### 技術面

- **高性能プロセッサ**: AWS 専用のカスタム第 4 世代 Intel Xeon Scalable プロセッサによる優れたパフォーマンス
- **内蔵アクセラレータ**: ベアメタルサイズでは DSA、IAA、QAT によりデータ操作、分析、暗号化・圧縮処理を高速化

## デメリット・制約事項

### 制限事項

- DSA、IAA、QAT アクセラレータはベアメタルサイズ (metal-24xl、metal-48xl) でのみ利用可能
- 新規リージョンでの初期のサービスクォータが制限される場合がある

### 考慮すべき点

- すべてのコンピューティングリソースを完全に活用しないワークロードには、より価格パフォーマンスに優れた C7i-flex の利用を検討すべき
- 既存の C6i インスタンスからの移行は新規起動で行う必要がある

## ユースケース

### ユースケース: 大規模バッチ処理と分散分析

**シナリオ**: カナダ西部のデータレジデンシー要件を満たしながら、大規模なバッチ処理や分散分析をカルガリーリージョンで実行したい。

**実装例**:
```bash
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type c7i.48xlarge \
  --region ca-west-1 \
  --iam-instance-profile Name=Batch-Processing-Role
```

**効果**: 最大 192 vCPU と 384 GiB メモリにより、大規模なバッチ処理を高速に実行。データレジデンシー要件を満たしながら、C6i 比で最大 15% 優れた価格パフォーマンスを実現。

## 料金

C7i インスタンスの料金は、インスタンスサイズ、リージョン、購入オプション (オンデマンド、Savings Plans、スポットインスタンス) によって異なります。詳細は [Amazon EC2 料金ページ](https://aws.amazon.com/ec2/pricing/) を参照してください。

## 利用可能リージョン

今回のアップデートで、以下の 2 リージョンが追加されました。

**新規対応リージョン (2026 年 7 月 31 日)**:
- 欧州 (ミラノ) - eu-south-1
- カナダ西部 (カルガリー) - ca-west-1

最新のリージョン情報は [AWS Regional Services List](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) を参照してください。

## 関連サービス・機能

- **Amazon EC2 C7i-flex インスタンス**: コンピューティングリソースを完全に活用しないワークロード向けの同世代インスタンス (同日にミラノリージョンで提供開始)
- **Amazon EC2 C6i インスタンス**: C7i の前世代のコンピューティング最適化インスタンス
- **AWS Compute Optimizer**: ワークロードに最適なインスタンスタイプの推奨

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260731-amazon-ec2-c7i-instances-mxp-yyc-region.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-ec2-c7i-instances-mxp-yyc-region/)
- [C7i インスタンスタイプページ](https://aws.amazon.com/ec2/instance-types/c7i/)
- [Amazon EC2 料金ページ](https://aws.amazon.com/ec2/pricing/)

## まとめ

Amazon EC2 C7i インスタンスが欧州 (ミラノ) およびカナダ西部 (カルガリー) リージョンで利用可能になりました。カスタム第 4 世代 Intel Xeon Scalable プロセッサ (Sapphire Rapids) を搭載し、C6i インスタンスと比較して最大 15% 優れた価格パフォーマンスを提供します。最大 48xlarge と 2 つのベアメタルサイズにより、大規模なコンピューティング集約型ワークロードにも対応します。両リージョンでコンピューティング集約型ワークロードを実行しているお客様は、C7i インスタンスへの移行を検討し、パフォーマンスとコスト効率の向上を実現してください。
