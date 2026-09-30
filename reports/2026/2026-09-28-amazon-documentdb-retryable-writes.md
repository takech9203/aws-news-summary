# Amazon DocumentDB - 再試行可能な書き込み (Retryable Writes) のサポート

**リリース日**: 2026 年 9 月 28 日
**サービス**: Amazon DocumentDB (with MongoDB compatibility)
**機能**: 再試行可能な書き込み (Retryable Writes)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260928-amazon-documentdb-retryable-writes.html)

## 概要

Amazon DocumentDB (with MongoDB compatibility) が、エンジンバージョン 8.0.2 以降で再試行可能な書き込み (Retryable Writes) をサポートしました。再試行可能な書き込みは、ネットワークの一時的な中断やプライマリインスタンスのフェイルオーバーなどの一時的なエラーが発生した際に、MongoDB ドライバーが対象の書き込みオペレーションを自動的に 1 回だけ再試行する機能です。Amazon DocumentDB 側で再試行された書き込みを重複排除するため、オペレーションは最大 1 回のみ適用され、冪等性が保たれます。

現行の MongoDB 互換ドライバーの多くは、デフォルトで再試行可能な書き込みを有効 (`retryWrites=true`) にしています。これまで Amazon DocumentDB ではこの機能が未サポートだったため、接続文字列に `retryWrites=false` を明示的に指定してエラーを回避する必要がありました。今回のリリースにより、Amazon DocumentDB 8.0.2 に接続するアプリケーションではこの指定が不要になり、追加のコード変更なしでドライバーのデフォルト動作のまま接続できます。

MongoDB 互換アプリケーションを構築する開発者にとって、一時的な障害に対するアプリケーションの回復力が向上し、MongoDB からの移行時の互換性ギャップも 1 つ解消されるアップデートです。

**アップデート前の課題**

- Amazon DocumentDB は再試行可能な書き込みをサポートしておらず、多くのドライバーがデフォルトで有効にしているため、接続文字列に `retryWrites=false` を明示的に指定する必要があった
- 指定を忘れると、書き込み時にエラーが発生し、MongoDB からの移行時のつまずきポイントになっていた
- ネットワーク断やフェイルオーバーなどの一時的なエラー発生時、書き込みの再試行ロジックをアプリケーション側で実装する必要があった
- アプリケーション側の独自リトライでは、書き込みが二重に適用されるリスク (冪等性の欠如) をアプリケーションで考慮する必要があった

**アップデート後の改善**

- エンジンバージョン 8.0.2 以降では、接続文字列から `retryWrites=false` を削除するだけで再試行可能な書き込みが有効になり、アプリケーションコードの変更は不要
- 一時的なエラー発生時、ドライバーが対象の書き込みを自動的に 1 回再試行し、サーバー側の重複排除により最大 1 回のみ適用される
- `updateMany` と `deleteMany` を除くすべての書き込みコマンド、およびトランザクションのコミット/アボートコマンドが再試行の対象になった
- インスタンスベースのクラスターとサーバーレスクラスターの両方で利用可能

## アーキテクチャ図

```mermaid
sequenceDiagram
    participant App as 👤 アプリケーション
    participant Drv as 🔌 MongoDB ドライバー
    participant DDB as 🗄️ Amazon DocumentDB 8.0.2

    App->>Drv: insertOne / updateOne など
    Drv->>DDB: 書き込みコマンド送信<br/>lsid と txnNumber を付与
    Note over DDB: 書き込みを実行し<br/>結果をキャッシュ
    DDB--xDrv: ⚡ 一時的なエラー<br/>ネットワーク断・フェイルオーバー
    Drv->>DDB: 同じ lsid と txnNumber で<br/>自動的に 1 回だけ再試行
    Note over DDB: 重複排除により<br/>再実行せずキャッシュ済みの<br/>結果を返却
    DDB-->>Drv: 書き込み結果
    Drv-->>App: 成功レスポンス
```

再試行可能な書き込みの動作フローです。ドライバーが論理セッション ID (`lsid`) とトランザクション番号 (`txnNumber`) を書き込みコマンドに付与し、一時的なエラー時に同じ識別子で再試行します。Amazon DocumentDB は識別子をもとに重複排除を行い、初回実行時にキャッシュした結果を返すため、書き込みは最大 1 回のみ適用されます。

## サービスアップデートの詳細

### 主要機能

1. **書き込みの自動再試行**
   - 一時的なネットワークエラーやプライマリ選出 (フェイルオーバー) による書き込み失敗時に、ドライバーが自動的に 1 回だけ再試行
   - アプリケーション側での再試行ロジックの実装が不要
   - 現行の MongoDB 互換ドライバーの多くはデフォルトで有効 (`retryWrites=true`)

2. **サーバー側の重複排除による冪等性の保証**
   - ドライバーが付与する論理セッション ID (`lsid`) とトランザクション番号 (`txnNumber`) を使用して重複排除
   - 初回実行時に結果をキャッシュし、同一の書き込みが再試行された場合は再実行せずキャッシュ済みの結果を返却
   - 再試行は元の書き込みから 60 分間有効 (ドライバーの再試行は即時のため実用上十分な猶予)
   - `insertMany` や `bulkWrite` などのバッチオペレーションでは、バッチ内の各ドキュメントが個別に重複排除され、再試行時は未適用のドキュメントのみが挿入される

3. **接続文字列の互換性向上**
   - エンジンバージョン 8.0.2 以降では `retryWrites=false` の指定が不要
   - MongoDB からの移行時に接続文字列を変更せずそのまま利用可能になり、互換性ギャップが解消
   - 8.0.2 より前のエンジンバージョンでは引き続き未サポートのため、`retryWrites=false` の指定が必要

## 技術仕様

### 再試行対象のオペレーション

| 分類 | オペレーション | 再試行可否 |
|------|----------------|-----------|
| 単一ドキュメント書き込み | `insertOne`, `updateOne`, `deleteOne` | ✓ 可能 |
| 検索して変更 | `findOneAndUpdate`, `findOneAndDelete`, `findOneAndReplace` | ✓ 可能 |
| バッチ書き込み | `insertMany`, `bulkWrite` (単一ドキュメント操作で構成される場合) | ✓ 可能 (ドキュメント単位で重複排除) |
| トランザクション制御 | `commitTransaction`, `abortTransaction` | ✓ 可能 |
| 複数ドキュメント書き込み | `updateMany`, `deleteMany` | ✗ 不可 |
| トランザクション内の個々の書き込み | - | ✗ 不可 |

### 要件

| 項目 | 詳細 |
|------|------|
| エンジンバージョン | Amazon DocumentDB 8.0.2 以降 |
| クラスタータイプ | インスタンスベースおよびサーバーレスの両方に対応 |
| ドライバー | 再試行可能な書き込みプロトコルをサポートする MongoDB 互換ドライバー (最小バージョンは各ドライバーのドキュメントを参照) |
| 接続文字列 | `retryWrites=true` を指定、またはドライバーのデフォルトを使用 |
| 再試行の有効期間 | 元の書き込みから 60 分間 (それ以降の再試行は新規オペレーションとして実行) |

### エラーコード

| エラーコード | 名称 | 説明 |
|-------------|------|------|
| 225 | TransactionTooOld | 同じセッション・ステートメントに対してより新しいトランザクション番号が既にコミット済みのため、この再試行は古すぎて適用できない |
| 301 | Retryable writes not supported | 書き込みに再試行用フィールドが含まれているが、エンジンバージョンが未サポート、またはオペレーションが再試行対象外。8.0.2 より前のバージョンでは `retryWrites=false` を指定する |

## 設定方法

### 前提条件

1. Amazon DocumentDB クラスターがエンジンバージョン 8.0.2 以降であること
2. 再試行可能な書き込みをサポートする MongoDB 互換ドライバーを使用していること
3. 再試行可能な挿入を行うドキュメントには `_id` フィールドが含まれていること

### 手順

#### ステップ1: エンジンバージョンの確認

```bash
aws docdb describe-db-clusters \
    --db-cluster-identifier my-docdb-cluster \
    --query 'DBClusters[0].EngineVersion'
```

対象クラスターのエンジンバージョンを確認します。8.0.2 未満の場合は、先にエンジンのアップグレードが必要です。

#### ステップ2: 接続文字列の更新

```text
mongodb://<username>:<password>@<cluster-endpoint>:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=true
```

接続文字列に `retryWrites=true` を指定します。既存のアプリケーションで `retryWrites=false` を指定している場合は、その指定を削除するか `retryWrites=true` に変更します。ドライバーのデフォルトが `retryWrites=true` の場合は、`retryWrites=false` を削除するだけで有効になります。

#### ステップ3: 動作確認

```javascript
// Node.js ドライバーの例
const { MongoClient } = require("mongodb");

const client = new MongoClient(uri); // retryWrites はデフォルトで有効
const collection = client.db("mydb").collection("orders");

// 一時的なエラー発生時、ドライバーが自動的に 1 回再試行する
await collection.insertOne({ _id: orderId, item: "book", qty: 1 });
```

アプリケーションコードの変更は不要です。ドライバーが自動的に再試行を処理します。フェイルオーバーテスト (`aws docdb failover-db-cluster`) を実施し、書き込み中のフェイルオーバーでもアプリケーションがエラーなく継続することを確認するとより確実です。

## メリット

### ビジネス面

- **アプリケーションの可用性向上**: フェイルオーバーやネットワーク断などの一時的な障害時にも書き込みが自動的に再試行されるため、エンドユーザーに影響するエラーが減少する
- **移行の容易化**: MongoDB からの移行時に接続文字列の変更 (`retryWrites=false` の追加) が不要になり、移行時のつまずきポイントと検証工数が削減される
- **開発コストの削減**: 再試行と冪等性の担保をアプリケーション側で実装する必要がなくなり、開発・保守コストが下がる

### 技術面

- **冪等性の保証**: サーバー側で `lsid` と `txnNumber` による重複排除が行われ、書き込みが最大 1 回のみ適用されることが保証される
- **コード変更不要**: ドライバーのデフォルト動作をそのまま利用でき、既存アプリケーションは接続文字列の修正のみで恩恵を受けられる
- **バッチ書き込みへの対応**: `insertMany` や `bulkWrite` でもドキュメント単位で重複排除され、再試行時は未適用分のみが挿入される

## デメリット・制約事項

### 制限事項

- `updateMany` と `deleteMany` は再試行の対象外
- マルチステートメントトランザクション内の個々の書き込みは再試行不可 (トランザクションのコミット/アボートは個別に再試行可能)
- 再試行可能な挿入には、ドキュメントに `_id` フィールドが必要
- エンジンバージョン 8.0.2 以降でのみ利用可能。それより前のバージョンでは引き続き `retryWrites=false` の指定が必要
- クエリプランナーバージョン 1.0 を使用するクラスターでは書き込みの再試行は不可

### 考慮すべき点

- `findOneAndUpdate`、`findOneAndDelete`、`findOneAndReplace` で大きなドキュメントを返す場合、重複排除のために結果ドキュメント全体がキャッシュされるため、書き込みレイテンシーが増加する可能性がある。書き込み性能が重要で返却ドキュメントが大きいワークロードでは、`retryWrites=false` の設定を検討する
- 再試行のキャッシュ有効期間は 60 分間。それを超えて到達した再試行は新規オペレーションとして実行される (ドライバーの再試行は即時のため通常は問題にならない)
- 8.0.2 未満のクラスターと 8.0.2 以降のクラスターが混在する環境では、接続文字列の管理に注意が必要

## ユースケース

### ユースケース1: フェイルオーバー時の書き込み継続性の確保

**シナリオ**: EC サイトの注文処理システムで、Amazon DocumentDB のプライマリインスタンスのフェイルオーバー (計画メンテナンスや障害) 中も注文の書き込みを失敗させたくない。

**実装例**:
```javascript
// retryWrites はドライバーのデフォルトで有効
const client = new MongoClient(
  "mongodb://user:pass@cluster.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0"
);
await client.db("shop").collection("orders").insertOne({
  _id: orderId,
  items: cart,
  createdAt: new Date()
});
```

**効果**: フェイルオーバーによるプライマリ選出中に発生した書き込みエラーをドライバーが自動的に再試行し、注文の取りこぼしや二重登録を防止できる。

### ユースケース2: MongoDB からの移行時の接続文字列互換性

**シナリオ**: セルフマネージドの MongoDB から Amazon DocumentDB への移行を計画しており、多数のマイクロサービスの接続文字列を変更する工数を最小化したい。

**実装例**:
```text
# 移行前 (MongoDB) と同じ接続オプションをそのまま利用可能
# retryWrites=false の追加が不要に
mongodb://user:pass@docdb-cluster.cluster-xxxx.ap-northeast-1.docdb.amazonaws.com:27017/?tls=true&replicaSet=rs0
```

**効果**: 移行時に各サービスの接続文字列へ `retryWrites=false` を追加する作業と、追加漏れによる書き込みエラーのリスクが解消され、移行の検証工数を削減できる。

### ユースケース3: バッチ書き込みの部分的な再試行

**シナリオ**: IoT データの取り込みパイプラインで `insertMany` による一括挿入中にネットワーク断が発生した場合でも、重複挿入なしで確実にデータを登録したい。

**実装例**:
```javascript
// バッチ内の各ドキュメントが個別に重複排除される
await collection.insertMany(
  sensorReadings.map(r => ({ _id: r.readingId, ...r }))
);
```

**効果**: 再試行時には未適用のドキュメントのみが挿入されるため、バッチの途中で障害が発生しても重複や欠損なくデータを取り込める。

## 料金

再試行可能な書き込みの利用自体に追加料金はありません。Amazon DocumentDB の標準料金 (インスタンス時間またはサーバーレスの DCU、ストレージ、I/O) が適用されます。

## 利用可能リージョン

Amazon DocumentDB 8.0 が利用可能なすべてのリージョンで、8.0.2 のインスタンスベースおよびサーバーレスクラスターにて利用可能です。

## 関連サービス・機能

- **Amazon DocumentDB 8.0**: 本機能の前提となるメジャーバージョン。2026 年 8 月に 5.0 からのメジャーバージョンアップグレードもサポートされており、8.0.2 への移行パスが整備されている
- **Amazon DocumentDB Serverless**: サーバーレスクラスターでも再試行可能な書き込みを利用可能
- **AWS Database Migration Service (DMS)**: MongoDB から Amazon DocumentDB への移行に利用。本機能により移行後の接続文字列の互換性が向上

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260928-amazon-documentdb-retryable-writes.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-documentdb-retryable-writes/)
- [ドキュメント: Retryable writes in Amazon DocumentDB](https://docs.aws.amazon.com/documentdb/latest/developerguide/retryable-writes.html)
- [料金ページ](https://aws.amazon.com/documentdb/pricing/)

## まとめ

Amazon DocumentDB 8.0.2 での再試行可能な書き込みのサポートにより、MongoDB との互換性ギャップが 1 つ解消され、一時的な障害に対するアプリケーションの回復力がコード変更なしで向上します。8.0.2 以降を利用している場合は接続文字列から `retryWrites=false` を削除して有効化し、フェイルオーバーテストで動作を確認することを推奨します。8.0.2 未満のクラスターでは引き続き `retryWrites=false` が必要な点に注意してください。
