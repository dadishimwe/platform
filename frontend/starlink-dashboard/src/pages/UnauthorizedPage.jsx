import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { ShieldAlert, Home, ArrowLeft } from 'lucide-react';

/**
 * Unauthorized page component
 * @returns {JSX.Element} UnauthorizedPage component
 */
export default function UnauthorizedPage() {
  const { user, hasRole } = useAuth();
  
  // Determine home route based on user role
  const homeRoute = hasRole('Admin') || hasRole('Super Admin') ? '/admin' : '/client';
  
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4 text-center">
      <div className="rounded-full bg-muted p-6">
        <ShieldAlert className="h-16 w-16 text-destructive" />
      </div>
      
      <h1 className="mt-6 text-4xl font-bold">Access Denied</h1>
      
      <p className="mt-4 max-w-md text-lg text-muted-foreground">
        You don't have permission to access this page. Please contact your administrator if you believe this is an error.
      </p>
      
      <div className="mt-8 flex flex-col gap-4 sm:flex-row">
        <Button asChild>
          <Link to={homeRoute} className="flex items-center">
            <Home className="mr-2 h-4 w-4" />
            <span>Go to Dashboard</span>
          </Link>
        </Button>
        
        <Button variant="outline" asChild>
          <Link to={-1} className="flex items-center">
            <ArrowLeft className="mr-2 h-4 w-4" />
            <span>Go Back</span>
          </Link>
        </Button>
      </div>
    </div>
  );
}

