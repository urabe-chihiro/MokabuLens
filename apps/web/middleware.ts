import { withAuth } from "next-auth/middleware"
import { NextResponse } from "next/server"

export default withAuth(
  function middleware(req) {
    // 認証が必要なページにアクセスした場合の処理
    if (req.nextUrl.pathname.startsWith('/dashboard') || 
        req.nextUrl.pathname === '/') {
      // 既に認証されている場合はそのまま進む
      return NextResponse.next()
    }
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        // 認証が必要なパスを定義
        const protectedPaths = ['/', '/dashboard']
        const isProtectedPath = protectedPaths.some(path => 
          req.nextUrl.pathname === path || 
          req.nextUrl.pathname.startsWith(path + '/')
        )
        
        // 認証が必要なパスの場合、トークンが存在するかチェック
        if (isProtectedPath) {
          return !!token
        }
        
        // 認証が不要なパス（サインインページなど）は常に許可
        return true
      },
    },
  }
)

// 認証が必要なパスを定義
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api/auth (NextAuth.js API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!api/auth|_next/static|_next/image|favicon.ico|public).*)',
  ],
}
