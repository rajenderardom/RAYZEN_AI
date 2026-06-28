# RAYZEN AI

> Personal AI Productivity Assistant for Windows

---

## 1. Project Overview
RAYZEN AI is a modular AI productivity assistant focused on automating daily Windows tasks. It streamlines desktop control, web browser automation, Excel operations, and PDF processing, providing a solid foundation for future advanced AI planning.

---

## 2. Current Features
*   **Interactive Console**: Real-time CLI command loop interface with graceful handling of exits, interrupts, and contextual messages.
*   **Natural Language Interpreter**: Normalizes and translates multi-lingual user phrasing (e.g., Hinglish `kholo` commands) to standardized execution scripts.
*   **Command Engine**: High-extensibility registry dispatcher mapping structured queries to matching automation functions.
*   **Desktop Launcher**: Controls and opens standard Windows desktop applications (Notepad, Calculator, File Explorer, Paint) with exception shielding.
*   **Browser Controller**: Standard library-based system default browser dispatcher with standard lookup shortcut configurations.
*   **Excel Manager**: Open, save, close, and metadata inspection of workbook files utilizing `openpyxl`.
*   **Workbook Analyzer**: Extracts worksheets information, workbook summaries, active sheets, and cell dimensions (rows/columns).
*   **Duplicate Detector**: Reads and detects identical values, row numbers, and duplicates inside columns without data loss.
*   **Logging System**: Core logging architecture utilizing standardized console status reporting.
*   **Configuration Manager**: Central configurations holder for system variables.

---

## 3. Architecture
```
User Input
    ↓
Interactive Console
    ↓
Natural Language Interpreter
    ↓
Command Engine
    ↓
Skills Registry
 ├── Desktop Subsystem
 ├── Browser Subsystem
 └── Excel Subsystem
```

---

## 4. Folder Structure
```text
RAYZEN_AI/
├── src/
│   ├── browser/
│   │   └── controller.py
│   ├── core/
│   │   ├── app.py
│   │   ├── command_engine.py
│   │   ├── config.py
│   │   ├── interpreter.py
│   │   └── logger.py
│   ├── desktop/
│   │   └── launcher.py
│   └── excel/
│       ├── analyzer.py
│       ├── duplicate_detector.py
│       └── manager.py
├── tests/
│   ├── test_app.py
│   ├── test_analyzer.py
│   ├── test_browser.py
│   ├── test_command_engine.py
│   ├── test_duplicate_detector.py
│   ├── test_excel.py
│   ├── test_integration.py
│   ├── test_interpreter.py
│   └── test_launcher.py
├── launcher.py
├── pyproject.toml
└── README.md
```

---

## 5. Installation
### Prerequisites
- Python 3.12+

### Step-by-Step Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Rajender-Kumar/RAYZEN_AI.git
   cd RAYZEN_AI
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the interactive console:
   ```bash
   python launcher.py
   ```

---

## 6. Example Commands
Inside the interactive console prompt (`> `), you can input:
*   `help`
*   `google kholo`
*   `notepad kholo`
*   `open github`
*   `calculator kholo`
*   `exit`

---

## 7. Roadmap
### Current Version
- **v0.3 Alpha**

### Upcoming Milestones
- **Excel Intelligence**: Advanced formulas auditing, cell writing, and automated report building.
- **Browser Automation**: Element selection, form filling, scraping, and dynamic session flows.
- **PDF Automation**: Document merging, splitting, extraction, and formatting.
- **OCR (Optical Character Recognition)**: Image to text parsing.
- **Voice Interface**: Audio control commands parsing and speech recognition.
- **Memory Subsystem**: Context preservation across multiple conversation loops.
- **AI Task Engine**: Automated scheduling and execution of complex workflows.

---

## 8. Tech Stack
### Active
*   **Python 3.12+**
*   **OpenPyXL**
*   **Git**
*   **unittest**

### Planned additions
*   **Playwright** (for browser automation)
*   **OpenAI API** / **Local LLM** (for advanced query interpretation and reasoning)

---

## 9. Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Commit your changes: `git commit -m 'Add amazing feature'`.
4. Push to the branch: `git push origin feature/amazing-feature`.
5. Open a Pull Request.

---

## 10. License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 11. Author
*   **Rajender Kumar**