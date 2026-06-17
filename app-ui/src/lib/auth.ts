import { cookies } from "next/headers";

export type SessionUser = {
  email: string;
  role: "admin" | "shopper";
};

export function getSessionUser(): SessionUser | null {
  const value = cookies().get("session-user")?.value;
  if (!value) {
    return null;
  }

  try {
    return JSON.parse(value) as SessionUser;
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  return getSessionUser() !== null;
}
