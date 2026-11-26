# Amazon EC2 - C9gd インスタンスが欧州 (アイルランド、スペイン) リージョンで利用可能に

**リリース日**: 2026 年 11 月 25 日
**サービス**: Amazon Elastic Compute Cloud (Amazon EC2)
**機能**: AWS Graviton5 プロセッサ搭載 C9gd インスタンスのリージョン拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261125-amazon-ec2-c9gd-instances-additional-regions.html)

## 概要

AWS Graviton5 プロセッサを搭載した Amazon EC2 C9gd インスタンスが、欧州 (アイルランド) および欧州 (スペイン) リージョンで新たに利用可能になりました。Graviton5 は AWS がカスタム設計した第 5 世代 CPU であり、コンピューティング負荷の高いワークロードに対して Amazon EC2 上で最高のコストパフォーマンスを提供します。

C9gd インスタンスは、Graviton4 ベースの C8gd インスタンスと比較して最大 25% 高いコンピューティング性能を実現し、データベースで最大 30%、Web アプリケーションで最大 35%、機械学習で最大 35% の高速化を達成します。第 6 世代 AWS Nitro System 上に構築されており、Nitro Isolation Engine を初めて搭載した世代のインスタンスです。Nitro Isolation Engine は形式的検証 (formal verification) を活用し、お客様のワークロードが相互に、および AWS オペレーターから分離されていることを保証します。

C9gd インスタンスはローカル NVMe ベースの SSD ブロックレベルストレージを備えており、スクラッチ領域、一時ファイル、キャッシュなど高速かつ低レイテンシーなローカルストレージを必要とするワークロードに適しています。HPC、バッチ処理、ゲーミング、動画エンコーディング、科学技術モデリング、分散分析、CPU ベースの機械学習 (ML) 推論、リアルタイム分析、広告配信などの用途が想定されています。

**アップデート前の課題**

- C9gd インスタンスは欧州 (アイルランド、スペイン) リージョンで提供されておらず、これらのリージョンのワークロードで Graviton5 とローカル NVMe ストレージの組み合わせを活用できなかった
- 欧州のデータレジデンシー要件や低レイテンシー要件のあるワークロードでは、他リージョンの C9gd を利用しにくかった
- 欧州 (アイルランド、スペイン) では Graviton4 ベースの C8gd が最新の選択肢であり、さらなるコストパフォーマンス向上の余地があった

**アップデート後の改善**

- 欧州 (アイルランド) および欧州 (スペイン) リージョンで C9gd インスタンスを起動できるようになり、C8gd 比で最大 25% の性能向上を活用可能になった
- 欧州内でデータを保持したまま、ローカル NVMe SSD を必要とするコンピューティング集約型ワークロードを Graviton5 で実行できるようになった
- Nitro Isolation Engine による形式的検証に基づく分離保証を、両リージョンのワークロードでも利用可能になった

## サービスアップデートの詳細

### 主要機能

1. **欧州 2 リージョンでの提供開始**
   - AWS Graviton5 搭載の C9gd インスタンスが欧州 (アイルランド) および欧州 (スペイン) リージョンで利用可能に
   - 欧州のユーザーやシステムに近い場所で、低レイテンシーを維持しながら Graviton5 の性能を活用できる
   - Savings Plans、オンデマンド、スポットインスタンス、Dedicated Instances、Dedicated Hosts で購入可能

2. **AWS Graviton5 プロセッサによる性能向上**
   - C8gd 比でコンピューティング性能が最大 25% 向上
   - データベースで最大 30%、Web アプリケーションで最大 35%、機械学習で最大 35% 高速化
   - コンピューティング負荷の高いワークロードで Amazon EC2 上最高のコストパフォーマンスを提供

3. **Nitro Isolation Engine**
   - 第 6 世代 AWS Nitro System 上に構築され、Nitro Isolation Engine を初めて搭載
   - 形式的検証により、ワークロードが相互に、および AWS オペレーターから分離されていることを保証

4. **ローカル NVMe ストレージ**
   - スクラッチ領域、一時ファイル、キャッシュ向けの高速・低レイテンシーなローカル NVMe SSD ブロックレベルストレージを提供

## 技術仕様

### C9gd インスタンスのサイズ構成

| サイズ | vCPU | メモリ (GiB) | ローカル NVMe ストレージ | ネットワーク帯域 (Gbps) | EBS 帯域 (Gbps) |
|------|------|------|------|------|------|
| medium | 1 | 2 | 1 x 59 GB | 最大 15 | 最大 12 |
| large | 2 | 4 | 1 x 118 GB | 最大 15 | 最大 12 |
| xlarge | 4 | 8 | 1 x 237 GB | 最大 15 | 最大 12 |
| 2xlarge | 8 | 16 | 1 x 474 GB | 最大 17 | 最大 12 |
| 4xlarge | 16 | 32 | 1 x 950 GB | 最大 17 | 最大 12 |
| 8xlarge | 32 | 64 | 1 x 1900 GB | 17 | 12 |
| 12xlarge | 48 | 96 | 3 x 950 GB | 25 | 18 |
| 16xlarge | 64 | 128 | 1 x 3800 GB | 34 | 24 |
| 24xlarge | 96 | 192 | 3 x 1900 GB | 50 | 36 |
| 48xlarge | 192 | 384 | 3 x 3800 GB | 100 | 72 |
| metal-48xl | 192 | 384 | 3 x 3800 GB | 100 | 72 |

### 購入オプション

| 項目 | 詳細 |
|------|------|
| 購入モデル | Savings Plans、オンデマンド、スポットインスタンス、Dedicated Instances、Dedicated Hosts |
| ストレージ | ローカル NVMe SSD + Amazon EBS |
| Nitro System | 第 6 世代 (Nitro Isolation Engine 搭載) |
| プロセッサ | AWS Graviton5 (第 5 世代カスタム設計 Arm CPU) |

## 設定方法

### 前提条件

1. AWS アカウントを保有し、欧州 (アイルランド: eu-west-1) または欧州 (スペイン: eu-south-2) リージョンで EC2 インスタンスを起動できる IAM 権限があること
2. Arm64 (aarch64) アーキテクチャに対応した AMI を使用すること
3. 必要に応じて、対象アプリケーションが Arm アーキテクチャで動作することを事前に検証しておくこと

### 手順

#### ステップ 1: 利用可能なインスタンスタイプを確認する

```bash
aws ec2 describe-instance-type-offerings \
  --region eu-west-1 \
  --filters "Name=instance-type,Values=c9gd.*" \
  --query "InstanceTypeOfferings[].InstanceType" \
  --output table
```

欧州 (アイルランド) リージョンで提供されている C9gd のインスタンスサイズの一覧を取得します。欧州 (スペイン) を確認する場合は `--region eu-south-2` を指定します。

#### ステップ 2: Arm64 対応の AMI を確認する

```bash
aws ec2 describe-images \
  --region eu-west-1 \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-arm64" "Name=state,Values=available" \
  --query "sort_by(Images, &CreationDate)[-1].{ImageId:ImageId,Name:Name}" \
  --output table
```

対象リージョンで利用可能な最新の Arm64 版 Amazon Linux 2023 AMI を検索します。

#### ステップ 3: C9gd インスタンスを起動する

```bash
aws ec2 run-instances \
  --region eu-west-1 \
  --instance-type c9gd.xlarge \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --key-name my-key-pair \
  --subnet-id subnet-xxxxxxxx \
  --security-group-ids sg-xxxxxxxx
```

ステップ 2 で確認した Arm64 対応 AMI を指定し、欧州 (アイルランド) リージョンで c9gd.xlarge インスタンスを起動します。起動後、ローカル NVMe SSD はインスタンスストアボリュームとして認識されるため、必要に応じてフォーマットしてマウントします。

## メリット

### ビジネス面

- **欧州ワークロードのコストパフォーマンス向上**: C8gd 比で最大 25% の性能向上により、同一ワークロードをより少ないリソースで実行し、コストを削減できる
- **データレジデンシー要件への対応**: 欧州 (アイルランド、スペイン) 内でデータを保持したまま、最新世代の Graviton5 インスタンスを利用できる
- **柔軟な購入オプション**: Savings Plans やスポットインスタンスなど複数の購入モデルにより、コスト最適化の選択肢が広い

### 技術面

- **ワークロード別の大幅な高速化**: データベースで最大 30%、Web アプリケーションで最大 35%、機械学習で最大 35% の高速化を実現
- **形式的検証に基づく分離**: Nitro Isolation Engine により、ワークロード間および AWS オペレーターからの分離を保証
- **ローカル NVMe による低レイテンシー**: スクラッチ領域や一時ファイル、キャッシュ用途で高速なローカルストレージを利用可能

## デメリット・制約事項

### 制限事項

- Arm アーキテクチャ (AWS Graviton) ベースであるため、x86 依存のバイナリや商用ソフトウェアは Arm 向けのビルド・ライセンス確認・検証が必要
- 本発表は C9gd インスタンスのリージョン拡大であり、追加された欧州リージョンは今回発表のアイルランドとスペインの 2 つ

### 考慮すべき点

- ローカル NVMe ストレージはインスタンス停止・終了時にデータが失われるため、永続化が必要なデータには Amazon EBS や Amazon S3 を併用する
- 既存の C8gd や x86 ベースワークロードから移行する場合は、性能・互換性の検証を事前に実施することが推奨される
- 新しいインスタンスファミリーはリージョンやアベイラビリティーゾーンによって在庫状況が異なる場合があるため、大規模利用時はキャパシティの確保方法 (オンデマンドキャパシティ予約など) を検討する

## ユースケース

### ユースケース 1: 欧州向け動画エンコーディング / メディア処理

**シナリオ**: 一時ファイルや中間データを多用する動画トランスコードパイプラインを欧州 (アイルランド) リージョンで運用しているメディア企業。

**実装例**:
```
AWS Batch のコンピューティング環境に c9gd インスタンスを指定し、
ローカル NVMe SSD をスクラッチ領域としてマウントして処理する
```

**効果**: ローカル NVMe SSD への高速な読み書きにより、パイプライン全体の処理時間を短縮できます。スポットインスタンスと組み合わせることでコストをさらに抑制できます。

### ユースケース 2: ログ処理・リアルタイム分析基盤

**シナリオ**: 欧州 (スペイン) リージョンで大量のログを集約・加工し、リアルタイム分析を行っている事業者。中間データの書き込み速度がボトルネックになっている。

**実装例**:
```
分析クラスターのノードを c8gd から c9gd に変更し、
ローカル NVMe をシャッフル領域・キャッシュとして利用して性能を比較検証する
```

**効果**: C8gd 比で最大 25% の性能向上とローカル NVMe の低レイテンシーにより、同一スループットをより少ないノード数で処理でき、分析レイテンシーの改善とコスト削減を両立できます。

### ユースケース 3: CPU ベースの ML 推論とキャッシュ活用

**シナリオ**: 欧州のユーザー向けに低レイテンシーの推論 API を提供しており、モデルファイルや特徴量キャッシュの読み込み高速化と推論コストの削減が課題となっているアプリケーション。

**実装例**:
```
Amazon ECS / Amazon EKS のノードグループに c9gd インスタンスを追加し、
モデルや特徴量キャッシュをローカル NVMe に配置した Arm64 対応コンテナをデプロイする
```

**効果**: 機械学習で最大 35% の高速化とローカル NVMe による高速なキャッシュアクセスにより、欧州ユーザー向けの低レイテンシーを維持しながら推論コストを削減できます。

## 料金

C9gd インスタンスは、Savings Plans、オンデマンド、スポットインスタンス、Dedicated Instances、Dedicated Hosts で購入できます。具体的な料金はリージョンおよびインスタンスサイズによって異なるため、欧州 (アイルランド、スペイン) リージョンの最新価格は Amazon EC2 の料金ページを参照してください。

## 利用可能リージョン

今回のアップデートにより、C9gd インスタンスが以下のリージョンで新たに利用可能になりました。

- 欧州 (アイルランド)
- 欧州 (スペイン)

C9gd は 2026 年 6 月の一般提供開始以降、米国東部 (バージニア北部、オハイオ)、米国西部 (オレゴン)、欧州 (フランクフルト)、アジアパシフィック (東京) などへ順次拡大しています。最新の提供リージョンは C9g / C9gd インスタンスの製品ページを参照してください。

## 関連サービス・機能

- **AWS Graviton**: C9gd を支える AWS カスタム設計 CPU ファミリー。第 5 世代の Graviton5 を搭載
- **AWS Nitro System**: 第 6 世代 Nitro System 上に構築。Nitro Isolation Engine による形式的検証ベースの分離を提供
- **Amazon EBS**: 永続化が必要なデータの保存先として、ローカル NVMe と併用するブロックストレージ
- **Amazon EC2 Savings Plans**: C9gd のコスト最適化に活用できる柔軟な料金モデル
- **Amazon EC2 Auto Scaling / AWS Batch**: C9gd を組み込んだスケーラブルなコンピューティング基盤の構築に活用

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261125-amazon-ec2-c9gd-instances-additional-regions.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-ec2-c9gd-instances-additional-regions/)
- [C9g / C9gd インスタンスの製品ページ](https://aws.amazon.com/ec2/instance-types/c9g/)
- [AWS Graviton](https://aws.amazon.com/ec2/graviton/level-up-with-graviton/)
- [AWS Nitro System](https://aws.amazon.com/ec2/nitro/)
- [Nitro Isolation Engine のブログ](https://aws.amazon.com/blogs/compute/aws-nitro-isolation-engine-formally-verifying-the-hypervisor-in-the-aws-nitro-system/)

## まとめ

AWS Graviton5 搭載の Amazon EC2 C9gd インスタンスが欧州 (アイルランド) および欧州 (スペイン) リージョンで利用可能になり、両リージョンのワークロードでも C8gd 比で最大 25% の性能向上と、ローカル NVMe SSD による低レイテンシーストレージ、Nitro Isolation Engine による分離保証を活用できるようになりました。欧州で C8gd や x86 ベースのコンピューティング最適化インスタンスを運用しているお客様は、C9gd への移行によるコストパフォーマンス改善の検証を推奨します。
