# Amazon EC2 - M7i インスタンスがアフリカ (ケープタウン) で利用可能に

**リリース日**: 2026 年 2 月 19 日
**サービス**: Amazon EC2
**機能**: M7i インスタンスの Africa (Cape Town) リージョンへの拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260219-amazon-ec2-m7i-africa-cape-town-regions.html)

## 概要

Amazon EC2 M7i インスタンスが、アフリカ (ケープタウン) リージョンで利用可能になりました。M7i インスタンスは AWS 専用のカスタム第 4 世代 Intel Xeon Scalable プロセッサ (コードネーム Sapphire Rapids) を搭載した汎用インスタンスです。同等の x86 ベース Intel プロセッサと比較して最大 15% 優れたパフォーマンスを提供し、M6i インスタンスと比較して最大 15% 優れた価格パフォーマンスを実現します。

M7i インスタンスはゲームサーバー、CPU ベースの機械学習 (ML)、動画ストリーミングなどのワークロードに最適です。最大 48xlarge サイズまで 11 サイズを提供し、2 つのベアメタルサイズ (metal-24xl、metal-48xl) も利用可能です。さらに、4 つの内蔵 Intel アクセラレータ (Data Streaming Accelerator、In-Memory Analytics Accelerator、QuickAssist Technology、Advanced Matrix Extensions) を搭載しています。

**アップデート前の課題**

- M7i インスタンスがアフリカ (ケープタウン) リージョンで利用できなかった
- アフリカリージョンのユーザーは、最新世代の Intel ベース汎用インスタンスの恩恵を受けられなかった
- データレジデンシー要件のあるワークロードで、ケープタウンリージョンに最新の汎用インスタンスをデプロイできなかった

**アップデート後の改善**

- アフリカ (ケープタウン) リージョンで M7i インスタンスを直接起動できるようになった
- アフリカリージョンのユーザーが AWS 専用のカスタム Intel プロセッサの性能を活用できるようになった
- データローカリティ要件を満たしながら、高性能な汎用コンピューティングを利用可能になった

## サービスアップデートの詳細

### 主要機能

1. **カスタム第 4 世代 Intel Xeon Scalable プロセッサ (Sapphire Rapids)**
   - AWS 専用のカスタムプロセッサ (他のクラウドプロバイダーでは利用不可)
   - オールコアターボ周波数 3.2 GHz (最大コアターボ周波数 3.8 GHz)
   - Intel Total Memory Encryption (TME) による常時メモリ暗号化をサポート

2. **内蔵 Intel アクセラレータ**
   - **Advanced Matrix Extensions (AMX)**: CPU ベースの機械学習における行列乗算を高速化 (M7i および M7i-flex で利用可能)
   - **Data Streaming Accelerator (DSA)**: データベース操作のオフロードに最適 (ベアメタルのみ)
   - **In-Memory Analytics Accelerator (IAA)**: インメモリ分析の高速化 (ベアメタルのみ)
   - **QuickAssist Technology (QAT)**: 暗号化、圧縮、キュー管理の高速化 (ベアメタルのみ)

3. **豊富なインスタンスサイズ**
   - 11 サイズを提供 (large から 48xlarge)
   - 2 つのベアメタルサイズ (metal-24xl、metal-48xl)
   - 最大 192 vCPU、768 GiB メモリ

4. **高性能インターフェース**
   - DDR5 メモリによる高帯域幅
   - 最大 50 Gbps のネットワーク帯域幅
   - 最大 40 Gbps の EBS 帯域幅
   - 最大 128 EBS ボリュームのアタッチが可能
   - 48xlarge および metal-48xl サイズで EFA をサポート

## 技術仕様

### M7i インスタンスの主要仕様

| 項目 | 詳細 |
|------|------|
| プロセッサ | カスタム第 4 世代 Intel Xeon Scalable (Sapphire Rapids) |
| オールコアターボ周波数 | 3.2 GHz |
| 最大コアターボ周波数 | 3.8 GHz |
| メモリタイプ | DDR5 |
| vCPU : メモリ比率 | 1:4 |
| 最大ネットワーク帯域幅 | 50 Gbps |
| 最大 EBS 帯域幅 | 40 Gbps |
| 最大 EBS ボリューム数 | 128 |
| インスタンスストレージ | EBS のみ |
| 内蔵アクセラレータ | AMX、DSA、IAA、QAT |

### インスタンスサイズ一覧

| インスタンスサイズ | vCPU | メモリ (GiB) | ネットワーク帯域幅 (Gbps) | EBS 帯域幅 (Gbps) |
|-------------------|------|-------------|--------------------------|-------------------|
| m7i.large | 2 | 8 | 最大 12.5 | 最大 10 |
| m7i.xlarge | 4 | 16 | 最大 12.5 | 最大 10 |
| m7i.2xlarge | 8 | 32 | 最大 12.5 | 最大 10 |
| m7i.4xlarge | 16 | 64 | 最大 12.5 | 最大 10 |
| m7i.8xlarge | 32 | 128 | 12.5 | 10 |
| m7i.12xlarge | 48 | 192 | 18.75 | 15 |
| m7i.16xlarge | 64 | 256 | 25 | 20 |
| m7i.24xlarge | 96 | 384 | 37.5 | 30 |
| m7i.48xlarge | 192 | 768 | 50 | 40 |
| m7i.metal-24xl | 96 | 384 | 37.5 | 30 |
| m7i.metal-48xl | 192 | 768 | 50 | 40 |

### パフォーマンス比較

| 指標 | M7i vs M6i |
|------|-----------|
| パフォーマンス | 最大 15% 向上 (同等の x86 ベース Intel 比) |
| 価格パフォーマンス | 最大 15% 向上 |
| メモリ帯域幅 | DDR5 により向上 |
| Nitro System スループット | 他のクラウドプロバイダー比で 15% 以上向上 |

## 設定方法

### 前提条件

1. AWS アカウントとアフリカ (ケープタウン) リージョンへのアクセス権限
2. M7i インスタンスタイプのサービスクォータ確認
3. 適切な VPC およびサブネット設定

### 手順

#### ステップ 1: M7i インスタンスの起動

```bash
# AWS CLI を使用して M7i インスタンスを起動
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type m7i.4xlarge \
  --region af-south-1 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx \
  --key-name my-key-pair
```

アフリカ (ケープタウン) リージョン (af-south-1) で M7i インスタンスを起動するコマンドです。

#### ステップ 2: 利用可能なインスタンスタイプの確認

```bash
# 利用可能な M7i インスタンスタイプを確認
aws ec2 describe-instance-types \
  --filters "Name=instance-type,Values=m7i.*" \
  --region af-south-1 \
  --query "InstanceTypes[].{Type:InstanceType,vCPU:VCpuInfo.DefaultVCpus,Memory:MemoryInfo.SizeInMiB}" \
  --output table
```

ケープタウンリージョンで利用可能な M7i インスタンスタイプとスペックを一覧表示するコマンドです。

#### ステップ 3: 購入オプションの選択

M7i インスタンスは、以下の購入オプションで利用できます。

- **オンデマンドインスタンス**: 使用した分だけ支払い
- **Savings Plans**: 1 年または 3 年のコミットメントで割引
- **スポットインスタンス**: 未使用の EC2 容量を大幅な割引で利用

## メリット

### ビジネス面

- **リージョン拡大**: アフリカ (ケープタウン) リージョンのユーザーが最新世代の Intel ベース汎用インスタンスにアクセス可能
- **コスト効率の向上**: M6i と比較して最大 15% 優れた価格パフォーマンスにより、汎用ワークロードのコストを削減
- **柔軟なサイジング**: 11 サイズ + 2 ベアメタルサイズにより、ワークロードに最適なインスタンスを選択可能

### 技術面

- **AWS 専用プロセッサ**: 他のクラウドプロバイダーでは利用できないカスタム Intel Xeon Scalable プロセッサにより、最高のパフォーマンスを提供
- **内蔵アクセラレータ**: AMX による CPU ベース ML の高速化、ベアメタルでの DSA、IAA、QAT による専門的なワークロードの最適化
- **高ネットワーク帯域幅**: 最大 50 Gbps のネットワーク帯域幅と 40 Gbps の EBS 帯域幅
- **AWS Nitro System**: 最新の Nitro System によりセキュリティとパフォーマンスを最適化

## デメリット・制約事項

### 制限事項

- DSA、IAA、QAT アクセラレータはベアメタルサイズ (metal-24xl、metal-48xl) でのみ利用可能
- EFA ネットワーキングは 48xlarge および metal-48xl サイズでのみサポート
- 新規リージョンでの初期のサービスクォータが制限される場合がある

### 考慮すべき点

- M7i-flex インスタンスがこのリージョンで利用可能かは別途確認が必要
- リソースを完全に活用しないワークロードの場合は、M7i-flex インスタンスの方がコスト効率が良い場合がある
- 既存のインスタンスからの移行時には、パフォーマンステストを実施して期待される改善を確認することを推奨

## ユースケース

### ユースケース 1: ゲームサーバー

**シナリオ**: アフリカ地域のプレイヤーに低レイテンシーのゲーム体験を提供するために、ゲームサーバーをケープタウンリージョンで実行したい。

**実装例**:
```bash
# M7i インスタンスでゲームサーバーを起動
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type m7i.8xlarge \
  --region af-south-1 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx
```

**効果**: カスタム Intel Xeon Scalable プロセッサによる高いシングルスレッドパフォーマンスと、ケープタウンリージョンへの近接性により、アフリカ地域のプレイヤーに対して低レイテンシーのゲーム体験を提供できる。

### ユースケース 2: CPU ベース機械学習

**シナリオ**: AMX アクセラレータを活用して、CPU ベースの機械学習推論を実行したい。

**実装例**:
```bash
# M7i インスタンスで ML 推論サーバーを起動
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type m7i.24xlarge \
  --region af-south-1 \
  --iam-instance-profile Name=ML-Inference-Role
```

**効果**: AMX アクセラレータにより行列乗算操作が高速化され、CPU ベースの機械学習推論パフォーマンスが向上する。データをアフリカリージョンに保持しながら ML ワークロードを実行できる。

### ユースケース 3: 動画ストリーミングとエンコーディング

**シナリオ**: アフリカ地域の視聴者向けに、動画のトランスコーディングとストリーミング配信をケープタウンリージョンで実行したい。

**実装例**:
```bash
# M7i インスタンスで動画処理サーバーを起動
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type m7i.16xlarge \
  --region af-south-1 \
  --block-device-mappings file://storage-config.json
```

**効果**: M6i と比較して最大 15% のパフォーマンス向上により、動画のトランスコーディング処理が高速化され、視聴者へのコンテンツ配信が迅速化される。

## 料金

M7i インスタンスは、オンデマンドインスタンス、Savings Plans、スポットインスタンスで購入可能です。料金はリージョンとインスタンスサイズによって異なります。

詳細な料金については、[Amazon EC2 料金ページ](https://aws.amazon.com/ec2/pricing/) を参照してください。

## 利用可能リージョン

M7i インスタンスは、今回のアップデートでアフリカ (ケープタウン) リージョンが追加されました。

**新規対応リージョン (2026 年 2 月 19 日)**:
- アフリカ (ケープタウン) - af-south-1

最新のリージョン情報は [AWS Regional Services List](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) を参照してください。

## 関連サービス・機能

- **Amazon EC2 M7i-flex インスタンス**: リソースを完全に活用しないワークロードに最適な柔軟な汎用インスタンス
- **Amazon EC2 M7g インスタンス**: AWS Graviton3 ベースの汎用インスタンス
- **Amazon EC2 Auto Scaling**: M7i インスタンスの自動スケーリング
- **AWS Savings Plans**: M7i インスタンスのコスト削減オプション
- **Amazon CloudWatch**: M7i インスタンスのパフォーマンスメトリクス監視

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260219-amazon-ec2-m7i-africa-cape-town-regions.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-ec2-m7i-africa-cape-town-regions/)
- [Amazon EC2 M7i インスタンスタイプ](https://aws.amazon.com/ec2/instance-types/m7i/)
- [Amazon EC2 料金ページ](https://aws.amazon.com/ec2/pricing/)
- [Amazon EC2 ドキュメント](https://docs.aws.amazon.com/ec2/)

## まとめ

Amazon EC2 M7i インスタンスがアフリカ (ケープタウン) リージョンで利用可能になりました。AWS 専用のカスタム第 4 世代 Intel Xeon Scalable プロセッサ (Sapphire Rapids) を搭載し、同等の x86 ベース Intel プロセッサと比較して最大 15% 優れたパフォーマンスを提供します。11 サイズと 2 つのベアメタルサイズを提供し、ゲームサーバー、CPU ベースの ML、動画ストリーミングなどのワークロードに最適です。内蔵 Intel アクセラレータ (DSA、IAA、QAT) をベアメタルサイズで利用でき、専門的なワークロードの最適化が可能です。アフリカ地域で汎用ワークロードを実行している場合は、M7i インスタンスの活用を検討してください。
