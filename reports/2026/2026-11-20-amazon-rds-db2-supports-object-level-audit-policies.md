# Amazon RDS for Db2 - オブジェクトレベル監査ポリシーのサポート

**リリース日**: 2026 年 11 月 20 日
**サービス**: Amazon RDS for Db2
**機能**: オブジェクトレベル監査ポリシー (Object-Level Audit Policies)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261120-amazon-rds-db2-supports-object-level-audit-policies.html)

## 概要

Amazon RDS for Db2 がオブジェクトレベル監査ポリシーをサポートしました。独自の監査ポリシーを作成し、特定のテーブル、ユーザー、グループ、ロール、トラステッドコンテキスト、権限 (Authority) といったデータベースオブジェクトに個別にアタッチできるようになります。これにより、データベース全体ではなく、監査が必要なオブジェクトだけを対象とした、きめ細かな監査が可能になります。

監査ポリシーの作成、変更、アタッチ、デタッチ、削除は、Amazon RDS が提供する `rdsadmin` のストアドプロシージャを通じて行います。記録された監査レコードは、既存の Db2 監査ログ機能で設定済みの Amazon S3 バケットにアップロードされます。機密データを含む特定のテーブルや特定のユーザーの操作のみを監視したい、コンプライアンス要件に対応したいといったニーズを持つデータベース管理者やセキュリティ担当者に有用なアップデートです。

**アップデート前の課題**

- 以前は `rdsadmin.configure_db_audit` によるデータベースレベルの監査ログのみがサポートされており、データベース全体が監査対象となっていた
- 特定のテーブルやユーザーだけを監査したい場合でも、データベース全体の監査レコードが生成され、ログ量が増大しノイズが多かった
- 監査対象を絞り込めないため、監査によるデータベースへの負荷やストレージコストを最適化しにくかった

**アップデート後の改善**

- 特定のテーブル、ユーザー、グループ、ロール、トラステッドコンテキスト、権限に対して個別の監査ポリシーをアタッチできるようになった
- 必要なオブジェクトのみを監査対象とすることで、監査レコードの量と監査オーバーヘッドを抑えられるようになった
- データベースレベルの監査ログとオブジェクトレベル監査ポリシーを同一データベースで併用でき、両者は独立して動作する

## アーキテクチャ図

```mermaid
flowchart TD
    Admin(["👤 データベース管理者"]) --> RDSAdmin["🔧 rdsadmin データベース<br/>ストアドプロシージャ"]

    subgraph Instance["🗄️ RDS for Db2 DB インスタンス DB2_AUDIT オプション有効"]
        RDSAdmin --> Policy["📜 オブジェクトレベル<br/>監査ポリシー"]
        DBAudit["📜 DBA_AUDIT ポリシー<br/>データベースレベル監査"]
        subgraph Objects["📦 監査対象オブジェクト"]
            direction LR
            Table["📋 テーブル"]
            User["👥 ユーザー / グループ"]
            Role["🔑 ロール / 権限"]
            Table ~~~ User ~~~ Role
        end
        Policy -->|アタッチ| Objects
        DBAudit -.->|データベース全体| Instance
    end

    Objects -->|監査レコード生成| Records["📝 Db2 監査レコード"]
    DBAudit -.-> Records
    Records -->|自動アップロード| S3[("🪣 Amazon S3 バケット<br/>db2-audit-logs")]

    classDef user fill:#E3F2FD,stroke:#BBDEFB,stroke-width:2px,color:#1565C0
    classDef process fill:#FFFFFF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef internal fill:#E8F1FF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef storage fill:#DCEDC8,stroke:#C5E1A5,stroke-width:2px,color:#33691E
    classDef layer fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef input fill:#E9F7EC,stroke:#66BB6A,stroke-width:2px,color:#333333

    class Admin user
    class RDSAdmin,Records process
    class Policy,DBAudit internal
    class Table,User,Role input
    class Instance,Objects layer
    class S3 storage
```

ストアドプロシージャで作成した監査ポリシーを特定のオブジェクトにアタッチすると、該当オブジェクトの操作が監査され、監査レコードは既存のデータベースレベル監査と同じ S3 バケットにアップロードされます。

## サービスアップデートの詳細

### 主要機能

1. **カスタム監査ポリシーの作成とオブジェクトへのアタッチ**
   - `rdsadmin.create_audit_policy` で監査カテゴリ、ステータス (SUCCESS / FAILURE / BOTH / NONE)、エラータイプを指定してポリシーを作成
   - `rdsadmin.attach_audit_policy` でテーブル、ユーザー、グループ、ロール、トラステッドコンテキスト、権限にアタッチ
   - 入力データまで監査する場合は `EXECUTE WITH DATA` カテゴリを使用

2. **ストアドプロシージャによるライフサイクル管理**
   - 変更は `rdsadmin.alter_audit_policy` (1 回の呼び出しで 1 カテゴリまたはエラータイプを変更)
   - 付け替えは `rdsadmin.detach_audit_policy` の完了後に `rdsadmin.attach_audit_policy` を実行
   - 削除は全オブジェクトからデタッチした後に `rdsadmin.drop_audit_policy` を実行
   - 各プロシージャは非同期で実行され、`rdsadmin.get_task_status` でタスクの状態を確認可能

3. **データベースレベル監査との併用**
   - `rdsadmin.configure_db_audit` が管理する `DBA_AUDIT` ポリシーと同時に利用でき、両者は独立して動作
   - 同一イベントが両方の対象になった場合は、適用されるすべてのポリシーに従って監査される
   - `rdsadmin.disable_db_audit` を呼び出してもオブジェクトレベル監査ポリシーには影響しない

4. **既存の S3 ベースのログ基盤を利用**
   - 監査レコードは Db2 監査ログで設定済みの S3 バケットのデータベースレベルの場所 (`{bucket}/db2-audit-logs/{dbi_resource_id}/{date_time_utc}/{db_name}/`) にアップロード
   - 監査レコードはカテゴリ単位でファイルに書き込まれ、どちらのポリシー由来でも同じカテゴリのレコードは同じファイルに格納される

## 技術仕様

### 監査ポリシー管理用ストアドプロシージャ

| ストアドプロシージャ | 役割 |
|------|------|
| `rdsadmin.create_audit_policy` | 監査ポリシーの作成 (カテゴリ、ステータス、エラータイプを指定) |
| `rdsadmin.alter_audit_policy` | 監査ポリシーの変更 (1 回の呼び出しで 1 カテゴリ) |
| `rdsadmin.attach_audit_policy` | オブジェクトへの監査ポリシーのアタッチ |
| `rdsadmin.detach_audit_policy` | オブジェクトからの監査ポリシーのデタッチ |
| `rdsadmin.drop_audit_policy` | 監査ポリシーの削除 |
| `rdsadmin.get_task_status` | 非同期タスクの実行状態の確認 |

### ポリシーの確認に使用するカタログビュー

| カタログビュー | 内容 |
|------|------|
| `SYSCAT.AUDITPOLICIES` | 監査ポリシーとその設定 (カテゴリごとのステータス、エラータイプ) |
| `SYSCAT.AUDITUSE` | 監査ポリシーがアタッチされているオブジェクトの一覧 |

### DB インスタンス・データベース操作時の挙動

| 操作 | 挙動 |
|------|------|
| 再起動、フェイルオーバー、インスタンスクラス / ストレージ変更 | ポリシーとアタッチは維持され、監査は継続 |
| `DB2_AUDIT` オプションの削除 | 全データベースのオブジェクトレベル監査ポリシーがデタッチされる (ポリシー自体は保持)。オプション再追加後に再アタッチが必要 |
| `rdsadmin.restore_database` によるリストア | リストアされたデータベースからポリシーが削除される。リストア後に再作成・再アタッチが必要 |
| テーブルの削除 | 該当テーブルへのアタッチが削除される。テーブル再作成後は再アタッチが必要 |
| `rdsadmin.remove_user` によるユーザー削除 | アタッチは維持される。同名ユーザーを後で追加するとそのユーザーが監査される |
| `rdsadmin.disable_db_audit` の呼び出し | オブジェクトレベル監査ポリシーには影響なし |

## 設定方法

### 前提条件

1. RDS for Db2 DB インスタンスが `DB2_AUDIT` オプションを持つオプショングループに関連付けられていること (Db2 監査ログのセットアップ手順 1〜4 を完了)
2. 監査レコードのアップロード先となる Amazon S3 バケットと IAM ロールが設定済みであること
3. `rdsadmin` データベースにマスターユーザーで接続できること (なお、`rdsadmin.configure_db_audit` の呼び出しは不要)

### 手順

#### ステップ 1: 監査ポリシーの作成

```bash
db2 "connect to rdsadmin user {{master_username}} using {{master_password}}"
db2 "call rdsadmin.create_audit_policy(?, 'TESTDB', 'TEST_POLICY', 'EXECUTE WITH DATA', 'BOTH', 'NORMAL')"
```

`rdsadmin` データベースに接続し、`TESTDB` データベースに監査ポリシー `TEST_POLICY` を作成しています。このポリシーは `EXECUTE WITH DATA` カテゴリを対象に、成功・失敗の両方のイベントをエラータイプ `NORMAL` で監査します。呼び出しはタスク ID を返します。

#### ステップ 2: 監査ポリシーのアタッチ

```bash
db2 "call rdsadmin.attach_audit_policy(?, 'TESTDB', 'TABLE', 'TESTSCHEMA.TESTTABLE', 'TEST_POLICY')"
```

`TESTDB` データベースの `TESTSCHEMA.TESTTABLE` テーブルに `TEST_POLICY` をアタッチしています。監査ポリシーはオブジェクトにアタッチするまで何も監査しません。テーブル名はスキーマ付きの `SCHEMA.TABLE` 形式で指定します。

#### ステップ 3: タスクの状態確認

```bash
db2 "select task_id, task_type, database_name, lifecycle,
    varchar(bson_to_json(task_input_params), 500) as task_params,
    cast(task_output as varchar(500)) as task_output
    from table(rdsadmin.get_task_status(null, 'TESTDB', null))
    where task_type like '%AUDIT_POLICY'"
```

ストアドプロシージャは非同期で実行されるため、`rdsadmin.get_task_status` で `CREATE_AUDIT_POLICY` や `ATTACH_AUDIT_POLICY` タスクの `LIFECYCLE` が `SUCCESS` になったことを確認します。失敗時は `ERROR` となり、`TASK_OUTPUT` に SQLSTATE、SQLCODE とエラー詳細が記録されます。

#### ステップ 4: アタッチ状態の確認とログの参照

```bash
db2 "connect to TESTDB user {{master_username}} using {{master_password}}"
db2 "select auditpolicyname, objecttype, objectschema, objectname
    from syscat.audituse
    where auditpolicyname <> 'DBA_AUDIT'"
```

対象データベースに接続し、`SYSCAT.AUDITUSE` カタログビューでポリシーのアタッチ状態を確認しています。アタッチ後、監査レコードが S3 バケットに反映されるまで最低 1 時間待ってから確認します。

## メリット

### ビジネス面

- **コンプライアンス対応の精緻化**: 機密データを含むテーブルや特権ユーザーに限定した監査により、規制要件に沿った証跡を効率的に取得できる
- **コスト最適化**: 必要なオブジェクトのみを監査することで、監査レコードの量と S3 ストレージコストを抑制できる
- **移行の促進**: オンプレミス Db2 で利用していたオブジェクト単位の監査要件を RDS for Db2 でも実現でき、マネージドサービスへの移行障壁が下がる

### 技術面

- **きめ細かな監査制御**: テーブル、ユーザー、グループ、ロール、トラステッドコンテキスト、権限という多様なオブジェクトタイプに対応
- **監査オーバーヘッドの低減**: データベース全体ではなく対象を絞ることで、監査によるデータベース負荷を軽減できる
- **既存基盤との統合**: データベースレベル監査と同じ S3 バケット・同じログ形式を利用するため、既存のログ分析パイプラインをそのまま活用できる

## デメリット・制約事項

### 制限事項

- すべてのオブジェクトレベル監査ポリシー操作 (デタッチ・削除を含む) に `DB2_AUDIT` オプションが必要
- `rdsadmin.create_audit_policy` と `rdsadmin.alter_audit_policy` は 1 回の呼び出しで 1 カテゴリのみ指定可能
- 各オブジェクトにアタッチできる監査ポリシーは 1 つのみ
- `DATABASE`、`SYSADM`、`DBADM` オブジェクトにはアタッチ不可 (データベースレベルは `rdsadmin.configure_db_audit` を使用)
- `DBA_AUDIT` という名前や `RDS_DAS_` で始まる名前のポリシーは作成・変更・アタッチ・削除不可
- Amazon RDS が使用する `RDSDB`、`RDSADMIN`、`SECADMUSER` ユーザーにはアタッチ不可
- ポリシー名とオブジェクト名は Db2 の通常識別子 (最大 128 文字、大文字に変換) である必要があり、二重引用符が必要な名前のオブジェクトは使用不可
- `rdsadmin` データベースでは使用不可

### 考慮すべき点

- `EXECUTE WITH DATA` などのカテゴリは、頻繁に使用されるオブジェクトで大量の監査レコードを生成する可能性があるため、本番適用前にワークロードへの影響をテストする必要がある
- オブジェクトレベルの `ALL` カテゴリは `EXECUTE` と `CONTEXT` を含む全カテゴリが対象であり、`rdsadmin.configure_db_audit` の `ALL` (これらを含まない) とは挙動が異なる
- `DB2_AUDIT` オプションの削除やデータベースのリストアでポリシーのアタッチが失われるため、運用手順に再アタッチ作業を組み込む必要がある

## ユースケース

### ユースケース 1: 機密データテーブルのアクセス監査

**シナリオ**: 個人情報や決済情報を含む特定のテーブルへのすべてのアクセスを、入力データ付きで記録したい。

**実装例**:
```sql
call rdsadmin.create_audit_policy(?, 'PRODDB', 'PII_POLICY', 'EXECUTE WITH DATA', 'BOTH', 'NORMAL')
call rdsadmin.attach_audit_policy(?, 'PRODDB', 'TABLE', 'APP.CUSTOMER_PII', 'PII_POLICY')
```

**効果**: 機密テーブルへのクエリのみが入力データ付きで記録され、データベース全体を監査する場合と比べてログ量とオーバーヘッドを大幅に削減できる。

### ユースケース 2: 特権ユーザーの操作監視

**シナリオ**: `DATAACCESS` 権限を持つユーザーや特定の管理者ユーザーの操作を重点的に監視し、内部不正や誤操作の証跡を残したい。

**実装例**:
```sql
call rdsadmin.create_audit_policy(?, 'PRODDB', 'PRIV_POLICY', 'EXECUTE', 'BOTH', 'NORMAL')
call rdsadmin.attach_audit_policy(?, 'PRODDB', 'USER', 'ADMINUSER01', 'PRIV_POLICY')
```

**効果**: 特権ユーザーの操作履歴のみを S3 に蓄積でき、セキュリティインシデント調査や内部統制の証跡として活用できる。

### ユースケース 3: 失敗した認可チェックの検知

**シナリオ**: 権限のないアクセス試行を検知するため、認可チェックの失敗イベントだけを記録したい。

**実装例**:
```sql
call rdsadmin.create_audit_policy(?, 'PRODDB', 'AUTHFAIL_POLICY', 'CHECKING', 'FAILURE', 'NORMAL')
call rdsadmin.attach_audit_policy(?, 'PRODDB', 'TABLE', 'APP.FINANCE_LEDGER', 'AUTHFAIL_POLICY')
```

**効果**: 失敗した認可チェックのみが記録されるため、不正アクセスの兆候を低ノイズで検知でき、S3 上のログを分析基盤に連携してアラートを構成できる。

## 料金

オブジェクトレベル監査ポリシー機能自体に追加料金はありません。監査レコードの保存先となる Amazon S3 の標準的なストレージ料金とリクエスト料金が発生します。監査カテゴリと対象オブジェクトの範囲によってログ量が変わるため、必要最小限の監査設定にすることでコストを抑制できます。

## 利用可能リージョン

Amazon RDS for Db2 が利用可能なすべての AWS リージョンで利用できます。

## 関連サービス・機能

- **Db2 監査ログ (データベースレベル)**: `rdsadmin.configure_db_audit` による既存のデータベース全体の監査機能。オブジェクトレベル監査ポリシーと併用可能
- **Amazon S3**: 監査レコードのアップロード先。既存の Db2 監査ログと同じバケット・同じ場所を使用
- **AWS IAM**: RDS が S3 バケットへ監査レコードをアップロードするためのロールと権限の管理

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261120-amazon-rds-db2-supports-object-level-audit-policies.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-rds-db2-supports-object-level-audit-policies)
- [ドキュメント: Db2 object-level audit policies](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/db2-object-level-audit.html)
- [ドキュメント: Db2 audit logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Db2.Options.Audit.html)
- [料金ページ: Amazon RDS for Db2](https://aws.amazon.com/rds/db2/pricing/)

## まとめ

Amazon RDS for Db2 のオブジェクトレベル監査ポリシーにより、機密テーブルや特権ユーザーなど監査が必要な対象だけを狙い撃ちした、きめ細かな監査が可能になりました。既存のデータベースレベル監査と独立して併用でき、同じ S3 バケットにログが集約されるため、導入の手間も小さいアップデートです。コンプライアンス要件を持つ RDS for Db2 利用者は、`DB2_AUDIT` オプションを有効化した上で、監査対象を絞り込んだポリシー設計から始めることを推奨します。
