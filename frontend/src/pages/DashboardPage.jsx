import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { UploadCloud, FileText, Briefcase } from 'lucide-react';

export default function DashboardPage() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadMessage, setUploadMessage] = useState('');
    const [parsedData, setParsedData] = useState(null);
    const [targetRole, setTargetRole] = useState('');

    const handleFileChange = (e) => {
        if (e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setIsUploading(true);
        setUploadMessage('Uploading and parsing resume...');

        try {
            // In a real app we'd need to configure axios to handle FormData properly 
            // by setting Content-Type to multipart/form-data
            const response = await api.post('/resume/upload', formData, {
                headers: {
                    'Content-Type': undefined, // Setting undefined allows Axios to build the proper FormData boundary instead of standard application/json
                },
            });

            setUploadMessage('Resume uploaded successfully!');
            setParsedData(response.data.parsed_data);
        } catch (error) {
            setUploadMessage(error.response?.data?.msg || error.response?.data?.error || 'Failed to upload resume.');
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="space-y-8 max-w-5xl mx-auto py-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Welcome back, {user?.name}</h1>
                <p className="text-gray-500 mt-2">Manage your resume and find matched jobs.</p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
                {/* Upload Section */}
                <Card className="border-2 border-dashed border-gray-200">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <UploadCloud className="w-5 h-5 text-brand-blue" />
                            Upload Resume
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="flex flex-col items-center justify-center p-6 space-y-4">
                        <input
                            type="file"
                            accept=".pdf,.docx"
                            onChange={handleFileChange}
                            className="text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:border-0 file:text-sm file:font-semibold file:bg-brand-light file:text-brand-dark hover:file:bg-brand-light/80"
                        />
                        <Button
                            onClick={handleUpload}
                            disabled={!file || isUploading}
                            className="w-full"
                        >
                            {isUploading ? 'Processing...' : 'Upload & Parse'}
                        </Button>
                        {uploadMessage && (
                            <p className={`text-sm ${uploadMessage.includes('Failed') ? 'text-red-500' : 'text-green-600'}`}>
                                {uploadMessage}
                            </p>
                        )}
                    </CardContent>
                </Card>

                {/* Parsed Info Summary */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <FileText className="w-5 h-5 text-brand-dark" />
                            Resume Profile
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {parsedData ? (
                            <div className="space-y-4">
                                <div>
                                    <h4 className="font-semibold text-sm text-gray-500 mb-2">Detected Skills</h4>
                                    <div className="flex flex-wrap gap-2">
                                        {parsedData.skills?.map(skill => (
                                            <Badge key={skill}>{skill}</Badge>
                                        ))}
                                        {(!parsedData.skills || parsedData.skills.length === 0) && (
                                            <span className="text-sm text-gray-400">No skills detected.</span>
                                        )}
                                    </div>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-sm text-gray-500 mb-2">Experience</h4>
                                    <p className="text-sm">{parsedData.years_of_experience || 0} years</p>
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-8 text-gray-400 flex flex-col items-center">
                                <FileText className="w-12 h-12 mb-2 opacity-20" />
                                <p>No parsed resume data available.</p>
                                <p className="text-sm mt-1">Upload a resume to see your profile.</p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>

            <div className="flex flex-col items-center pt-8 border-t max-w-md mx-auto w-full">
                <div className="w-full mb-4">
                    <label className="text-sm font-semibold mb-2 block text-gray-700">What role are you targeting?</label>
                    <input
                        type="text"
                        value={targetRole}
                        onChange={(e) => setTargetRole(e.target.value)}
                        placeholder="e.g. Senior Frontend Developer"
                        className="w-full rounded-md border p-3 border-gray-300 focus:ring-brand-blue"
                    />
                    <div className="flex gap-4 w-full mt-2">
                        <Button
                            size="lg"
                            className="bg-brand-blue text-white hover:bg-brand-blue/90 flex-1"
                            onClick={() => navigate(`/jobs?role=${encodeURIComponent(targetRole || 'Developer')}&provider=rapidapi`)}
                        >
                            <Briefcase className="w-5 h-5 mr-2" />
                            Search RapidAPI
                        </Button>
                        <Button
                            size="lg"
                            className="bg-brand-accent text-white hover:bg-brand-accent/90 flex-1"
                            onClick={() => navigate(`/jobs?role=${encodeURIComponent(targetRole || 'Developer')}&provider=adzuna`)}
                        >
                            <Briefcase className="w-5 h-5 mr-2" />
                            Search Adzuna
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
