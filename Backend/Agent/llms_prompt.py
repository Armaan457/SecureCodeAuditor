import os

from dotenv import load_dotenv
load_dotenv() 

gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_api_key_2 = os.getenv('GEMINI_API_KEY_2')
gemini_api_key_3 = os.getenv('GEMINI_API_KEY_3')
gemini_api_key_4 = os.getenv('GEMINI_API_KEY_4')
gemini_api_key_5 = os.getenv('GEMINI_API_KEY_5')

MODELS = [
    {
        "name": "gemini-1.5-flash-8b",
        "api_key": gemini_api_key,
        "task": f"Inspect the code for vulnerabilities in XML processing and API configurations. Look for XML External Entity (XXE) attacks, insecure API usage, and Security Misconfigurations. Provide the output STRICTLY in the specified structure ONLY, no markdown or other text needed. Required output structure {{\"findings\":[{{\"vulnerability_type\":\"XML External Entity (XXE)\",\"code_snippet\":\"etree.parse(user_input)\",\"recommendation\":\"Disable external entity resolution when processing XML files.\"}},{{\"vulnerability_type\":\"API Misuse\",\"code_snippet\":\"response = requests.post(api_url, data=user_data)\",\"recommendation\":\"Use secure authentication and validate API responses.\"}}]}}. In case no vulnerability found return findings empty"
    },
    {
        "name": "gemini-1.5-flash",
        "api_key": gemini_api_key_2,
        "task": f"Analyze the code for access control vulnerabilities. Look for Insecure Direct Object References (IDOR), Host Header Injection, and Subdomain Takeover risks. Identify instances where access control mechanisms are improperly implemented. Provide the output STRICTLY in the specified structure ONLY, no markdown or other text needed. Required output structure {{\"findings\":[{{\"vulnerability_type\":\"Insecure Direct Object Reference (IDOR)\",\"code_snippet\":\"GET /user/123\",\"recommendation\":\"Implement access controls to verify the requester is authorized to access the resource.\"}},{{\"vulnerability_type\":\"Host Header Injection\",\"code_snippet\":\"url = request.headers['Host'] + '/login'\",\"recommendation\":\"Validate and sanitize the Host header to prevent injection attacks.\"}}]}}. In case no vulnerability found return findings empty"
    },
    {
        "name": "gemini-1.5-flash-8b",
        "api_key": gemini_api_key_3,
        "task": f"Scan the code for vulnerabilities related to file access. Detect instances of Path Traversal, Local File Inclusion (LFI), and Remote File Inclusion (RFI). Focus on functions that handle file paths or include external files. Provide the output STRICTLY in the specified structure ONLY, no markdown or other text needed. Required output structure {{\"findings\":[{{\"vulnerability_type\":\"Path Traversal\",\"code_snippet\":\"open('../../etc/passwd', 'r')\",\"recommendation\":\"Validate file paths and restrict access to specific directories.\"}},{{\"vulnerability_type\":\"Local File Inclusion (LFI)\",\"code_snippet\":\"exec(open(user_input).read())\",\"recommendation\":\"Ensure user input is validated and does not reference sensitive files.\"}}]}}. In case no vulnerability found return findings empty"
    },
    {
        "name": "gemini-1.5-flash",
        "api_key": gemini_api_key_4,
        "task": f"Examine the code for client-side vulnerabilities. Specifically, identify potential Cross-Site Scripting (XSS), Clickjacking, and Content Spoofing issues. Look for improper handling of user-generated content or unsafe rendering practices. Provide the output STRICTLY in the specified structure ONLY, no markdown or other text needed. Required output structure {{\"findings\":[{{\"vulnerability_type\":\"Cross-Site Scripting (XSS)\",\"code_snippet\":\"{{{{ user_input }}}}\",\"recommendation\":\"Escape or sanitize user-generated content before rendering.\"}},{{\"vulnerability_type\":\"Clickjacking\",\"code_snippet\":\"response.headers['X-Frame-Options'] = 'ALLOW'\",\"recommendation\":\"Set 'X-Frame-Options' to 'DENY' or 'SAMEORIGIN' to prevent clickjacking.\"}}]}}. In case no vulnerability found return findings empty"
    },
    {
        "name": "gemini-1.5-flash",
        "api_key": gemini_api_key_5,
        "task": f"Analyze the provided code for vulnerabilities related to user input handling. Specifically, detect cases where user input is directly passed into SQL queries, system commands, or dynamic code execution without validation or sanitization. Focus on identifying potential SQL Injection, Command Injection, and Code Injection vulnerabilities. Provide the output STRICTLY in the specified structure ONLY, no markdown or other text needed. Required output structure {{\"findings\":[{{\"vulnerability_type\":\"SQL Injection\",\"code_snippet\":\"cursor.execute('SELECT * FROM users WHERE id = ' + user_input)\",\"recommendation\":\"Use parameterized queries to prevent SQL injection.\"}},{{\"vulnerability_type\":\"Command Injection\",\"code_snippet\":\"os.system('ping ' + user_input)\",\"recommendation\":\"Validate and sanitize user input before passing it to system commands.\"}}]}}. In case no vulnerability found return findings empty"
    }
]