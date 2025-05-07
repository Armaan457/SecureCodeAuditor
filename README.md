# SecureCodeAuditor - Agents & Backend

SecureCodeAuditor is a project designed to analyze code files for vulnerabilities using AI Agents. It supports multiple file types and provides detailed findings with recommendations for improving code security. The project is built with a FastAPI backend and uses LangGraph for agent orchestration.

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

- **Backend**: FastAPI
- **AI Agents**: LangGraph and Gemini

---

## Installation

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Armaan457/SecureCodeAuditor-Agents_and_Backend.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   \env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   cd Backend
   python main.py
   ```

## API Documentation

### Endpoint: `/analyze`

#### Method: `POST`

#### Request:

- **Body**:
  - `file` (required): A ZIP file containing code files to be analyzed. Only files with the following extensions are processed: `.py`, `.js`, `.ts`, `.json`, `.jsx`, `.tsx`, `.java`, `.xml`, `.html`, `.css`, `.go`, `.c`, `.cpp`.

#### Response:
- **Status Code**: `200 OK`
- **Response Model**: `FindingsResponse`
  ```json
  {
    "results": {
      "filename1": [
        {
          "vulnerability_type": "string",
          "code_snippet": "string",
          "recommendation": "string"
        }
      ],
      "filename2": [
        {
          "vulnerability_type": "string",
          "code_snippet": "string",
          "recommendation": "string"
        }
      ]
    }
  }
  ```

#### Error Responses:
- **400 Bad Request**:
  - Invalid file format:
    ```json
    {
      "detail": "Invalid file format. Only ZIP files are allowed."
    }
    ```
  - No valid files in the ZIP:
    ```json
    {
      "detail": "No valid files found in the ZIP."
    }
    ```

- **429 Too Many Requests**:
  - Rate limit exceeded:
    ```json
    {
      "detail": "Rate limit exceeded. Try again later."
    }
    ```

- **500 Internal Server Error**:
  - Processing error:
    ```json
    {
      "detail": "We're still in developement phase, Try again later with less number of files"
    }
    ```

#### Rate Limiting:
- **Limit**: 5 requests per minute per client.
- **Response on exceeding limit**: `429 Too Many Requests`

#### Example Usage:
**Request**:
```bash
curl -X POST "http://localhost:8000/analyze" \
-F "file=@path/to/your/code.zip"
```

**Response**:
```json
{
  "results": {
    "example.py": [
      {
        "vulnerability_type": "SQL Injection",
        "code_snippet": "cursor.execute('SELECT * FROM users WHERE id = ' + user_input)",
        "recommendation": "Use parameterized queries to prevent SQL injection."
      },
      {
        "vulnerability_type": "Command Injection",
        "code_snippet": "os.system('ping ' + user_input)",
        "recommendation": "Validate and sanitize user input before passing it to system commands."
      }
    ]
  }
}
```



