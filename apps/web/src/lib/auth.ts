import {
  apiClient,
  LoginRequest,
  LoginResponse,
  SignUpRequest,
  PasswordReset,
} from './api';

const TOKEN_KEY = 'token';
const TENANT_ID_KEY = 'tenant_id';

export class AuthManager {
  static setToken(token: string): void {
    if (typeof window !== 'undefined') {
      document.cookie = `${TOKEN_KEY}=${token}; path=/; max-age=${
        7 * 24 * 60 * 60
      }; secure; samesite=strict`;
    }
  }

  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      const cookies = document.cookie.split(';');
      const tokenCookie = cookies.find(cookie => cookie.trim().startsWith(`${TOKEN_KEY}=`));
      if (tokenCookie) {
        const tokenValue = tokenCookie.split('=')[1];
        return tokenValue || null;
      }
    }
    return null;
  }

  static removeToken(): void {
    if (typeof window !== 'undefined') {
      document.cookie = `${TOKEN_KEY}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
    }
  }

  static setTenantId(tenantId: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TENANT_ID_KEY, tenantId);
    }
  }

  static getTenantId(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(TENANT_ID_KEY);
    }
    return null;
  }

  static removeTenantId(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TENANT_ID_KEY);
    }
  }

  static async login(credentials: LoginRequest, tenantId?: string): Promise<LoginResponse> {
    try {
      const response = await apiClient.login(credentials, tenantId);

      // Store the token
      this.setToken(response.access_token);

      // Store tenant ID if provided
      if (tenantId) {
        this.setTenantId(tenantId);
      }

      return response;
    } catch (error) {
      throw error;
    }
  }

  static async signUp(data: SignUpRequest): Promise<LoginResponse> {
    try {
      const response = await apiClient.signUp(data);
      this.setToken(response.access_token);
      return response;
    } catch (error) {
      throw error;
    }
  }

  static async logout(): Promise<void> {
    const token = this.getToken();

    if (token) {
      try {
        await apiClient.logout(token);
      } catch (error) {
        console.error('Logout API call failed:', error);
        // Continue with local logout even if API call fails
      }
    }

    // Clear local storage
    this.removeToken();
    this.removeTenantId();

    // Redirect to login page
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }

  static async requestPasswordReset(email: string): Promise<void> {
    await apiClient.requestPasswordReset(email);
  }

  static async resetPassword(data: PasswordReset): Promise<void> {
    await apiClient.resetPassword(data);
  }

  static isAuthenticated(): boolean {
    return !!this.getToken();
  }

  static async getCurrentUser() {
    const token = this.getToken();
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      return await apiClient.getCurrentUser(token);
    } catch (error) {
      // If token is invalid, clear it
      this.removeToken();
      throw error;
    }
  }
}
