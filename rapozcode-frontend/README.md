# RapoZCode Frontend

A modern, AI-powered coding platform frontend built with Streamlit.

## 🚀 Features

- **AI Problem Generation**: Generate personalized coding problems using AI
- **Multi-Language Code Editor**: Write and execute code in Python, Java, and C++
- **Real-time Code Execution**: Safe, sandboxed code execution with instant feedback
- **AI Code Review**: Get intelligent feedback and suggestions for code improvement
- **Modern UI**: Beautiful, responsive interface with intuitive navigation

## 🛠️ Technology Stack

- **Frontend Framework**: Streamlit (Python)
- **HTTP Client**: Requests
- **Environment Management**: python-dotenv
- **Styling**: Custom CSS with Streamlit components

## 📋 Prerequisites

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`
- Backend server running (see backend README)

## 🔧 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd rapozcode-frontend
   ```

2. **Create a virtual environment:**
   ```bash
   uv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Copy the environment example file:**
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file:**
   ```env
   BACKEND_URL=http://localhost:5000
   ```

## 🚀 Running the Application

### Method 1: Using the startup script
```bash
python run_frontend.py
```

### Method 2: Direct Streamlit command
```bash
streamlit run app.py
```

### Method 3: With custom port
```bash
streamlit run app.py --server.port 8501
```

## 📱 Accessing the Application

Once started, the frontend will be available at:
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501

## 🎯 Usage Guide

### 1. Home Page
- Overview of the platform features
- Quick start guide
- Supported programming languages

### 2. Problem Generator
- Enter a programming topic (e.g., "arrays", "recursion")
- Select difficulty level
- Choose preferred programming language
- Generate AI-powered coding problems

### 3. Code Editor
- Write code in Python, Java, or C++
- Execute code with custom input
- Get real-time execution results
- Access code templates

### 4. Code Review
- Paste your code for AI analysis
- Get feedback on code quality, performance, and best practices
- Receive suggestions for improvement
- View code quality scores

### 5. About Page
- Platform information
- System status
- Technology stack details

## 🔧 Supported Languages

### Python 🐍
- Full Python 3 support
- Standard library available
- Safe execution environment

### Java ☕
- Java 11+ support
- Standard library included
- Compilation and execution

### C++ ⚡
- C++17 support
- Standard library available
- Compiled execution

## 🛡️ Security Features

- Safe code execution in sandboxed environment
- Input validation and sanitization
- No persistent storage of user code
- Time and memory limits

## 🔍 Troubleshooting

### Backend Connection Issues
- Ensure the backend server is running on the correct port
- Check the `BACKEND_URL` in your `.env` file
- Verify network connectivity

### Streamlit Issues
- Make sure all dependencies are installed
- Check Python version compatibility
- Clear Streamlit cache if needed: `streamlit cache clear`

### Code Execution Issues
- Verify the backend code execution service is working
- Check language-specific requirements (Java JDK, C++ compiler)
- Review execution logs for detailed error messages

## 📁 Project Structure

```
rapozcode-frontend/
├── app.py              # Main Streamlit application
├── run_frontend.py     # Startup script
├── requirements.txt    # Python dependencies
├── env.example         # Environment variables template
├── .env               # Environment variables (create from example)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the backend documentation
3. Check system requirements
4. Contact the development team

## 📄 License

This project is part of the RapoZCode platform. 