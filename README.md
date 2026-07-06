# 🛡️ SecureCodeAuditor

SecureCodeAuditor is an **AI-powered Static Application Security Testing (SAST) platform** designed to help developers identify security vulnerabilities before deployment.

SecureCodeAuditor leverages a **LangGraph-powered multi-agent architecture**, where specialized AI security agents independently analyze source code for different classes of vulnerabilities. 

Whether you're auditing a mini project or an entire repository, SecureCodeAuditor provides fast, scalable, and explainable security analysis through an intuitive web interface.

---

## Features

* AI-powered security analysis using multiple specialized agents
* Analyze public GitHub repositories directly through repository ingestion
* Evidence-based vulnerability detection to reduce false positives and improve accuracy
* Fast repository scanning with parallel file processing and AI analysis
* Smart commit-based caching to instantly return results for unchanged repositories
* Automatic repository validation, including repository availability, supported file types, size, and file limits
* Comprehensive security reports with severity, confidence, affected code, explanations, and remediation suggestions
* Modular architecture that makes it easy to extend with additional security agents

---

## Tech Stack

- **Frontend:** React (TypeScript) and Tailwind CSS
- **Backend:** FastAPI and Pydantic
- **AI Agents:** LangGraph
- **Caching:** Upstash Redis

## Supported Languages

* Python
* Java
* JavaScript
* TypeScript
* React (JSX/TSX)
* C
* C++
* Go
* HTML
* CSS

##  Security Coverage

SecureCodeAuditor analyzes code for a broad range of security issues, including:
* Injection vulnerabilities (SQL, Command, Code)
* Cross-Site Scripting (XSS)
* Insecure Direct Object References (IDOR)
* XML External Entity (XXE)
* Path Traversal
* API Security Misuse
* Authentication & Authorization flaws
* Security Misconfigurations
* Clickjacking
* Unsafe File Handling

## Developers

- [Armaan Jagirdar](https://github.com/Armaan457)
- [Amandeep Singh](https://github.com/amandeepsingh29)
