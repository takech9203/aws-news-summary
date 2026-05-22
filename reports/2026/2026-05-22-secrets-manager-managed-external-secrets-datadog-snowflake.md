# AWS Secrets Manager - Datadog および Snowflake PAT 向けマネージド外部シークレットサポート

**リリース日**: 2026 年 5 月 22 日
**サービス**: AWS Secrets Manager
**機能**: Managed External Secrets (Datadog vended keys / Snowflake Programmatic Access Tokens)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260522-secrets-manager-managed-external-secrets-datadog-snowflake.html)

## 概要

AWS Secrets Manager のマネージド外部シークレット機能に、Datadog のベンダーキーおよび Snowflake のプログラマティックアクセストークン (PAT) のサポートが追加された。これにより、サードパーティサービスの認証情報を AWS Secrets Manager で一元管理し、カスタム Lambda 関数を作成・維持することなく自動ローテーションを実現できる。

マネージド外部シークレットは、サードパーティアプリケーションの認証情報を事前定義されたフォーマットで保存し、自動的にローテーションする機能である。今回の発表により、既存の BigID、Confluent Cloud、MongoDB Atlas、Salesforce に加え、Datadog と Snowflake PAT が新たにサポートされた。

**アップデート前の課題**

- Datadog API キーや Snowflake トークンのローテーションにカスタム Lambda 関数の開発・維持が必要だった
- サードパーティごとに異なるローテーションロジックを実装する必要があった
- トークン更新時のダウンタイムを防ぐための猶予期間管理を独自に実装する必要があった

**アップデート後の改善**

- Lambda 関数不要でマネージドローテーションが自動的に実行される
- 事前定義されたシークレットフォーマットにより統一的な管理が可能になった
- Snowflake PAT では設定可能な猶予期間によりゼロダウンタイムでのトークン移行が実現された

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph AWS["☁️ AWS"]
        subgraph SM["🔐 Secrets Manager"]
            direction LR
            DDSecret["🐶 Datadog シークレット<br/>API Key / App Key / Admin Key"]
            SFSecret["❄️ Snowflake シークレット<br/>PAT"]
            DDSecret ~~~ SFSecret
        end
        subgraph IAM["🛡️ IAM"]
            Role["⚙️ ローテーション用 IAM ロール"]
        end
        CT["📋 CloudTrail"]
    end

    subgraph External["🌐 サードパーティ"]
        DD["🐶 Datadog API<br/>Key Management API v2"]
        SF["❄️ Snowflake<br/>ALTER USER ROTATE PAT"]
    end

    SM -->|AssumeRole| Role
    Role -->|API 呼び出し| DD
    Role -->|キーペア認証| SF
    SM -->|監査ログ| CT

    classDef cloud fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef sm fill:#E8F1FF,stroke:#4A90E2,stroke-width:2px,color:#1565C0
    classDef iam fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#E65100
    classDef external fill:#E9F7EC,stroke:#66BB6A,stroke-width:2px,color:#2E7D32
    classDef audit fill:#F3E5F5,stroke:#7B61FF,stroke-width:2px,color:#4A148C

    class AWS cloud
    class SM,DDSecret,SFSecret sm
    class IAM,Role iam
    class External,DD,SF external
    class CT audit
```

Secrets Manager がサービスプリンシパルとして IAM ロールを引き受け、Datadog API や Snowflake に対してローテーション操作を直接実行する。Lambda 関数はアカウント内にデプロイされない。

## サービスアップデートの詳細

### 主要機能

1. **Datadog ベンダーキー管理**
   - **DatadogApiKey**: 32 文字の 16 進 API キーを自動ローテーション。2 キー交互パターンでゼロダウンタイムを実現
   - **DatadogApplicationKey**: サービスアカウントが所有するアプリケーションキーのローテーション
   - **DatadogAdminKey**: API キーとアプリケーションキーのペアを同時にローテーション。自己ローテーションにも対応

2. **Snowflake プログラマティックアクセストークン**
   - Snowflake ネイティブ認証 (キーペア認証) を使用した PAT ローテーション
   - `ALTER USER ... ROTATE PAT` コマンドによるアトミックなトークン生成
   - 設定可能な猶予期間 (0-720 時間) で旧トークンの段階的な無効化が可能

3. **Lambda 不要のマネージドローテーション**
   - カスタム Lambda 関数の作成・デプロイ・管理が一切不要
   - コンソールでシークレット作成時にローテーションが自動的に有効化
   - AWS CloudTrail による全操作の完全な監査証跡

## 技術仕様

### サポートされるシークレットタイプ

| インテグレーションパートナー | シークレットタイプ | 用途 |
|------|----------|----------|
| Datadog | DatadogApiKey | メトリクス・ログ・トレース送信用 API キー |
| Datadog | DatadogApplicationKey | サービスアカウント用アプリケーションキー |
| Datadog | DatadogAdminKey | 管理用 API キー + アプリケーションキーペア |
| Snowflake | SnowflakePat | プログラマティックアクセストークン |

### Datadog シークレットフォーマット

**DatadogApiKey のシークレット値:**

```json
{
  "apiKey": "{{32文字の16進APIキー}}",
  "apiKeyId": "{{APIキーのUUID}}"
}
```

**DatadogAdminKey のシークレット値:**

```json
{
  "adminApiKey": "{{32文字の16進APIキー}}",
  "adminApiKeyId": "{{APIキーのUUID}}",
  "adminAppKey": "{{ddapp_で始まるアプリケーションキー}}",
  "adminAppKeyId": "{{アプリケーションキーのUUID}}",
  "serviceAccountId": "{{サービスアカウントのUUID}}",
  "site": "datadoghq.com"
}
```

### Snowflake PAT シークレットフォーマット

**シークレット値:**

```json
{
  "account": "{{Snowflakeアカウント識別子}}",
  "user": "{{Snowflakeユーザー名}}",
  "privateKey": "{{PEMエンコードされた秘密鍵}}",
  "passphrase": "{{秘密鍵のパスフレーズ (オプション)}}",
  "patTokenName": "{{PATの名前}}",
  "patTokenValue": "{{PATの値}}"
}
```

**ローテーションメタデータ:**

```json
{
  "daysToExpiry": "15",
  "expireOldTokenAfterHours": "24"
}
```

| パラメータ | 説明 | デフォルト値 | 範囲 |
|------|----------|----------|----------|
| daysToExpiry | PAT の有効期限 (日数) | 15 | 1-365 |
| expireOldTokenAfterHours | 旧トークンの猶予期間 (時間) | 24 | 0-720 |

### API 変更履歴

今回のアップデートに関連する API 変更は awsapichanges.com で確認された範囲内では検出されなかった。既存の `CreateSecret` API および `RotateSecret` API のシークレットタイプパラメータとして新しい値 (DatadogApiKey、DatadogApplicationKey、DatadogAdminKey、SnowflakePat) が追加される形で実装されている。

### IAM 権限設定

**ローテーション用 IAM ポリシー例:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRotationAccess",
      "Action": [
        "secretsmanager:DescribeSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:PutSecretValue",
        "secretsmanager:UpdateSecretVersionStage"
      ],
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "secretsmanager:resource/Type": "DatadogApiKey"
        }
      }
    },
    {
      "Sid": "AllowPasswordGenerationAccess",
      "Action": [
        "secretsmanager:GetRandomPassword"
      ],
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
```

**信頼ポリシー例:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SecretsManagerPrincipalAccess",
      "Effect": "Allow",
      "Principal": {
        "Service": "secretsmanager.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "111122223333"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:secretsmanager:us-east-1:111122223333:secret:*"
        }
      }
    }
  ]
}
```

## 設定方法

### 前提条件

1. AWS Secrets Manager へのアクセス権限を持つ IAM ロールまたはユーザー
2. Datadog の場合: サービスアカウントと管理用 API キー + アプリケーションキー (スコープ: `api_keys_write`, `api_keys_delete`)
3. Snowflake の場合: キーペア認証が設定されたユーザーと既存の PAT

### 手順

#### ステップ 1: Datadog Admin シークレットの作成 (Datadog の場合)

```bash
aws secretsmanager create-secret \
  --name "datadog/admin-key" \
  --secret-string '{
    "adminApiKey": "your-32-char-hex-api-key",
    "adminApiKeyId": "api-key-uuid",
    "adminAppKey": "ddapp_your-application-key",
    "adminAppKeyId": "app-key-uuid",
    "serviceAccountId": "service-account-uuid",
    "site": "datadoghq.com"
  }' \
  --secret-type DatadogAdminKey
```

Datadog の管理用認証情報を含むシークレットを作成する。このシークレットは他の Datadog シークレットのローテーション時に認証に使用される。

#### ステップ 2: Datadog API キーシークレットの作成とローテーション設定

```bash
# シークレット作成
aws secretsmanager create-secret \
  --name "datadog/api-key" \
  --secret-string '{
    "apiKey": "your-32-char-hex-api-key",
    "apiKeyId": "api-key-uuid"
  }' \
  --secret-type DatadogApiKey

# ローテーション設定
aws secretsmanager rotate-secret \
  --secret-id "datadog/api-key" \
  --rotation-rules '{"AutomaticallyAfterDays": 30}' \
  --rotation-metadata '{"adminSecretArn": "arn:aws:secretsmanager:us-east-1:111122223333:secret:datadog/admin-key-AbCdEf"}' \
  --role-arn "arn:aws:iam::111122223333:role/SecretsManagerRotationRole"
```

Datadog API キーのシークレットを作成し、30 日ごとの自動ローテーションを設定する。adminSecretArn にはステップ 1 で作成した管理用シークレットの ARN を指定する。

#### ステップ 3: Snowflake PAT シークレットの作成とローテーション設定

```bash
# シークレット作成
aws secretsmanager create-secret \
  --name "snowflake/pat" \
  --secret-string '{
    "account": "myorg-myaccount",
    "user": "my_user",
    "privateKey": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
    "passphrase": "",
    "patTokenName": "my_pat_token",
    "patTokenValue": "current-pat-value"
  }' \
  --secret-type SnowflakePat

# ローテーション設定
aws secretsmanager rotate-secret \
  --secret-id "snowflake/pat" \
  --rotation-rules '{"AutomaticallyAfterDays": 14}' \
  --rotation-metadata '{"daysToExpiry": "15", "expireOldTokenAfterHours": "24"}' \
  --role-arn "arn:aws:iam::111122223333:role/SecretsManagerRotationRole"
```

Snowflake PAT のシークレットを作成し、14 日ごとの自動ローテーションを設定する。猶予期間を 24 時間に設定することで、アプリケーションが新しいトークンに移行する時間を確保する。

## メリット

### ビジネス面

- **運用コスト削減**: カスタム Lambda 関数の開発・テスト・維持にかかる工数を排除
- **セキュリティ態勢の強化**: 定期的な自動ローテーションにより認証情報の漏洩リスクを低減
- **コンプライアンス対応の簡素化**: CloudTrail による完全な監査証跡で認証情報管理の追跡が容易

### 技術面

- **ゼロダウンタイムローテーション**: 2 キー交互パターン (Datadog) や猶予期間 (Snowflake) により中断なしでの更新が可能
- **統一的な管理インターフェース**: AWS SDK、CLI、コンソールから複数のサードパーティ認証情報を一元管理
- **最小権限の原則**: シークレットタイプごとに条件キーでスコープダウンされた IAM ポリシーの適用が可能

## デメリット・制約事項

### 制限事項

- Datadog の API キーおよびアプリケーションキーはサービスアカウントが所有するものに限定される (個人ユーザー所有のキーは非対応)
- Snowflake PAT のローテーションには事前にキーペア認証の設定が必要
- Datadog の Admin Key ローテーションには `api_keys_write`、`api_keys_delete`、`org_app_keys_read`、`org_app_keys_write`、`service_account_write` スコープが必要

### 考慮すべき点

- Datadog の 2 シークレットアーキテクチャでは Admin シークレットの管理も必要になるため、権限の階層構造の設計が重要
- Snowflake の `daysToExpiry` はローテーションスケジュールより長い値に設定する必要がある (ローテーション間隔 < トークン有効期限)
- IP 制限を設定する場合、AWS の IP レンジは変更される可能性があるため定期的な更新が必要

## ユースケース

### ユースケース 1: マルチサービス監視基盤の認証情報管理

**シナリオ**: Datadog を使用してマルチアカウント AWS 環境を監視しているエンタープライズ企業。各アカウントに Datadog API キーが配布されており、セキュリティポリシーにより 30 日ごとのキーローテーションが求められている。

**実装例**:
```bash
# 各アカウントの Datadog API キーを Secrets Manager で管理
aws secretsmanager create-secret \
  --name "monitoring/datadog-api-key" \
  --secret-string '{"apiKey": "abc123...", "apiKeyId": "uuid-here"}' \
  --secret-type DatadogApiKey

# AWS Organizations の共有 Admin シークレットを参照してローテーション
aws secretsmanager rotate-secret \
  --secret-id "monitoring/datadog-api-key" \
  --rotation-rules '{"AutomaticallyAfterDays": 30}' \
  --rotation-metadata '{"adminSecretArn": "arn:aws:secretsmanager:us-east-1:central-account:secret:datadog-admin"}' \
  --role-arn "arn:aws:iam::111122223333:role/DatadogRotationRole"
```

**効果**: 数十アカウントの Datadog API キーの手動ローテーションが不要になり、運用チームの負荷を大幅に削減

### ユースケース 2: データパイプラインにおける Snowflake アクセス管理

**シナリオ**: AWS Glue や Lambda から Snowflake にデータをロードするパイプラインで、PAT を使用して認証を行っている。セキュリティ要件としてトークンの定期的な更新が必要だが、パイプラインの中断は許容できない。

**実装例**:
```bash
# Snowflake PAT を作成 (猶予期間48時間で設定)
aws secretsmanager create-secret \
  --name "pipeline/snowflake-pat" \
  --secret-string '{
    "account": "myorg-prod",
    "user": "ETL_SERVICE_USER",
    "privateKey": "-----BEGIN PRIVATE KEY-----\n...",
    "passphrase": "",
    "patTokenName": "etl_pipeline_token",
    "patTokenValue": "pat-value"
  }' \
  --secret-type SnowflakePat

# 7日ごとのローテーション、猶予期間48時間
aws secretsmanager rotate-secret \
  --secret-id "pipeline/snowflake-pat" \
  --rotation-rules '{"AutomaticallyAfterDays": 7}' \
  --rotation-metadata '{"daysToExpiry": "15", "expireOldTokenAfterHours": "48"}' \
  --role-arn "arn:aws:iam::111122223333:role/SnowflakeRotationRole"
```

**効果**: 48 時間の猶予期間により、分散したパイプラインコンポーネントが新しいトークンをキャッシュから取得する時間を確保しつつ、セキュリティ要件を満たす

### ユースケース 3: Datadog 管理キーの自己ローテーション

**シナリオ**: セキュリティチームが Datadog の管理用認証情報自体もローテーションしたい。管理キーが侵害された場合の影響範囲を最小化するため、90 日ごとの自動ローテーションを設定する。

**実装例**:
```bash
# Admin Key を自己ローテーションモードで作成
aws secretsmanager create-secret \
  --name "security/datadog-admin" \
  --secret-string '{
    "adminApiKey": "admin-api-key-value",
    "adminApiKeyId": "admin-api-key-uuid",
    "adminAppKey": "ddapp_admin-app-key-value",
    "adminAppKeyId": "admin-app-key-uuid",
    "serviceAccountId": "service-account-uuid",
    "site": "datadoghq.com"
  }' \
  --secret-type DatadogAdminKey

# 自己ローテーション (adminSecretArn 省略)
aws secretsmanager rotate-secret \
  --secret-id "security/datadog-admin" \
  --rotation-rules '{"AutomaticallyAfterDays": 90}' \
  --role-arn "arn:aws:iam::111122223333:role/DatadogAdminRotationRole"
```

**効果**: 管理キー自体のローテーションにより、認証情報の侵害リスクを全階層で低減。自己ローテーションモードにより追加のシークレット管理が不要

## 料金

AWS Secrets Manager の標準料金が適用される。マネージド外部シークレットやローテーション機能に対する追加料金はない。

### 料金例

| 項目 | 月額料金 (概算) |
|--------|------------------|
| シークレット保存 (1 シークレットあたり) | $0.40 |
| API コール (10,000 回あたり) | $0.05 |
| Datadog 3 タイプ + Snowflake PAT = 4 シークレット | $1.60 |
| ローテーション関連 API コール (月 4 回 x 4 シークレット) | $0.05 未満 |

ローテーションによる新バージョン作成には追加のシークレット保存料金は発生しない。

## 利用可能リージョン

AWS Secrets Manager のマネージド外部シークレットがサポートされているすべての AWS リージョンで利用可能。

## 関連サービス・機能

- **AWS Secrets Manager ローテーション**: Lambda ベースのカスタムローテーションと比較して、マネージド外部シークレットは Lambda 不要で動作
- **AWS CloudTrail**: マネージド外部シークレットの全ローテーション操作が自動的に記録される
- **AWS IAM**: シークレットタイプごとの条件キーによるきめ細かなアクセス制御
- **AWS KMS**: カスタマーマネージドキーによるシークレット値の暗号化

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260522-secrets-manager-managed-external-secrets-datadog-snowflake.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/05/secrets-manager-managed-external-secrets-datadog-snowflake/)
- [マネージド外部シークレット ドキュメント](https://docs.aws.amazon.com/secretsmanager/latest/userguide/managed-external-secrets.html)
- [インテグレーションパートナー一覧](https://docs.aws.amazon.com/secretsmanager/latest/userguide/mes-partners.html)
- [セキュリティと権限](https://docs.aws.amazon.com/secretsmanager/latest/userguide/mes-security.html)
- [料金ページ](https://aws.amazon.com/secrets-manager/pricing/)

## まとめ

AWS Secrets Manager のマネージド外部シークレットに Datadog と Snowflake PAT が追加されたことで、サードパーティ認証情報のライフサイクル管理がさらに簡素化された。カスタム Lambda 関数の開発・運用が不要になり、事前定義されたフォーマットとマネージドローテーションにより、セキュリティベストプラクティスへの準拠を最小限の運用負荷で実現できる。Datadog や Snowflake を利用している組織は、既存の認証情報管理をマネージド外部シークレットに移行することを推奨する。
