# Amazon EVS - FedRAMP Class C 認証範囲への追加

**リリース日**: 2026 年 9 月 21 日
**サービス**: Amazon Elastic VMware Service (Amazon EVS)
**機能**: FedRAMP Class C (旧 Moderate ベースライン) 認証範囲への追加

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260921-amazon-evs-fedramp-class-c.html)

## 概要

Amazon Elastic VMware Service (Amazon EVS) が、すべての米国リージョンにおいて FedRAMP Class C (旧 Moderate ベースライン) の認証範囲に追加されました。FedRAMP (Federal Risk and Authorization Management Program) は、クラウドサービスのセキュリティ評価、認証、継続的モニタリングに対する標準的なアプローチを提供する米国政府全体のプログラムです。

Amazon EVS は、VMware Cloud Foundation (VCF) ソフトウェアを Amazon VPC 内の EC2 ベアメタルインスタンス上で直接実行できるサービスです。完全な VCF 環境を数時間でセットアップでき、ワークロードを AWS へ迅速に移行することが可能です。今回の認証範囲追加により、FedRAMP Moderate 相当の準拠が求められる米国政府機関や関連組織が、VMware ワークロードを Amazon EVS 上で運用できるようになります。

**アップデート前の課題**

- FedRAMP Moderate 相当の準拠が必要な組織は、Amazon EVS を利用したワークロード移行を選択できなかった
- オンプレミスの VMware 環境を維持する必要があり、老朽化したインフラストラクチャの運用リスクやデータセンター退去期限への対応が課題だった

**アップデート後の改善**

- FedRAMP Class C (旧 Moderate ベースライン) 準拠が必要な組織が、すべての米国リージョンで Amazon EVS を利用可能になった
- 準拠要件を満たしながら、VMware ワークロードを AWS へ迅速に移行できるようになった

## サービスアップデートの詳細

### 主要ポイント

1. **FedRAMP Class C 認証範囲への追加**
   - Amazon EVS が FedRAMP Class C (旧 Moderate ベースライン) の認証範囲に追加された
   - すべての米国リージョンが対象
   - セキュリティ評価、認証、継続的モニタリングの標準的なアプローチに準拠

2. **Amazon EVS の特徴**
   - 最新の VMware Cloud Foundation (VCF) ソフトウェアを Amazon VPC 内で直接実行
   - EC2 ベアメタルインスタンス上で動作
   - 完全な VCF 環境を数時間でセットアップ可能

3. **政府機関向けワークロード移行の促進**
   - 老朽化したインフラストラクチャの廃止を支援
   - 運用リスクの低減とデータセンター退去期限への対応が可能

## 技術仕様

### 認証範囲の概要

| 項目 | 詳細 |
|------|------|
| 対象サービス | Amazon Elastic VMware Service (Amazon EVS) |
| 準拠プログラム | FedRAMP Class C (旧 Moderate ベースライン) |
| 対象リージョン | すべての米国リージョン |
| 基盤技術 | VMware Cloud Foundation (VCF)、EC2 ベアメタルインスタンス |

## メリット

### ビジネス面

- **準拠要件への対応**: FedRAMP Moderate 相当の準拠が求められる米国政府機関や関連組織が Amazon EVS を採用可能になった
- **移行期限への対応**: データセンター退去期限を控えた組織が、準拠を維持しながら迅速に移行できる
- **運用リスクの低減**: 老朽化したオンプレミスインフラストラクチャからの脱却により運用リスクを削減できる

### 技術面

- **既存スキルの活用**: VMware の運用スキルやツールをそのまま活用しながら AWS 上で運用できる
- **迅速な環境構築**: 完全な VCF 環境を数時間でセットアップ可能
- **AWS ネイティブ統合**: Amazon VPC 内で動作するため、AWS の各種サービスとの連携が容易

## デメリット・制約事項

### 考慮すべき点

- 今回の発表は米国リージョンにおける準拠範囲の追加であり、米国以外のリージョンには適用されない
- FedRAMP 準拠が必要なワークロードを展開する際は、[FedRAMP 対応サービス一覧](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/)で最新の認証状況を確認する必要がある
- 準拠はサービス側の認証範囲を示すものであり、ワークロード全体の準拠には利用者側の責任範囲での対応も必要 (責任共有モデル)

## ユースケース

### ユースケース1: 米国政府機関の VMware ワークロード移行

**シナリオ**: FedRAMP Moderate 相当の準拠が必要な米国政府機関が、データセンター退去期限までにオンプレミスの VMware 環境を移行したい。

**効果**: Amazon EVS の FedRAMP Class C 準拠により、既存の VMware 運用手法を維持したまま、準拠要件を満たしつつ短期間で AWS へ移行できる。

### ユースケース2: 政府関連 SaaS プロバイダーの基盤刷新

**シナリオ**: 政府機関向けにサービスを提供する事業者が、FedRAMP 準拠を維持しながら老朽化した VMware 基盤を刷新したい。

**効果**: EC2 ベアメタルインスタンス上の VCF 環境へ移行することで、ハードウェア更改の負担を排除し、運用リスクを低減できる。

## 利用可能リージョン

すべての米国リージョンで FedRAMP Class C の認証範囲に含まれます。

## 関連サービス・機能

- **AWS FedRAMP コンプライアンスプログラム**: AWS サービスの FedRAMP 準拠状況を管理するプログラム
- **Amazon EC2 ベアメタルインスタンス**: Amazon EVS の VCF 環境が動作する基盤
- **Amazon VPC**: VCF 環境が展開されるネットワーク環境

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260921-amazon-evs-fedramp-class-c.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-evs-fedramp-class-c/)
- [AWS FedRAMP コンプライアンス](https://aws.amazon.com/compliance/fedramp/)
- [FedRAMP 対応 AWS サービス一覧](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/)
- [Amazon EVS 製品ページ](https://aws.amazon.com/evs/)
- [Amazon EVS ユーザーガイド](https://docs.aws.amazon.com/evs/latest/userguide/what-is-evs.html)

## まとめ

Amazon EVS が FedRAMP Class C (旧 Moderate ベースライン) の認証範囲に追加され、すべての米国リージョンで利用可能になりました。FedRAMP 準拠が求められる米国政府機関や関連組織は、VMware ワークロードを準拠を維持したまま AWS へ迅速に移行できます。対象の組織は [FedRAMP 対応サービス一覧](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/)で最新の認証状況を確認のうえ、移行計画の検討を推奨します。
