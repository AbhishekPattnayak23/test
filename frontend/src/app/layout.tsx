import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from '@/lib/auth/auth';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';
import { createTheme } from '@mui/material/styles';
import { SnackbarProvider } from 'notistack';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CV Villas Agent Assist',
  description: 'Knowledge assistant for villa rental sales agents',
  keywords: ['villa rentals', 'knowledge base', 'sales agent', 'AI assistant'],
};

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#0d47a1',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff4081',
      dark: '#9a0036',
    },
    villa: {
      blue: '#2c3e50',
      teal: '#1abc9c',
      sand: '#f5deb3',
      gold: '#f39c12',
    } as any,
    success: {
      main: '#4caf50',
    },
    warning: {
      main: '#ff9800',
    },
    error: {
      main: '#f44336',
    },
  },
  typography: {
    fontFamily: 'Inter, Roboto, sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      color: '#2c3e50',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      color: '#2c3e50',
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 500,
      color: '#2c3e50',
    },
  },
  shape: {
    borderRadius: 8,
  },
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <SnackbarProvider maxSnack={3}>
            <AuthProvider>
              <div className="min-h-screen flex flex-col">
                <Navbar />
                <div className="flex flex-1">
                  <Sidebar />
                  <main className="flex-1 p-6 bg-gray-50">
                    {children}
                  </main>
                </div>
              </div>
            </AuthProvider>
          </SnackbarProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
