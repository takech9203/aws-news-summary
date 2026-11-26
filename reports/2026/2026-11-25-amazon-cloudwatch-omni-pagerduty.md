# Amazon CloudWatch Omni - PagerDuty 統合

**リリース日**: 2026 年 11 月 25 日
**サービス**: Amazon CloudWatch Omni
**機能**: PagerDuty インテグレーション (アラートからの PagerDuty インシデント自動作成)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261125-amazon-cloudwatch-omni-pagerduty.html)

## 概要

Amazon CloudWatch Omni が PagerDuty との統合に対応しました。CloudWatch Omni は、AI エージェント、アプリケーション、インフラストラクチャを横断して監視できる、オープンスタンダードに基づいたフルマネージドの AI 搭載オブザーバビリティ体験です。今回のアップデートにより、CloudWatch Omni のアラートから PagerDuty インシデントを自動的に作成できるようになり、既存のインシデント管理ワークフローに通知を直接組み込めるようになりました。

PagerDuty に送信されたアラートは、既存のオンコールスケジュールとエスカレーションポリシーに従ってルーティングされるため、緊急性の高い問題が時間帯を問わず適切な担当者に届きます。各アラートには重要度、影響を受けるサービス、CloudWatch Omni 内の関連データへのリンクが含まれており、対応者は診断に必要なコンテキストをすぐに把握できます。手動での通知手順を排除し、一貫したインシデントワークフローを確保することで、平均復旧時間 (MTTR) の短縮に貢献します。

**アップデート前の課題**

このアップデート以前には、以下の課題がありました。

- CloudWatch Omni のアラートを PagerDuty のインシデントに変換するには、手動での通知や独自の中継実装が必要だった
- アラート発生から担当者への通知までに手動のステップが介在し、対応開始が遅れる要因となっていた
- PagerDuty 側のオンコールスケジュールやエスカレーションポリシーと CloudWatch Omni のアラートを連動させる標準的な仕組みがなかった

**アップデート後の改善**

今回のアップデートにより、以下が可能になりました。

- CloudWatch Omni のアラートから PagerDuty インシデントが自動的に作成されるようになった
- 既存のオンコールスケジュールとエスカレーションポリシーをそのまま活用し、適切な担当者へ確実に通知できるようになった
- 重要度、影響サービス、Omni 内の関連データへのリンクがアラートに含まれ、対応者が診断コンテキストを即座に確認できるようになった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph Omni["☁️ Amazon CloudWatch Omni スペース"]
        direction LR
        Alert["🚨 アラート"]
        Profile["🔐 アクセスプロファイル<br/>InvokeIntegration 権限"]
        Integ["🔌 PagerDuty<br/>インテグレーション"]
        Alert ~~~ Profile ~~~ Integ
    end

    subgraph PD["🏢 PagerDuty"]
        direction LR
        Svc["🛎️ サービス"]
        Esc["📋 エスカレーション<br/>ポリシー"]
        Svc ~~~ Esc
    end

    Signal(["📈 メトリクス / ログ / トレース"]) --> Alert
    Alert --> Profile
    Profile --> Integ
    Integ -->|"Events API v2<br/>trigger / resolve"| Svc
    Svc --> Esc
    Esc --> OnCall(["👤 オンコール担当者"])

    classDef space fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef internal fill:#E8F1FF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef decision fill:#F3E5F5,stroke:#7B61FF,stroke-width:2px,color:#333333
    classDef external fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#5D4037
    classDef input fill:#E9F7EC,stroke:#66BB6A,stroke-width:2px,color:#333333

    class Omni,PD space
    class Alert,Integ internal
    class Profile decision
    class Svc,Esc external
    class Signal,OnCall input
```

CloudWatch Omni のアラートが発火すると、アクセスプロファイルによる権限チェックを経て、PagerDuty Events API v2 経由でイベントが送信され、PagerDuty 側のサービスとエスカレーションポリシーに従ってオンコール担当者に通知されます。

## サービスアップデートの詳細

### 主要機能

1. **PagerDuty インシデントの自動作成**
   - CloudWatch Omni のアラートが発火すると、PagerDuty Events API v2 のイベントが自動送信される
   - アラートの状態 (Critical / Warning / No data / OK) に応じて trigger または resolve イベントが送信される
   - 重要度、影響サービス、Omni 内の関連データへのリンクがイベントに含まれる

2. **既存のインシデント管理ワークフローとの連動**
   - PagerDuty 側の既存のオンコールスケジュールとエスカレーションポリシーをそのまま利用できる
   - アラートの通知先として、連携済みの PagerDuty サービスを個別に選択できる
   - 連携時に追加した PagerDuty サービスのみが通知先の候補として表示される

3. **インシデントの重複排除と自動解決**
   - デフォルトでは、1 つのアラートから発生するすべてのイベントがアラートの ARN を重複排除キーとして共有し、アラートごとに 1 件のインシデントが開かれる
   - 後続の Critical イベントはインシデントの重要度を引き上げ、OK イベントはインシデントを解決する
   - 通知ルールの追加設定で、独自の重複排除キーや class、group、component フィールドを指定できる

4. **アクセスプロファイルによる通知制御**
   - アラートのアクセスプロファイルにインテグレーションへの権限付与 (grant) が必要
   - 権限は通知設定の保存時と配信のたびにチェックされ、権限を取り消すと既存アラートの通知も停止する
   - 権限付与は特定の PagerDuty サービス ID に限定することも可能

## 技術仕様

### アラート状態と PagerDuty イベントのマッピング

| アラート状態 | イベントアクション | 重要度 (Severity) |
|------|------|------|
| Critical | trigger | critical |
| Warning | trigger | warning |
| No data | trigger | error |
| OK | resolve | info |

### 統合の仕様

| 項目 | 詳細 |
|------|------|
| 接続単位 | スペース全体に適用 (1 人が接続すればスペース全員が利用可能) |
| 接続数の制限 | 1 リージョン内で 1 AWS アカウントにつき 1 つの PagerDuty 接続 |
| 認証方式 | PagerDuty の Scoped OAuth アプリ (Amazon CloudWatch Omni アプリ) |
| PagerDuty 側の権限 | 読み取り専用 (`services.read`、`event_orchestrations.read` スコープ) |
| 送信プロトコル | PagerDuty Events API v2 |
| サービスリージョン | US / EU を選択可能 (EU アカウントのイベントは PagerDuty の EU サービスリージョン内に留まる) |

### アクセスプロファイルの権限付与の例

アラートの通知を許可するには、アクセスプロファイルに `cloudwatch:InvokeIntegration` の権限付与が必要です。以下は 2 つの PagerDuty サービスに限定した権限付与の例です。

```json
{
  "name": "pagerduty-alert-integration",
  "permission": "CUSTOM",
  "scopedActions": [
    {
      "actions": ["cloudwatch:InvokeIntegration"],
      "resources": [
        {
          "resourceType": "Integration",
          "resourceArns": ["arn:aws:cloudwatch:{{region}}:{{account-id}}:integration/{{integration-id}}"]
        }
      ],
      "contextConditions": { "serviceIds": ["{{PABC123}}", "{{PDEF456}}"] }
    }
  ]
}
```

- `contextConditions` を省略すると、PagerDuty アカウント内のすべてのサービスが許可されます
- 1 つの `scopedActions` エントリで制限できるのは `channelNames` または `serviceIds` のいずれか一方のみです。Slack と PagerDuty は別々のエントリで権限付与します

## 設定方法

### 前提条件

1. CloudWatch Omni のスペースが作成済みであること
2. PagerDuty アカウントを保有しており、Admin またはアカウントオーナーがアプリをインストールできること
3. 統合を管理するメンバーに、インテグレーションの作成・更新・削除アクションの権限付与があること

### 手順

#### ステップ 1: PagerDuty に Amazon CloudWatch Omni アプリをインストールする

1. CloudWatch Omni の [Settings] から [Integrations] を選択します
2. [PagerDuty] カードで、PagerDuty アカウントのサービスリージョン (US または EU) を選択します
3. [Install the app in PagerDuty] を選択すると、PagerDuty のアプリページが開きます
4. PagerDuty の Admin またはアカウントオーナーとしてサインインし、スコープを確認して [Install on your account] を選択します

PagerDuty アカウントごとに 1 回インストールすれば、スペース内の誰でも PagerDuty を接続できるようになります。Admin でない場合は、インストールリンクをコピーして Admin に送付します。

#### ステップ 2: PagerDuty アカウントを接続する

1. [Settings] の [Integrations] ページで [PagerDuty] カードのサービスリージョンを選択します
2. [Enable] を選択すると PagerDuty が開きます
3. PagerDuty にサインインし、Amazon CloudWatch Omni アプリを承認します

接続が完了すると、[PagerDuty] カードに [Connected] と表示され、PagerDuty アカウント、サービスリージョン、インテグレーションの ARN が確認できます。

#### ステップ 3: 通知先となる PagerDuty サービスを追加する

1. 接続済みの [PagerDuty] カードで [Add services] を選択します
2. PagerDuty 側で対象サービスを選択すると、各サービスに Amazon CloudWatch Omni アプリのインテグレーションが追加されます

接続しただけではサービスは追加されません。アラートの通知先に指定できるのは、この手順で追加したサービスのみです。サービスは後からいつでも追加できます。

#### ステップ 4: アラートの通知先に PagerDuty サービスを設定する

アラートの通知先 (destinations) の設定で PagerDuty サービスを選択します。アラートのアクセスプロファイルに権限付与がない状態で保存しようとすると拒否されるため、[Grant permission] から権限付与を追加してから再度保存します。新しい権限付与が有効になるまで数分かかる場合があります。インシデントを自動解決させたい場合は、通知ルールのアラート状態に OK を含めます。

## メリット

### ビジネス面

- **MTTR の短縮**: 手動の通知ステップを排除し、アラート発生から担当者への通知までを自動化することで、平均復旧時間を短縮できる
- **既存投資の活用**: PagerDuty で構築済みのオンコールスケジュールやエスカレーションポリシーをそのまま活用でき、運用プロセスの再構築が不要
- **一貫したインシデントワークフロー**: すべてのアラートが同じインシデント管理プロセスを通るため、対応品質のばらつきを低減できる

### 技術面

- **豊富な診断コンテキスト**: 重要度、影響サービス、Omni 内の関連データへのリンクがアラートに含まれ、対応者が即座に調査を開始できる
- **インテリジェントな重複排除**: アラート単位でインシデントが集約され、重要度の自動引き上げと OK 時の自動解決により、インシデントのライフサイクルが自動管理される
- **最小権限の設計**: Omni が PagerDuty に持つのは読み取り専用スコープのみで、アクセスプロファイルによりアラートごと・サービスごとに通知を細かく制御できる

## デメリット・制約事項

### 制限事項

- 1 リージョン内で 1 AWS アカウントにつき接続できる PagerDuty アカウントは 1 つのみ (別アカウントに接続するには一度無効化して再接続が必要)
- アラートの通知先に指定できるのは、[Add services] で明示的に追加した PagerDuty サービスのみ
- 1 つの `scopedActions` エントリで `channelNames` と `serviceIds` の両方を制限することはできない
- CloudWatch Omni 自体の利用可能リージョンに依存する

### 考慮すべき点

- アクセスプロファイルの権限付与は配信のたびにチェックされるため、権限を取り消すと稼働中のアラート通知も停止する。アラートが発火しても PagerDuty にインシデントが開かれない場合は、まずプロファイルを確認する
- 統合を無効化しても、インテグレーションへの権限付与や PagerDuty サービス側のアプリインテグレーションは削除されない
- インシデントの自動解決を利用するには、通知ルールのアラート状態に OK を含める必要がある
- 新しい権限付与が有効になるまで数分かかる場合がある

## ユースケース

### ユースケース 1: 24 時間 365 日のオンコール体制との連動

**シナリオ**: グローバルにサービスを展開する企業が、PagerDuty のフォローザサン型オンコールスケジュールを運用しており、CloudWatch Omni で検知した重大なアラートを時間帯に応じた担当者へ自動的にエスカレーションしたい。

**実装例**:
```
1. PagerDuty に Amazon CloudWatch Omni アプリをインストール
2. CloudWatch Omni のスペースで PagerDuty を接続し、本番サービスを追加
3. 重要メトリクスのアラートの通知先に該当 PagerDuty サービスを設定
4. アラート状態に Critical / Warning / OK を含め、自動解決も有効化
```

**効果**: 深夜や休日でも既存のエスカレーションポリシーに従って適切な担当者に自動で通知され、人手による連絡の遅延や漏れがなくなる。

### ユースケース 2: アラートの重複によるノイズの抑制

**シナリオ**: 同一の障害で状態変化が繰り返されるたびにインシデントが乱立し、対応者が本質的な問題に集中できない。

**実装例**:
```
1. デフォルトの重複排除キー (アラートの ARN) を利用し、アラートごとに 1 インシデントへ集約
2. 必要に応じて通知ルールの PagerDuty 追加設定で独自の重複排除キーを指定し、
   複数アラートを 1 つのインシデントにまとめる
3. class / group / component フィールドを設定し、PagerDuty のイベントルールで分類
```

**効果**: インシデントの乱立を防ぎ、重要度の自動引き上げと OK イベントによる自動解決でインシデント管理の運用負荷を削減できる。

### ユースケース 3: チームごとの通知権限の分離

**シナリオ**: 複数チームが同じ CloudWatch Omni スペースを共有しており、各チームのアラートが自チーム担当の PagerDuty サービスのみに通知されるよう統制したい。

**実装例**:
```json
{
  "name": "team-a-pagerduty",
  "permission": "CUSTOM",
  "scopedActions": [
    {
      "actions": ["cloudwatch:InvokeIntegration"],
      "resources": [
        {
          "resourceType": "Integration",
          "resourceArns": ["arn:aws:cloudwatch:ap-northeast-1:123456789012:integration/example-id"]
        }
      ],
      "contextConditions": { "serviceIds": ["PABC123"] }
    }
  ]
}
```

**効果**: アクセスプロファイルの権限付与を PagerDuty サービス ID 単位で制限することで、チーム間の誤通知を防ぎ、ガバナンスを維持したままスペースを共有できる。

## 料金

公式発表には本統合に関する追加料金の記載はありません。CloudWatch Omni 自体の料金は Amazon CloudWatch の料金ページを参照してください。PagerDuty 側の料金は PagerDuty の契約プランに準じます。

## 利用可能リージョン

本統合は CloudWatch Omni が利用可能なすべてのリージョンで提供されます。ドキュメントによると、CloudWatch Omni は以下のリージョンで利用可能です。

- 米国東部 (バージニア北部、オハイオ)
- 米国西部 (オレゴン)
- カナダ (中部)
- 南米 (サンパウロ)
- アジアパシフィック (ムンバイ、シンガポール、シドニー、東京)
- 欧州 (フランクフルト、アイルランド、ロンドン)

## 関連サービス・機能

- **Amazon CloudWatch**: Omni の基盤となるオブザーバビリティサービス。メトリクス、ログ、トレースを収集・分析する
- **CloudWatch Omni アラート**: 本統合の通知元となるアラート機能。通知先 (destinations) として PagerDuty サービスを指定する
- **CloudWatch Omni アクセスプロファイル**: アラートからインテグレーションへの通知可否を制御する権限管理の仕組み
- **Slack 統合**: CloudWatch Omni が対応するもう 1 つの外部通知先。権限付与は PagerDuty とは別エントリで設定する

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261125-amazon-cloudwatch-omni-pagerduty.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-cloudwatch-omni-pagerduty/)
- [ドキュメント: Amazon CloudWatch Omni](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-omni.html)
- [ドキュメント: Connect PagerDuty](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/omni-connect-pagerduty.html)
- [ドキュメント: Supported Regions for CloudWatch Omni](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/omni-supported-regions.html)
- [料金ページ: Amazon CloudWatch](https://aws.amazon.com/cloudwatch/pricing/)

## まとめ

CloudWatch Omni と PagerDuty の統合により、アラートから担当者への通知までが完全に自動化され、既存のオンコール体制をそのまま活かしたインシデント対応が可能になりました。PagerDuty を利用中で CloudWatch Omni を導入している、または検討しているチームは、まず PagerDuty アプリのインストールと通知先サービスの追加を行い、重要なアラートの通知先として設定することを推奨します。
