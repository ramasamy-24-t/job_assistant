import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Building, MapPin, Target, AlertCircle, DollarSign, ExternalLink, X } from 'lucide-react';

export default function JobResultsPage() {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [selectedJob, setSelectedJob] = useState(null);
    const location = useLocation();

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const searchParams = new URLSearchParams(location.search);
                const role = searchParams.get('role') || 'Developer';
                const provider = searchParams.get('provider') || 'rapidapi';

                const response = await api.get(`/jobs/ranked?role=${encodeURIComponent(role)}&provider=${encodeURIComponent(provider)}`);
                setJobs(response.data.jobs);
            } catch (err) {
                setError(err.response?.data?.error || 'Failed to fetch jobs. Make sure you uploaded a resume.');
            } finally {
                setLoading(false);
            }
        };

        fetchJobs();
    }, [location.search]);

    if (loading) {
        return <div className="flex justify-center items-center py-20 text-gray-500">Loading your ranked jobs...</div>;
    }

    if (error) {
        return (
            <div className="max-w-3xl mx-auto mt-12 bg-red-50 border border-red-200 text-red-700 p-6 rounded-lg flex items-start gap-4">
                <AlertCircle className="w-6 h-6 mt-0.5 flex-shrink-0" />
                <div>
                    <h3 className="font-bold text-lg mb-1">Couldn't load jobs</h3>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto py-8 relative">
            <div className="mb-8">
                <h1 className="text-3xl font-bold tracking-tight">Your Top Matches</h1>
                <p className="text-gray-500 mt-2">Ranked based on your ATS resume score across your preferred locations.</p>
            </div>

            <div className="space-y-6">
                {jobs.map((job, idx) => (
                    <Card
                        key={job.id || idx}
                        className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer border-l-4 border-l-brand-blue"
                        onClick={() => setSelectedJob(job)}
                    >
                        <div className="p-6 md:flex gap-6">

                            {/* Job Info */}
                            <div className="flex-1 space-y-4">
                                <div>
                                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-brand-blue">{job.title}</h3>
                                    <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-3 text-sm text-gray-600">
                                        <span className="flex items-center gap-1 font-medium">
                                            <Building className="w-4 h-4 text-gray-400" /> {job.company || 'Confidential'}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <MapPin className="w-4 h-4 text-gray-400" /> {job.location}
                                        </span>
                                        {job.salary && job.salary !== 'N/A' && (
                                            <span className="flex items-center gap-1 bg-green-50 text-green-700 px-2 py-0.5 rounded-full font-semibold">
                                                <DollarSign className="w-3 h-3" /> {job.salary}
                                            </span>
                                        )}
                                    </div>
                                </div>

                                <div
                                    className="text-sm text-gray-600 line-clamp-2"
                                    dangerouslySetInnerHTML={{ __html: job.requirements || '' }}
                                />

                            </div>

                            {/* Score Box */}
                            <div className="mt-6 md:mt-0 md:w-48 flex flex-col justify-center items-center bg-gray-50 rounded-lg p-4 border shrink-0">
                                <div className="text-center w-full">
                                    <div className="text-sm text-gray-500 font-medium mb-1">ATS Match</div>
                                    <div className="text-4xl font-black text-brand-dark flex justify-center items-end gap-1">
                                        {Math.round(job.ats_match_score || 0)}
                                        <span className="text-lg text-gray-400 font-medium pb-1">%</span>
                                    </div>
                                    <div className="text-xs text-gray-500 mt-2 truncate w-full">
                                        {job.ats_details?.experience_gap || 'Experience match'}
                                    </div>
                                </div>
                                <Button
                                    className="w-full mt-4"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        window.open(job.link, '_blank');
                                    }}
                                >
                                    Apply Now
                                </Button>
                            </div>

                        </div>
                    </Card>
                ))}

                {jobs.length === 0 && (
                    <div className="text-center py-20 text-gray-500 border-2 border-dashed rounded-lg">
                        <p className="text-lg">No jobs found for this role and your locations.</p>
                        <p className="text-sm mt-2">Try updating your preferred locations in your profile.</p>
                    </div>
                )}
            </div>

            {/* Modal for Job Details */}
            {selectedJob && (
                <div className="fixed inset-0 bg-black/60 z-50 flex justify-center items-center p-4 sm:p-6">
                    <div className="bg-white rounded-xl shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in duration-200">

                        {/* Modal Header */}
                        <div className="p-6 border-b flex justify-between items-start bg-gray-50/50">
                            <div className="pr-8">
                                <h2 className="text-2xl font-bold text-gray-900">{selectedJob.title}</h2>
                                <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-gray-600">
                                    <span className="flex items-center gap-1.5 font-medium">
                                        <Building className="w-4 h-4" /> {selectedJob.company || 'Confidential'}
                                    </span>
                                    <span className="flex items-center gap-1.5">
                                        <MapPin className="w-4 h-4" /> {selectedJob.location}
                                    </span>
                                </div>
                            </div>
                            <button
                                onClick={() => setSelectedJob(null)}
                                className="text-gray-400 hover:text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-full p-2 transition-colors absolute top-6 right-6"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Modal Body */}
                        <div className="overflow-y-auto p-6 space-y-8">

                            {/* Metadata Grid */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                                <div>
                                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1">Salary</p>
                                    <p className="font-semibold text-gray-900">{selectedJob.salary && selectedJob.salary !== 'N/A' ? selectedJob.salary : 'Not specified'}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1">Job Type</p>
                                    <p className="font-semibold text-gray-900">{selectedJob.type || 'Standard'}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1">Source</p>
                                    <p className="font-semibold text-gray-900 truncate" title={selectedJob.source}>{selectedJob.source}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1">ATS Score</p>
                                    <p className="font-bold text-brand-dark">{Math.round(selectedJob.ats_match_score || 0)}%</p>
                                </div>
                            </div>

                            {/* Description */}
                            <div>
                                <h3 className="text-lg font-bold mb-3 border-b pb-2">About the Role</h3>
                                <div
                                    className="text-gray-700 text-sm leading-relaxed prose prose-sm max-w-none"
                                    dangerouslySetInnerHTML={{ __html: selectedJob.requirements || 'No description provided.' }}
                                />
                            </div>

                            {/* ATS Analysis */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-bold mb-3 border-b pb-2">Your ATS Analysis</h3>

                                {/* Matched Skills */}
                                <div>
                                    <h4 className="text-sm font-semibold text-green-700 mb-2">Matched Skills ✅</h4>
                                    {selectedJob.ats_details?.matched_skills?.length > 0 ? (
                                        <div className="flex flex-wrap gap-2">
                                            {selectedJob.ats_details.matched_skills.map(skill => (
                                                <Badge key={skill} variant="success" className="bg-green-100 text-green-800 hover:bg-green-200 border-green-200">{skill}</Badge>
                                            ))}
                                        </div>
                                    ) : (
                                        <p className="text-sm text-gray-500 italic">No direct matches found.</p>
                                    )}
                                </div>

                                {/* Missing Skills */}
                                <div className="pt-2">
                                    <h4 className="text-sm font-semibold text-red-600 mb-2">Missing Skills ⚠️</h4>
                                    {selectedJob.ats_details?.missing_skills?.length > 0 ? (
                                        <div className="flex flex-wrap gap-2">
                                            {selectedJob.ats_details.missing_skills.map(skill => (
                                                <Badge key={skill} variant="destructive" className="bg-red-50 text-red-700 hover:bg-red-100 border-red-200">{skill}</Badge>
                                            ))}
                                        </div>
                                    ) : (
                                        <p className="text-sm text-gray-500 italic">All required skills detected! 🎉</p>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Modal Footer */}
                        <div className="p-6 border-t bg-gray-50 rounded-b-xl flex justify-end gap-3 shrink-0">
                            <Button variant="outline" onClick={() => setSelectedJob(null)}>
                                Close File
                            </Button>
                            <Button
                                className="bg-brand-accent hover:bg-brand-accent/90 text-white min-w-[180px]"
                                onClick={() => window.open(selectedJob.link, '_blank')}
                            >
                                Apply Now <ExternalLink className="w-4 h-4 ml-2" />
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
