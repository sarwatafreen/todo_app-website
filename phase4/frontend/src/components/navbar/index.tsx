'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <div className="flex items-center">
          <Link href="/dashboard" className="text-xl font-bold text-blue-600 hover:text-blue-800">
            Todo App
          </Link>
          <nav className="ml-10 flex space-x-8">
            <Link href="/dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </Link>
            <Link href="/tasks" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Tasks
            </Link>
            <Link href="/chat" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Chat
            </Link>
          </nav>
        </div>

        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <span className="text-sm text-gray-600">Welcome, {user.email}</span>
              <button
                onClick={handleLogout}
                className="text-sm bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <Link href="/login" className="text-sm text-gray-700 hover:text-blue-600">
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;