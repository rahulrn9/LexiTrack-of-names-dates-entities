import re
from typing import Optional
import dateparser

# Common date patterns (dd/mm/yyyy, dd-mm-yyyy, Month dd, yyyy, etc.)
DATE_REGEXPS = [
    r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b",
    r"\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s*\d{4}\b",
    r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*,?\s*\d{4}\b",
]

def normalize_date(text: str) -> Optional[str]:
    dt = dateparser.parse(text, settings={"DATE_ORDER": "DMY"})
    if not dt:
        return None
    return dt.date().isoformat()
