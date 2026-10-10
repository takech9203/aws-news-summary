# AWS Lambda - セルフマネージド Apache Kafka イベントソースの OAuth 認証サポート

**リリース日**: 2026 年 10 月 9 日
**サービス**: AWS Lambda
**機能**: セルフマネージド Apache Kafka イベントソースマッピングにおける OAuth 認証サポート

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261009-aws-Lambda-supports-oauth-kafka-esm.html)

## 概要

AWS Lambda が、セルフマネージド Apache Kafka イベントソースマッピング (ESM) における OAuth 認証のサポートを発表しました。対象には、お客様自身が運用する Kafka クラスターに加え、Confluent Cloud、Aiven、Redpanda などのマネージドサービスも含まれます。これにより、Amazon Cognito や Okta といったエンタープライズ ID プロバイダーを使用して Lambda の Kafka コンシューマーを認証できるようになります。

Kafka ESM は、決済処理、不正検出、リアルタイムデータパイプラインなどのイベント駆動型ワークロードで広く利用されており、自動スケーリング、エラー処理、バッチ処理、イベントフィルタリングを提供します。今回の OAuth 対応により、Kafka クラスターと Lambda コンシューマーの両方に同一の ID 統制とアクセスポリシーを適用でき、セキュリティおよびコンプライアンス要件を満たしやすくなります。

**アップデート前の課題**

- セルフマネージド Kafka ESM の認証方式は SASL/PLAIN、SASL/SCRAM、mTLS の 3 種類に限定されていた
- OAuth 認証が必須とされる規制業界のお客様は、Kafka ESM を利用できなかった
- Kafka クラスター側で OAuth による ID 統制を導入していても、Lambda コンシューマーだけ別の認証方式と認証情報を管理する必要があった

**アップデート後の改善**

- SASL/OAUTHBEARER (TLS 暗号化付き) による OAuth 2.0 認証が利用可能になった
- Amazon Cognito、Okta などのエンタープライズ ID プロバイダーで Lambda Kafka コンシューマーを一元的に認証できるようになった
- トークンの取得と有効期限前の自動更新を Lambda が代行するため、トークン管理の実装が不要になった
- Secrets Manager 上の認証情報をローテーションしても、ESM を再作成せずに新しい値が自動的に反映されるようになった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph AWS["☁️ AWS"]
        SM[("🔐 Secrets Manager<br/>OAuth シークレット")]
        ESM["🔄 Lambda ESM<br/>Kafka コンシューマー"]
        Fn["⚡ Lambda 関数"]
    end

    subgraph External["🌐 外部システム"]
        direction LR
        IdP{{"🪪 OAuth 2.0 ID プロバイダー<br/>Amazon Cognito / Okta など"}}
        Kafka{{"📨 セルフマネージド Kafka<br/>Confluent Cloud / Aiven / Redpanda"}}
        IdP ~~~ Kafka
    end

    ESM -->|1 シークレット取得| SM
    ESM -->|2 アクセストークン要求| IdP
    IdP -.->|3 トークン発行と自動更新| ESM
    ESM -->|4 SASL/OAUTHBEARER でトークン提示| Kafka
    Kafka -->|5 メッセージポーリング| ESM
    ESM -->|6 バッチで関数を呼び出し| Fn

    classDef cloud fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef internal fill:#E8F1FF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef storage fill:#E8EAF6,stroke:#C5CAE9,stroke-width:2px,color:#283593
    classDef external fill:#E9F7EC,stroke:#66BB6A,stroke-width:2px,color:#333333

    class AWS,External cloud
    class ESM,Fn internal
    class SM storage
    class IdP,Kafka external
```

Lambda の ESM が Secrets Manager から OAuth 認証情報を取得して ID プロバイダーにアクセストークンを要求し、取得したトークンを SASL/OAUTHBEARER で Kafka ブローカーに提示して認証します。トークンの有効期限前の更新は Lambda が自動的に行います。

## サービスアップデートの詳細

### 主要機能

1. **SASL/OAUTHBEARER による OAuth 2.0 認証**
   - TLS 暗号化 (`SASL_SSL`) 付きの SASL/OAUTHBEARER 認証をサポート
   - Lambda が OAuth 2.0 ID プロバイダーのトークンエンドポイントからアクセストークンを取得し、Kafka ブローカーに提示
   - トークンは有効期限が切れる前に Lambda が自動的に更新
   - `SourceAccessConfiguration` の `Type` に `OAUTHBEARER_AUTH` を指定し、`URI` に OAuth シークレットの Secrets Manager ARN を設定

2. **2 種類のグラントタイプをサポート**
   - **クライアントクレデンシャル**: クライアント ID とクライアントシークレットをトークンエンドポイントに送信。ID プロバイダーがクライアントシークレットを発行する場合に使用
   - **JWT ベアラー**: 秘密鍵で署名した JWT アサーションをトークンエンドポイントに送信。ID プロバイダーが署名付きアサーションを要求する場合に使用
   - Secrets Manager シークレットに格納するフィールドによって、使用されるグラントタイプが決まる

3. **追加の OAuth パラメーター**
   - `OAUTHBEARER_SCOPE`: トークン要求時に Lambda が指定するスコープ
   - `OAUTHBEARER_AUDIENCE`: トークン要求時に Lambda が指定するオーディエンス
   - `OAUTHBEARER_LOGICAL_CLUSTER`: SASL 拡張としてブローカーに送信される論理クラスター ID (Confluent Cloud などで使用)
   - `OAUTHBEARER_IDENTITY_POOL`: SASL 拡張としてブローカーに送信される ID プール ID
   - これらは `URI` フィールドにシークレット ARN ではなくリテラル値を直接指定する

4. **IAM 認証との組み合わせ (IAM_OAUTHBEARER_AUTH)**
   - ブローカーが OAuth 2.0 トークンを受け入れる場合、AWS 自体を ID プロバイダーとして使用可能
   - Lambda が `sts:GetWebIdentityToken` で関数の実行ロールの短期トークンを取得し、SASL/OAUTHBEARER でブローカーに提示
   - Secrets Manager に認証情報を保存する必要がなく、`OAUTHBEARER_AUDIENCE` の指定が必須
   - ブローカー側で AWS を OpenID Connect (OIDC) の ID プロバイダーとして信頼するよう事前設定が必要

## 技術仕様

### セルフマネージド Kafka ESM の認証方式一覧

| 認証方式 | Type 値 | 認証情報の保存先 |
|------|------|------|
| SASL/PLAIN | `BASIC_AUTH` | Secrets Manager |
| SASL/SCRAM | `SASL_SCRAM_256_AUTH` / `SASL_SCRAM_512_AUTH` | Secrets Manager |
| mTLS | `CLIENT_CERTIFICATE_TLS_AUTH` | Secrets Manager |
| **OAuth 2.0 (新規)** | `OAUTHBEARER_AUTH` | Secrets Manager |
| **IAM (新規)** | `IAM_AUTH` | 不要 (実行ロールを使用) |
| **IAM + SASL/OAUTHBEARER (新規)** | `IAM_OAUTHBEARER_AUTH` | 不要 (実行ロールを使用) |

### OAuth シークレットのフィールド

| フィールド | 必須 | 説明 |
|------|------|------|
| `oauthTokenEndpointUrl` | 必須 | ID プロバイダーのトークンエンドポイント (HTTPS URL) |
| `oauthClientId` | 必須 | ID プロバイダーが発行したクライアント ID |
| `oauthClientSecret` | クライアントクレデンシャルのみ | ID プロバイダーが発行したクライアントシークレット |
| `oauthClientEmail` | JWT ベアラーのみ | JWT アサーションに含めるサービスアカウント ID |
| `oauthPrivateKey` | JWT ベアラーのみ | JWT アサーションの署名に使用する秘密鍵 (PEM 形式) |
| `oauthTokenExpirationSeconds` | 任意 | Lambda が署名する JWT アサーションの有効期間 (JWT ベアラーのみ) |
| `oauthIdpCaCertificate` | 任意 | ID プロバイダーのルート CA 証明書 (プライベート CA の場合、PEM 形式) |

両方のグラントタイプのフィールドを同時に指定すると、Lambda は検証エラーを返します。

### API 変更履歴

| 日付 | サービス | 変更内容 |
|------|----------|----------|
| 2026/10/08 | [AWS Lambda](https://awsapichanges.com/archive/changes/6b8067-lambda.html) | 5 updated api methods - セルフマネージド Kafka ESM 向けの OAuth 2.0 (OAUTHBEARER)、IAM、IAM + OAUTHBEARER 認証のサポート追加。OAuth のスコープ、オーディエンス、論理クラスター、ID プールのオプションパラメーターを含む。Confluent Schema Registry でも OAuth 2.0 が利用可能に |

### シークレットの例 (クライアントクレデンシャルグラント)

```json
{
  "oauthTokenEndpointUrl": "https://idp.example.com/oauth2/token",
  "oauthClientId": "my-client-id",
  "oauthClientSecret": "my-client-secret"
}
```

## 設定方法

### 前提条件

1. セルフマネージド Apache Kafka クラスター (または Confluent Cloud、Aiven、Redpanda などのマネージドサービス) が稼働していること
2. Kafka ブローカーが OAuth 2.0 トークンを検証するように設定されており、Lambda が使用するものと同じ ID プロバイダーを信頼していること
3. OAuth 認証情報を保存する Secrets Manager シークレットが、Lambda 関数と同じ AWS リージョンに存在すること
4. Lambda 関数の実行ロールに、シークレットへの `secretsmanager:GetSecretValue` 権限があること

### 手順

#### ステップ 1: OAuth シークレットの作成

```bash
aws secretsmanager create-secret \
  --name kafka-oauth-credentials \
  --secret-string '{
    "oauthTokenEndpointUrl": "https://idp.example.com/oauth2/token",
    "oauthClientId": "my-client-id",
    "oauthClientSecret": "my-client-secret"
  }'
```

ID プロバイダーのトークンエンドポイント、クライアント ID、クライアントシークレットを含む OAuth シークレットを Secrets Manager に作成します。JWT ベアラーグラントを使用する場合は、`oauthClientSecret` の代わりに `oauthClientEmail` と `oauthPrivateKey` を指定します。

#### ステップ 2: イベントソースマッピングの作成

```bash
aws lambda create-event-source-mapping \
  --function-name my-kafka-consumer \
  --topics payment-events \
  --self-managed-event-source '{"Endpoints":{"KAFKA_BOOTSTRAP_SERVERS":["broker1.example.com:9092","broker2.example.com:9092"]}}' \
  --source-access-configurations '[
    {"Type":"OAUTHBEARER_AUTH","URI":"arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:kafka-oauth-credentials"},
    {"Type":"OAUTHBEARER_SCOPE","URI":"kafka:read"}
  ]'
```

`OAUTHBEARER_AUTH` タイプでシークレットの ARN を指定し、セルフマネージド Kafka の ESM を作成します。ID プロバイダーやブローカーが追加の値を要求する場合は、`OAUTHBEARER_SCOPE` や `OAUTHBEARER_AUDIENCE` などをリテラル値として追加します。コンソール、CloudFormation、AWS SAM でも同様に設定できます。

#### ステップ 3: 動作確認

```bash
aws lambda get-event-source-mapping \
  --uuid <event-source-mapping-uuid> \
  --query '{State: State, LastProcessingResult: LastProcessingResult}'
```

ESM の状態を確認し、`State` が `Enabled` になっていること、認証エラーが発生していないことを確認します。その後、Kafka トピックにテストメッセージを送信し、Lambda 関数が呼び出されることを確認します。

## メリット

### ビジネス面

- **コンプライアンス対応**: OAuth 認証が必須の規制業界 (金融、ヘルスケアなど) でも Kafka ESM を利用可能になり、監査要件を満たしやすくなる
- **ID 統制の一元化**: Kafka クラスターと Lambda コンシューマーに同一の ID プロバイダーとアクセスポリシーを適用でき、ガバナンスが向上する
- **運用コストの削減**: トークンの取得・更新・ローテーション対応を Lambda が代行するため、認証管理の運用負荷が軽減される

### 技術面

- **トークン管理の自動化**: Lambda がアクセストークンの取得と有効期限前の自動更新を行うため、カスタム実装が不要
- **柔軟なグラントタイプ**: クライアントクレデンシャルと JWT ベアラーの 2 種類に対応し、Okta、Amazon Cognito など幅広い ID プロバイダーと統合できる
- **ダウンタイムなしの認証情報ローテーション**: シークレットの値を更新するだけで、ESM を再作成せずに新しい認証情報が反映される
- **Confluent Cloud 固有の拡張に対応**: 論理クラスター ID や ID プール ID を SASL 拡張として送信でき、Confluent Cloud の OAuth 構成とそのまま統合できる

## デメリット・制約事項

### 制限事項

- OAuth 認証はプレーンテキスト接続では利用できず、TLS 暗号化 (`SASL_SSL`) が必須
- シークレットは Lambda 関数と同じ AWS リージョンに保存する必要がある
- 1 つのシークレットに両方のグラントタイプのフィールドを含めると検証エラーになる
- `OAUTHBEARER_SCOPE`、`OAUTHBEARER_LOGICAL_CLUSTER`、`OAUTHBEARER_IDENTITY_POOL` は `OAUTHBEARER_AUTH` と組み合わせる必要があり、`IAM_OAUTHBEARER_AUTH` では `OAUTHBEARER_AUDIENCE` のみ指定可能
- 本機能はセルフマネージド Kafka ESM が対象であり、提供範囲は AWS 商用リージョンに限られる

### 考慮すべき点

- Kafka ブローカー側で、Lambda が使用する ID プロバイダーのトークンを検証するよう事前に設定が必要
- ブローカーがプライベート CA により署名された証明書を提示する場合は、`SERVER_ROOT_CA_CERTIFICATE` の設定も必要
- ID プロバイダーのトークンエンドポイントがプライベート CA の証明書を使用する場合は、シークレットに `oauthIdpCaCertificate` を含める必要がある
- 実行ロールに `secretsmanager:GetSecretValue` 権限 (IAM + OAUTHBEARER の場合は `sts:GetWebIdentityToken` 権限) を付与する必要がある

## ユースケース

### ユースケース 1: Confluent Cloud と Okta を利用した決済イベント処理

**シナリオ**: 金融企業が Confluent Cloud 上の Kafka トピックで決済イベントを管理しており、社内標準の ID プロバイダーである Okta による OAuth 認証が必須となっている。Lambda で決済イベントをリアルタイム処理したい。

**実装例**:
```json
[
  {"Type": "OAUTHBEARER_AUTH", "URI": "arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:confluent-oauth"},
  {"Type": "OAUTHBEARER_LOGICAL_CLUSTER", "URI": "lkc-abc123"},
  {"Type": "OAUTHBEARER_IDENTITY_POOL", "URI": "pool-xyz789"}
]
```

**効果**: 社内のセキュリティポリシーに準拠したまま、Kafka クラスターと Lambda コンシューマーの認証を Okta で一元管理し、サーバーレスで決済処理パイプラインを構築できる。

### ユースケース 2: Amazon Cognito を利用した不正検出パイプライン

**シナリオ**: EC サイト運営企業が、セルフマネージド Kafka クラスターに流れるトランザクションイベントを Lambda で消費し、不正検出モデルで評価したい。追加の ID プロバイダーを導入せず、Amazon Cognito で認証を統一したい。

**実装例**:
```json
{
  "oauthTokenEndpointUrl": "https://my-domain.auth.ap-northeast-1.amazoncognito.com/oauth2/token",
  "oauthClientId": "cognito-app-client-id",
  "oauthClientSecret": "cognito-app-client-secret"
}
```

**効果**: Cognito のクライアントクレデンシャルグラントを利用して、追加の ID 基盤を構築することなく OAuth 認証付きのリアルタイム不正検出パイプラインを実現できる。

### ユースケース 3: JWT ベアラーグラントによるレガシー認証からの移行

**シナリオ**: クライアントシークレットの配布を禁止し、署名付き JWT アサーションのみを受け付ける ID プロバイダーを採用している企業が、SASL/SCRAM で運用していた Lambda の Kafka コンシューマーを OAuth 認証へ移行したい。

**実装例**:
```json
{
  "oauthTokenEndpointUrl": "https://idp.example.com/oauth2/token",
  "oauthClientId": "my-client-id",
  "oauthClientEmail": "lambda-consumer@example.com",
  "oauthPrivateKey": "-----BEGIN PRIVATE KEY-----\n<private key contents>\n-----END PRIVATE KEY-----"
}
```

**効果**: 共有パスワード方式の SASL/SCRAM から、秘密鍵による署名ベースの JWT ベアラーグラントに移行し、認証情報漏えいリスクを低減できる。

## 料金

本アップデートに伴う追加料金は発表されていません。AWS Lambda の通常の料金体系 (関数の実行時間、リクエスト数、イベントソースマッピングの料金) が適用されます。また、OAuth シークレットの保存には AWS Secrets Manager の料金が別途発生します。詳細は [AWS Lambda 料金ページ](https://aws.amazon.com/lambda/pricing/) を参照してください。

## 利用可能リージョン

セルフマネージド Apache Kafka イベントソースマッピングが利用可能なすべての AWS 商用リージョンで利用できます。

## 関連サービス・機能

- **AWS Secrets Manager**: OAuth 認証情報 (トークンエンドポイント、クライアント ID など) をシークレットとして安全に保存。ローテーションにも対応
- **Amazon Cognito**: AWS ネイティブの OAuth 2.0 対応 ID プロバイダーとして、Lambda Kafka コンシューマーの認証に利用可能
- **Amazon MSK**: AWS マネージドの Kafka サービス。カスタムネットワーク構成の MSK クラスターをセルフマネージド Kafka ESM として登録し、IAM 認証で接続することも可能
- **AWS CloudFormation / AWS SAM**: 本機能の認証設定を Infrastructure as Code で管理可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261009-aws-Lambda-supports-oauth-kafka-esm.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/10/aws-Lambda-supports-oauth-kafka-esm/)
- [ドキュメント: Apache Kafka イベントソースマッピング](https://docs.aws.amazon.com/lambda/latest/dg/with-kafka.html)
- [ドキュメント: Kafka クラスター認証方式の設定](https://docs.aws.amazon.com/lambda/latest/dg/kafka-cluster-auth.html)
- [API リファレンス: SourceAccessConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_SourceAccessConfiguration.html)
- [料金ページ](https://aws.amazon.com/lambda/pricing/)

## まとめ

AWS Lambda のセルフマネージド Kafka イベントソースマッピングが OAuth 認証に対応したことで、OAuth が必須の規制業界でもサーバーレスな Kafka コンシューマーを構築できるようになりました。Confluent Cloud をはじめとするマネージド Kafka サービスとエンタープライズ ID プロバイダーを組み合わせている場合、既存の ID 統制をそのまま Lambda に適用できます。現在 SASL/SCRAM などで認証情報を個別管理している場合は、OAuth 認証への移行を検討することを推奨します。
