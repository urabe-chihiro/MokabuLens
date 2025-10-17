import { signIn, signOut, getSession } from 'next-auth/react'
import { AuthCallback, User } from '@/types/auth.types'

// Google サインイン
export async function signInWithGoogle(callbackUrl: string = '/'): Promise<AuthCallback> {
  try {
    const result = await signIn('google', {
      callbackUrl,
      redirect: false,
    })
    
    return {
      ok: result?.ok || false,
      error: result?.error || undefined,
      url: result?.url || undefined,
    }
  } catch (error) {
    console.error('Sign in error:', error)
    return {
      ok: false,
      error: 'An unexpected error occurred',
    }
  }
}

// サインアウト
export async function signOutUser(callbackUrl: string = '/'): Promise<void> {
  try {
    await signOut({ callbackUrl })
  } catch (error) {
    console.error('Sign out error:', error)
    throw error
  }
}

// 現在のセッション取得
export async function getCurrentSession() {
  try {
    return await getSession()
  } catch (error) {
    console.error('Get session error:', error)
    return null
  }
}

// 認証状態チェック
export async function isAuthenticated(): Promise<boolean> {
  const session = await getCurrentSession()
  return !!session
}

// 現在のユーザー取得
export async function getCurrentUser(): Promise<User | null> {
  const session = await getCurrentSession()
  if (!session?.user) {
    return null
  }
  
  return {
    id: session.user.email || '', // Use email as ID fallback
    email: session.user.email || '',
    name: session.user.name || '',
    image: session.user.image || undefined,
  }
}
