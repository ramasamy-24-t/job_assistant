import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export default function SignupPage() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        password: '',
        preferred_locations: '',
        actively_looking: true
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const { signup, login } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        // Format locations string to array
        const locationsArray = formData.preferred_locations
            .split(',')
            .map(loc => loc.trim())
            .filter(loc => loc.length > 0);

        const submissionData = {
            ...formData,
            preferred_locations: locationsArray
        };

        const result = await signup(submissionData);

        if (result.success) {
            // Auto-login after successful signup
            const loginResult = await login(formData.email, formData.password);
            if (loginResult.success) {
                navigate('/dashboard');
            } else {
                navigate('/login');
            }
        } else {
            setError(result.error);
            setIsLoading(false);
        }
    };

    return (
        <div className="flex justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
            <Card className="w-full max-w-lg">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl text-center">Create an account</CardTitle>
                    <p className="text-center text-sm text-gray-500">
                        Enter your information to get started with JobAssistant
                    </p>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {error && (
                            <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
                                {error}
                            </div>
                        )}

                        <div className="space-y-2">
                            <label className="text-sm font-medium" htmlFor="name">Full Name *</label>
                            <input
                                id="name" name="name" type="text" required
                                className="w-full rounded-md border p-2"
                                value={formData.name} onChange={handleChange}
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium" htmlFor="email">Email *</label>
                            <input
                                id="email" name="email" type="email" required
                                className="w-full rounded-md border p-2"
                                value={formData.email} onChange={handleChange}
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium" htmlFor="password">Password *</label>
                            <input
                                id="password" name="password" type="password" required
                                className="w-full rounded-md border p-2"
                                value={formData.password} onChange={handleChange}
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium" htmlFor="phone">Phone Number</label>
                            <input
                                id="phone" name="phone" type="tel"
                                className="w-full rounded-md border p-2"
                                value={formData.phone} onChange={handleChange}
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium" htmlFor="preferred_locations">Preferred Locations</label>
                            <p className="text-xs text-gray-400">Comma separated (e.g. New York, Remote, London)</p>
                            <input
                                id="preferred_locations" name="preferred_locations" type="text"
                                className="w-full rounded-md border p-2"
                                value={formData.preferred_locations} onChange={handleChange}
                            />
                        </div>

                        <div className="flex items-center space-x-2 pt-2">
                            <input
                                type="checkbox" id="actively_looking" name="actively_looking"
                                checked={formData.actively_looking} onChange={handleChange}
                                className="w-4 h-4 text-brand-blue rounded border-gray-300 focus:ring-brand-blue"
                            />
                            <label htmlFor="actively_looking" className="text-sm font-medium">
                                I am actively looking for jobs
                            </label>
                        </div>

                        <Button className="w-full mt-6" type="submit" disabled={isLoading}>
                            {isLoading ? 'Creating account...' : 'Create Account'}
                        </Button>

                        <div className="text-center text-sm pt-4 border-t">
                            Already have an account?{' '}
                            <Link to="/login" className="text-brand-blue hover:underline font-medium">
                                Sign in
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
