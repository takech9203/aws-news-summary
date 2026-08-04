# AWS Config - 15 種類の新しいリソースタイプのサポート

**リリース日**: 2026 年 8 月 3 日
**サービス**: AWS Config
**機能**: 新規リソースタイプのサポート拡大 (15 種類追加)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260803-aws-config-new-resource-types.html)

## 概要

AWS Config が、Amazon Bedrock、Amazon OpenSearch Serverless、Amazon SageMaker など主要サービスにまたがる 15 種類の AWS リソースタイプに新たに対応しました。今回の拡張により、AWS 環境に対する可視性の範囲が広がり、より多くのリソースを発見、評価、監査、修復できるようになります。

すべてのリソースタイプの記録を有効にしている場合、AWS Config はこれらの新しいリソースタイプを自動的に追跡します。追加のリソースタイプは、Config ルールおよび Config アグリゲーターでも利用可能です。今回サポートされたリソースタイプは、リソースが利用可能なすべての AWS リージョンでモニタリングできます。

対象となるのは、構成管理、コンプライアンス監査、ガバナンス、変更追跡を担当する運用チームやセキュリティチームです。特に今回は Bedrock の Automated Reasoning ポリシーや SageMaker の推論コンポーネントなど、生成 AI・機械学習関連のリソースが多く含まれており、AI ワークロードのガバナンス強化に役立ちます。

**アップデート前の課題**

- 今回追加された 15 種類のリソースタイプ (Bedrock の Automated Reasoning ポリシー、SageMaker の推論コンポーネントなど) は AWS Config で構成情報を記録できませんでした。
- 対象外のリソースは構成変更履歴が残らず、コンプライアンス評価や変更監査の対象にできませんでした。
- Config ルールや Config アグリゲーターを使った横断的なガバナンスに、これらのリソースを組み込めませんでした。

**アップデート後の改善**

- 15 種類の新規リソースタイプについて、構成情報の記録と変更履歴の追跡が可能になりました。
- すべてのリソースタイプの記録を有効化している場合、追加設定なしで自動的に新しいリソースタイプが記録対象に含まれます。
- 新規リソースタイプが Config ルールおよびアグリゲーターに対応し、コンプライアンス評価やマルチアカウント集約の対象になりました。

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Resources["☁️ 監視対象リソース 新規追加分"]
        direction LR
        R1["🤖 Bedrock<br/>AutomatedReasoningPolicy<br/>Blueprint ほか"]
        R2["🧠 SageMaker<br/>InferenceComponent<br/>Space ほか"]
        R3["🔍 OpenSearch Serverless<br/>AccessPolicy<br/>LifecyclePolicy"]
        R4["🔌 AppSync / Connect / Glue<br/>DomainName ほか"]
        R1 ~~~ R2 ~~~ R3 ~~~ R4
    end

    subgraph Config["⚙️ AWS Config"]
        Recorder["📝 Configuration Recorder"]
        Rules["✅ Config Rules"]
        Agg["📊 Aggregator"]
    end

    S3[("🪣 S3 配信先")]

    Resources --> Recorder
    Recorder --> Rules
    Recorder --> Agg
    Recorder --> S3

    classDef cloud fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef compute fill:#FFE0B2,stroke:#FFCC80,stroke-width:2px,color:#5D4037
    classDef storage fill:#DCEDC8,stroke:#C5E1A5,stroke-width:2px,color:#33691E
    classDef process fill:#FFFFFF,stroke:#4A90E2,stroke-width:2px,color:#333333

    class Resources,Config cloud
    class R1,R2,R3,R4 compute
    class S3 storage
    class Recorder,Rules,Agg process
```

Configuration Recorder が新規リソースタイプの構成変更を記録し、Config ルールによる評価、アグリゲーターによる集約、S3 への配信を行う流れを示しています。

## サービスアップデートの詳細

### 主要機能

1. **15 種類の新規リソースタイプのサポート**
   - 今回追加されたリソースタイプは以下のとおりです。
   - `AWS::AppSync::DomainName`
   - `AWS::Bedrock::AutomatedReasoningPolicy`
   - `AWS::Bedrock::AutomatedReasoningPolicyVersion`
   - `AWS::Bedrock::Blueprint`
   - `AWS::Bedrock::DataAutomationProject`
   - `AWS::BedrockAgentCore::ApiKeyCredentialProvider`
   - `AWS::Connect::UserHierarchyGroup`
   - `AWS::Glue::Trigger`
   - `AWS::OpenSearchServerless::AccessPolicy`
   - `AWS::OpenSearchServerless::LifecyclePolicy`
   - `AWS::SageMaker::ImageVersion`
   - `AWS::SageMaker::InferenceComponent`
   - `AWS::SageMaker::PartnerApp`
   - `AWS::SageMaker::Project`
   - `AWS::SageMaker::Space`

2. **自動的な記録対象への追加**
   - すべてのリソースタイプの記録を有効化している場合、追加設定なしで新しいリソースタイプが自動的に追跡されます。
   - 特定のリソースタイプのみを記録する構成の場合は、明示的に対象へ追加することで記録できます。

3. **Config ルールとアグリゲーターへの対応**
   - 新規リソースタイプは Config ルールによるコンプライアンス評価の対象になります。
   - Config アグリゲーターを利用することで、複数アカウント・複数リージョンにまたがってこれらのリソースの構成情報を集約できます。

## 技術仕様

### 追加されたリソースタイプ一覧

| リソースタイプ | 関連サービス |
|------|------|
| `AWS::AppSync::DomainName` | AWS AppSync |
| `AWS::Bedrock::AutomatedReasoningPolicy` | Amazon Bedrock |
| `AWS::Bedrock::AutomatedReasoningPolicyVersion` | Amazon Bedrock |
| `AWS::Bedrock::Blueprint` | Amazon Bedrock |
| `AWS::Bedrock::DataAutomationProject` | Amazon Bedrock |
| `AWS::BedrockAgentCore::ApiKeyCredentialProvider` | Amazon Bedrock AgentCore |
| `AWS::Connect::UserHierarchyGroup` | Amazon Connect |
| `AWS::Glue::Trigger` | AWS Glue |
| `AWS::OpenSearchServerless::AccessPolicy` | Amazon OpenSearch Serverless |
| `AWS::OpenSearchServerless::LifecyclePolicy` | Amazon OpenSearch Serverless |
| `AWS::SageMaker::ImageVersion` | Amazon SageMaker |
| `AWS::SageMaker::InferenceComponent` | Amazon SageMaker |
| `AWS::SageMaker::PartnerApp` | Amazon SageMaker |
| `AWS::SageMaker::Project` | Amazon SageMaker |
| `AWS::SageMaker::Space` | Amazon SageMaker |

### 記録モードと設定例

すべてのリソースタイプを記録する構成の例です。この設定では新規リソースタイプも自動的に対象になります。

```json
{
  "ConfigurationRecorder": {
    "name": "default",
    "roleARN": "arn:aws:iam::123456789012:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
    "recordingGroup": {
      "allSupported": true,
      "includeGlobalResourceTypes": true
    }
  }
}
```

特定のリソースタイプのみを記録する場合は、`resourceTypes` に明示的に追加します。

```json
{
  "ConfigurationRecorder": {
    "name": "default",
    "recordingGroup": {
      "allSupported": false,
      "resourceTypes": [
        "AWS::Bedrock::AutomatedReasoningPolicy",
        "AWS::SageMaker::InferenceComponent",
        "AWS::OpenSearchServerless::AccessPolicy"
      ]
    }
  }
}
```

## 設定方法

### 前提条件

1. 対象リージョンで AWS Config が有効化されていること。
2. Configuration Recorder に適切な IAM ロールが設定されていること。
3. 構成スナップショットと履歴の配信先となる Amazon S3 バケットが設定されていること。

### 手順

#### ステップ1: 現在の記録設定を確認

```bash
aws configservice describe-configuration-recorders
```

現在の Configuration Recorder の設定を表示し、`allSupported` が有効か、特定リソースタイプのみを記録しているかを確認します。

#### ステップ2: 新規リソースタイプを記録対象に含める

```bash
aws configservice put-configuration-recorder \
  --configuration-recorder '{
    "name": "default",
    "roleARN": "arn:aws:iam::123456789012:role/aws-config-role",
    "recordingGroup": { "allSupported": true, "includeGlobalResourceTypes": true }
  }'
```

すべてのリソースタイプを記録する設定に更新します。この構成では、今回追加されたリソースタイプも自動的に記録対象となります。

#### ステップ3: 記録の開始と評価

```bash
aws configservice start-configuration-recorder \
  --configuration-recorder-name default
```

記録を開始します。以降、対象リソースの作成・変更・削除が構成項目として記録され、Config ルールによる評価が実行されます。

## メリット

### ビジネス面

- **ガバナンス範囲の拡大**: これまで可視化できなかった生成 AI・機械学習関連のリソースを監査・コンプライアンス評価の対象に加え、統制の抜け漏れを減らせます。
- **設定変更なしでの適用**: 全リソースタイプ記録を有効にしている環境では、追加の運用負荷なしで自動的にカバレッジが広がります。
- **監査対応の効率化**: 構成変更履歴が残ることで、監査要求への証跡提供が容易になります。

### 技術面

- **構成ドリフトの検知**: 新規リソースの構成変更を継続的に記録し、意図しない変更を検知できます。
- **マルチアカウント集約**: Config アグリゲーターにより、組織全体でこれらのリソースの構成状態を一元的に把握できます。
- **ルールベースの自動評価**: Config ルールにより、アクセスポリシーやライフサイクル設定などの要件をリソースタイプごとに自動評価できます。

## デメリット・制約事項

### 制限事項

- 新規リソースタイプの記録は、そのリソースが利用可能なリージョンでのみ行われます。
- 構成項目の記録が増えるため、記録数に応じた料金が発生します。
- 特定リソースタイプのみを記録する構成の場合は、手動で対象へ追加しない限り記録されません。

### 考慮すべき点

- 全リソースタイプ記録を有効にしている環境では、記録される構成項目が増加し、コストが増える可能性があります。想定される増分を事前に評価してください。
- 記録対象を絞っている環境では、必要なリソースタイプを明示的に追加する運用が必要です。

## ユースケース

### ユースケース1: OpenSearch Serverless アクセスポリシーの監査

**シナリオ**: 検索基盤や RAG アプリケーションで利用する Amazon OpenSearch Serverless のコレクションについて、アクセスポリシーの意図しない変更を検知したい。

**実装例**:
```
記録対象: AWS::OpenSearchServerless::AccessPolicy, AWS::OpenSearchServerless::LifecyclePolicy
Config ルール: アクセスポリシーが想定外のプリンシパルへ許可を与えていないか評価
```

**効果**: アクセスポリシーやライフサイクルポリシーの変更が構成項目として記録され、コンプライアンス違反を早期に検知できます。

### ユースケース2: Bedrock Automated Reasoning ポリシーの変更追跡

**シナリオ**: 生成 AI アプリケーションのガードレールとして利用する Bedrock の Automated Reasoning ポリシーについて、ポリシーとバージョンの変更履歴を監査証跡として残したい。

**実装例**:
```
記録対象: AWS::Bedrock::AutomatedReasoningPolicy, AWS::Bedrock::AutomatedReasoningPolicyVersion
Config アグリゲーター: 全アカウント・全リージョンの設定を集約して一覧化
```

**効果**: 生成 AI のガードレール設定の変更履歴が残り、組織横断で AI ガバナンスの状態を一元的に把握できます。

### ユースケース3: SageMaker 推論環境の構成管理

**シナリオ**: 本番稼働中の SageMaker 推論コンポーネントや Studio のスペースについて、設定変更の経緯を追跡し、トラブルシューティングに活用したい。

**実装例**:
```
記録対象: AWS::SageMaker::InferenceComponent, AWS::SageMaker::Space, AWS::SageMaker::Project
用途: 構成タイムラインで変更前後の設定を比較
```

**効果**: 推論コンポーネントやスペースの変更履歴を可視化し、性能問題や障害発生時の原因調査、監査対応に活用できます。

## 料金

AWS Config は従量課金制で、最低料金や前払いのコミットメントはありません。今回のアップデート自体に追加料金はなく、記録される構成項目や評価の数に応じて既存の料金体系が適用されます。

### 料金例

| 項目 | 料金 (概算) |
|--------|------------------|
| 継続的な構成項目の記録 | 1 構成項目あたり 0.003 USD |
| 定期的な構成項目の記録 | 1 構成項目あたり 0.012 USD |
| Config ルールの評価 (最初の 100,000 件) | 1 評価あたり 0.001 USD |
| コンフォーマンスパックの評価 (最初の 100,000 件) | 1 評価あたり 0.001 USD |

新規リソースタイプの記録が増えると構成項目数が増加するため、記録コストにも影響します。カスタムルールや配信に伴う Amazon S3、Amazon SNS、AWS Lambda の標準料金が別途発生する場合があります。

## 利用可能リージョン

今回サポートされたリソースタイプは、対象リソースが利用可能なすべての AWS リージョンでモニタリングできます。リソースタイプごとの対応状況は、AWS Config のリソースカバレッジのドキュメントを参照してください。

## 関連サービス・機能

- **Amazon Bedrock / Bedrock AgentCore**: Automated Reasoning ポリシー、Blueprint、Data Automation プロジェクト、API キー認証プロバイダーの構成管理に対応します。
- **Amazon SageMaker**: 推論コンポーネント、イメージバージョン、パートナーアプリ、プロジェクト、スペースが記録対象になります。
- **Amazon OpenSearch Serverless / AWS AppSync / Amazon Connect / AWS Glue**: アクセスポリシーやドメイン名、ユーザー階層グループ、トリガーなどの運用リソースを監査対象に加えられます。

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260803-aws-config-new-resource-types.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/08/aws-config-new-resource-types)
- [AWS Config リソースカバレッジ (ドキュメント)](https://docs.aws.amazon.com/config/latest/developerguide/what-is-resource-config-coverage.html)
- [AWS Config 料金ページ](https://aws.amazon.com/config/pricing/)

## まとめ

今回のアップデートにより、AWS Config が Amazon Bedrock や SageMaker、OpenSearch Serverless など 15 種類のリソースタイプに新たに対応し、特に生成 AI・機械学習関連リソースのガバナンスと監査の対象範囲が広がりました。全リソースタイプ記録を有効にしている環境では追加設定なしでカバレッジが拡大するため、構成項目数の増加によるコスト影響を確認しつつ、必要に応じて Config ルールでの評価を追加することを推奨します。
