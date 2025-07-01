# Port Scanner 🔍  
**3rd ACS Project - Group 10**  
*Advanced Computer Systems Course, [University], [2025]*

A high-performance Python port scanner with multi-threading support for efficient TCP/UDP port scanning.

---

## 📋 Project Information
| Category       | Details                          |
|----------------|----------------------------------|
| **Course**     | ASEAN CYBER SHIELD (ACS)         |
| **Mentor**     | Pakaysit Latsavong               |
| **Semester**   | Fall/Spring 2025                 |

---

## ✨ Key Features
- **Protocol Support**
  - TCP port scanning
  - UDP port scanning
- **Performance**
  - Multi-threaded architecture (200+ threads)
  - Configurable timeout settings
- **Flexibility**
  - Multiple port specification modes:
    - Single port (`-p 80`)
    - Port range (`-p 1-1000`)
    - All ports (`-p all`)
  - Adjustable verbosity levels
- **Output Options**
  - Results logging to file
  - Closed port visibility toggle

---

## ⚙️ Installation & Setup
```bash
# Clone repository
git clone https://github.com/Jacob-Valor/ACS-Projects.git
cd ACS-Projects

# Setup virtual environment
python3 -m venv .venv      # Linux/MacOS
python -m venv .venv       # Windows 


source .venv/bin/activate         # Linux/MacOS
source .venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt