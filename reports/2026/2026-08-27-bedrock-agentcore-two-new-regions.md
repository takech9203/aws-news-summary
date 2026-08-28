# Amazon Bedrock AgentCore - 提供リージョン拡大 (米国西部 北カリフォルニア、アジアパシフィック ハイデラバード)

**リリース日**: 2026 年 8 月 27 日
**サービス**: Amazon Bedrock AgentCore
**機能**: Amazon Bedrock AgentCore のリージョン拡大

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260827-bedrock-agentcore-two-new-regions.html)

## 概要

Amazon Bedrock AgentCore が、新たに米国西部 (北カリフォルニア) リージョンとアジアパシフィック (ハイデラバード) リージョンで利用可能になりました。

Amazon Bedrock AgentCore は、AI エージェントの構築、接続、最適化のためのプラットフォームです。任意のフレームワークと任意のモデルを使用してエージェントを迅速に構築し、エンタープライズシステムやツールに接続し、継続的に最適化できます。セキュリティはエージェントが回避できないインフラストラクチャレイヤーで適用されます。

今回の拡大により、これらのリージョンのお客様は、エンドユーザーにより近い場所で低レイテンシーにエージェントを構築・実行できるようになります。

## サービスアップデートの詳細

### 主要機能

1. **新規対応リージョン**
   - 米国西部 (北カリフォルニア)
   - アジアパシフィック (ハイデラバード)

2. **提供開始時点で利用可能な AgentCore の機能**
   - エージェントランタイム
   - アイデンティティとアクセス制御
   - ポリシー管理
   - セッション永続化
   - ツール接続
   - 評価とオブザーバビリティ

## メリット

### ビジネス面

- **データレジデンシー対応**: 米国西部やインド国内でのデータ保持要件を持つワークロードでも AgentCore を活用したエージェント基盤を構築可能
- **ユーザー体験の向上**: エンドユーザーに近いリージョンでエージェントを実行することで、応答の低レイテンシー化が期待できる

### 技術面

- **フル機能での提供**: ランタイム、アイデンティティ、ポリシー管理、セッション永続化、ツール接続、評価、オブザーバビリティといった AgentCore の主要機能が提供開始時点から利用可能
- **既存アーキテクチャの展開が容易**: 他リージョンで構築済みのエージェント構成を、新リージョンにそのまま展開しやすい

## デメリット・制約事項

### 考慮すべき点

- エージェントが利用する基盤モデル (Amazon Bedrock のモデル) の提供状況はリージョンごとに異なるため、利用予定のモデルが対象リージョンで利用可能か事前に確認が必要
- 機能ごとの詳細なリージョン対応状況は、開発者ガイドのリージョン一覧で確認することを推奨

## ユースケース

### ユースケース: インド国内向けエージェントアプリケーションの低レイテンシー化

**シナリオ**: インド国内のユーザー向けに AI エージェントを提供する企業が、これまで他リージョンで運用していた AgentCore ベースのエージェントをアジアパシフィック (ハイデラバード) リージョンに展開する。

**効果**: エンドユーザーに近いリージョンでエージェントが実行されるため応答レイテンシーが低減し、データをインド国内に保持する要件にも対応しやすくなる。

## 料金

AgentCore は利用した分だけ課金される従量課金制です。詳細は [Amazon Bedrock AgentCore 料金ページ](https://aws.amazon.com/bedrock/agentcore/pricing/) を参照してください。

## 利用可能リージョン

今回の拡大により、以下のリージョンが追加されました。

- 米国西部 (北カリフォルニア)
- アジアパシフィック (ハイデラバード)

その他の利用可能リージョンは [開発者ガイドのリージョン一覧](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html) を参照してください。

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260827-bedrock-agentcore-two-new-regions.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-agentcore-two-new-regions/)
- [Amazon Bedrock AgentCore 製品ページ](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon Bedrock AgentCore 開発者ガイド](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Amazon Bedrock AgentCore 料金ページ](https://aws.amazon.com/bedrock/agentcore/pricing/)

## まとめ

AI エージェントの構築・運用プラットフォームである Amazon Bedrock AgentCore が、米国西部 (北カリフォルニア) とアジアパシフィック (ハイデラバード) で利用可能になり、主要機能が提供開始時点からすべて利用できます。該当リージョンの近くにエンドユーザーを持つワークロードや、データレジデンシー要件のあるエージェント基盤では、新リージョンへの展開を検討することを推奨します。
