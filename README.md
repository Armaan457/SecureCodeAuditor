# SecureCodeAuditor

SecureCodeAuditor is an AI-powered security tool that helps developers identify and fix vulnerabilities in their code. Just upload a ZIP file containing your code files, and the tool will scan it using intelligent AI agents to detect security issues. It supports multiple programming languages and provides clear, actionable suggestions to improve your code’s safety. With a modern, user friendly interface, SecureCodeAuditor brings powerful security insights to your fingertips.

---

## Features

- **Multi-File Analysis**: Upload ZIP files containing multiple code files for batch analysis.
- **AI-Powered Vulnerability Detection**: Uses AI Agents to identify vulnerabilities such as:
  - XML External Entity (XXE) attacks
  - API Misuse
  - Insecure Direct Object References (IDOR)
  - SQL Injection
  - Command Injection
  - Cross-Site Scripting (XSS)
  - Clickjacking
- **Rate Limiting**: Protects the API from abuse with request rate limits.
- **Multithreading**: Utilizes multithreading to process multiple files simultaneously, along with parallel execution of the agents for each file.

---

## Tech Stack

- **Frontend**: React and Tailwind CSS
- **Backend**: FastAPI
- **AI Agents**: LangGraph
- **Containerization**: Docker

---

## Developers

- [Armaan Jagirdar](https://github.com/Armaan457)
- [Amandeep Singh](https://github.com/amandeepsingh29)
