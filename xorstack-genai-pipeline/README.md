# Xorstack Gen-AI Developer – Interview Assignment (Python + FastAPI)

A small AI-powered pipeline that ingests plain-text documents, extracts structured information (**person names** and **dates**), and exposes it via a **FastAPI** service. Results are stored in **SQLite** and **CSV**.

---

## 🧰 Tech Stack
- **Python 3.10+**
- **FastAPI** (lightweight API)
- **spaCy** (NER for `PERSON` + `DATE`)
- **dateparser** (normalize date strings to ISO-8601)
- **SQLite** + **CSV (pandas)** for storage

> The pipeline works **offline** after installation. On first run, it will attempt to auto-download the spaCy English model if it's missing.

---

## 📦 Setup

```bash
# 1) Create a virtualenv (recommended)
python -m venv .venv && source .venv/bin/activate   # (Linux/Mac)
# or: .venv\Scripts\activate                      # (Windows PowerShell)

# 2) Install dependencies
pip install -r requirements.txt

# 3) Download spaCy English model if not auto-installed on first run
python -m spacy download en_core_web_sm
```

---

## ▶️ Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Open docs at: **http://localhost:8000/docs**

### Endpoints
- `GET /health` – health check
- `POST /extract` – accepts either:
  - **multipart/form-data** with `file` (a `.txt` file), or
  - **application/json** with `{"text": "your text here", "filename": "optional_name.txt"}`

**Response Example**
```json
{
  "filename": "sample1.txt",
  "people": ["John Doe", "Alice"],
  "dates": ["2025-09-15", "2023-01-01"]
}
```

---

## 🗄️ Storage

- **SQLite** at `outputs/results.db`
  - Table: `extractions`
  - Columns: `id, filename, entity_type, entity_text, normalized, start_char, end_char, processed_at`
- **CSV** at `outputs/results.csv` (append-only)

---

## 📂 Batch Processing (folder)

Process all `.txt` files in `data/samples`:

```bash
python app/process_folder.py
```

---

## 🧪 Quick Test

We include a sample text in `data/samples/sample1.txt`. Try:

```bash
curl -X POST "http://localhost:8000/extract"   -H "Content-Type: multipart/form-data"   -F "file=@data/samples/sample1.txt"
```

Or JSON:
```bash
curl -X POST "http://localhost:8000/extract"   -H "Content-Type: application/json"   -d '{"text":"John met Alice on 15/09/2025 in Bengaluru. Meeting on Jan 1, 2023 too."}'
```

---

## 🧩 n8n (Optional Automation Idea)

If you want to show automation with **n8n**, create a simple flow:
1. **Manual Trigger**
2. **Read Binary File** (a `.txt` path)
3. **HTTP Request** (POST to `http://host.docker.internal:8000/extract` or `http://fastapi:8000/extract` in Docker)
4. **SQLite** (write results into `outputs/results.db`) or **Google Sheets**

We also include a minimal example export you can tweak at `n8n/workflow.example.json`.

---

## 📤 Deliverables (ready to email)
- Full **code** under this repo.
- **README** (this file).
- **Example input**: `data/samples/sample1.txt`
- **Outputs**: populated once you run the API or the batch script.

---

## 📧 Emails
Send the repo or a zip to:
- revanna@xorstack.com
- basanagouda@xorstack.com

Good luck!
```

