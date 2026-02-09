/**
 * Centralized API client with automatic JWT injection.
 *
 * All API requests automatically include Authorization header with JWT token from localStorage.
 */

let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Force HTTPS for Hugging Face Spaces to prevent Mixed Content errors
if (API_BASE_URL.includes("hf.space") && API_BASE_URL.startsWith("http://")) {
  API_BASE_URL = API_BASE_URL.replace("http://", "https://");
  console.log("🔒 Upgraded API URL to HTTPS:", API_BASE_URL);
}

export interface ApiClientOptions extends RequestInit {
  requireAuth?: boolean;
}

export class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Get JWT token from localStorage.
   */
  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  }

  /**
   * Get current user ID from decoded JWT token.
   */
  getUserId(): string | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      // Decode JWT payload (base64)
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.sub; // user ID is in 'sub' claim
    } catch (error) {
      console.error("Failed to decode JWT token:", error);
      return null;
    }
  }

  /**
   * Make HTTP request with automatic JWT injection.
   */
  async request<T>(
    endpoint: string,
    options: ApiClientOptions = {}
  ): Promise<T> {
    const { requireAuth = true, ...fetchOptions } = options;

    // Build headers
    const headers = new Headers(fetchOptions.headers);
    headers.set("Content-Type", "application/json");

    // Add JWT token if authentication is required
    if (requireAuth) {
      const token = this.getToken();
      if (!token) {
        // Redirect to login if token is missing
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
        throw new Error("Authentication required");
      }
      headers.set("Authorization", `Bearer ${token}`);
    }

    // Make request with CORS mode
    const url = `${this.baseURL}${endpoint}`;
    console.log(`🌐 API Request: ${fetchOptions.method || 'GET'} ${url}`);
    
    try {
      const response = await fetch(url, {
        ...fetchOptions,
        headers,
        mode: 'cors', // Explicitly set CORS mode
        credentials: 'omit', // Don't send cookies for CORS
      });

      console.log(`✅ API Response: ${response.status} ${response.statusText}`);

      // Handle authentication errors
      if (response.status === 401) {
        // Token expired or invalid - redirect to login
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          window.location.href = "/login";
        }
        throw new Error("Authentication failed");
      }

      // Handle forbidden errors (user isolation violation)
      if (response.status === 403) {
        throw new Error("You do not have permission to access this resource");
      }

      // Parse response
      if (response.status === 204) {
        // No content (e.g., DELETE success)
        return undefined as T;
      }

      const data = await response.json();

      // Handle error responses
      if (!response.ok) {
        const error = data.detail || `Request failed with status ${response.status}`;
        throw new Error(error);
      }

      return data as T;
    } catch (error) {
      console.error(`❌ API Error for ${url}:`, error);
      
      // Check if it's a network error
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error(`Cannot connect to backend at ${this.baseURL}. Please ensure the backend is running on port 8000.`);
      }
      
      throw error;
    }
  }

  /**
   * Convenience methods for common HTTP verbs.
   */

  async get<T>(endpoint: string, options?: ApiClientOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  }

  async post<T>(
    endpoint: string,
    body: any,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async put<T>(
    endpoint: string,
    body: any,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "PUT",
      body: JSON.stringify(body),
    });
  }

  async patch<T>(
    endpoint: string,
    body?: any,
    options?: ApiClientOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async delete<T>(endpoint: string, options?: ApiClientOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: "DELETE" });
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
