import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Bot, FileText, TrendingUp, CheckCircle } from 'lucide-react';

export default function LandingPage() {
    return (
        <div className="flex flex-col items-center">
            {/* Hero Section */}
            <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 flex flex-col items-center text-center">
                <div className="space-y-4 max-w-3xl">
                    <Badge className="mb-4" variant="secondary">Job Assistant Phase 1 MVP</Badge>
                    <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
                        Let AI land your next <span className="text-brand-accent">Dream Job</span>
                    </h1>
                    <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl leading-relaxed">
                        Upload your resume and let our intelligent ATS matching engine find the best roles for you.
                        Ranked, analyzed, and ready to apply.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
                        <Link to="/signup">
                            <Button size="lg" className="w-full sm:w-auto text-lg px-8">Get Started</Button>
                        </Link>
                        <Link to="/login">
                            <Button variant="outline" size="lg" className="w-full sm:w-auto text-lg px-8">Log In</Button>
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="w-full py-12 md:py-24 bg-brand-blue/5 rounded-3xl mb-12">
                <div className="container px-4 md:px-6">
                    <div className="grid gap-12 lg:grid-cols-3 lg:gap-8">
                        <div className="flex flex-col items-center text-center space-y-4">
                            <div className="p-4 bg-brand-light rounded-2xl text-brand-dark">
                                <FileText className="w-8 h-8" />
                            </div>
                            <h3 className="text-xl font-bold">Smart Parsing</h3>
                            <p className="text-gray-500">
                                Upload your PDF or DOCX resume. Our engine extracts your skills and experience instantly.
                            </p>
                        </div>
                        <div className="flex flex-col items-center text-center space-y-4">
                            <div className="p-4 bg-brand-accent rounded-2xl text-white">
                                <Bot className="w-8 h-8" />
                            </div>
                            <h3 className="text-xl font-bold">ATS Scoring</h3>
                            <p className="text-gray-500">
                                See how well you match job requirements before you apply, with highlighted experience gaps.
                            </p>
                        </div>
                        <div className="flex flex-col items-center text-center space-y-4">
                            <div className="p-4 bg-brand-blue rounded-2xl text-white">
                                <TrendingUp className="w-8 h-8" />
                            </div>
                            <h3 className="text-xl font-bold">Job Ranking</h3>
                            <p className="text-gray-500">
                                Stop scrolling through irrelevant listings. We rank top jobs based on your unique profile.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

// Temporary internal badge for landing page until imports are perfectly verified
function Badge({ children, variant, className }) {
    return (
        <span className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold ${variant === 'secondary' ? 'bg-brand-blue/10 text-brand-blue' : 'bg-gray-100'
            } ${className}`}>
            {children}
        </span>
    );
}
