import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import time
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

# Page configuration
st.set_page_config(
    page_title="RapoZCode - AI-Powered Coding Platform",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject JavaScript to suppress Popper.js warnings
components.html("""
<script>
// Suppress Popper.js warnings immediately
(function() {
    const originalWarn = console.warn;
    const originalError = console.error;
    
    console.warn = function(...args) {
        const message = args.join(' ');
        if (message.includes('preventOverflow') || 
            message.includes('hide modifier') || 
            message.includes('isModifierRequired')) {
            return; // Suppress Popper.js warnings
        }
        originalWarn.apply(console, args);
    };
    
    console.error = function(...args) {
        const message = args.join(' ');
        if (message.includes('preventOverflow') || 
            message.includes('hide modifier') || 
            message.includes('isModifierRequired')) {
            return; // Suppress Popper.js errors
        }
        originalError.apply(console, args);
    };
    
    // Also suppress warnings that might appear later
    window.addEventListener('load', function() {
        // Additional suppression for dynamically loaded content
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    // Check for any new script tags that might trigger warnings
                    mutation.addedNodes.forEach(function(node) {
                        if (node.tagName === 'SCRIPT') {
                            // Override any new console methods
                            if (window.console) {
                                window.console.warn = console.warn;
                                window.console.error = console.error;
                            }
                        }
                    });
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
})();
</script>
""", height=0)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .code-editor {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_connection():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def generate_problem(topic):
    """Generate a coding problem using the backend API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate-problem",
            json={"topic": topic},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error generating problem: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def execute_code(code, language, custom_input=""):
    """Execute code using the backend API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/execute-code",
            json={
                "code": code,
                "language": language,
                "custom_input": custom_input
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error executing code: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def get_code_review(code, language, problem=None):
    """Get AI code review using the backend API"""
    try:
        payload = {
            "code": code,
            "language": language
        }
        if problem:
            payload["problem"] = problem
        response = requests.post(
            f"{BACKEND_URL}/review-code",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting code review: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">💻 RapoZCode</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Coding Platform</p>', unsafe_allow_html=True)
    
    # Check backend connection
    if not check_backend_connection():
        st.error("⚠️ Backend server is not running. Please start the backend server first.")
        st.info("To start the backend, run: `cd rapozcode-backend && python app.py`")
        return
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "🎯 Problem Generator", "💻 Code Editor", "🔍 Code Review", "📚 About"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "🎯 Problem Generator":
        show_problem_generator()
    elif page == "💻 Code Editor":
        show_code_editor()
    elif page == "🔍 Code Review":
        show_code_review()
    elif page == "📚 About":
        show_about_page()

def show_home_page():
    """Display the home page"""
    st.markdown('<h2 class="sub-header">Welcome to RapoZCode!</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Generate Problems
        Get AI-powered coding problems tailored to your interests and skill level.
        """)
    
    with col2:
        st.markdown("""
        ### 💻 Write & Execute Code
        Write code in Python, Java, or C++ and execute it safely in our sandboxed environment.
        """)
    
    with col3:
        st.markdown("""
        ### 🤖 AI Feedback
        Receive intelligent feedback, debugging help, and code optimization suggestions.
        """)
    
    st.markdown("---")
    
    # Quick start section
    st.markdown('<h3 class="sub-header">🚀 Quick Start</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    1. **Generate a Problem**: Go to the Problem Generator page and enter a topic
    2. **Write Your Code**: Use the Code Editor to write your solution
    3. **Execute & Test**: Run your code and see the results
    4. **Get Feedback**: Use the Code Review feature for AI-powered suggestions
    """)
    
    # Supported languages
    st.markdown('<h3 class="sub-header">🔧 Supported Languages</h3>', unsafe_allow_html=True)
    
    lang_col1, lang_col2, lang_col3 = st.columns(3)
    
    with lang_col1:
        st.markdown("""
        ### Python 🐍
        - Full Python 3 support
        - Standard library available
        - Safe execution environment
        """)
    
    with lang_col2:
        st.markdown("""
        ### Java ☕
        - Java 11+ support
        - Standard library included
        - Compilation and execution
        """)
    
    with lang_col3:
        st.markdown("""
        ### C++ ⚡
        - C++17 support
        - Standard library available
        - Compiled execution
        """)

def show_problem_generator():
    """Display the problem generator page"""
    st.markdown('<h2 class="sub-header">🎯 AI Problem Generator</h2>', unsafe_allow_html=True)
    
    # Problem generation form
    with st.form("problem_generator"):
        st.markdown("### Enter a topic to generate a coding problem:")
        
        # Topic input with suggestions
        topic = st.text_input(
            "Topic (e.g., 'arrays', 'recursion', 'dynamic programming', 'graph algorithms')",
            placeholder="Enter a programming topic..."
        )
        
        # Difficulty selection
        difficulty = st.selectbox(
            "Difficulty Level:",
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        # Language preference
        language_pref = st.selectbox(
            "Preferred Language:",
            ["Any", "Python", "Java", "C++"]
        )
        
        submitted = st.form_submit_button("🎯 Generate Problem")
    
    if submitted and topic:
        with st.spinner("🤖 Generating your coding problem..."):
            # Add difficulty and language to the topic
            enhanced_topic = f"{topic} - {difficulty} level"
            if language_pref != "Any":
                enhanced_topic += f" in {language_pref}"
            
            problem_data = generate_problem(enhanced_topic)
            
            if problem_data:
                # Store problem in session state
                st.session_state.current_problem = problem_data
                st.session_state.problem_topic = topic
                
                st.success("✅ Problem generated successfully!")
                
                # Display the problem
                st.markdown("---")
                st.markdown('<h3 class="sub-header">📝 Your Coding Problem</h3>', unsafe_allow_html=True)
                
                st.markdown(f"**Topic:** {topic}")
                st.markdown(f"**Difficulty:** {difficulty}")
                st.markdown(f"**Language:** {language_pref}")
                
                # Display problem statement (use either 'problem' or 'problem_statement')
                problem_text = problem_data.get("problem") or problem_data.get("problem_statement", "No problem description available.")
                st.markdown("**Problem Description:**")
                st.markdown(f'<div class="info-box">{problem_text}</div>', unsafe_allow_html=True)
                
                # Display sample input and output
                if "sample_input" in problem_data and problem_data["sample_input"] != "Sample input":
                    st.markdown("**Sample Input:**")
                    st.code(problem_data["sample_input"], language="text")
                
                if "sample_output" in problem_data and problem_data["sample_output"] != "Sample output":
                    st.markdown("**Sample Output:**")
                    st.code(problem_data["sample_output"], language="text")
                
                # Display test case explanation
                if "testcase_explanation" in problem_data and problem_data["testcase_explanation"] != "Basic test case":
                    st.markdown("**Test Case Explanation:**")
                    st.markdown(problem_data["testcase_explanation"])
                
                # Display constraints
                if "constraints" in problem_data and problem_data["constraints"] != "No specific constraints":
                    st.markdown("**Constraints:**")
                    st.markdown(problem_data["constraints"])
                
                # Display difficulty if available
                if "difficulty" in problem_data:
                    st.markdown(f"**Difficulty Level:** {problem_data['difficulty'].title()}")
                
                # Show error message if there was an API issue
                if "error" in problem_data and "API key" in problem_data["error"]:
                    st.warning("⚠️ Note: Using fallback problem due to API key issues. For full AI-generated problems, please check your Gemini API key.")
                
                # Quick action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💻 Open in Code Editor"):
                        st.switch_page("💻 Code Editor")
                
                with col2:
                    if st.button("🔍 Get Solution Hints"):
                        show_solution_hints(problem_data)
    
    elif submitted and not topic:
        st.error("Please enter a topic to generate a problem.")

def show_solution_hints(problem_data):
    """Show solution hints for the current problem"""
    st.markdown("### 💡 Solution Hints")
    
    # This would typically call the backend for hints
    # For now, we'll show some general hints
    st.markdown("""
    **General Approach:**
    1. Read the problem carefully and identify the key requirements
    2. Think about the data structures you might need
    3. Consider edge cases and constraints
    4. Plan your algorithm before coding
    5. Test with the provided examples
    """)

def show_code_editor():
    """Display the code editor page"""
    st.markdown('<h2 class="sub-header">💻 Code Editor</h2>', unsafe_allow_html=True)
    
    # Language selection
    language = st.selectbox(
        "Select Programming Language:",
        ["python", "java", "cpp"],
        format_func=lambda x: {"python": "Python", "java": "Java", "cpp": "C++"}[x]
    )
    
    # Code editor
    st.markdown("### Write your code:")
    
    # Default code templates
    default_code = {
        "python": """# Write your Python code here
def main():
    # Your solution goes here
    print("Hello, World!")

if __name__ == "__main__":
    main()""",
        "java": """public class Main {
    public static void main(String[] args) {
        // Your solution goes here
        System.out.println("Hello, World!");
    }
}""",
        "cpp": """#include <iostream>
using namespace std;

int main() {
    // Your solution goes here
    cout << "Hello, World!" << endl;
    return 0;
}"""
    }
    
    # Get current problem if available
    current_problem = st.session_state.get('current_problem', {})
    if current_problem:
        # Show main problem statement
        problem_text = current_problem.get("problem") or current_problem.get("problem_statement")
        if problem_text:
            st.markdown("**Current Problem:**")
            st.markdown(f'<div class="info-box">{problem_text}</div>', unsafe_allow_html=True)
        # Show constraints
        if current_problem.get("constraints") and current_problem["constraints"] != "No specific constraints":
            st.markdown("**Constraints:**")
            st.markdown(current_problem["constraints"])
        # Show sample input
        if current_problem.get("sample_input") and current_problem["sample_input"] != "Sample input":
            st.markdown("**Sample Input:**")
            st.code(current_problem["sample_input"], language="text")
        # Show sample output
        if current_problem.get("sample_output") and current_problem["sample_output"] != "Sample output":
            st.markdown("**Sample Output:**")
            st.code(current_problem["sample_output"], language="text")
    
    # Code input
    code = st.text_area(
        "Code:",
        value=default_code[language],
        height=400,
        help="Write your code here. You can use standard input/output."
    )
    
    # Custom input
    st.markdown("### Custom Input (Optional):")
    custom_input = st.text_area(
        "Input:",
        height=100,
        help="Enter custom input for your program (optional)"
    )
    
    # Execute button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("▶️ Run Code", type="primary"):
            if code.strip():
                with st.spinner("🔄 Executing your code..."):
                    result = execute_code(code, language, custom_input)
                    
                    if result:
                        st.markdown("### 📊 Execution Results")
                        
                        if result.get("success"):
                            st.markdown('<div class="success-box">✅ Code executed successfully!</div>', unsafe_allow_html=True)
                            
                            # Output
                            if result.get("output"):
                                st.markdown("**Output:**")
                                st.code(result["output"], language="text")
                            
                            # Execution time
                            if result.get("execution_time"):
                                st.markdown(f"**Execution Time:** {result['execution_time']:.3f} seconds")
                            
                            # Memory usage (if available)
                            if result.get("memory_usage"):
                                st.markdown(f"**Memory Usage:** {result['memory_usage']} KB")
                        else:
                            st.markdown('<div class="error-box">❌ Code execution failed!</div>', unsafe_allow_html=True)
                            
                            # Error details
                            if result.get("error"):
                                st.markdown("**Error:**")
                                st.code(result["error"], language="text")
                            
                            # Error type
                            if result.get("error_type"):
                                st.markdown(f"**Error Type:** {result['error_type']}")
            else:
                st.error("Please enter some code to execute.")
    
    with col2:
        if st.button("🔍 Get Code Review"):
            if code.strip():
                with st.spinner("🤖 Analyzing your code..."):
                    review = get_code_review(code, language, current_problem if current_problem else None)
                    if review:
                        st.markdown("### 🤖 AI Code Review")
                        st.write("AI Review Response:", review)
                        shown = False
                        if review.get("correctness"):
                            st.markdown(f"**Correctness:** {review['correctness']}")
                            shown = True
                        if review.get("quality_assessment"):
                            st.markdown(f"**Quality Assessment:** {review['quality_assessment']}")
                            shown = True
                        if review.get("optimization_suggestions"):
                            st.markdown(f"**Optimization Suggestions:** {review['optimization_suggestions']}")
                            shown = True
                        if review.get("readability_improvements"):
                            st.markdown(f"**Readability Improvements:** {review['readability_improvements']}")
                            shown = True
                        if review.get("best_practices"):
                            st.markdown(f"**Best Practices:** {review['best_practices']}")
                            shown = True
                        if not shown:
                            st.markdown("No review available.")
                        if review.get("suggestions"):
                            st.markdown("**Suggestions:**")
                            for suggestion in review["suggestions"]:
                                st.markdown(f"- {suggestion}")
                        if review.get("score"):
                            st.markdown(f"**Code Quality Score:** {review['score']}/10")
            else:
                st.error("Please enter some code to review.")
    
    with col3:
        if st.button("💾 Save Code"):
            st.info("💾 Code saved to session (this is a demo - no permanent storage)")
    
    # Code templates
    st.markdown("### 📋 Code Templates")
    
    template_col1, template_col2, template_col3 = st.columns(3)
    
    with template_col1:
        if st.button("🐍 Python Template"):
            st.session_state.code_template = default_code["python"]
            st.rerun()
    
    with template_col2:
        if st.button("☕ Java Template"):
            st.session_state.code_template = default_code["java"]
            st.rerun()
    
    with template_col3:
        if st.button("⚡ C++ Template"):
            st.session_state.code_template = default_code["cpp"]
            st.rerun()

def show_code_review():
    """Display the code review page"""
    st.markdown('<h2 class="sub-header">🔍 AI Code Review</h2>', unsafe_allow_html=True)
    
    # Get current problem if available
    current_problem = st.session_state.get('current_problem', {})
    
    st.markdown("""
    Get AI-powered feedback on your code, including:
    - Code quality analysis
    - Performance optimization suggestions
    - Best practices recommendations
    - Bug detection and debugging help
    """)
    
    # Language selection
    language = st.selectbox(
        "Select Programming Language:",
        ["python", "java", "cpp"],
        format_func=lambda x: {"python": "Python", "java": "Java", "cpp": "C++"}[x]
    )
    
    # Code input
    code = st.text_area(
        "Paste your code here:",
        height=300,
        help="Enter the code you want to review"
    )
    
    # Problem context (optional)
    problem_context = st.text_area(
        "Problem Context (Optional):",
        height=100,
        help="Describe what the code is supposed to do (optional)"
    )
    
    # Review options
    review_type = st.multiselect(
        "Review Focus:",
        ["Code Quality", "Performance", "Security", "Best Practices", "Debugging"],
        default=["Code Quality", "Best Practices"]
    )
    
    if st.button("🔍 Get AI Review", type="primary"):
        if code.strip():
            with st.spinner("🤖 Analyzing your code..."):
                # Add review type to the context
                enhanced_context = problem_context
                if review_type:
                    enhanced_context += f"\n\nReview focus: {', '.join(review_type)}"
                review = get_code_review(code, language, current_problem if current_problem else None)
                if review:
                    st.markdown("### 🤖 AI Code Review Results")
                    
                    # Overall assessment
                    if review.get("overall_assessment"):
                        st.markdown("**Overall Assessment:**")
                        st.markdown(review["overall_assessment"])
                    
                    # Detailed review
                    if review.get("review"):
                        st.markdown("**Detailed Review:**")
                        st.markdown(review["review"])
                    
                    # Suggestions
                    if review.get("suggestions"):
                        st.markdown("**Suggestions for Improvement:**")
                        for i, suggestion in enumerate(review["suggestions"], 1):
                            st.markdown(f"{i}. {suggestion}")
                    
                    # Score
                    if review.get("score"):
                        st.markdown(f"**Code Quality Score:** {review['score']}/10")
                        
                        # Progress bar for score
                        score_percentage = (review['score'] / 10) * 100
                        st.progress(score_percentage / 100)
                    
                    # Performance analysis
                    if review.get("performance_analysis"):
                        st.markdown("**Performance Analysis:**")
                        st.markdown(review["performance_analysis"])
                    
                    # Security concerns
                    if review.get("security_concerns"):
                        st.markdown("**Security Concerns:**")
                        st.markdown(review["security_concerns"])
                    st.write("AI Review Response:", review)
        else:
            st.error("Please enter some code to review.")

def show_about_page():
    """Display the about page"""
    st.markdown('<h2 class="sub-header">📚 About RapoZCode</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    **RapoZCode** is an AI-powered coding platform designed to help programmers learn, practice, and improve their coding skills.
    
    ### 🚀 Features
    
    - **AI Problem Generation**: Get personalized coding problems based on your interests and skill level
    - **Multi-Language Support**: Write and execute code in Python, Java, and C++
    - **Safe Code Execution**: Run code in a secure, sandboxed environment
    - **AI Code Review**: Receive intelligent feedback and suggestions for improvement
    - **Real-time Feedback**: Get instant results and debugging help
    
    ### 🛠️ Technology Stack
    
    - **Backend**: Flask (Python)
    - **Frontend**: Streamlit (Python)
    - **AI Integration**: Google Gemini API
    - **Code Execution**: Secure sandboxed environment
    
    ### 🔧 Supported Languages
    
    - **Python**: Full Python 3 support with standard library
    - **Java**: Java 11+ with compilation and execution
    - **C++**: C++17 with standard library support
    
    ### 🛡️ Security
    
    - All code execution is performed in isolated containers
    - Time and memory limits prevent resource abuse
    - Input validation and sanitization
    - No persistent storage of user code
    
    ### 📞 Support
    
    For questions or issues, please check the documentation or contact the development team.
    """)
    
    # System status
    st.markdown("### 🔧 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if check_backend_connection():
            st.success("✅ Backend Server: Online")
        else:
            st.error("❌ Backend Server: Offline")
    
    with col2:
        st.info("✅ Frontend: Running")

if __name__ == "__main__":
    main() 