import os
import json
import subprocess
import tempfile
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import uuid
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Try different model names in order of preference
MODEL_NAMES = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
model = None

for model_name in MODEL_NAMES:
    try:
        model = genai.GenerativeModel(model_name)
        # Test the model with a simple prompt
        response = model.generate_content("Hello")
        print(f"✅ Using Gemini model: {model_name}")
        break
    except Exception as e:
        print(f"❌ Model {model_name} failed: {str(e)}")
        continue

if model is None:
    print("⚠️ Warning: No Gemini model available. AI features will use fallback responses.")
    model = None

# Supported languages and their configurations
SUPPORTED_LANGUAGES = {
    'python': {
        'extension': '.py',
        'compile_cmd': None,
        'run_cmd': ['python', '{file_path}'],
        'timeout': 10
    },
    'java': {
        'extension': '.java',
        'compile_cmd': ['javac', '{file_path}'],
        'run_cmd': ['java', '{class_name}'],
        'timeout': 15
    },
    'cpp': {
        'extension': '.cpp',
        'compile_cmd': ['g++', '-o', '{output_path}', '{file_path}'],
        'run_cmd': ['{output_path}'],
        'timeout': 15
    }
}

def generate_coding_problem(topic):
    """Generate a coding problem using Gemini API"""
    required_fields = [
        "problem", "problem_statement", "sample_input", "sample_output",
        "testcase_explanation", "difficulty", "constraints"
    ]
    default_problem = {
        "problem": f"Write a program to solve problems related to {topic}",
        "problem_statement": f"Write a program to solve problems related to {topic}",
        "sample_input": "Sample input",
        "sample_output": "Sample output",
        "testcase_explanation": "Basic test case",
        "difficulty": "medium",
        "constraints": "No specific constraints"
    }

    if model is None:
        default_problem["error"] = "Gemini API model not available"
        return default_problem

    prompt = f"""
    Generate a coding problem related to the topic: {topic}
    Please provide the response in the following JSON format:
    {{
        "problem": "Clear description of the problem",
        "problem_statement": "Clear description of the problem",
        "sample_input": "Example input",
        "sample_output": "Expected output for the sample input",
        "testcase_explanation": "Explanation of the test case",
        "difficulty": "easy/medium/hard",
        "constraints": "Any constraints or requirements"
    }}
    Make sure the problem is:
    1. Clear and well-defined
    2. Appropriate for the topic
    3. Has a single correct solution
    4. Includes proper constraints
    """

    try:
        response = model.generate_content(prompt)
        # Try to extract JSON from the response text
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            result = json.loads(match.group(0))
        else:
            result = json.loads(response.text)
        # Ensure all required fields are present
        for field in required_fields:
            if field not in result:
                result[field] = default_problem[field]
        return result
    except Exception as e:
        default_problem["error"] = f"Failed to generate problem: {str(e)}"
        return default_problem

def get_ai_feedback(code, language, output=None, error=None, problem=None):
    """Get AI feedback on code execution, considering problem context if provided"""
    if model is None:
        # Return fallback feedback when model is not available
        if error:
            return {
                "error_analysis": "Code execution failed",
                "solution": "Check your code syntax and logic",
                "best_practices": "Always test your code with simple examples first",
                "suggested_code": "Unable to provide specific suggestions without AI model"
            }
        else:
            return {
                "quality_assessment": "Code executed successfully",
                "optimization_suggestions": "Consider code efficiency and readability",
                "readability_improvements": "Add comments and use clear variable names",
                "best_practices": "Follow language-specific coding conventions"
            }
    
    # Build problem context string if provided
    problem_context = ""
    if problem:
        problem_context = f"""
You are given the following coding problem:

Problem Statement:
{problem.get('problem_statement', '')}

Constraints:
{problem.get('constraints', '')}

Sample Input:
{problem.get('sample_input', '')}

Sample Output:
{problem.get('sample_output', '')}
"""
    
    if error:
        prompt = f"""
{problem_context}
The following {language} code has an error:

Code:
{code}

Error:
{error}

Please provide:
1. What caused the error (with respect to the problem statement if possible)
2. How to fix it
3. Best practices to avoid this error
4. If possible, provide a corrected version of the code

Format your response as JSON:
{{
    "error_analysis": "What went wrong",
    "solution": "How to fix it",
    "best_practices": "Tips to avoid this error",
    "suggested_code": "Corrected version if applicable"
}}
"""
    else:
        prompt = f"""
{problem_context}
Here is the user's solution in {language}:

{code}

Output:
{output}

Please review the code for:
1. Correctness with respect to the problem statement and constraints.
2. Code quality, optimization, and best practices.

Format your response as JSON:
{{
  "correctness": "Does the code solve the problem correctly?",
  "quality_assessment": "Overall code quality",
  "optimization_suggestions": "Performance improvements",
  "readability_improvements": "Code clarity suggestions",
  "best_practices": "Programming best practices"
}}
"""
    try:
        response = model.generate_content(prompt)
        print("AI Review Response:", json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        return {
            "error": f"Failed to get AI feedback: {str(e)}",
            "message": "Unable to analyze code at this time"
        }

def execute_code_safely(code, language, custom_input=""):
    """Execute code in a safe sandboxed environment"""
    if language not in SUPPORTED_LANGUAGES:
        return {"error": f"Unsupported language: {language}"}
    
    lang_config = SUPPORTED_LANGUAGES[language]
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create unique filename
            file_id = str(uuid.uuid4())
            file_path = os.path.join(temp_dir, f"code{lang_config['extension']}")
            
            # Write code to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile if needed
            if lang_config['compile_cmd']:
                compile_cmd = [cmd.format(
                    file_path=file_path,
                    output_path=os.path.join(temp_dir, 'output'),
                    class_name='Code'
                ) for cmd in lang_config['compile_cmd']]
                
                compile_result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    timeout=lang_config['timeout'],
                    cwd=temp_dir
                )
                
                if compile_result.returncode != 0:
                    return {
                        "error": f"Compilation error: {compile_result.stderr}",
                        "output": None
                    }
            
            # Run the code
            run_cmd = [cmd.format(
                file_path=file_path,
                output_path=os.path.join(temp_dir, 'output'),
                class_name='Code'
            ) for cmd in lang_config['run_cmd']]
            
            run_result = subprocess.run(
                run_cmd,
                input=custom_input,
                capture_output=True,
                text=True,
                timeout=lang_config['timeout'],
                cwd=temp_dir
            )
            
            if run_result.returncode != 0:
                return {
                    "error": f"Runtime error: {run_result.stderr}",
                    "output": None
                }
            
            return {
                "output": run_result.stdout,
                "error": None
            }
            
    except subprocess.TimeoutExpired:
        return {"error": "Code execution timed out", "output": None}
    except Exception as e:
        return {"error": f"Execution error: {str(e)}", "output": None}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "AI Coding Platform Backend is running"})

@app.route('/generate-problem', methods=['POST'])
def generate_problem():
    """Generate a coding problem based on topic"""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        problem = generate_coding_problem(topic)
        return jsonify(problem)
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate problem: {str(e)}"}), 500

@app.route('/execute-code', methods=['POST'])
def execute_code():
    """Execute user code and return results"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python').lower()
        custom_input = data.get('custom_input', '')
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        # Execute code
        result = execute_code_safely(code, language, custom_input)
        
        # Get AI feedback
        if result.get('error'):
            feedback = get_ai_feedback(code, language, error=result['error'])
        else:
            feedback = get_ai_feedback(code, language, output=result['output'])
        
        # Return a more frontend-friendly structure
        response = {
            "success": result.get('error') is None,
            "output": result.get('output', ''),
            "error": result.get('error'),
            "execution_result": result,
            "ai_feedback": feedback
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Failed to execute code: {str(e)}"}), 500

@app.route('/review-code', methods=['POST'])
def review_code():
    """Get AI code review without execution, considering problem context if provided"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python').lower()
        problem = data.get('problem', None)
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        feedback = get_ai_feedback(code, language, problem=problem)
        return jsonify(feedback)
        
    except Exception as e:
        print('Error in review-code:', e)
        return jsonify({"error": f"Failed to review code: {str(e)}"}), 500

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug) 