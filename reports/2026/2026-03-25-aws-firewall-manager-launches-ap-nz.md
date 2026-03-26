# AWS Firewall Manager - アジアパシフィック (ニュージーランド) リージョンでの提供開始

**リリース日**: 2026 年 3 月 25 日
**サービス**: AWS Firewall Manager
**機能**: アジアパシフィック (ニュージーランド) リージョンでの利用可能化

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/aws-news-summary/20260325-aws-firewall-manager-launches-ap-nz.html)

## 概要

AWS Firewall Manager がアジアパシフィック (ニュージーランド) リージョン (ap-southeast-5) で利用可能になりました。AWS Firewall Manager は、クラウドセキュリティ管理者や SRE がアプリケーションを保護する際の運用オーバーヘッドを削減し、ファイアウォールルールの手動設定・管理の負担を軽減するセキュリティ管理サービスです。

AWS Firewall Manager を使用することで、AWS のセキュリティサービス全体にわたる多層防御ポリシーを一元的に設定・管理できます。AWS WAF を使用してアセットを保護したいユーザーは、Firewall Manager でセキュリティポリシーを作成・維持できます。今回のリージョン拡張により、ニュージーランドおよびオセアニア地域でワークロードを運用する組織が、同リージョン内でセキュリティポリシーの統合管理を行えるようになります。

**アップデート前の課題**

- ニュージーランドリージョンにデプロイされたリソースに対して、Firewall Manager によるセキュリティポリシーの一元管理ができなかった
- ニュージーランドリージョンのリソースを保護するために、個別にセキュリティ設定を手動で管理する必要があった
- オセアニア地域でのセキュリティガバナンスにおいて、Firewall Manager のリージョン選択肢が限られていた

**アップデート後の改善**

- ニュージーランドリージョンのリソースに対して Firewall Manager のセキュリティポリシーを適用可能になった
- AWS Organizations 全体のセキュリティポリシーをニュージーランドリージョンにも一括展開できるようになった
- AWS WAF、Shield Advanced、VPC セキュリティグループ、Network Firewall、Route 53 Resolver DNS Firewall の一元管理がニュージーランドリージョンで可能になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Org["🏢 AWS Organizations"]
        Admin(["👤 Firewall Manager 管理者"])
        subgraph NZ["☁️ ap-southeast-5 ニュージーランド"]
            direction LR
            FM["🛡️ Firewall Manager"]
            WAF["🔒 AWS WAF"]
            SG["🔒 セキュリティグループ"]
            NF["🔒 Network Firewall"]
            DNS["🔒 DNS Firewall"]
            FM ~~~ WAF ~~~ SG ~~~ NF ~~~ DNS
        end
        subgraph Resources["📦 保護対象リソース"]
            direction LR
            ALB["⚙️ ALB"]
            CF["⚙️ CloudFront"]
            EC2["⚙️ EC2"]
            VPC["⚙️ VPC"]
            ALB ~~~ CF ~~~ EC2 ~~~ VPC
        end
    end

    Admin --> FM
    FM --> WAF
    FM --> SG
    FM --> NF
    FM --> DNS
    WAF --> Resources
    SG --> Resources
    NF --> Resources
    DNS --> Resources

    classDef cloud fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef security fill:#FFEBEE,stroke:#F44336,stroke-width:2px,color:#B71C1C
    classDef compute fill:#FFE0B2,stroke:#FFCC80,stroke-width:2px,color:#5D4037
    classDef user fill:#E3F2FD,stroke:#BBDEFB,stroke-width:2px,color:#1565C0
    classDef org fill:none,stroke:#E1BEE7,stroke-width:2px,color:#666666
    classDef resource fill:none,stroke:#C5E1A5,stroke-width:2px,color:#666666

    class NZ cloud
    class Org org
    class FM,WAF,SG,NF,DNS security
    class ALB,CF,EC2,VPC compute
    class Admin user
    class Resources resource
```

この図は、AWS Firewall Manager がニュージーランドリージョンで AWS WAF、セキュリティグループ、Network Firewall、DNS Firewall を一元管理し、保護対象リソースに対してセキュリティポリシーを適用する構成を示しています。

## サービスアップデートの詳細

### 主要機能

1. **セキュリティポリシーの一元管理**
   - AWS Organizations 全体でファイアウォールルールやセキュリティポリシーを一括設定
   - 新しいアカウントやリソースが追加された際にポリシーを自動的に適用
   - ニュージーランドリージョンのリソースも管理対象に含めることが可能

2. **多層防御の実現**
   - AWS WAF によるウェブアプリケーション保護
   - AWS Shield Advanced による DDoS 対策
   - VPC セキュリティグループによるネットワークレベルの制御
   - AWS Network Firewall による VPC トラフィックフィルタリング
   - Amazon Route 53 Resolver DNS Firewall による DNS クエリのフィルタリング

3. **コンプライアンス監視と自動修復**
   - ポリシーに準拠していないリソースの自動検出
   - 非準拠リソースに対する自動修復アクションの設定
   - AWS Security Hub との統合によるセキュリティ状態の可視化

## 技術仕様

### リージョン情報

| 項目 | 詳細 |
|------|------|
| リージョン名 | アジアパシフィック (ニュージーランド) |
| リージョンコード | ap-southeast-5 |
| サービス | AWS Firewall Manager |

### Firewall Manager で管理可能なサービス

| サービス | 用途 |
|----------|------|
| AWS WAF | ウェブアプリケーションの保護 |
| AWS Shield Advanced | DDoS 攻撃からの保護 |
| VPC セキュリティグループ | ネットワークアクセス制御 |
| AWS Network Firewall | VPC トラフィックのフィルタリング |
| Amazon Route 53 Resolver DNS Firewall | DNS クエリのフィルタリング |
| サードパーティファイアウォール | Palo Alto Networks 等のサードパーティ製品 |

## 設定方法

### 前提条件

1. AWS Organizations が有効化されていること
2. Firewall Manager の管理者アカウントが設定されていること
3. ニュージーランドリージョン (ap-southeast-5) が Organizations で有効化されていること

### 手順

#### ステップ 1: Firewall Manager 管理者の確認

```bash
aws fms get-admin-account --region ap-southeast-5
```

Firewall Manager の管理者アカウントがニュージーランドリージョンで認識されているか確認します。

#### ステップ 2: セキュリティポリシーの作成

```bash
aws fms put-policy \
  --region ap-southeast-5 \
  --policy '{
    "PolicyName": "nz-waf-policy",
    "RemediationEnabled": true,
    "ResourceType": "AWS::ElasticLoadBalancingV2::LoadBalancer",
    "SecurityServicePolicyData": {
      "Type": "WAF",
      "ManagedServiceData": "{\"type\":\"WAF\",\"defaultAction\":{\"type\":\"ALLOW\"},\"overrideCustomerWebACLAssociation\":false}"
    },
    "IncludeMap": {
      "ACCOUNT": ["123456789012"]
    }
  }'
```

ニュージーランドリージョンの ALB に対して AWS WAF ポリシーを作成します。`RemediationEnabled` を `true` に設定すると、非準拠リソースが自動的に修復されます。

#### ステップ 3: ポリシーの準拠状況確認

```bash
aws fms get-compliance-detail \
  --region ap-southeast-5 \
  --policy-id "policy-id" \
  --member-account "123456789012"
```

作成したポリシーに対するリソースの準拠状況を確認します。非準拠のリソースがある場合、自動修復が有効であれば Firewall Manager が自動的にポリシーを適用します。

## メリット

### ビジネス面

- **コンプライアンス対応**: ニュージーランド国内のデータ保護規制やセキュリティ要件への対応が容易になる
- **運用コスト削減**: セキュリティポリシーの一元管理により、個別設定の運用オーバーヘッドを削減
- **セキュリティガバナンス強化**: AWS Organizations 全体で一貫したセキュリティポリシーをニュージーランドリージョンにも適用可能

### 技術面

- **自動化**: 新規リソースへのセキュリティポリシーの自動適用により、設定漏れを防止
- **多層防御**: WAF、Shield Advanced、Network Firewall、DNS Firewall を組み合わせた包括的なセキュリティ対策が可能
- **可視化**: 非準拠リソースの自動検出と Security Hub との統合により、セキュリティ状態を一元的に把握可能

## デメリット・制約事項

### 制限事項

- AWS Firewall Manager の利用には AWS Organizations の有効化が必須
- Firewall Manager 自体の利用料に加えて、管理対象の各セキュリティサービスの料金が別途発生する
- 一部の管理対象サービスがニュージーランドリージョンで未提供の場合、そのサービスのポリシーは適用できない

### 考慮すべき点

- Firewall Manager の管理者アカウントは AWS Organizations 全体で 1 つのため、既存環境への影響を事前に確認すること
- ニュージーランドリージョンは比較的新しいリージョンのため、サービスクォータのデフォルト値が他リージョンと異なる場合がある

## ユースケース

### ユースケース 1: マルチリージョンでのセキュリティポリシー統合管理

**シナリオ**: オセアニア地域に展開するアプリケーションに対して、シドニーリージョンとニュージーランドリージョンの両方で一貫したセキュリティポリシーを適用する。

**実装例**:
```bash
# ニュージーランドリージョンにも既存の WAF ポリシーを適用
aws fms put-policy \
  --region ap-southeast-5 \
  --policy file://existing-waf-policy.json
```

**効果**: リージョン間で一貫したセキュリティポリシーを維持しながら、運用オーバーヘッドを削減できます。

### ユースケース 2: 新規アカウントへの自動セキュリティ適用

**シナリオ**: AWS Organizations に新しいアカウントが追加された際に、ニュージーランドリージョンのリソースにも自動的にセキュリティポリシーを適用する。

**実装例**:
```json
{
  "PolicyName": "auto-apply-waf",
  "RemediationEnabled": true,
  "ResourceType": "AWS::ElasticLoadBalancingV2::LoadBalancer",
  "ExcludeResourceTags": false,
  "SecurityServicePolicyData": {
    "Type": "WAF",
    "ManagedServiceData": "{\"type\":\"WAF\",\"defaultAction\":{\"type\":\"ALLOW\"}}"
  }
}
```

**効果**: 新規アカウントやリソースが追加されても、手動設定なしでセキュリティポリシーが自動適用されます。

### ユースケース 3: ニュージーランドのデータ主権要件への対応

**シナリオ**: ニュージーランド国内のデータ主権要件に基づき、同リージョン内でセキュリティポリシーを管理・適用する必要がある。

**実装例**:
```bash
# Network Firewall ポリシーをニュージーランドリージョンに作成
aws fms put-policy \
  --region ap-southeast-5 \
  --policy '{
    "PolicyName": "nz-network-firewall-policy",
    "RemediationEnabled": true,
    "ResourceType": "AWS::EC2::VPC",
    "SecurityServicePolicyData": {
      "Type": "NETWORK_FIREWALL"
    }
  }'
```

**効果**: ニュージーランドリージョン内でセキュリティポリシーを運用し、データ主権要件を満たすことができます。

## 料金

AWS Firewall Manager の料金はポリシーごとに課金されます。各リージョンの各ポリシーに対して月額料金が発生します。

### 料金例

| 項目 | 月額料金 |
|------|----------|
| Firewall Manager ポリシー | $100/ポリシー/リージョン |

※ 上記は Firewall Manager 自体の料金です。AWS WAF、Shield Advanced、Network Firewall など管理対象サービスの料金は別途発生します。正確な料金は [AWS Firewall Manager 料金ページ](https://aws.amazon.com/firewall-manager/pricing/) を参照してください。

## 利用可能リージョン

今回のアップデートにより、AWS Firewall Manager はアジアパシフィック (ニュージーランド) リージョン (ap-southeast-5) で利用可能になりました。Firewall Manager は既に多数の AWS 商用リージョンで提供されており、今回の拡張によりオセアニア地域でのカバレッジが強化されました。

## 関連サービス・機能

- **AWS WAF**: ウェブアプリケーションを一般的なウェブエクスプロイトから保護するサービス。Firewall Manager で一元管理可能
- **AWS Shield Advanced**: DDoS 攻撃に対する高度な保護を提供するサービス。Firewall Manager で保護対象リソースを一括設定可能
- **AWS Network Firewall**: VPC トラフィックのフィルタリングと監視を行うマネージドファイアウォールサービス
- **Amazon Route 53 Resolver DNS Firewall**: DNS クエリに基づくドメインフィルタリングサービス。Firewall Manager でポリシーを一元管理可能
- **AWS Security Hub**: セキュリティアラートの集約と準拠状況の確認。Firewall Manager の検出結果を統合可能

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/aws-news-summary/20260325-aws-firewall-manager-launches-ap-nz.html)
- [公式発表 (What's New)](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-firewall-manager-launches-ap-nz/)
- [AWS Firewall Manager ドキュメント](https://docs.aws.amazon.com/waf/latest/developerguide/fms-chapter.html)
- [AWS Firewall Manager 料金ページ](https://aws.amazon.com/firewall-manager/pricing/)

## まとめ

AWS Firewall Manager がアジアパシフィック (ニュージーランド) リージョンで利用可能になったことで、同リージョンにデプロイされたアプリケーションに対するセキュリティポリシーの一元管理が可能になりました。AWS Organizations を活用して、WAF ルール、セキュリティグループ、Network Firewall、DNS Firewall のポリシーを一括管理することで、運用オーバーヘッドを削減しながら多層防御を実現できます。ニュージーランドリージョンでワークロードを運用している場合は、Firewall Manager を活用してセキュリティガバナンスの強化を検討してください。
