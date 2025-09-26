# ⚡ VulnReaper by ahm0x v1.0

<div align="center">
    
*disclaimer!!!! this tool is not fully finished, there might be bugs/errors. Feel free to leave me a comment if you find one!*
    
![VulnReaper](https://img.shields.io/badge/VulnReaper%20by%20ahm0x-v1.0-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11.9-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-GPL--3.0-orange?style=for-the-badge)

**Professional Bug Bounty & Penetration Testing Framework**

*Developed by [ahm0x](https://github.com/ahm0x)*

</div>

---

## 🌐 Web Interface

This repository includes both the original Python framework and a modern web interface for easier access to VulnReaper's capabilities.

### Quick Start - Web Interface
```bash
# Clone the repository
git clone https://github.com/ahm0x/VulnReaper-ahm0x.git
cd VulnReaper

# Setup and start web interface
npm run setup
npm run dev

# Or manually:
npm install
npm run dev
```

The web interface will be available at `http://localhost:3000`

### Quick Start - Python Framework
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run system health check (recommended)
python -c "from Settings.Program.Config.ErrorHandler import error_handler; error_handler.validate_dependencies()"

# Launch the framework
python Main.py
```

---

## 🔧 Fixed Issues in v1.0.1

### Critical Fixes
- ✅ **Fixed missing Util.py imports** - Resolved all import errors
- ✅ **Added comprehensive error handling** - Centralized error management
- ✅ **Enhanced security validation** - Input sanitization and validation
- ✅ **Fixed API integration issues** - Proper rate limiting and caching
- ✅ **Improved report generation** - Professional templates and formats

### New Features
- 🆕 **System Health Check** - Comprehensive system monitoring
- 🆕 **API Security Scanner** - Advanced API endpoint testing
- 🆕 **Enhanced Database Management** - SQLite-based result storage
- 🆕 **Professional Report Templates** - Executive and technical reports
- 🆕 **Centralized Security Module** - Input validation and sanitization

### Security Improvements
- 🛡️ **Input Sanitization** - All user inputs are properly sanitized
- 🛡️ **Rate Limiting** - API calls are properly rate limited
- 🛡️ **Target Validation** - Prevents scanning of restricted targets
- 🛡️ **Error Logging** - Comprehensive error tracking and logging
- 🛡️ **Dependency Validation** - Automatic dependency checking

---

## 🚀 New Quick Start Guide

### Web Interface (Recommended)
```bash
# Start the web interface
npm install
npm run dev
```

### Quick Start - Python Framework
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run setup (optional)
python Setup.py

# Launch the framework
python Main.py
```

---

## 🚀 Overview

**VulnReaper by ahm0x** is a comprehensive cybersecurity framework designed for penetration testers, bug bounty hunters, and security researchers. With **79 professional modules** organized across multiple categories, it provides everything needed for modern security assessments and vulnerability discovery.

### ⭐ Core Philosophy: **Professional Vulnerability Discovery**
Built by a professional pentester and bug bounty hunter, this framework revolutionizes vulnerability discovery with real-time API integration, automated reconnaissance, and enterprise-grade reporting.

---

## 🛠️ Installation

### Prerequisites
- **Python 3.11.9** or higher
- **Windows** or **Linux** operating system
- **Internet connection** for API integrations

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/ahm0x/VulnReaper.git
cd VulnReaper

# Install dependencies
npm install

# Start web interface
npm run dev
```

### Python Framework
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run health check
python Settings/Program/System-Health-Check.py

# Start framework
python Main.py
```

---

## 📁 Project Structure

```
VulnReaper/
├── Main.py                 # Main application entry point
├── Setup.py               # Dependency installer
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # GPL-3.0 License
├── Results/               # Output directory
│   ├── BugBounty/        # Bug bounty results
│   ├── Discord/          # Discord tool outputs
│   └── Website/          # Website analysis results
└── Settings/
    └── Program/          # All tool modules
        ├── Config/       # Configuration files
        ├── VulnReaper-by-ahm0x.py  # Core automation engine
        ├── Discord-*.py  # Discord tools
        ├── Website-*.py  # Web tools
        └── ...           # Other modules
```

---

## 🎯 Quick Start - Bug Bounty Automation

```bash
# Launch the framework
python Main.py
# Navigate to Menu 2 (press N)
# Select option 37 - Bug Bounty Automation
# Choose option 01 - Full Bug Bounty Automation
# Enter target: example.com
```

The automation will:
1. 🔍 **Subdomain Discovery** - Find all subdomains
2. 🌐 **Port Scanning** - Identify open services
3. 🔎 **Technology Detection** - Analyze tech stack
4. 🛡️ **Vulnerability Scanning** - Automated security checks
5. 📊 **Professional Reporting** - Generate detailed reports

---

## 📞 Support & Contact

- 🌐 **Website**: [ahm0x.github.io](https://ahm0x.github.io/)
- 💬 **Discord**: [Join our server](https://discord.gg/ZqpqmRXR)
- 📱 **Telegram**: [@ahm0x](https://t.me/ahm0x)
- 🐛 **Issues**: [GitHub Issues](https://github.com/ahm0x/VulnReaper/issues)

---

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🏆 Recognition

**VulnReaper by ahm0x** has been recognized by the cybersecurity community for:
- 🎯 **Comprehensive toolset** for security professionals
- 🔥 **Advanced automation** - Industry-leading bug bounty workflows
- 🛡️ **Responsible disclosure** approach
- 📚 **Educational value** for learning cybersecurity

---

## 📄 License

This project is licensed under the **GPL-3.0 License** - see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2025 ahm0x - VulnReaper
```

---

<div align="center">

**⚡ VulnReaper by ahm0x - Professional Vulnerability Discovery Framework ⚡**

*Built with ❤️ by [ahm0x](https://github.com/ahm0x)*

</div>
