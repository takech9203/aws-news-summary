# Amazon Corretto - 2026 年 10 月四半期アップデート

**リリース日**: 2026年10月23日
**サービス**: Amazon Corretto
**機能**: 四半期セキュリティおよびクリティカルアップデート

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20261023-amazon-corretto-october-2026-quarterly-updates.html)
<!-- INFOGRAPHIC_BASE_URL は環境変数から取得 -->

## 概要

2026 年 10 月 22 日、Amazon は Amazon Corretto の Long-Term Support (LTS) バージョンに対する四半期セキュリティおよびクリティカルアップデートを発表しました。今回のアップデートにより、Corretto 27.0.1.0.10、25.0.5.0.9、21.0.13.0.10、17.0.21.0.10、11.0.33.0.9、および 8u512 が[ダウンロード](https://aws.amazon.com/corretto)可能になりました。Amazon Corretto は、無料で、マルチプラットフォームに対応した、本番環境対応の OpenJDK ディストリビューションです。

今回のリリースは、2026 年 9 月に一般提供が開始された Corretto 27 を含む 6 つのバージョンを対象とした定期アップデートです。各バージョンの最新ビルドには、セキュリティ修正とクリティカルなバグ修正が含まれており、本番環境での安全かつ安定した Java アプリケーションの実行をサポートします。

本番環境で Java アプリケーションを運用しているすべての組織が対象となります。特にセキュリティを重視する環境では、四半期ごとのアップデートを適用することで、既知の脆弱性への対応と安定性の維持が可能になります。Linux ユーザーは、Corretto の Apt、Yum、または Apk リポジトリを設定することで、パッケージマネージャー経由でアップデートを受け取ることもできます。

**アップデート前の課題**

- 以前のビルドにはセキュリティ脆弱性が存在していた可能性がある
- クリティカルなバグが未修正のまま残っている可能性があった
- 四半期ごとの定期アップデートを適用しない場合、既知の問題への露出が継続する

**アップデート後の改善**

- セキュリティおよびクリティカルな問題が修正され、より安全で安定した Java 実行環境を提供
- Corretto 27 を含む 6 つのバージョンすべてで最新のセキュリティ修正を利用可能
- ダウンロードに加えて、Linux では Apt / Yum / Apk リポジトリ経由での更新にも対応

## サービスアップデートの詳細

### 主要機能

1. **セキュリティおよびクリティカルアップデート**
   - 既知のセキュリティ脆弱性を修正
   - クリティカルなバグ修正を含み、安定性を向上
   - 本番環境での安全かつ信頼性の高い使用をサポート

2. **6 つのバージョンを対象とした更新**
   - Corretto 27.0.1.0.10 (2026 年 9 月に GA した最新バージョン)
   - Corretto 25.0.5.0.9
   - Corretto 21.0.13.0.10
   - Corretto 17.0.21.0.10
   - Corretto 11.0.33.0.9
   - Corretto 8u512

3. **複数の配布チャネル**
   - [Corretto ホームページ](https://aws.amazon.com/corretto)から全バージョンをダウンロード可能
   - Linux では Apt、Yum、Apk リポジトリを設定してパッケージマネージャー経由で更新可能
   - フィードバックは [GitHub](https://github.com/corretto) で受付

## 技術仕様

### 更新されたバージョン

| バージョン | アップデート |
|-----------|------------|
| Corretto 27 | 27.0.1.0.10 |
| Corretto 25 | 25.0.5.0.9 |
| Corretto 21 | 21.0.13.0.10 |
| Corretto 17 | 17.0.21.0.10 |
| Corretto 11 | 11.0.33.0.9 |
| Corretto 8 | 8u512 |

### 対応プラットフォーム

- Linux (x86_64、aarch64)
- Windows (x86_64)
- macOS (x86_64、aarch64)
- Docker コンテナイメージ

## 設定方法

### 前提条件

1. Java アプリケーションまたは開発環境
2. 適切なプラットフォーム (Linux、Windows、macOS)
3. 管理者権限 (インストールに必要)

### 手順

#### ステップ1: Corretto のダウンロード

[Corretto ホームページ](https://aws.amazon.com/corretto) から適切なバージョンをダウンロードします。ここでは各プラットフォーム向けのインストーラーやアーカイブを入手できます。

#### ステップ2: Linux でのリポジトリ設定 (オプション)

Linux システムでは、Corretto の Apt、Yum、または Apk リポジトリを設定することで、パッケージマネージャー経由でインストールおよびアップデートを受け取ることができます。

```bash
# Apt の例 (Debian/Ubuntu)
wget -O- https://apt.corretto.aws/corretto.key | sudo gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" | sudo tee /etc/apt/sources.list.d/corretto.list
sudo apt-get update
sudo apt-get install -y java-21-amazon-corretto-jdk
```

上記のコマンドは、Corretto の署名キーを登録し、Apt リポジトリを追加したうえで、Corretto 21 の JDK をインストールしています。詳細は[インストールガイド](https://docs.aws.amazon.com/corretto/latest/corretto-25-ug/generic-linux-install.html)を参照してください。

#### ステップ3: 既存環境のアップデート

リポジトリを設定済みの環境では、パッケージマネージャーの更新コマンドで最新ビルドを適用します。

```bash
# Yum の例 (Amazon Linux / RHEL 系)
sudo yum update java-21-amazon-corretto
```

このコマンドは、インストール済みの Corretto 21 を今回リリースされた最新ビルドに更新しています。

#### ステップ4: バージョンの確認

インストールまたは更新後、Java バージョンを確認します。

```bash
java -version
```

このコマンドで、インストールされた Corretto のバージョンが今回のアップデート (例: 21.0.13.0.10) に正しく反映されていることを確認できます。

## メリット

### ビジネス面

- **無料**: ライセンス費用なしで商用利用可能
- **本番環境対応**: AWS が本番環境での使用をサポート
- **継続的なサポート**: 四半期ごとのセキュリティおよびクリティカルアップデートを提供

### 技術面

- **セキュリティ**: 定期的なセキュリティアップデートで脆弱性を修正
- **幅広いバージョンカバレッジ**: Corretto 8 から最新の Corretto 27 まで 6 バージョンを同時に更新
- **柔軟な配布チャネル**: ダウンロードに加え、Linux パッケージリポジトリ経由での更新に対応

## デメリット・制約事項

### 制限事項

- 今回の発表では、個別の CVE 識別子や具体的な脆弱性の一覧は明示されていない
- 特定の商用 Java ディストリビューションの独自機能は含まれない

### 考慮すべき点

- バージョンアップデートの適用前に、アプリケーションの互換性テストが推奨される
- コンテナ環境では、ベースイメージの更新とアプリケーションの再ビルド・再デプロイが必要
- 自動更新を有効にしている場合、更新タイミングが運用ポリシーと整合しているか確認が必要

## ユースケース

### ユースケース1: 本番環境での Java アプリケーション運用

**シナリオ**: EC2 インスタンスで LTS バージョンの Java アプリケーションを運用

**実装例**:
- EC2 インスタンスに Corretto 21 をインストール
- Java アプリケーションを Corretto で実行
- 四半期アップデート (例: 21.0.13.0.10) を定期的に適用

**効果**: 無料で本番環境対応の Java ランタイムを使用し、セキュリティアップデートを継続的に受け取る

### ユースケース2: コンテナ化された Java アプリケーション

**シナリオ**: Amazon ECS / EKS 上で Java マイクロサービスを Docker コンテナとして実行

**実装例**:
```dockerfile
FROM amazoncorretto:21
COPY target/myapp.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

**効果**: 最新のセキュリティ修正を含む Corretto イメージでコンテナを再ビルドし、脆弱性への露出を低減できる

### ユースケース3: 複数バージョンが混在する環境の一括更新

**シナリオ**: Corretto 8 のレガシーアプリケーションと Corretto 27 の新規アプリケーションが混在する環境を運用

**実装例**:
- レガシー環境には 8u512 を適用
- 新規環境には 27.0.1.0.10 を適用
- Linux パッケージリポジトリを活用して各環境の更新を自動化

**効果**: 新旧すべての Java バージョンで同一タイミングのセキュリティ修正を適用し、環境全体のセキュリティレベルを統一できる

## 料金

Amazon Corretto は完全に無料で、ライセンス費用は発生しません。

## 利用可能リージョン

Amazon Corretto は、すべての AWS リージョンおよびオンプレミス環境で利用可能です。

## 関連サービス・機能

- **AWS Lambda**: サーバーレス Java 関数の実行
- **Amazon EC2**: Java アプリケーションのホスティング
- **Amazon ECS/EKS**: コンテナ化された Java アプリケーションの実行
- **AWS CodeBuild**: Corretto を使用した Java アプリケーションのビルド

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20261023-amazon-corretto-october-2026-quarterly-updates.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/10/amazon-corretto-october-2026-quarterly-updates)
- [Corretto ホームページ](https://aws.amazon.com/corretto)
- [Corretto Linux インストールガイド](https://docs.aws.amazon.com/corretto/latest/corretto-25-ug/generic-linux-install.html)
- [GitHub - Corretto](https://github.com/corretto)

## まとめ

Amazon Corretto の 2026 年 10 月四半期アップデートにより、Corretto 8 から最新の Corretto 27 まで 6 つのバージョンでセキュリティおよびクリティカルな問題が修正されました。本番環境で Java アプリケーションを運用している組織は、互換性テストを実施したうえで、無料のアップデートを早期に適用し、セキュリティと安定性を維持してください。
