AI Legal Contract Analyzer

An AI-powered web application built with Flask that analyses legal contracts using OCR and artificial intelligence. Users can upload PDF or image-based contracts, extract text automatically, identify important clauses, assess legal risks, generate concise summaries, chat with the document using AI, and export professional reports.

🚀 Features
📄 Upload legal contracts (PDF, PNG, JPG)
🔍 OCR-based text extraction using EasyOCR
🤖 AI-powered contract analysis
📑 Automatic clause identification
⚠️ Risk assessment and highlighting
📝 AI-generated contract summaries
💬 Interactive AI legal chat for document queries
📥 Export analysis as a professional PDF report
🌐 Simple and responsive Flask web interface
🛠️ Tech Stack
Backend: Python, Flask
Frontend: HTML, CSS, JavaScript
OCR: EasyOCR, OpenCV, pdf2image
AI: Google Gemini API
PDF Processing: ReportLab, Pillow, Poppler
Environment Management: python-dotenv

📂 Project Structure
legal-contract-analyzer/
│── app.py
│── config.py
│── requirements.txt
│── modules/
│── templates/
│── static/
│── uploads/
│── reports/
└── README.md

python app.py
📖 How It Works
Upload a legal contract.
OCR extracts text from scanned or image-based documents.
AI analyses the contract and identifies important clauses.
Risks and key observations are highlighted.
A concise summary is generated.
Users can ask questions about the contract through the AI chat.
The complete analysis can be exported as a PDF report.
📌 Future Improvements
Support for DOCX contracts
Multi-language OCR
Clause comparison between contracts
AI-powered contract recommendations
User authentication and history

Author
Cyril Atony
