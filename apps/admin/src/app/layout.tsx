import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'DriveGuard V3 Admin',
  description: 'DriveGuard Administrative Dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex h-screen bg-gray-50 text-gray-900 font-sans">
        <aside className="w-64 bg-dgSecondary text-white flex flex-col">
          <div className="p-4 border-b border-gray-700">
            <h1 className="text-xl font-bold tracking-wider">DriveGuard Admin</h1>
          </div>
          <nav className="flex-1 overflow-y-auto py-4">
            <ul className="space-y-1">
              <li><Link href="/" className="block px-4 py-2 hover:bg-gray-800">Dashboard</Link></li>
              <li><Link href="/enforcement" className="block px-4 py-2 hover:bg-gray-800">Enforcement Map</Link></li>
              <li><Link href="/review" className="block px-4 py-2 hover:bg-gray-800">Review Queue</Link></li>
              <li><Link href="/coverage" className="block px-4 py-2 hover:bg-gray-800">Coverage Metrics</Link></li>
              <li><Link href="/ingestion" className="block px-4 py-2 hover:bg-gray-800">Ingestion Status</Link></li>
              <li><Link href="/audit" className="block px-4 py-2 hover:bg-gray-800">Audit Log</Link></li>
              <li><Link href="/field-verification" className="block px-4 py-2 hover:bg-gray-800">Field Verification</Link></li>
            </ul>
          </nav>
        </aside>
        <main className="flex-1 flex flex-col overflow-hidden">
          <header className="h-16 bg-white border-b flex items-center px-6 shadow-sm">
            <div className="ml-auto">Admin User</div>
          </header>
          <div className="flex-1 overflow-auto p-6">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
