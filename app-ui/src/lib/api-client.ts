const APP_API_BASE_URL = process.env.APP_API_BASE_URL ?? "http://localhost:8000";

function assertAllowedPath(path: string): void {
  if (!path.startsWith("/")) {
    throw new Error("API path must start with '/'");
  }
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  assertAllowedPath(path);
  const response = await fetch(`${APP_API_BASE_URL}${path}`, {
    ...init,
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-Correlation-ID": crypto.randomUUID(),
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}
