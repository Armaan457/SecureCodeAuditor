import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Download, ArrowLeft, X, Terminal, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
// import * as img from './final.png';
import img from '../assets/final.png';
import { GlitchText } from '../components/GlitchText';
const API_URL = 'http://localhost:8000';

type Vulnerability = {
  vulnerability_type: string;
  code_snippet: string;
  recommendation: string;
};

type AnalysisResults = {
  [filename: string]: Vulnerability[];
};

export default function BetaPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [_, setReport] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const navigate = useNavigate();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    setSelectedFile(acceptedFiles[0]);
    setReport(null);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    maxFiles: 1,
    accept: {
      'application/zip': ['.zip']
    }
  });

const handleProcess = async () => {
  if (!selectedFile) return;

  setIsProcessing(true);
  setError(null);
  setReport(null);
  setAnalysisResults(null);

  try {
    const formData = new FormData();
    formData.append('file', selectedFile);

    const response = await axios.post(`${API_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
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
              setError('Bad request. Please check your file and try again.');
              break;
            case 413:
              setError('File too large. Please upload a smaller file.');
              break;
            case 415:
              setError('Invalid file format. Only ZIP files are allowed.');
              break;
            case 500:
              setError('Server error. Please try again later.');
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
    a.download = `security-report-${selectedFile?.name || 'analysis'}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const clearFile = () => {
    setSelectedFile(null);
    setReport(null);
    setError(null);
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
            Upload your code file for security analysis
          </p>
        </header>

        {/* Enhanced Upload Section */}
        <section className="max-w-2xl mx-auto mb-8 reveal reveal-delay-1">
          {!selectedFile ? (
            <div
              {...getRootProps()}
              className={`
                p-10 border-2 border-dashed rounded-xl backdrop-blur-sm
                ${isDragActive 
                  ? 'border-green-400 bg-green-500/10 shadow-[0_0_15px_rgba(34,197,94,0.3)]' 
                  : 'border-green-500/20'}
                hover:border-green-400 hover:bg-green-500/5 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)]
                transition-all duration-300 cursor-pointer
                flex flex-col items-center justify-center
                min-h-[200px]
              `}
            >
              <input {...getInputProps()} />
              <Upload className={`w-12 h-12 mb-4 text-green-400 ${isDragActive ? 'animate-bounce' : 'animate-float'}`} />
              {isDragActive ? (
                <p className="text-green-300 animate-pulse">Drop the file here...</p>
              ) : (
                <div className="text-center">
                  <p className="mb-2">Drag & drop a code file here, or click to select</p>
                  <p className="text-sm text-green-500/60">Supported format: .zip (archive your code files)</p>
                </div>
              )}
            </div>
          ) : (
            <div className="p-6 border border-green-500/20 rounded-xl bg-green-500/5 backdrop-blur-sm hover:shadow-[0_0_15px_rgba(34,197,94,0.2)] transition-all duration-300">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Terminal className="w-5 h-5 text-green-400" />
                  <span className="text-green-400 font-medium">{selectedFile.name}</span>
                </div>
                <button
                  onClick={clearFile}
                  className="text-green-400 hover:text-green-300 transition-colors p-2 hover:bg-green-500/10 rounded-full"
                  title="Remove file"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <button
                onClick={handleProcess}
                disabled={isProcessing}
                className={`
                  w-full py-3 px-6 rounded-lg
                  flex items-center justify-center gap-2
                  ${isProcessing 
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
                    Process File
                  </>
                )}
              </button>
            </div>
          )}
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
              {vulns.length === 0 ? (
                <p className="text-green-400">No vulnerabilities found.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-left text-green-400">
                    <thead>
                      <tr>
                        <th className="px-4 py-2 border-b border-green-500/20">Type</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Code Snippet</th>
                        <th className="px-4 py-2 border-b border-green-500/20">Recommendation</th>
                      </tr>
                    </thead>
                    <tbody>
                      {vulns.map((vuln, idx) => (
                        <tr key={idx} className="hover:bg-green-500/10">
                          <td className="px-4 py-2 border-b border-green-500/10">{vuln.vulnerability_type}</td>
                          <td className="px-4 py-2 border-b border-green-500/10 whitespace-pre-wrap font-mono text-xs">{vuln.code_snippet}</td>
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
    
