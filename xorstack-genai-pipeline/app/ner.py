from typing import List, Dict
from datetime import datetime
import re
import spacy
from spacy.cli import download as spacy_download
from .utils import DATE_REGEXPS, normalize_date

_NLP = None

def get_nlp():
    global _NLP
    if _NLP is None:
        try:
            _NLP = spacy.load("en_core_web_sm")
        except Exception:
            spacy_download("en_core_web_sm")
            _NLP = spacy.load("en_core_web_sm")
    return _NLP

def extract_entities(text: str, filename: str):
    nlp = get_nlp()
    doc = nlp(text)

    people = set()
    date_chunks = []

    # 1) Use spaCy NER
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.add(ent.text.strip())
        if ent.label_ == "DATE":
            date_chunks.append((ent.text, ent.start_char, ent.end_char))

    # 2) Augment with regex
    for pattern in DATE_REGEXPS:
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            date_chunks.append((m.group(0), m.start(), m.end()))

    # Normalize & deduplicate dates
    normalized_dates = []
    seen_norm = set()
    for s, start, end in date_chunks:
        norm = normalize_date(s)
        if norm and norm not in seen_norm:
            seen_norm.add(norm)
            normalized_dates.append((s, norm, start, end))

    # Prepare rows for DB insert
    now = datetime.utcnow().isoformat()
    rows = []
    for p in sorted(people):
        rows.append({
            "filename": filename,
            "entity_type": "PERSON",
            "entity_text": p,
            "normalized": None,
            "start_char": None,
            "end_char": None,
            "processed_at": now,
        })
    for original, norm, start, end in normalized_dates:
        rows.append({
            "filename": filename,
            "entity_type": "DATE",
            "entity_text": original,
            "normalized": norm,
            "start_char": start,
            "end_char": end,
            "processed_at": now,
        })

    return {
        "people": sorted(people),
        "dates": sorted({norm for _, norm, _, _ in normalized_dates}),
        "rows": rows,
    }
