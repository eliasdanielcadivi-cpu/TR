import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { SocketProvider } from '@/components/providers/SocketProvider';
import { StoreProvider } from '@/components/providers/StoreProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Cognitive Server - Sistema de Extracción Cognitiva',
  description: 'Sistema de interacción conversacional adaptativa con prompts vivos',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body className={`${inter.className} antialiased`}>
        <StoreProvider>
          <SocketProvider>
            <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black">
              {children}
            </div>
          </SocketProvider>
        </StoreProvider>
      </body>
    </html>
  );
}