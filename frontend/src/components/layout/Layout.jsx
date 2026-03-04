import { Outlet, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/button';
import { Briefcase } from 'lucide-react';

export default function Layout() {
    const { user, logout } = useAuth();

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
            <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
                <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2">
                        <div className="bg-brand-blue p-1.5 rounded-lg">
                            <Briefcase className="w-6 h-6 text-brand-light" />
                        </div>
                        <span className="font-bold text-xl tracking-tight hidden sm:inline-block">
                            Job<span className="text-brand-blue">Assistant</span>
                        </span>
                    </Link>

                    <nav className="flex items-center gap-4">
                        {user ? (
                            <>
                                <Link to="/dashboard">
                                    <Button variant="ghost">Dashboard</Button>
                                </Link>
                                <Button variant="outline" onClick={logout}>Logout</Button>
                            </>
                        ) : (
                            <>
                                <Link to="/login">
                                    <Button variant="ghost">Login</Button>
                                </Link>
                                <Link to="/signup">
                                    <Button>Sign Up</Button>
                                </Link>
                            </>
                        )}
                    </nav>
                </div>
            </header>

            <main className="flex-1 container mx-auto px-4 py-8">
                <Outlet />
            </main>

            <footer className="border-t py-6 md:py-0">
                <div className="container mx-auto px-4 flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
                    <p className="text-sm leading-loose text-center text-gray-500 md:text-left">
                        Built for job seekers. Phase 1 MVP.
                    </p>
                </div>
            </footer>
        </div>
    );
}
