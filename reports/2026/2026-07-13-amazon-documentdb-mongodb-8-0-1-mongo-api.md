# Amazon DocumentDB - 46 個の新しい MongoDB オペレーターのサポート

**リリース日**: 2026年7月13日
**サービス**: Amazon DocumentDB (with MongoDB compatibility)
**機能**: バージョン 8.0.1 での 46 個の MongoDB オペレーター追加

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260713-amazon-documentdb-mongodb-8-0-1-mongo-api.html)
<!-- INFOGRAPHIC_BASE_URL は環境変数から取得 -->

## 概要

Amazon DocumentDB (with MongoDB compatibility) は、マイナーバージョン 8.0.1 から 46 個の MongoDB 集計オペレーターおよびカーソルメソッドを新たにサポートしました。これにより、クエリ API の互換性が拡大し、MongoDB ワークロードをアプリケーションコードの変更なしで Amazon DocumentDB へ移行しやすくなります。

今回追加されたオペレーターは、アキュムレーター、三角関数、ビット単位集計、算術、データサイズおよびデータ型、タイムスタンプ、ステージなどの 7 つのカテゴリにわたります。統計計算、数学的な変換、データ分析など、これまで DocumentDB では利用できなかった高度な集計処理をネイティブに実行できるようになります。

このアップデートは、MongoDB の豊富なクエリ表現をそのまま活用したい開発者や、既存の MongoDB アプリケーションを DocumentDB へ移行するお客様を対象としています。オペレーターは Amazon DocumentDB が提供されているすべてのリージョンで、バージョン 8.0.1 から利用できます。

**アップデート前の課題**

このアップデート以前は、以下のような課題がありました。

- 統計計算 ($median, $percentile, $stdDevPop など) をデータベース側で実行できず、アプリケーション側での集計処理が必要だった
- 三角関数やビット単位演算などの数学的な集計オペレーターが利用できなかった
- 一部の MongoDB オペレーターが未サポートのため、移行時にアプリケーションコードの書き換えが必要になる場合があった

**アップデート後の改善**

今回のアップデートにより、以下が可能になりました。

- 中央値やパーセンタイル、標準偏差などの統計値をデータベース側で直接計算できるようになった
- 三角関数 (15 個)、ビット単位集計 (4 個) など高度な数値演算をネイティブに実行できるようになった
- MongoDB との API 互換性が拡大し、コード変更なしでの移行がより容易になった

## アーキテクチャ図

```mermaid
flowchart LR
    App(["👤 アプリケーション"]) --> Driver["🔌 MongoDB ドライバー"]
    Driver --> DocDB[("🗄️ Amazon DocumentDB 8.0.1")]

    subgraph Ops["🧮 新規サポートオペレーター 46 個"]
        direction LR
        Acc["📊 アキュムレーター 13"]
        Trig["📐 三角関数 15"]
        Bit["🔢 ビット単位 4"]
        Other["⚙️ その他 14"]
        Acc ~~~ Trig ~~~ Bit ~~~ Other
    end

    DocDB --> Ops

    classDef user fill:#E3F2FD,stroke:#BBDEFB,stroke-width:2px,color:#1565C0
    classDef process fill:#FFFFFF,stroke:#4A90E2,stroke-width:2px,color:#333333
    classDef database fill:#E8EAF6,stroke:#C5CAE9,stroke-width:2px,color:#283593
    classDef layer fill:none,stroke:#E1BEE7,stroke-width:2px,color:#666666

    class App user
    class Driver process
    class DocDB database
    class Ops layer
    class Acc,Trig,Bit,Other process
```

アプリケーションは既存の MongoDB ドライバーを通じて、DocumentDB 8.0.1 で新たに利用可能になった集計オペレーターを実行できます。

## サービスアップデートの詳細

### 主要機能

1. **アキュムレーター (13 個)**
   - 順位付けと抽出: `$top`, `$topN`, `$bottom`, `$bottomN`, `$firstN`, `$lastN`, `$maxN`, `$minN`
   - 統計計算: `$count`, `$median`, `$percentile`, `$stdDevPop`, `$stdDevSamp`
   - グループ内の上位・下位要素の抽出や、中央値・パーセンタイル・標準偏差の計算が可能

2. **三角関数 (15 個)**
   - 基本三角関数: `$sin`, `$cos`, `$tan`, `$asin`, `$acos`, `$atan`, `$atan2`
   - 双曲線関数: `$sinh`, `$cosh`, `$tanh`, `$asinh`, `$acosh`, `$atanh`
   - 角度変換: `$degreesToRadians`, `$radiansToDegrees`
   - 地理空間計算や科学技術計算の集計処理に活用可能

3. **ビット単位集計 (4 個)**
   - `$bitAnd`, `$bitOr`, `$bitXor`, `$bitNot`
   - フラグ管理やビットマスク処理を集計パイプライン内で実行可能

4. **算術 (3 個)**
   - `$round`, `$trunc`, `$sigmoid`
   - 数値の丸め・切り捨てや、シグモイド関数による正規化が可能

5. **データサイズおよびデータ型 (4 個)**
   - `$binarySize`, `$bsonSize`, `$isNumber`, `$toUUID`
   - ドキュメントやフィールドのサイズ取得、型判定、UUID 変換が可能

6. **タイムスタンプ (2 個)**
   - `$tsIncrement`, `$tsSecond`
   - BSON タイムスタンプ型からインクリメント値や秒値を抽出可能

7. **ステージおよびその他 (5 個)**
   - `$sortByCount`, `$listSearchIndexes`, `$sampleRate`, `cursor.min()`, `cursor.max()`
   - グループ化と件数ソートの一括処理、検索インデックス一覧の取得、サンプリング、カーソルによる範囲指定が可能

## 技術仕様

### 追加オペレーター一覧

| カテゴリ | 個数 | オペレーター |
|------|------|------|
| アキュムレーター | 13 | `$top`, `$topN`, `$bottom`, `$bottomN`, `$firstN`, `$lastN`, `$maxN`, `$minN`, `$count`, `$median`, `$percentile`, `$stdDevPop`, `$stdDevSamp` |
| 三角関数 | 15 | `$sin`, `$cos`, `$tan`, `$asin`, `$acos`, `$atan`, `$atan2`, `$sinh`, `$cosh`, `$tanh`, `$asinh`, `$acosh`, `$atanh`, `$degreesToRadians`, `$radiansToDegrees` |
| ビット単位集計 | 4 | `$bitAnd`, `$bitOr`, `$bitXor`, `$bitNot` |
| 算術 | 3 | `$round`, `$trunc`, `$sigmoid` |
| データサイズ・型 | 4 | `$binarySize`, `$bsonSize`, `$isNumber`, `$toUUID` |
| タイムスタンプ | 2 | `$tsIncrement`, `$tsSecond` |
| ステージ・その他 | 5 | `$sortByCount`, `$listSearchIndexes`, `$sampleRate`, `cursor.min()`, `cursor.max()` |

### バージョン別サポート状況

| 項目 | 詳細 |
|------|------|
| 対象バージョン | Amazon DocumentDB 8.0.1 以降 |
| MongoDB API 互換性 | 3.6、4.0、5.0、8.0 に対応 (今回の追加は 8.0.1+) |
| Elastic クラスター | 今回追加のオペレーターは対象外 |
| 提供リージョン | Amazon DocumentDB が利用可能なすべてのリージョン |

## 設定方法

### 前提条件

1. Amazon DocumentDB バージョン 8.0.1 以降のクラスターを利用していること
2. MongoDB 8.0 互換の API を使用していること
3. 対応する MongoDB ドライバーまたは mongosh クライアントを利用していること

### 手順

#### ステップ1: エンジンバージョンの確認

```javascript
// buildInfo コマンドでエンジンバージョンを確認
db.runCommand({ buildInfo: 1 })
```

現在のクラスターが 8.0.1 以降であることを確認します。既存クラスターの場合は、必要に応じてエンジンバージョンを 8.0.1 以降へアップグレードします。

#### ステップ2: 新しいオペレーターを使った集計クエリの実行

```javascript
// $percentile と $stdDevPop を使った統計集計の例
db.sales.aggregate([
  {
    $group: {
      _id: "$region",
      medianAmount: { $median: { input: "$amount", method: "approximate" } },
      p95: { $percentile: { input: "$amount", p: [0.95], method: "approximate" } },
      stdDev: { $stdDevPop: "$amount" }
    }
  }
])
```

このクエリは、リージョンごとの売上金額について中央値、95 パーセンタイル、母標準偏差を DocumentDB 側で直接計算します。

#### ステップ3: カーソルメソッドによる範囲指定

```javascript
// cursor.min() と cursor.max() でインデックス範囲を指定
db.orders.find().hint({ orderDate: 1 }).min({ orderDate: ISODate("2026-01-01") }).max({ orderDate: ISODate("2026-07-01") })
```

`min()` と `max()` を使用して、インデックスに基づくスキャン範囲の下限と上限を指定します。

## メリット

### ビジネス面

- **移行コストの削減**: MongoDB との API 互換性が拡大し、アプリケーションコードの変更を最小限に抑えて移行できる
- **分析処理の内製化**: 統計計算をデータベース側で完結でき、追加の分析基盤への依存を減らせる
- **開発生産性の向上**: 使い慣れた MongoDB のオペレーターをそのまま利用でき、学習コストを抑えられる

### 技術面

- **サーバーサイド集計**: 統計値や数値変換をデータベース側で処理することで、ネットワーク転送量とアプリケーション側の処理負荷を削減できる
- **高度な数値演算**: 三角関数やビット単位演算により、科学技術計算やフラグ管理を集計パイプライン内で完結できる
- **クエリ表現力の向上**: `$topN` や `$bottomN` などにより、グループ内の上位・下位要素抽出を単一クエリで実現できる

## デメリット・制約事項

### 制限事項

- 今回追加されたオペレーターは Amazon DocumentDB 8.0.1 以降でのみ利用可能
- Elastic クラスターでは今回追加のオペレーターはサポート対象外
- MongoDB 3.6、4.0、5.0 API では利用できない

### 考慮すべき点

- 既存クラスターで利用するには、エンジンバージョンを 8.0.1 以降へアップグレードする必要がある
- `$median` や `$percentile` は近似計算 (approximate) をサポートしており、用途に応じた method の選択が必要
- MongoDB のすべてのオペレーターがサポートされたわけではないため、移行前に対応状況の確認が必要

## ユースケース

### ユースケース1: 分析ダッシュボード向けの統計集計

**シナリオ**: EC サイトの売上データについて、リージョンごとの中央値やパーセンタイルをダッシュボードに表示したい

**実装例**:
```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$region",
      p50: { $median: { input: "$total", method: "approximate" } },
      p90: { $percentile: { input: "$total", p: [0.90], method: "approximate" } }
    }
  }
])
```

**効果**: アプリケーション側での集計処理が不要になり、データベースから直接統計値を取得できる

### ユースケース2: IoT センサーデータの数値変換

**シナリオ**: センサーから収集した角度データをラジアンに変換し、三角関数を用いた計算を行いたい

**実装例**:
```javascript
db.sensors.aggregate([
  {
    $project: {
      radians: { $degreesToRadians: "$angleDegrees" },
      sinValue: { $sin: { $degreesToRadians: "$angleDegrees" } }
    }
  }
])
```

**効果**: 数学的な変換をデータベース側で実行でき、アプリケーションロジックを簡素化できる

### ユースケース3: グループ内の上位ランキング抽出

**シナリオ**: カテゴリーごとに売上上位 3 件の商品を 1 回のクエリで取得したい

**実装例**:
```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      topProducts: {
        $topN: {
          n: 3,
          sortBy: { sales: -1 },
          output: { name: "$name", sales: "$sales" }
        }
      }
    }
  }
])
```

**効果**: 複数クエリや複雑なパイプラインを組まずに、単一の集計でランキングを取得できる

## 料金

このアップデートに伴う追加料金はありません。新しいオペレーターは、Amazon DocumentDB の既存の料金体系の範囲内で利用できます。料金はインスタンス、ストレージ、I/O、バックアップの使用量に基づきます。詳細は公式の料金ページを参照してください。

## 利用可能リージョン

Amazon DocumentDB が利用可能なすべてのリージョンで、バージョン 8.0.1 から利用できます。

## 関連サービス・機能

- **Amazon DocumentDB Elastic Clusters**: シャーディングによる水平スケーリングに対応するデプロイメントオプション (今回のオペレーターは対象外)
- **AWS Database Migration Service (DMS)**: MongoDB から Amazon DocumentDB への移行を支援するサービス
- **Amazon DocumentDB ベクトル検索**: `$vectorSearch` などによる類似検索機能で、生成 AI アプリケーションの構築に活用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260713-amazon-documentdb-mongodb-8-0-1-mongo-api.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-documentdb-mongodb-8-0-1-mongo-api)
- [サポートされている MongoDB API、オペレーション、データ型](https://docs.aws.amazon.com/documentdb/latest/developerguide/mongo-apis.html)
- [Amazon DocumentDB Announcements](https://aws.amazon.com/documentdb/resources/)
- [Amazon DocumentDB 料金ページ](https://aws.amazon.com/documentdb/pricing/)

## まとめ

今回のアップデートにより、Amazon DocumentDB は 46 個の MongoDB オペレーターを新たにサポートし、統計計算や数値演算などの高度な集計処理をネイティブに実行できるようになりました。MongoDB との API 互換性が拡大したことで、既存ワークロードの移行がさらに容易になっています。8.0.1 以降のクラスターを利用しているお客様は、アプリケーションコードを変更することなく、これらの新しいオペレーターを活用した集計処理の最適化を検討することをお勧めします。
