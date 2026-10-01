import Link from "next/link";
import { logoutAction } from "../actions/auth";
import { isAuthenticated } from "../lib/auth";
import MobileMenu from "./mobile-menu";

function AuthControl({
    authenticated,
    mobile = false,
}: {
    authenticated: boolean;
    mobile?: boolean;
}) {
    const className = mobile
        ? "w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-sm"
        : "bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-sm";

    if (authenticated) {
        return (
            <form action={logoutAction}>
                <button type="submit" className={className}>
                    Logout
                </button>
            </form>
        );
    }

    return (
        <Link href="/login" className={className}>
            Login
        </Link>
    );
}

export default async function Navbar() {
    const authenticated = await isAuthenticated();

    return (
        <nav className="bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">

                    {/* Desktop Menu */}
                    <div className="hidden md:flex items-center space-x-8">
                        <Link href="/" className="text-sm font-medium text-blue-600 dark:text-blue-500">
                            Home
                        </Link>
                        <Link href="/services" className="text-sm font-medium text-gray-600 hover:text-gray-950 dark:text-gray-300 dark:hover:text-white transition-colors">
                            Services
                        </Link>
                        <Link href="/parts" className="text-sm font-medium text-gray-600 hover:text-gray-950 dark:text-gray-300 dark:hover:text-white transition-colors">
                            Parts
                        </Link>
                        <Link href="/contact" className="text-sm font-medium text-gray-600 hover:text-gray-950 dark:text-gray-300 dark:hover:text-white transition-colors">
                            Contact
                        </Link>
                    </div>

                    <div className="hidden md:flex items-center">
                        <AuthControl authenticated={authenticated} />
                    </div>


                    <MobileMenu authenticated={authenticated} />
                </div>
            </div>
        </nav>
    );
}
