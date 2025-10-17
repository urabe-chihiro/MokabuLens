// API共通の型定義

export interface ApiResponse<T = unknown> {
  data?: T
  error?: string
  message?: string
}

export interface ApiError {
  error: string
  status: number
  message?: string
}

export interface PaginationParams {
  page?: number
  limit?: number
}

export interface SearchParams {
  search?: string
  sort?: string
  order?: 'asc' | 'desc'
}
