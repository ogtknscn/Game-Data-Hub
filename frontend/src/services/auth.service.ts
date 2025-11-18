import { apiClient } from './api-client'
import { LoginRequest, RegisterRequest, TokenResponse } from '../types/api'
import { User } from '../types/domain'

export const authService = {
  async login(request: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', request)
    return response.data
  },

  async register(request: RegisterRequest): Promise<User> {
    const response = await apiClient.post<User>('/api/v1/auth/register', request)
    return response.data
  },
}

