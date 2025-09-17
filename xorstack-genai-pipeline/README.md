

# LexiTrack – AI-Powered Text → JSON Pipeline

[![Made with FastAPI](https://img.shields.io/badge/Made%20with-FastAPI-109989.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5.svg?logo=python)](https://spacy.io/)
[![n8n Workflow](https://img.shields.io/badge/Workflow-n8n-1abc9c.svg?logo=n8n)](https://n8n.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python)](https://www.python.org/)

---

## 📖 Overview

**LexiTrack** is an AI-powered pipeline that ingests plain-text documents, extracts **entities** (currently `PERSON` and `DATE`), normalizes dates to ISO-8601, and outputs structured JSON.  

The pipeline is built with **FastAPI + spaCy**, persists results to **SQLite/CSV**, and includes an **n8n workflow** for automation (file → API → DB/CSV).

---

## ✨ Features

- 📂 **Document ingestion** (plain-text `.txt` files)  
- 👤 **Named Entity Recognition (NER)** using **spaCy** for `PERSON`  
- 📅 **Date extraction** using spaCy + regex, normalized with `dateparser`  
- 🗂️ **Structured output** as JSON + persistence into SQLite (`outputs/results.db`) and CSV (`outputs/results.csv`)  
- 🔄 **Automation workflow** with n8n (Manual/File Trigger → Read File → HTTP POST → DB/Sheets)  
- ⚡ **REST API** via FastAPI with interactive Swagger docs  

---

## 🧰 Tech Stack

- **Language:** Python 3.10+  
- **Framework:** FastAPI  
- **NLP:** spaCy + dateparser  
- **Storage:** SQLite + CSV  
- **Automation:** n8n workflow  

---

## 📂 Project Structure

LexiTrack-of-names-dates-entities/
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── ner.py # Entity extraction logic
│ ├── utils.py # Date regex + normalization
│ ├── db.py # SQLite helper
│ ├── models.py # Pydantic models
│ └── process_folder.py # Batch processor
├── data/
│ └── samples/sample1.txt # Example input file
├── outputs/
│ ├── results.csv # Appended CSV output
│ └── results.db # SQLite database
├── n8n/
│ └── workflow.example.json # Example workflow export
├── requirements.txt
├── README.md
└── LICENSE

yaml
Copy code

---

## ⚙️ Setup & Installation

```bash
# 1) Clone repo
git clone https://github.com/rahulrn9/LexiTrack-of-names-dates-entities.git
cd LexiTrack-of-names-dates-entities

# 2) Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.\.venv\Scripts\activate         # Windows

# 3) Install dependencies
pip install -r requirements.txt

# 4) Download spaCy model
python -m spacy download en_core_web_sm
▶️ Run the API
Start the FastAPI server:

bash
Copy code
uvicorn app.main:app --reload --port 8000
Check endpoints:

Health check → http://127.0.0.1:8000/health

Swagger UI → http://127.0.0.1:8000/docs

📤 Example Usage
1. JSON Request
bash
Copy code
curl -X POST "http://127.0.0.1:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "John met Alice on 15/09/2025 in Bengaluru.", "filename":"demo.txt"}'
Response:

json
Copy code
{
  "filename": "demo.txt",
  "people": ["Alice", "John"],
  "dates": ["2025-09-15"]
}
2. File Upload
bash
Copy code
curl -X POST "http://127.0.0.1:8000/extract" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/samples/sample1.txt"
Response:

json
Copy code
{
  "filename": "sample1.txt",
  "people": ["John Doe", "Alice Johnson", "Priya Singh"],
  "dates": ["2023-01-01", "2024-12-31", "2025-09-15"]
}
🔄 Batch Processing (all files in folder)
bash
Copy code
python app/process_folder.py
🧩 n8n Workflow (Automation)
Import n8n/workflow.example.json into n8n.
Example flow:

Manual Trigger

Read Binary File (sample1.txt)

HTTP Request → POST to FastAPI /extract

(Optional) Insert results into SQLite or Google Sheets

🗄️ Storage
SQLite DB: outputs/results.db

Table: extractions

Columns: filename, entity_type, entity_text, normalized, start_char, end_char, processed_at

CSV: outputs/results.csv

Append-only, same structure

🚀 Roadmap / Future Work
Add LOCATION and ORG entity extraction

Expose Dockerfile + docker-compose for one-command run

Build Google Sheets automation flow in n8n

Add CLI script for quick text-to-JSON conversion

📜 License
This project is licensed under the MIT License – see LICENSE file for details.

🤝 Contact
Rahul Naduvinamani
