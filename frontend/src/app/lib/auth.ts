import "server-only";

import { cookies } from "next/headers";

export async function isAuthenticated(): Promise<boolean> {
  const accessToken = (await cookies()).get("access_token")?.value;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  if (!accessToken || !apiUrl) {
    return false;
  }

  try {
    const response = await fetch(`${apiUrl}/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
      cache: "no-store",
    });

    return response.ok;
  } catch {
    return false;
  }
}