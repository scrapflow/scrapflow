import Link from "next/link";
import { isAuthenticated } from "./lib/auth";

export default async function Home() {
  const authenticated = await isAuthenticated();

  if (authenticated) {
    return (
      <section className="flex flex-1 items-center justify-center px-6 py-16">
        <div className="w-full max-w-3xl space-y-4">
          <h1 className="text-3xl font-bold">Zona protejată</h1>
          <p className="text-gray-600 dark:text-gray-300">
            Authenticathed
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="flex flex-1 items-center justify-center px-6 py-16">
      <div className="w-full max-w-3xl space-y-4">
        <h1 className="text-3xl font-bold">Scrap listing in here</h1>
      </div>
    </section>
  );
}