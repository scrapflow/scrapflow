'use client'

import Link from 'next/link'
import { useState } from 'react'
import { logoutAction } from '../actions/auth'

export default function MobileMenu({ authenticated }: { authenticated: boolean }) {
  const [isOpen, setIsOpen] = useState(false)
  const linkClassName =
    'block rounded-md px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800'

  return (
    <div className="relative flex md:hidden items-center">
      <button
        type="button"
        aria-label={isOpen ? 'Close menu' : 'Open menu'}
        aria-expanded={isOpen}
        aria-controls="mobile-navigation"
        onClick={() => setIsOpen((open) => !open)}
        className="inline-flex items-center justify-center rounded-md p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-900 focus-visible:outline-2 focus-visible:outline-offset-2 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-white"
      >
        {isOpen ? (
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        )}
      </button>

      {isOpen && (
        <div
          id="mobile-navigation"
          className="fixed left-0 right-0 top-16 flex w-full flex-col border-t border-gray-100 bg-gray-50 dark:border-gray-800 dark:bg-gray-900"
        >
          <div className="w-full space-y-1 px-2 pb-3 pt-2 sm:px-3">
            <Link href="/" onClick={() => setIsOpen(false)} className={`${linkClassName} bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-400`}>
              Home
            </Link>
            <Link href="/services" onClick={() => setIsOpen(false)} className={linkClassName}>
              Services
            </Link>
            <Link href="/parts" onClick={() => setIsOpen(false)} className={linkClassName}>
              Parts
            </Link>
            <Link href="/contact" onClick={() => setIsOpen(false)} className={linkClassName}>
              Contact
            </Link>
            <div className="border-t border-gray-200 px-3 pb-2 pt-4 dark:border-gray-800">
              {authenticated ? (
                <form action={logoutAction}>
                  <button
                    type="submit"
                    className="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition-all hover:bg-blue-700"
                  >
                    Logout
                  </button>
                </form>
              ) : (
                <Link
                  href="/login"
                  onClick={() => setIsOpen(false)}
                  className="block w-full rounded-lg bg-blue-600 px-4 py-2 text-center text-sm font-medium text-white shadow-sm transition-all hover:bg-blue-700"
                >
                  Login
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}