import { Outlet } from 'react-router-dom';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTheme } from 'next-themes';
import starlinkLogo from '@/assets/images/starlink-logo.svg';

/**
 * Authentication layout component
 * @returns {JSX.Element} AuthLayout component
 */
export default function AuthLayout() {
  const { theme, setTheme } = useTheme();
  
  const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');
  
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="flex h-16 items-center justify-between px-4 lg:px-6">
        <div className="flex items-center">
          <img src={starlinkLogo} alt="Starlink Logo" className="h-8 w-8" />
          <span className="ml-2 text-xl font-semibold">Starlink Reseller Platform</span>
        </div>
        
        <Button variant="ghost" size="icon" onClick={toggleTheme}>
          {theme === 'dark' ? (
            <Sun className="h-5 w-5" />
          ) : (
            <Moon className="h-5 w-5" />
          )}
        </Button>
      </header>
      
      <main className="flex flex-1 items-center justify-center p-4 lg:p-6">
        <div className="w-full max-w-md">
          <Outlet />
        </div>
      </main>
      
      <footer className="border-t border-border py-4 text-center text-sm text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} Starlink Reseller Platform. All rights reserved.</p>
      </footer>
    </div>
  );
}

