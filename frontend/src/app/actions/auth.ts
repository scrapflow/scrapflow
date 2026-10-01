"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export async function loginAction(formData: FormData) {
    const username = formData.get("username") as string;
    const password = formData.get("password") as string;

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        return { error: "Invalid username or password" };
    }

    const data = await response.json();
    const cookieStore = cookies();

    (await cookieStore).set("access_token", data.access_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",      
        sameSite: "strict",
        maxAge: 60 * 15,
        path: "/",
    });
    
    const setCookieHeader = response.headers.get("set-cookie");
      if (setCookieHeader) {

    const match = setCookieHeader.match(/refresh_token=([^;]+)/)
    if (match && match[1]) {
      (await cookieStore).set('refresh_token', match[1], {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60, 
        path: '/',
      })
    }
  }

  redirect('/');
}

export async function logoutAction() {
    const cookieStore = await cookies();
    cookieStore.delete("access_token");
    cookieStore.delete("refresh_token");
    redirect("/");
}