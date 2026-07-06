import { useState } from 'react';
import { Download, ArrowLeft, X, Terminal, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
// import * as img from './final.png';
import img from '../assets/final.png';
import { GlitchText } from '../components/GlitchText';
const API_URL = 'https://secure-code-auditor-backend.vercel.app';

type Severity =
  | "Critical"
  | "High"
  | "Medium"
  | "Low"
  | "Informational";

type Confidence = "High" | "Medium";

type Finding = {
  vulnerability_type: string;
  severity: Severity;
  confidence: Confidence;
  code_snippet: string;
  reason: string;
  recommendation: string;
};

type AnalysisResults = {
  [filename: string]: Finding[];
};

export default function BetaPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [githubUrl, setGithubUrl] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const navigate = useNavigate();

const handleProcess = async () => {
  const sanitizedUrl = githubUrl.trim();
  if (!sanitizedUrl) {
    setError('Please enter a GitHub repository URL.');
    return;
  }

  setIsProcessing(true);
  setError(null);
  setAnalysisResults(null);

  try {
    const response = await axios.post(`${API_URL}/analyze`, {
      github_url: sanitizedUrl,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.data?.results) {
      setAnalysisResults(response.data.results);
    } else {
      throw new Error('Invalid response format');
    }
  } catch (error: any) {
    console.error('Error processing file:', error);
    
    // Check if it's a network error (server offline)
    if (error.code === 'ERR_NETWORK' || error.message === 'Network Error' || !error.response) {
      setError('Server offline. Please check your connection or come back later.');
    }
    // Check for specific HTTP status codes
    else if (error.response) {
      const status = error.response.status;
      const detail = error.response.data?.detail;
      
      if (status !== 200) {
        if (detail) {
          setError(detail);
        } else {
          switch (status) {
            case 400:
              setError('Bad request. Please check the GitHub URL and try again.');
              break;
            case 422:
              setError('Invalid GitHub URL format. Please enter a valid repository link.');
              break;
            case 404:
              setError('Repository not found or inaccessible. Check the URL and repository visibility.');
              break;
            case 500:
              setError('Server error. Please try again later.');
              break;
            case 429:
              setError("Rate limit exceeded. Please wait a minute before trying again.");
              break;
            default:
              setError(`Request failed with status ${status}. Please try again.`);
          }
        }
      }
    }
    // Fallback error message
    else {
      setError('Failed to process file. Please try again.');
    }
  } finally {
    setIsProcessing(false);
  }
};

  const handleDownload = () => {
    if (!analysisResults) return;

    const content = JSON.stringify(analysisResults, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const repoSlug = githubUrl
      .trim()
      .replace(/^https?:\/\/github\.com\//, '')
      .replace(/[^a-zA-Z0-9-_/.]/g, '')
      .replace(/\//g, '-') || 'analysis';
    a.download = `security-report-${repoSlug}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const clearInput = () => {
    setGithubUrl('');
    setError(null);
    setAnalysisResults(null);
  };

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono relative overflow-hidden">
      {/* Enhanced Matrix-like Background */}
      <div className="fixed inset-0 bg-[linear-gradient(to_right,#0f0f0f_1px,transparent_1px),linear-gradient(to_bottom,#0f0f0f_1px,transparent_1px)] bg-[size:2rem_2rem] opacity-20 animate-pulse-slow" />
      <div className="fixed inset-0 bg-gradient-to-b from-black via-transparent to-black pointer-events-none" />
      
      {/* Enhanced Circuit Lines */}
      <div className="fixed inset-0 circuit-pattern opacity-20" />

      {/* Animated Glow Effects */}
      <div className="fixed inset-0">
        <div className="absolute inset-0 bg-gradient-radial from-green-500/10 via-transparent to-transparent blur-3xl animate-pulse-slow" />
        <div className="absolute inset-0 bg-gradient-conic from-green-500/5 via-transparent to-transparent animate-spin-slow" />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Enhanced Header */}
        <header className="text-center mb-20 ">
        <button
            onClick={() => navigate("/")}
            className="absolute top-4 left-4 hover:text-green-400 transition-colors inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-green-500/20 hover:border-green-400/40"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>
          
          <div className="flex justify-center mb-8 relative">
            <div className="absolute inset-0 animate-pulse-slow bg-green-500/20 blur-xl rounded-full" />
            <img 
              src={img}  
              alt="Logo" 
              className="w-25 h-25 relative animate-float drop-shadow-[0_0_15px_rgba(34,197,94,0.3)]" 
            />
          </div>
          <h1 className="text-5xl md:text-7xl lg:text-8xl mb-6 leading-none">
            <GlitchText text="SecureCodeAuditor" className="font-bold tracking-tight block" />
            {/* <GlitchText text="Beta" className="font-bold tracking-tight block text-green-500" /> */}
          </h1>
          <p className="text-xl text-green-500/80 max-w-2xl mx-auto typewriter-1">
            Paste a GitHub repository URL for security analysis
          </p>
        </header>

        {/* Repository Input Section */}
        <section className="max-w-2xl mx-auto mb-8 reveal reveal-delay-1">
          <div className="p-6 border border-green-500/20 rounded-xl bg-green-500/5 backdrop-blur-sm hover:shadow-[0_0_15px_rgba(34,197,94,0.2)] transition-all duration-300">
            <div className="mb-4">
              <label htmlFor="github-url" className="block text-sm text-green-500/80 mb-2">
                GitHub Repository URL
              </label>
              <div className="flex items-center gap-2">
                <input
                  id="github-url"
                  type="url"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                  placeholder="https://github.com/owner/repository"
                  className="w-full px-4 py-3 rounded-lg border border-green-500/30 bg-black/40 text-green-300 placeholder:text-green-500/50 focus:outline-none focus:ring-2 focus:ring-green-400/40 focus:border-green-400"
                />
                <button
                  onClick={clearInput}
                  type="button"
                  className="text-green-400 hover:text-green-300 transition-colors p-2 hover:bg-green-500/10 rounded-full"
                  title="Clear URL"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <p className="text-sm text-green-500/60 mt-2">Example: https://github.com/owner/repo</p>
            </div>

            <button
              onClick={handleProcess}
              disabled={isProcessing || !githubUrl.trim()}
              className={`
                w-full py-3 px-6 rounded-lg
                flex items-center justify-center gap-2
                ${isProcessing || !githubUrl.trim()
                  ? 'bg-green-500/20 cursor-not-allowed'
                  : 'bg-green-500/20 hover:bg-green-500/30 border border-green-500/40 hover:border-green-400 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]'}
                transition-all duration-300 group
              `}
            >
              {isProcessing ? (
                <>
                  <div className="animate-spin h-5 w-5 border-2 border-green-400 border-t-transparent rounded-full" />
                  Processing...
                </>
              ) : (
                <>
                  <Terminal className="w-5 h-5 group-hover:animate-bounce" />
                  Analyze Repository
                </>
              )}
            </button>

            <p className="text-xs text-green-500/50 mt-3">
              Public repositories work best. Private repositories require backend access credentials.
            </p>
            </div>
        </section>

        {/* Enhanced Error Message */}
        {error && (
          <div className="max-w-2xl mx-auto mb-8 text-red-400 text-center bg-red-500/10 border border-red-500/20 rounded-lg p-4 backdrop-blur-sm reveal">
            <div className="flex items-center justify-center gap-2">
              <AlertCircle className="w-5 h-5" />
              {error}
            </div>
          </div>
        )}

        {/* Enhanced Download Section */}
        {analysisResults && !isProcessing && (
        <section className="max-w-2xl mx-auto text-center reveal reveal-delay-2">
          <button
            onClick={handleDownload}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-green-500/20 hover:bg-green-500/30 border border-green-500/40 hover:border-green-400 transition-all duration-300 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)] group"
          >
            <Download className="w-5 h-5 group-hover:animate-bounce" />
            Download Report (JSON)
          </button>
        </section>
      )}

      {/* Vulnerability Table */}
      {analysisResults && (
        <section className="max-w-2xl mx-auto mt-8 bg-green-500/5 border border-green-500/20 rounded-lg p-6 backdrop-blur-sm reveal">
          {Object.entries(analysisResults).map(([filename, vulns]) => (
            <div key={filename} className="mb-8">
              <h2 className="text-xl font-bold mb-4 text-green-300">{filename}</h2>
              {!Array.isArray(vulns) || vulns.length === 0 ? (
                <p className="text-green-400">No vulnerabilities found.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-left text-green-400">
                    <thead>
                      <tr>
                        <th className="px-4 py-2 border-b border-green-500/20">Type</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Severity</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Confidence</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Code Snippet</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Reason</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Recommendation</th>
                      </tr>
                    </thead>
                    <tbody>
                      {vulns.map((vuln, idx) => (
                        <tr key={`${filename}-${idx}`} className="hover:bg-green-500/10">
                          <td className="px-4 py-2 border-b border-green-500/10">{vuln.vulnerability_type}</td>
                          <td className="px-4 py-2 border-b border-green-500/10">{vuln.severity}</td>
                          <td className="px-4 py-2 border-b border-green-500/10">{vuln.confidence}</td>
                          <td className="px-4 py-2 border-b border-green-500/10 whitespace-pre-wrap font-mono text-xs">{vuln.code_snippet}</td>
                          <td className="px-4 py-2 border-b border-green-500/10">{vuln.reason}</td>
                          <td className="px-4 py-2 border-b border-green-500/10">{vuln.recommendation}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          ))}
        </section>
      )}
    </div>
  </div>
  );
}
    
