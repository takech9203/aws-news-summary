# AWS Transfer Family - SFTP Connectors の認証情報ローテーション中のファイル転送継続サポート

**リリース日**: 2026 年 9 月 4 日
**サービス**: AWS Transfer Family
**機能**: SFTP Connectors における Secrets Manager バージョンステージのフォールバック (Secret version fallback)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260904-transfer-family-sftp-credential-rotation.html)

## 概要

AWS Transfer Family SFTP Connectors が、リモート SFTP サーバーへの認証に使用する認証情報のローテーション中も、ファイル転送を中断せずに継続できるようになりました。SFTP コネクタの設定で、AWS Secrets Manager のバージョンステージの順序付きリスト (例: `["AWSCURRENT", "AWSPREVIOUS"]`) を指定できるようになり、コネクタは認証時に指定した順序で各バージョンの認証情報を試行し、最初に認証に成功したものを使用してファイル転送を継続します。

これまでは、コネクタはデフォルトでシークレットの現在のバージョン (AWSCURRENT) のみを使用して認証を試行していました。そのため、パスワードや SSH 秘密鍵をローテーションした際に、外部パートナー側のリモート SFTP サーバーで新しい認証情報への更新が完了するまでの間、認証エラーによる転送失敗が発生する可能性がありました。今回のアップデートにより、どちらの側が先に認証情報を更新しても転送が継続されるため、ダウンタイムのないグレースフルな認証情報ローテーションを実現できます。

外部パートナーと B2B ファイル転送を行っている企業や、セキュリティポリシーとして定期的な認証情報ローテーションが義務付けられている組織にとって、運用負荷とリスクを大きく軽減するアップデートです。バージョンステージのリストはコネクタに一度設定するだけでよく、以降のローテーションで手動での介入は不要です。

**アップデート前の課題**

- コネクタはデフォルトでシークレットの現在のバージョンのみで認証を試行するため、ローテーションのタイミングによっては認証エラーが発生していた
- 外部パートナーがリモート SFTP サーバー側の認証情報を新しいものに更新するまでに時間がかかる場合、その間の転送が失敗するリスクがあった
- 転送失敗を避けるには、パートナーとローテーションのタイミングを綿密に調整するか、失敗時のリトライや再実行の仕組みを別途用意する必要があった

**アップデート後の改善**

- Secrets Manager のバージョンステージの順序付きリストを指定でき、コネクタが順番に試行して最初に認証に成功した認証情報で転送を継続するようになった
- 自社とパートナーのどちらが先に認証情報を更新しても、転送を中断せずにローテーションを完了できるようになった
- 設定は一度行うだけでよく、以降のローテーションでは手動での対応が不要になった

## アーキテクチャ図

```mermaid
sequenceDiagram
    participant WF as ⚙️ 転送ワークフロー
    participant C as 🔌 SFTP コネクタ
    participant SM as 🔐 Secrets Manager
    participant R as 🖥️ リモート SFTP サーバー

    Note over SM: 認証情報ローテーション実施<br/>AWSCURRENT が新しい認証情報に

    WF->>C: ファイル転送リクエスト
    C->>SM: AWSCURRENT の認証情報を取得
    C->>R: 新しい認証情報で認証を試行
    alt パートナー側が更新済み
        R-->>C: 認証成功
        C->>R: ファイル転送を実行
    else パートナー側が未更新
        R-->>C: 認証失敗
        C->>SM: AWSPREVIOUS の認証情報を取得
        C->>R: 以前の認証情報で認証を試行
        R-->>C: 認証成功
        C->>R: ファイル転送を実行
    end
    C-->>WF: 転送完了
```

`OrderedUserSecretVersionStages` に `["AWSCURRENT", "AWSPREVIOUS"]` を設定した場合の認証フローです。新しい認証情報での認証に失敗した場合、コネクタは自動的に以前の認証情報にフォールバックして転送を継続します。

## サービスアップデートの詳細

### 主要機能

1. **バージョンステージの順序付きリストによるフォールバック認証**
   - コネクタの `SftpConfig` に新しいパラメータ `OrderedUserSecretVersionStages` が追加された
   - Secrets Manager のバージョンステージ (例: `AWSCURRENT`、`AWSPREVIOUS`) を試行したい順序で指定する
   - コネクタは認証時にリストの先頭から順に各バージョンステージの認証情報を試行し、最初に認証に成功したものを使用する
   - 例として `["AWSCURRENT", "AWSPREVIOUS"]` を設定すると、まず新しい認証情報を試行し、失敗した場合に以前の認証情報へフォールバックする

2. **ダウンタイムのないグレースフルなローテーション**
   - 自社側で Secrets Manager のシークレットをローテーションした後、パートナー側のリモートサーバーの更新が遅れても転送が失敗しない
   - 逆にパートナー側が先に新しい認証情報へ切り替えた場合でも、新しいバージョンから試行するため転送を継続できる
   - ローテーションのタイミングをパートナーと厳密に同期させる必要がなくなる

3. **一度の設定で以降のローテーションに自動対応**
   - バージョンステージのリストはコネクタの作成時 (`CreateConnector`) または更新時 (`UpdateConnector`) に一度設定するだけでよい
   - 以降のローテーションでは、コネクタ側の設定変更などの手動介入は不要
   - 設定内容は `DescribeConnector` で確認できる

## 技術仕様

### Secret version fallback の仕様

| 項目 | 詳細 |
|------|------|
| 設定パラメータ | `SftpConfig.OrderedUserSecretVersionStages` (文字列のリスト) |
| 対象 API | `CreateConnector`、`UpdateConnector`、`DescribeConnector` |
| 指定する値 | Secrets Manager のバージョンステージ (例: `AWSCURRENT`、`AWSPREVIOUS`) |
| 試行順序 | リストの先頭から順に試行し、最初に認証に成功したバージョンを使用 |
| デフォルト動作 | 未設定の場合は従来どおり現在のバージョンのみで認証を試行 |
| シークレットの形式 | `Username` (必須) と、`Password` または `PrivateKey` の一方または両方 |
| 制約 | すべてのバージョンステージで `Username` は同一である必要がある |

### API 変更履歴

| 日付 | サービス | 変更内容 |
|------|----------|----------|
| 2026/09/03 | [AWS Transfer Family](https://awsapichanges.com/archive/changes/35b7c0-transfer.html) | 3 updated api methods - `CreateConnector`、`UpdateConnector`、`DescribeConnector` の `SftpConfig` に `OrderedUserSecretVersionStages` パラメータを追加 |

### SftpConfig の設定例

```json
{
    "SftpConfig": {
        "UserSecretId": "arn:aws:secretsmanager:us-east-1:123456789012:secret:aws/transfer/connector-1",
        "TrustedHostKeys": [
            "ssh-rsa AAAAB3Nza..."
        ],
        "OrderedUserSecretVersionStages": [
            "AWSCURRENT",
            "AWSPREVIOUS"
        ]
    }
}
```

## 設定方法

### 前提条件

1. AWS Transfer Family の SFTP コネクタが作成済みであること (新規作成時にも設定可能)
2. リモート SFTP サーバーへの認証情報が AWS Secrets Manager に保存されていること (`Username` と、`Password` または `PrivateKey`)
3. コネクタのアクセスロールに、対象シークレットへの `secretsmanager:GetSecretValue` 権限が付与されていること

### 手順

#### ステップ 1: Secrets Manager にコネクタ用のシークレットを保存する

```bash
aws secretsmanager create-secret \
    --name "aws/transfer/connector-1" \
    --secret-string '{"Username": "partner-user", "Password": "current-password"}'
```

リモート SFTP サーバーへの認証に使用するユーザー名とパスワード (または秘密鍵) を Secrets Manager に保存しています。シークレット名には `aws/transfer/` のプレフィックスを使用することが推奨されています。なお、パスフレーズ付きの秘密鍵は SFTP コネクタの認証に使用できません。

#### ステップ 2: コネクタにバージョンステージの順序付きリストを設定する

```bash
aws transfer update-connector \
    --connector-id c-1234567890abcdef0 \
    --sftp-config '{
        "UserSecretId": "arn:aws:secretsmanager:us-east-1:123456789012:secret:aws/transfer/connector-1",
        "OrderedUserSecretVersionStages": ["AWSCURRENT", "AWSPREVIOUS"]
    }'
```

既存のコネクタに対して、認証時に試行するバージョンステージの順序を設定しています。この例では、まず現在のバージョン (AWSCURRENT) の認証情報を試行し、認証に失敗した場合に以前のバージョン (AWSPREVIOUS) へフォールバックします。新規作成の場合は `create-connector` で同じパラメータを指定します。

#### ステップ 3: 設定を確認し、認証情報をローテーションする

```bash
# コネクタの設定を確認
aws transfer describe-connector \
    --connector-id c-1234567890abcdef0

# シークレットをローテーション (新しいバージョンが AWSCURRENT になる)
aws secretsmanager put-secret-value \
    --secret-id "aws/transfer/connector-1" \
    --secret-string '{"Username": "partner-user", "Password": "new-password"}'
```

`describe-connector` で `OrderedUserSecretVersionStages` の設定を確認した後、`put-secret-value` でシークレットの新しいバージョンを保存しています。ローテーション後、新しいバージョンが `AWSCURRENT`、以前のバージョンが `AWSPREVIOUS` となり、コネクタは両方を順に試行するため、パートナー側の更新が完了するまでの間も転送が継続されます。ローテーション時には、すべてのバージョンで `Username` を同一に保つ必要があります。

## メリット

### ビジネス面

- **転送失敗によるビジネス影響の回避**: 請求データや受発注データなど、業務上重要な B2B ファイル転送が認証情報ローテーションを理由に失敗するリスクを排除できる
- **パートナーとの調整負荷の軽減**: ローテーションのタイミングを外部パートナーと厳密に同期させる必要がなくなり、調整コストを削減できる
- **コンプライアンス対応の促進**: 転送失敗を恐れてローテーションを先送りすることがなくなり、定期的な認証情報ローテーションのポリシーを確実に実施できる

### 技術面

- **設定は一度だけ**: バージョンステージのリストをコネクタに一度設定すれば、以降のローテーションで手動介入が不要になる
- **双方向のローテーションに対応**: 自社側とパートナー側のどちらが先に認証情報を更新しても、順序付き試行により転送が継続される
- **Secrets Manager の標準機能との統合**: Secrets Manager の標準的なバージョンステージ (`AWSCURRENT`、`AWSPREVIOUS`) の仕組みをそのまま活用でき、自動ローテーション機能とも組み合わせられる

## デメリット・制約事項

### 制限事項

- 認証情報は AWS Secrets Manager に保存されている必要がある
- すべてのバージョンステージで `Username` は同一である必要がある (バージョンステージごとに異なるユーザー名は使用できない。ユーザー名を変更する場合は、同一シークレット内でのローテーションではなく、`UserSecretId` を新しいシークレットに変更する)
- パスフレーズ付きの秘密鍵は SFTP コネクタの認証に使用できない

### 考慮すべき点

- 古い認証情報へのフォールバックを許容する期間が長くなると、漏えいした旧認証情報が使用され続けるリスクがあるため、パートナー側の更新完了後は速やかに旧バージョンを無効化する運用が望ましい
- フォールバック認証が発生した場合は認証試行が複数回行われるため、リモートサーバー側のログイン失敗ロックアウト設定によっては注意が必要
- 既定ではフォールバックは行われないため、この機能を利用するにはコネクタに `OrderedUserSecretVersionStages` を明示的に設定する必要がある

## ユースケース

### ユースケース 1: 外部パートナーとの B2B ファイル転送での定期パスワードローテーション

**シナリオ**: 取引先の SFTP サーバーに日次で請求データを送信している。セキュリティポリシーにより 90 日ごとのパスワードローテーションが必須だが、取引先側でのパスワード更新作業に数日かかることがあり、その間の転送失敗が課題となっている。

**実装例**:
```json
{
    "SftpConfig": {
        "UserSecretId": "arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:aws/transfer/partner-a",
        "OrderedUserSecretVersionStages": ["AWSCURRENT", "AWSPREVIOUS"]
    }
}
```

**効果**: 自社側でシークレットをローテーションした後、取引先側の更新が完了するまでの間は自動的に以前のパスワードで認証が継続されるため、日次転送が失敗しない。取引先の更新完了後は新しいパスワードでの認証に自動的に切り替わる。

### ユースケース 2: SSH 鍵ペアの安全な移行

**シナリオ**: パートナーの SFTP サーバーへの認証に SSH 秘密鍵を使用しており、鍵の世代交代を計画している。パートナー側で新しい公開鍵の登録と旧公開鍵の削除が段階的に行われるため、切り替え期間中も転送を継続したい。

**実装例**:
```bash
# 新しい秘密鍵をシークレットの新バージョンとして保存
aws secretsmanager put-secret-value \
    --secret-id "aws/transfer/partner-b" \
    --secret-string '{"Username": "partner-user", "PrivateKey": "-----BEGIN OPENSSH PRIVATE KEY-----\n..."}'
```

**効果**: パートナー側に新しい公開鍵が登録されていれば新しい鍵で認証され、まだ登録されていない場合は AWSPREVIOUS の旧鍵で認証される。鍵の移行期間中もイベント駆動の転送ワークフローを停止する必要がない。

### ユースケース 3: Secrets Manager の自動ローテーションとの組み合わせ

**シナリオ**: 多数のパートナー向けコネクタを運用しており、Secrets Manager の自動ローテーション (Lambda ローテーション関数) で認証情報を定期更新している。ローテーション直後の転送失敗によるアラート対応が運用負荷となっている。

**実装例**:
```bash
aws transfer update-connector \
    --connector-id c-abcdef1234567890 \
    --sftp-config '{
        "UserSecretId": "arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:aws/transfer/partner-c",
        "OrderedUserSecretVersionStages": ["AWSCURRENT", "AWSPREVIOUS"]
    }'
```

**効果**: 自動ローテーションの実行タイミングとパートナー側の更新タイミングのずれを気にする必要がなくなり、ローテーション起因の転送失敗アラートと再実行対応が不要になる。多数のコネクタでも一度の設定で以降の運用が自動化される。

## 料金

この機能自体に追加料金はありません。関連する料金は以下のとおりです。

- **AWS Transfer Family SFTP コネクタ**: 従来どおりの SFTP コネクタの利用料金が適用されます。詳細は [AWS Transfer Family の料金ページ](https://aws.amazon.com/aws-transfer-family/pricing/) を参照してください
- **AWS Secrets Manager**: シークレットの保存 (シークレットあたり月額 0.40 USD) と API コール (10,000 コールあたり 0.05 USD) に対する料金が発生します。詳細は [AWS Secrets Manager の料金ページ](https://aws.amazon.com/secrets-manager/pricing/) を参照してください

## 利用可能リージョン

AWS Transfer Family SFTP Connectors がサポートされているすべての AWS リージョンで利用可能です。

## 関連サービス・機能

- **AWS Secrets Manager**: コネクタの認証情報の保存先。バージョンステージ (`AWSCURRENT`、`AWSPREVIOUS`、`AWSPENDING`) と自動ローテーション機能を提供し、今回の機能の基盤となる
- **AWS Transfer Family SFTP Connectors**: Amazon S3 とリモート SFTP サーバー間のファイル送受信を行うフルマネージドのコネクタ。サービスマネージド型と VPC Lattice 経由の VPC 型のエグレスをサポート
- **Amazon EventBridge / AWS Step Functions**: SFTP コネクタと組み合わせたイベント駆動のファイル転送ワークフローの構築に使用。ローテーション中も転送が継続されることでワークフローの信頼性が向上する

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260904-transfer-family-sftp-credential-rotation.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/09/transfer-family-sftp-credential-rotation/)
- [ドキュメント: Store authentication credentials for SFTP connectors in Secrets Manager (Secret version fallback)](https://docs.aws.amazon.com/transfer/latest/userguide/sftp-connector-secret-procedure.html)
- [ドキュメント: AWS Transfer Family SFTP connectors](https://docs.aws.amazon.com/transfer/latest/userguide/creating-connectors.html)
- [ドキュメント: AWS Secrets Manager のバージョンステージ](https://docs.aws.amazon.com/secretsmanager/latest/userguide/getting-started.html#term_version-stage)
- [料金ページ](https://aws.amazon.com/aws-transfer-family/pricing/)

## まとめ

AWS Transfer Family SFTP Connectors の Secret version fallback により、外部パートナーとの認証情報ローテーションに伴う転送失敗のリスクを排除し、ダウンタイムのないグレースフルなローテーションを実現できます。SFTP コネクタを利用している場合は、`OrderedUserSecretVersionStages` に `["AWSCURRENT", "AWSPREVIOUS"]` を設定することを推奨します。一度の設定で以降のローテーションが自動対応となり、定期的な認証情報ローテーションのポリシーを安心して運用できます。
