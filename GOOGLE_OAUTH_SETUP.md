# Google OAuth 設定ガイド

Google アカウントでのログイン機能を有効にするために、Google Cloud Console で OAuth アプリケーションを作成する必要があります。

## 手順

### 1. Google Cloud Console にアクセス
- [Google Cloud Console](https://console.cloud.google.com/) にアクセス
- Google アカウントでログイン

### 2. プロジェクトを作成または選択
- 新しいプロジェクトを作成するか、既存のプロジェクトを選択

### 3. OAuth 同意画面を設定
1. 左側のメニューから「API とサービス」→「OAuth 同意画面」を選択
2. ユーザータイプを選択（外部または内部）
3. アプリケーション名を入力（例: "MokabuLens"）
4. ユーザーサポートメールアドレスを入力
5. 開発者連絡先情報を入力
6. 「保存して次へ」をクリック

### 4. スコープを設定
1. 「スコープを追加または削除」をクリック
2. 以下のスコープを追加：
   - `userinfo.email`
   - `userinfo.profile`
   - `openid`
3. 「更新」をクリック
4. 「保存して次へ」をクリック

### 5. テストユーザーを追加（開発環境の場合）
1. テストユーザーとして使用する Google アカウントを追加
2. 「保存して次へ」をクリック

### 6. OAuth 2.0 クライアント ID を作成
1. 左側のメニューから「API とサービス」→「認証情報」を選択
2. 「+ 認証情報を作成」→「OAuth クライアント ID」を選択
3. アプリケーションの種類を「ウェブアプリケーション」に選択
4. 名前を入力（例: "MokabuLens Web Client"）
5. 承認済みの JavaScript 生成元に以下を追加：
   - `http://localhost:3000`（開発環境）
   - 本番環境のURL（本番環境の場合）
6. 承認済みのリダイレクト URI に以下を追加：
   - `http://localhost:3000/api/auth/callback/google`（開発環境）
   - `https://yourdomain.com/api/auth/callback/google`（本番環境）
7. 「作成」をクリック

### 7. クライアント ID とシークレットを取得
- 作成された OAuth クライアント ID の詳細画面で：
  - クライアント ID をコピー
  - クライアントシークレットをコピー

### 8. 環境変数を設定
プロジェクトの `.env.local` ファイルに以下を設定：

```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

## 注意事項

- `NEXTAUTH_SECRET` は安全なランダムな文字列に設定してください
- 本番環境では HTTPS を使用し、適切なドメインを設定してください
- クライアントシークレットは絶対に公開しないでください

## トラブルシューティング

- OAuth エラーが発生する場合は、リダイレクト URI が正しく設定されているか確認
- 開発環境ではテストユーザーが追加されているか確認
- 本番環境では OAuth 同意画面の公開が必要な場合があります
