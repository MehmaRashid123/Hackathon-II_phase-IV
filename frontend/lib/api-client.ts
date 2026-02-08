import { apiClient } from "./api/client";

/**
 * API Client for Authentication
 *
 * Provides functions to interact with the FastAPI backend auth endpoints.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Compatibility APIClient class for components that expect { success, data } response pattern.
 */
export class APIClient {
  async get<T>(endpoint: string) {
    try {
      const data = await apiClient.get<T>(endpoint);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : "Request failed" };
    }
  }

  async post<T>(endpoint: string, body: any) {
    try {
      const data = await apiClient.post<T>(endpoint, body);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : "Request failed" };
    }
  }
}

export interface SignUpData {
  email: string;
  password: string;
}

export interface SignInData {
  email: string;
  password: string;
}

export interface UserResponse {
  id: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserResponse;
}

export class AuthApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = "AuthApiError";
  }
}

/**
 * Sign up a new user
 */
export async function signUp(data: SignUpData): Promise<UserResponse> {
  try {
    const response = await fetch(`${API_URL}/api/auth/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // Check if response is HTML (Hugging Face space waking up)
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("text/html")) {
      throw new AuthApiError(
        "Backend is starting up. Please wait a moment and try again.",
        503,
        { detail: "Service temporarily unavailable" }
      );
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Sign up failed" }));
      throw new AuthApiError(
        error.detail || "Sign up failed",
        response.status,
        error
      );
    }

    return response.json();
  } catch (error) {
    // Handle network errors or JSON parse errors
    if (error instanceof AuthApiError) {
      throw error;
    }
    throw new AuthApiError(
      "Unable to connect to server. Please check your connection and try again.",
      0,
      { detail: error instanceof Error ? error.message : "Network error" }
    );
  }
}

/**
 * Sign in existing user
 */
export async function signIn(data: SignInData): Promise<TokenResponse> {
  try {
    const response = await fetch(`${API_URL}/api/auth/signin`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // Check if response is HTML (Hugging Face space waking up)
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("text/html")) {
      throw new AuthApiError(
        "Backend is starting up. Please wait a moment and try again.",
        503,
        { detail: "Service temporarily unavailable" }
      );
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Sign in failed" }));
      throw new AuthApiError(
        error.detail || "Sign in failed",
        response.status,
        error
      );
    }

    return response.json();
  } catch (error) {
    // Handle network errors or JSON parse errors
    if (error instanceof AuthApiError) {
      throw error;
    }
    throw new AuthApiError(
      "Unable to connect to server. Please check your connection and try again.",
      0,
      { detail: error instanceof Error ? error.message : "Network error" }
    );
  }
}

/**
 * Store JWT token in localStorage
 */
export function storeToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", token);
  }
}

/**
 * Get JWT token from localStorage
 */
export function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
}

/**
 * Remove JWT token from localStorage
 */
export function removeToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
  }
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return getToken() !== null;
}
