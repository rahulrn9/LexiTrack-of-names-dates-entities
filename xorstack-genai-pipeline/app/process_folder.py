from pathlib import Path
from app.ner import extract_entities
from app.db import insert_rows
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
SAMPLES = BASE / "data" / "samples"
CSV = BASE / "outputs" / "results.csv"

def main():
    rows_all = []
    for p in SAMPLES.glob("*.txt"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        r = extract_entities(text, p.name)
        rows_all.extend(r["rows"])

    if rows_all:
        insert_rows(rows_all)
        df = pd.DataFrame(rows_all)
        if CSV.exists():
            df.to_csv(CSV, mode="a", header=False, index=False)
        else:
            df.to_csv(CSV, index=False)
        print(f"Processed {len(rows_all)} rows across {len(list(SAMPLES.glob('*.txt')))} file(s). Written to {CSV}.")
    else:
        print("No entities found.")

if __name__ == "__main__":
    main()
