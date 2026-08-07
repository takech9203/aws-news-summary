# AWS Parallel Computing Service - FedRAMP、SOC、ISO、CSA STAR、PCI のコンプライアンス対象に追加

**リリース日**: 2026 年 8 月 7 日
**サービス**: AWS Parallel Computing Service (AWS PCS)
**機能**: セキュリティ・コンプライアンス認証の対象範囲拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260807-aws-pcs-august.html)

## 概要

AWS Parallel Computing Service (AWS PCS) が、FedRAMP、SOC、ISO、CSA STAR、PCI といった主要なセキュリティ・コンプライアンスプログラムの対象範囲に追加されました。AWS PCS は、Slurm を使用して AWS 上でハイパフォーマンスコンピューティング (HPC) ワークロードの実行とスケーリングを簡素化するマネージドサービスです。

今回の発表により、FedRAMP Class C (旧称 Moderate ベースライン) が米国東部 (オハイオ)、米国東部 (バージニア北部)、米国西部 (オレゴン) の各リージョンで、FedRAMP Class D (旧称 High ベースライン) が AWS GovCloud (US) リージョンで利用可能になりました。さらに、SOC 1/2/3 レポートへの追加、ISO 認証、CCM 4.0 に基づく CSA STAR 認証、PCI DSS および PCI 3DS 準拠証明への追加が行われ、HIPAA 対象サービスにもなっています。

このアップデートにより、米国連邦政府機関、公共部門、金融・医療などの規制産業の組織が、厳格なガバナンス・コンプライアンス要件を満たしながら、機密性の高いミッションクリティカルな HPC ワークロードを AWS PCS で実行できるようになります。

**アップデート前の課題**

以前は AWS PCS が主要なコンプライアンスプログラムの対象外であったため、以下の課題がありました。

- FedRAMP 認証が必須の米国連邦政府機関や公共部門は、AWS PCS を機密ワークロードに採用できなかった
- SOC レポートや ISO 認証の対象外であったため、規制産業の企業は監査要件を満たす証跡として AWS PCS を位置づけられなかった
- PCI DSS 準拠が必要な決済関連ワークロードや、HIPAA 準拠が必要な医療データを扱う HPC ワークロードで AWS PCS を利用することが困難だった

**アップデート後の改善**

今回のアップデートにより、以下が可能になりました。

- FedRAMP Class C / Class D 環境での機密 HPC ワークロードの実行が可能になった
- SOC 1/2/3 レポートにより、統制の有効性について独立した第三者による保証を得られるようになった
- ISO 認証、CSA STAR 認証 (CCM 4.0)、PCI DSS / PCI 3DS 準拠証明、HIPAA 対象化により、幅広い規制要件下で AWS PCS を採用できるようになった

## サービスアップデートの詳細

### 主要なコンプライアンス対応

1. **FedRAMP (連邦リスク認可管理プログラム)**
   - FedRAMP Class C (旧称 Moderate ベースライン): 米国東部 (オハイオ)、米国東部 (バージニア北部)、米国西部 (オレゴン) で利用可能
   - FedRAMP Class D (旧称 High ベースライン): AWS GovCloud (US) リージョンで利用可能
   - 米国連邦政府機関および政府向けサービスを提供する事業者が対象

2. **SOC (System and Organization Controls)**
   - SOC 1、SOC 2、SOC 3 の各レポートに AWS PCS が含まれるようになった
   - 統制の有効性に関する独立した第三者機関による保証を提供
   - 財務報告やセキュリティ・可用性・機密性に関する監査要件に対応

3. **ISO 認証**
   - 国際標準化機構 (ISO) の認証取得
   - 国際的なセキュリティマネジメント基準への準拠を証明

4. **CSA STAR 認証**
   - Cloud Security Alliance の Security, Trust & Assurance Registry (STAR) 認証を取得
   - Cloud Controls Matrix (CCM) 4.0 に基づく認証

5. **PCI 準拠**
   - PCI DSS (Payment Card Industry Data Security Standard) 準拠証明に追加
   - PCI 3DS (3-D Secure) 準拠証明にも追加
   - クレジットカード決済関連データを扱うワークロードで利用可能

6. **HIPAA 対象サービス**
   - HIPAA (医療保険の相互運用性と説明責任に関する法律) の対象サービスに追加
   - 保護対象保健情報 (PHI) を扱う医療・ライフサイエンス分野の HPC ワークロードで利用可能

## 技術仕様

### コンプライアンスプログラム対応状況

| プログラム | 対応内容 | 対象リージョン |
|------|------|------|
| FedRAMP Class C (旧 Moderate) | 認可取得 | us-east-2、us-east-1、us-west-2 |
| FedRAMP Class D (旧 High) | 認可取得 | AWS GovCloud (US) リージョン |
| SOC 1/2/3 | レポート対象に追加 | - |
| ISO | 認証取得 | - |
| CSA STAR | CCM 4.0 に基づく認証取得 | - |
| PCI DSS / PCI 3DS | 準拠証明に追加 | - |
| HIPAA | 対象サービスに追加 | - |

## 設定方法

### 前提条件

1. AWS アカウント (FedRAMP Class D 要件の場合は AWS GovCloud (US) アカウント)
2. AWS PCS を利用するための IAM 権限
3. HIPAA 対象ワークロードの場合は、AWS との事業提携契約 (BAA) の締結

### 手順

#### ステップ 1: コンプライアンス対象状況の確認

[AWS Services in Scope by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/) ページで、AWS PCS が必要なコンプライアンスプログラムの対象であることを確認します。

#### ステップ 2: コンプライアンスレポートの取得

```bash
# AWS Artifact でレポート一覧を確認
aws artifact list-reports --region us-east-1
```

AWS Artifact コンソールまたは CLI を使用して、SOC レポートや PCI 準拠証明 (AOC) などの監査資料をダウンロードし、組織内の監査・調達プロセスに活用します。

#### ステップ 3: 対象リージョンでのクラスター作成

```bash
# 例: FedRAMP Class C 対象リージョン (us-east-2) でクラスターを作成
aws pcs create-cluster \
  --region us-east-2 \
  --cluster-name my-compliant-hpc-cluster \
  --scheduler type=SLURM,version=24.05 \
  --size SMALL \
  --networking subnetIds=subnet-xxxxxxxx,securityGroupIds=sg-xxxxxxxx
```

コンプライアンス要件に対応したリージョンを選択して AWS PCS クラスターを作成します。上記コマンドは、Slurm スケジューラーを使用する小規模クラスターを us-east-2 リージョンに作成する例です。

## メリット

### ビジネス面

- **公共部門での採用が可能に**: FedRAMP 認可により、米国連邦政府機関や政府関連プロジェクトで AWS PCS を利用した HPC 環境の構築が可能になる
- **監査対応の効率化**: SOC レポートや PCI 準拠証明を AWS Artifact から取得でき、監査・調達プロセスにおけるエビデンス収集の負担が軽減される
- **規制産業での利用拡大**: 金融 (PCI)、医療 (HIPAA) などの規制産業で、機密データを扱う HPC ワークロードを AWS PCS に移行する道が開かれる

### 技術面

- **マネージド HPC とコンプライアンスの両立**: Slurm クラスターの構築・運用を AWS に任せながら、コンプライアンス要件を満たす環境を利用できる
- **オンプレミス HPC からの移行促進**: コンプライアンス上の理由でオンプレミスに留まっていた HPC ワークロードのクラウド移行が容易になる
- **GovCloud での高セキュリティ運用**: FedRAMP Class D 相当の要件を持つワークロードを AWS GovCloud (US) 上の AWS PCS で実行できる

## デメリット・制約事項

### 制限事項

- FedRAMP Class C の対象は米国内の 3 リージョン (us-east-2、us-east-1、us-west-2) に限定される
- FedRAMP Class D の対象は AWS GovCloud (US) リージョンのみ
- コンプライアンス対応は AWS 側のインフラ・サービス統制に関するものであり、ワークロード側の準拠は利用者の責任 (責任共有モデル)

### 考慮すべき点

- HIPAA 対象ワークロードを実行する場合は、事前に AWS と事業提携契約 (BAA) を締結する必要がある
- PCI DSS 準拠には、AWS PCS 上で動作するアプリケーションや運用プロセスを含めた全体での準拠評価が必要
- FedRAMP の認可境界や最新の対象状況は、AWS Services in Scope ページで随時確認することが推奨される

## ユースケース

### ユースケース 1: 連邦政府機関の科学技術計算

**シナリオ**: 米国連邦政府機関が、気象シミュレーションや物理解析などの科学技術計算を FedRAMP 準拠環境で実行する必要がある。

**実装例**:
```
1. us-east-1 (FedRAMP Class C) または AWS GovCloud (US) (Class D) を選択
2. AWS PCS で Slurm クラスターを作成
3. 機関のセキュリティ統制に合わせて IAM、VPC、暗号化を構成
4. 既存の Slurm ジョブスクリプトをそのまま移行して実行
```

**効果**: FedRAMP 認可要件を満たしながら、オンプレミス HPC と同等の Slurm ベースのワークフローをクラウドで実現できる。

### ユースケース 2: 製薬企業の創薬シミュレーション

**シナリオ**: 製薬企業が、患者データを含む創薬研究の分子動力学シミュレーションを HIPAA 準拠環境で実行したい。

**実装例**:
```
1. AWS と BAA を締結
2. AWS PCS クラスターを作成し、保存時・転送時の暗号化を設定
3. PHI を含むデータセットを暗号化された FSx for Lustre などに配置
4. Slurm ジョブとしてシミュレーションを大規模並列実行
```

**効果**: HIPAA 対象サービスとしての AWS PCS を活用し、コンプライアンスを維持しながら創薬研究の計算リソースを柔軟にスケールできる。

### ユースケース 3: 金融機関のリスク計算

**シナリオ**: 金融機関が、決済カードデータ環境に関連するリスク計算・不正検知モデルのバッチ処理を PCI DSS 準拠環境で実行する。

**実装例**:
```
1. PCI DSS 準拠証明 (AOC) を AWS Artifact から取得し、監査部門と共有
2. AWS PCS クラスターをセグメント化された VPC 内に構築
3. モンテカルロシミュレーションなどのリスク計算ジョブを Slurm で実行
4. CloudTrail / CloudWatch で監査ログを集約
```

**効果**: PCI DSS の統制要件を満たすインフラ上で、大規模なリスク計算を効率的に処理できる。

## 料金

今回のアップデートはコンプライアンス対象範囲の拡大であり、追加料金は発生しません。AWS PCS の料金は従来どおり、クラスターのコントローラーサイズに応じた時間課金と、コンピュートノードとして使用する EC2 インスタンスなどの関連リソース料金で構成されます。

詳細は [AWS PCS 料金ページ](https://aws.amazon.com/pcs/pricing/) を参照してください。

## 利用可能リージョン

- **FedRAMP Class C (旧 Moderate)**: 米国東部 (オハイオ)、米国東部 (バージニア北部)、米国西部 (オレゴン)
- **FedRAMP Class D (旧 High)**: AWS GovCloud (US) リージョン
- SOC、ISO、CSA STAR、PCI、HIPAA の対象範囲は、AWS のコンプライアンスプログラムごとの対象サービスページで確認できます

## 関連サービス・機能

- **AWS GovCloud (US)**: FedRAMP Class D 相当の要件を持つワークロード向けの分離されたリージョン。AWS PCS を高セキュリティ環境で利用可能
- **AWS Artifact**: SOC レポートや PCI 準拠証明などの監査資料をセルフサービスでダウンロードできるサービス
- **AWS ParallelCluster**: セルフマネージド型の HPC クラスター管理ツール。マネージドサービスである AWS PCS との使い分けが可能
- **Amazon FSx for Lustre**: HPC ワークロード向けの高性能ファイルシステム。AWS PCS クラスターの共有ストレージとして利用される

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260807-aws-pcs-august.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/08/aws-pcs-august/)
- [AWS PCS 製品ページ](https://aws.amazon.com/pcs/)
- [AWS PCS ドキュメント](https://docs.aws.amazon.com/pcs/latest/userguide/what-is-service.html)
- [FedRAMP 対象サービス一覧](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/)
- [SOC 対象サービス一覧](https://aws.amazon.com/compliance/services-in-scope/SOC/)
- [ISO 認証](https://aws.amazon.com/compliance/iso-certified/)
- [PCI 対象サービス一覧](https://aws.amazon.com/compliance/services-in-scope/PCI/)
- [HIPAA 対象サービス一覧](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/)

## まとめ

AWS PCS が FedRAMP、SOC、ISO、CSA STAR、PCI の各コンプライアンスプログラムの対象となり、HIPAA 対象サービスにも追加されたことで、公共部門や規制産業における機密 HPC ワークロードの実行基盤として採用できるようになりました。コンプライアンス要件によりオンプレミス HPC を維持してきた組織は、AWS Artifact で監査資料を確認した上で、AWS PCS への移行を検討することを推奨します。
