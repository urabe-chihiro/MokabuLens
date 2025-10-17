// 認証関連の型定義

export interface User {
  id: string
  email: string
  name: string
  image?: string
}

export interface Session {
  user: User
  expires: string
}

export interface AuthCallback {
  ok: boolean
  error?: string
  url?: string
}
