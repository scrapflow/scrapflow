import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">

                    <div className="flex-shrink-0 flex items-center">
                        <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">
                            Scrap<span className="text-blue-600">Flow</span>
                        </Link>
                    </div>

                    {/* Meniu Desktop (Ascuns pe mobil) */}
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
                        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-sm">
                            Login
                        </button>
                    </div>


                    <div className="flex md:hidden items-center">
                        <input type="checkbox" id="navbar-toggle" className="peer hidden" />

                        <label
                            htmlFor="navbar-toggle"
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800 focus:outline-none cursor-pointer select-none"
                        >
                            <span className="sr-only">Open menu</span>

                            <svg className="h-6 w-6 block peer-checked:hidden" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                            </svg>

                            <svg className="h-6 w-6 hidden peer-checked:block" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </label>

                        <div className="hidden peer-checked:flex flex-col absolute top-16 left-0 w-full border-t border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 z-50">
                            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 w-full">
                                <Link href="/" className="block px-3 py-2 rounded-md text-base font-medium bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-400">
                                    Home
                                </Link>
                                <Link href="/services" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800">
                                    Services
                                </Link>
                                <Link href="/parts" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800">
                                    Parts
                                </Link>
                                <Link href="/contact" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800">
                                    Contact
                                </Link>
                                <div className="pt-4 pb-2 border-t border-gray-200 dark:border-gray-800 px-3">
                                    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-sm">
                                        Login
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>


                </div>
            </div>
        </nav>
    );
}
