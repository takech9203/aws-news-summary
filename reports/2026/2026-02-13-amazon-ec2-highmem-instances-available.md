# Amazon EC2 - High Memory U7i インスタンスが追加リージョンで利用可能に

**リリース日**: 2026 年 02 月 13 日
**サービス**: Amazon EC2
**機能**: High Memory U7i インスタンスのリージョン拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260213-amazon-ec2-highmem-instances-available.html)

## 概要

AWS は 2026 年 2 月 13 日、Amazon EC2 High Memory U7i インスタンスが新たなリージョンで利用可能になったことを発表しました。U7i-6tb.112xlarge インスタンスが南米 (サンパウロ) およびヨーロッパ (ミラノ) リージョンに、U7i-12tb.224xlarge インスタンスが AWS GovCloud (US-East) リージョンに、U7in-16tb.224xlarge インスタンスがヨーロッパ (ロンドン) リージョンに追加されました。

U7i インスタンスは AWS 第 7 世代のインスタンスファミリーに属し、カスタム第 4 世代 Intel Xeon Scalable Processors (Sapphire Rapids) を搭載しています。DDR5 メモリを採用しており、U7i-6tb は 6TiB、U7i-12tb は 12TiB、U7in-16tb は 16TiB のメモリを提供します。これらのインスタンスは、SAP HANA、Oracle、SQL Server などのミッションクリティカルなインメモリデータベースに最適化されており、急速に成長するデータ環境においてトランザクション処理のスループットをスケールさせることができます。

**アップデート前の課題**

- 南米 (サンパウロ) およびヨーロッパ (ミラノ) リージョンでは U7i-6tb インスタンスが利用できず、6TiB メモリを必要とする大規模インメモリワークロードを地理的に近い場所で実行できなかった
- AWS GovCloud (US-East) リージョンでは U7i-12tb インスタンスが利用できず、12TiB メモリを必要とする米国政府関連のワークロードに対応できなかった
- ヨーロッパ (ロンドン) リージョンでは U7in-16tb インスタンスが利用できず、16TiB メモリと 200Gbps ネットワーク帯域幅を必要とするヨーロッパのワークロードに制約があった

**アップデート後の改善**

- 南米 (サンパウロ) およびヨーロッパ (ミラノ) リージョンで U7i-6tb インスタンスが利用可能になり、6TiB メモリのインメモリデータベースをこれらのリージョンで実行できるようになった
- AWS GovCloud (US-East) リージョンで U7i-12tb インスタンスが利用可能になり、米国政府機関向けの大規模インメモリワークロードに対応できるようになった
- ヨーロッパ (ロンドン) リージョンで U7in-16tb インスタンスが利用可能になり、16TiB メモリと最大 200Gbps のネットワーク帯域幅を活用した高性能ワークロードを実行できるようになった

## サービスアップデートの詳細

### 主要機能

1. **U7i-6tb.112xlarge インスタンス (サンパウロ、ミラノ)**
   - 448 vCPUs と 6TiB (6,144 GiB) の DDR5 メモリを提供
   - 最大 100Gbps の EBS 帯域幅をサポート
   - 最大 100Gbps のネットワーク帯域幅を提供
   - ENA Express をサポート

2. **U7i-12tb.224xlarge インスタンス (GovCloud US-East)**
   - 896 vCPUs と 12TiB (12,288 GiB) の DDR5 メモリを提供
   - 最大 100Gbps の EBS 帯域幅をサポート
   - 最大 100Gbps のネットワーク帯域幅を提供
   - ENA Express をサポート

3. **U7in-16tb.224xlarge インスタンス (ロンドン)**
   - 896 vCPUs と 16TiB (16,384 GiB) の DDR5 メモリを提供
   - 最大 100Gbps の EBS 帯域幅をサポート
   - 最大 200Gbps のネットワーク帯域幅を提供し、より高速なデータロードとバックアップを実現
   - ENA Express をサポート

## 技術仕様

### U7i インスタンスファミリーの仕様

今回のアップデートで追加された 3 つのインスタンスタイプの仕様は以下のとおりです。

| インスタンスタイプ | vCPU | メモリ (GiB) | ストレージ | ネットワーク帯域幅 (Gbps) | EBS 帯域幅 (Gbps) |
|-------------------|------|-------------|-----------|--------------------------|-------------------|
| u7i-6tb.112xlarge | 448 | 6,144 | EBS のみ | 100 | 100 |
| u7i-12tb.224xlarge | 896 | 12,288 | EBS のみ | 100 | 100 |
| u7in-16tb.224xlarge | 896 | 16,384 | EBS のみ | 200 | 100 |

### U7i インスタンスファミリー全体の仕様

U7i インスタンスファミリーには、以下のインスタンスタイプが含まれています。

| インスタンスタイプ | vCPU | メモリ (TiB) | ネットワーク帯域幅 (Gbps) | EBS 帯域幅 (Gbps) |
|-------------------|------|-------------|--------------------------|-------------------|
| u7i-6tb.112xlarge | 448 | 6 | 100 | 100 |
| u7i-8tb.112xlarge | 448 | 8 | 100 | 100 |
| u7i-12tb.224xlarge | 896 | 12 | 100 | 100 |
| u7in-16tb.224xlarge | 896 | 16 | 200 | 100 |
| u7in-24tb.224xlarge | 896 | 24 | 200 | 100 |
| u7in-32tb.224xlarge | 896 | 32 | 200 | 100 |
| u7inh-32tb.480xlarge | 1,920 | 32 | 200 | 160 |

### 主要な技術特性

| 項目 | 詳細 |
|------|------|
| プロセッサー | カスタム第 4 世代 Intel Xeon Scalable Processors (Sapphire Rapids) |
| メモリタイプ | DDR5 |
| AWS Nitro System | 対応 |
| ENA Express | 全 U7i インスタンスでサポート |
| SAP 認定 | U7i (6, 8, 12, 16, 24, 32TiB) で SAP HANA 認定取得済み |
| 既存 U-1 インスタンスとの比較 | コンピューティング性能最大 135% 向上、メモリ性能最大 115% 向上 |

## 設定方法

### 前提条件

1. AWS アカウントが有効化されている
2. 適切な IAM 権限 (ec2:RunInstances など) が設定されている
3. 対象リージョンで U7i インスタンスの利用が承認されている (High Memory インスタンスは事前にアカウントチームへの連絡が必要な場合がある)

### 手順

#### ステップ 1: 利用可能なインスタンスタイプを確認

```bash
# サンパウロリージョンで利用可能な U7i インスタンスタイプを確認
aws ec2 describe-instance-types \
  --filters "Name=instance-type,Values=u7i*" \
  --region sa-east-1 \
  --query "InstanceTypes[].{Type:InstanceType,vCPU:VCpuInfo.DefaultVCpus,Memory:MemoryInfo.SizeInMiB}" \
  --output table
```

このコマンドは、サンパウロリージョンで利用可能な U7i インスタンスタイプとそのスペック (vCPU 数、メモリサイズ) を表示します。

#### ステップ 2: インスタンスを起動

```bash
# U7i-6tb インスタンスをサンパウロリージョンで起動
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type u7i-6tb.112xlarge \
  --region sa-east-1 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx \
  --key-name my-key-pair
```

このコマンドは、サンパウロリージョン (sa-east-1) で U7i-6tb.112xlarge インスタンスを起動します。High Memory インスタンスは大量のリソースを使用するため、事前にサービスクォータの確認が推奨されます。

#### ステップ 3: インスタンスの状態を確認

```bash
# インスタンスの状態を確認
aws ec2 describe-instances \
  --instance-ids i-xxxxxxxxxxxxxxxxx \
  --region sa-east-1 \
  --query "Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}" \
  --output table
```

このコマンドは、起動したインスタンスの状態 (running, pending など) を確認します。

## メリット

### ビジネス面

- **データレジデンシー要件への対応**: 南米やヨーロッパのデータ主権要件に準拠しながら、大規模インメモリデータベースを現地リージョンで運用可能
- **レイテンシーの削減**: エンドユーザーに近いリージョンでインスタンスを実行することで、データベースアクセスのレイテンシーを低減
- **ガバメントクラウドの拡充**: GovCloud (US-East) での U7i-12tb 提供により、米国政府機関の大規模インメモリワークロードに対応

### 技術面

- **大容量メモリ**: 最大 16TiB の DDR5 メモリにより、大規模な SAP HANA データベースを単一インスタンスで実行可能
- **高速ネットワーク**: U7in-16tb は最大 200Gbps のネットワーク帯域幅を提供し、データロードとバックアップを高速化
- **ENA Express サポート**: 全インスタンスで ENA Express をサポートし、シングルフローのスループットを向上
- **高性能 EBS 接続**: 最大 100Gbps の EBS 帯域幅により、高速なストレージ I/O を実現

## デメリット・制約事項

### 制限事項

- High Memory インスタンスは専用ホスト上で実行されるため、起動前にアカウントチームへの連絡が必要な場合がある
- 全リージョンで全インスタンスタイプが利用可能ではなく、リージョンごとに利用可能なサイズが異なる
- 非常に大規模なインスタンスのため、オンデマンド料金が高額になる

### 考慮すべき点

- ワークロードに必要なメモリ容量を正確に見積もり、適切なインスタンスサイズを選択することが重要
- Savings Plans やリザーブドインスタンスを活用してコストを最適化することを検討
- インスタンスの起動には時間がかかる場合があるため、Capacity Reservations の活用を検討

## ユースケース

### ユースケース 1: 南米での SAP HANA 本番環境

**シナリオ**: ブラジルに拠点を持つ企業が、データレジデンシー要件に準拠しながら SAP HANA データベースをサンパウロリージョンで運用したい。

**実装例**:
```bash
# サンパウロリージョンで SAP HANA 向け U7i インスタンスを起動
aws ec2 run-instances \
  --instance-type u7i-6tb.112xlarge \
  --image-id ami-sap-hana-xxxxxxxxx \
  --region sa-east-1 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx \
  --key-name sap-key-pair \
  --block-device-mappings DeviceName=/dev/sda1,Ebs='{VolumeSize=1000,VolumeType=io2,Iops=64000}'
```

**効果**: 6TiB のメモリを活用して SAP HANA データベースを単一インスタンスで実行し、ブラジル国内のデータレジデンシー要件に準拠しながら低レイテンシーのアクセスを実現

### ユースケース 2: 米国政府機関の大規模データベース

**シナリオ**: 米国政府機関が、GovCloud 環境で 12TiB のメモリを必要とする大規模インメモリデータベースを運用したい。

**実装例**:
```bash
# GovCloud (US-East) で U7i-12tb インスタンスを起動
aws ec2 run-instances \
  --instance-type u7i-12tb.224xlarge \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --region us-gov-east-1 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx \
  --key-name govcloud-key-pair
```

**効果**: 12TiB のメモリと 896 vCPUs により、FedRAMP 準拠の環境でミッションクリティカルなインメモリデータベースを実行し、セキュリティとコンプライアンス要件を満たしながら高性能を実現

### ユースケース 3: ヨーロッパでの高帯域幅データ処理

**シナリオ**: 英国の金融機関が、16TiB メモリと 200Gbps のネットワーク帯域幅を活用して大規模なトランザクションデータベースを運用したい。

**実装例**:
```bash
# ロンドンリージョンで U7in-16tb インスタンスを起動
aws ec2 run-instances \
  --instance-type u7in-16tb.224xlarge \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --region eu-west-2 \
  --subnet-id subnet-xxxxxxxxxxxxxxxxx \
  --security-group-ids sg-xxxxxxxxxxxxxxxxx \
  --key-name london-key-pair
```

**効果**: 16TiB のメモリと 200Gbps のネットワーク帯域幅により、大規模なインメモリトランザクション処理を高速に実行し、データのロードやバックアップ時間を大幅に短縮

## 料金

U7i インスタンスの料金は、選択したインスタンスタイプ、リージョン、購入オプションによって異なります。High Memory インスタンスは専用ホスト上で実行されるため、通常のオンデマンド料金とは異なる料金体系が適用されます。詳細な料金については、[Amazon EC2 料金ページ](https://aws.amazon.com/ec2/pricing/) および AWS アカウントチームにお問い合わせください。

### 料金例

| インスタンスタイプ | メモリ | vCPU | 購入オプション |
|-------------------|--------|------|--------------|
| u7i-6tb.112xlarge | 6 TiB | 448 | オンデマンド、Savings Plans |
| u7i-12tb.224xlarge | 12 TiB | 896 | オンデマンド、Savings Plans |
| u7in-16tb.224xlarge | 16 TiB | 896 | オンデマンド、Savings Plans |

*料金は変動する可能性があります。最新の料金については [AWS 料金ページ](https://aws.amazon.com/ec2/pricing/)を参照してください。

## 利用可能リージョン

今回のアップデートで以下のリージョンに U7i インスタンスが追加されました。

**新規対応リージョン (2026 年 2 月 13 日)**:
- 南米 (サンパウロ) - sa-east-1: U7i-6tb.112xlarge
- ヨーロッパ (ミラノ) - eu-south-1: U7i-6tb.112xlarge
- AWS GovCloud (US-East) - us-gov-east-1: U7i-12tb.224xlarge
- ヨーロッパ (ロンドン) - eu-west-2: U7in-16tb.224xlarge

## 関連サービス・機能

- **Amazon EBS (io2 Block Express)**: U7i インスタンスと組み合わせて高性能なストレージ I/O を実現し、データハイドレーションやバックアップ/リストアを高速化
- **SAP HANA on AWS**: U7i インスタンスは SAP 認定を取得しており、SAP HANA の本番環境で利用可能
- **AWS Nitro System**: U7i インスタンスは AWS Nitro System 上に構築されており、高いパフォーマンスとセキュリティを提供
- **ENA Express**: 全 U7i インスタンスで ENA Express をサポートし、シングルフローのネットワークスループットを向上

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260213-amazon-ec2-highmem-instances-available.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-ec2-highmem-instances-available/)
- [U7i インスタンス製品ページ](https://aws.amazon.com/ec2/instance-types/u7i/)
- [Amazon EC2 料金ページ](https://aws.amazon.com/ec2/pricing/)
- [Amazon EC2 ドキュメント](https://docs.aws.amazon.com/ec2/)

## まとめ

Amazon EC2 High Memory U7i インスタンスが南米 (サンパウロ)、ヨーロッパ (ミラノ、ロンドン)、AWS GovCloud (US-East) の 4 つのリージョンに追加されたことにより、大規模インメモリデータベースをより多くの地域で実行できるようになりました。SAP HANA、Oracle、SQL Server などのミッションクリティカルなワークロードを、データレジデンシー要件に準拠しながら低レイテンシーで運用したい場合は、これらの新規リージョンでの U7i インスタンスの利用を検討してください。
