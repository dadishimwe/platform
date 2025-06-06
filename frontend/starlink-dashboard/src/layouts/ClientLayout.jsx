import { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { 
  Menu, 
  X, 
  User, 
  LogOut, 
  Bell, 
  Settings, 
  Moon, 
  Sun,
  LayoutDashboard,
  Satellite,
  LineChart,
  LifeBuoy,
  FileText,
  CreditCard,
  Settings as SettingsIcon
} from 'lucide-react';
import { useTheme } from 'next-themes';
import starlinkLogo from '@/assets/images/starlink-logo.svg';

/**
 * Client layout component
 * @returns {JSX.Element} ClientLayout component
 */
export default function ClientLayout() {
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { theme, setTheme } = useTheme();
  
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');
  
  const navigation = [
    { name: 'Dashboard', href: '/client', icon: LayoutDashboard },
    { name: 'My Devices', href: '/client/devices', icon: Satellite },
    { name: 'Usage & Performance', href: '/client/usage', icon: LineChart },
    { name: 'Support', href: '/client/support', icon: LifeBuoy },
    { name: 'Documents', href: '/client/documents', icon: FileText },
    { name: 'Account', href: '/client/account', icon: User },
    { name: 'Settings', href: '/client/settings', icon: SettingsIcon },
  ];
  
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside 
        className={`fixed inset-y-0 left-0 z-50 w-64 transform bg-sidebar text-sidebar-foreground transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-16 items-center justify-between px-4">
          <div className="flex items-center">
            <img src={starlinkLogo} alt="Starlink Logo" className="h-8 w-8 text-sidebar-primary" />
            <span className="ml-2 text-xl font-semibold">Client Portal</span>
          </div>
          <Button 
            variant="ghost" 
            size="icon" 
            onClick={toggleSidebar} 
            className="lg:hidden"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
        
        <div className="mt-6 px-4">
          <nav className="space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    `flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                        : 'text-sidebar-foreground hover:bg-sidebar-accent/50'
                    }`
                  }
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </aside>
      
      {/* Main content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="flex h-16 items-center justify-between border-b border-border px-4 lg:px-6">
          <div className="flex items-center">
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={toggleSidebar} 
              className="lg:hidden"
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            
            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {theme === 'dark' ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>
            
            <div className="relative group">
              <Button variant="ghost" className="flex items-center gap-2">
                <User className="h-5 w-5" />
                <span className="hidden md:inline">{user?.first_name || user?.email}</span>
              </Button>
              
              <div className="absolute right-0 mt-2 hidden w-48 rounded-md bg-popover p-2 shadow-lg group-hover:block">
                <div className="px-4 py-2">
                  <p className="text-sm font-medium">{user?.email}</p>
                  <p className="text-xs text-muted-foreground">Client</p>
                </div>
                
                <div className="mt-2 border-t border-border pt-2">
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <NavLink to="/client/account" className="flex items-center">
                      <User className="mr-2 h-4 w-4" />
                      <span>My Account</span>
                    </NavLink>
                  </Button>
                  
                  <Button variant="ghost" className="w-full justify-start" asChild>
                    <NavLink to="/client/settings" className="flex items-center">
                      <Settings className="mr-2 h-4 w-4" />
                      <span>Settings</span>
                    </NavLink>
                  </Button>
                  
                  <Button 
                    variant="ghost" 
                    className="w-full justify-start text-destructive" 
                    onClick={logout}
                  >
                    <div className="flex items-center">
                      <LogOut className="mr-2 h-4 w-4" />
                      <span>Logout</span>
                    </div>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </header>
        
        {/* Content */}
        <main className="flex-1 overflow-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

