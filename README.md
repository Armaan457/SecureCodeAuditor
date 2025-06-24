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
- **AI Agents**: LangGraph and Gemini

---

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Armaan457/SecureCodeAuditor
   ```
2. Navigate to the `Backend` directory:
   ```bash
   cd Backend
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the server:
   ```bash
   cd Backend
   python main.py
   ```

### Frontend Setup

1. Navigate to the `Frontend` directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and go to `http://localhost:5173` (or the port shown in your terminal).


## Developers

- [Armaan Jagirdar](https://github.com/Armaan457)
- [Amandeep Singh](https://github.com/amandeepsingh29)
