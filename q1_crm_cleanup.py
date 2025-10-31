# Setting up file
with open("contacts_raw.txt", "w", encoding="utf-8") as f:
    f.write('Alice Johnson <alice@example.com> , +1 (469) 555-1234\nBob Roberts <bob[at]example.com> , 972-555-777\nSara M. , sara@mail.co , 214 555 8888\n"Mehdi A." <mehdi.ay@example.org> , (469)555-9999\nDelaram <delaram@example.io>, +1-972-777-2121\nNima <NIMA@example.io> , 972.777.2121\nduplicate <Alice@Example.com> , 469 555 1234')
print("Wrote contacts_raw.txt with sample DalaShop data.")


import re
import csv
from pathlib import Path

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# ------------------------------
# 1️⃣ Phone normalization
# ------------------------------
def normalize_phone(raw: str) -> str:
    """Keep only digits; return last 10 digits if >=10, else empty."""
    digits = ''.join(re.findall(r"\d", raw))
    return digits[-10:] if len(digits) >= 10 else ""

# ------------------------------
# 2️⃣ Email cleaning/validation
# ------------------------------
def clean_email(email: str) -> str:
    """Strip whitespace, remove angle brackets, replace [at] with @."""
    email = email.strip("<> ").replace("[at]", "@")
    return email if EMAIL_REGEX.fullmatch(email) else ""

# ------------------------------
# 3️⃣ Parse a single line into structured data
# ------------------------------
def parse_line(line: str) -> dict | None:
    """
    Parse a line like 'Name <email>, phone' into a dict.
    Returns None if email is invalid.
    """
    parts = [p.strip() for p in line.split(",") if p.strip()]
    if len(parts) < 2:
        return None

    # Extract name and email
    if "<" in parts[0] and ">" in parts[0]:
        name = parts[0][:parts[0].find("<")].strip().strip('"')
        email = parts[0][parts[0].find("<")+1 : parts[0].find(">")]
    else:
        name = parts[0].strip().strip('"')
        email = parts[1]

    email = clean_email(email)
    if not email:
        return None

    # Extract phone (last part)
    phone = normalize_phone(parts[-1])

    return {"name": name, "email": email, "phone": phone}

# ------------------------------
# 4️⃣ Deduplicate rows by email (case-insensitive)
# ------------------------------
def deduplicate_rows(rows: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for row in rows:
        key = row["email"].casefold()
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result

# ------------------------------
# 5️⃣ Parse multiple lines of text
# ------------------------------
def parse_text(text: str) -> list[dict]:
    rows = [parse_line(line) for line in text.splitlines()]
    rows = [row for row in rows if row is not None]
    return deduplicate_rows(rows)

# ------------------------------
# 6️⃣ Write cleaned rows to CSV
# ------------------------------
def write_csv(rows: list[dict], output_file: Path):
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email", "phone"])
        writer.writeheader()
        writer.writerows(rows)

# ------------------------------
# Optional: convenience function to read file + process
# ------------------------------
def process_file(input_file: Path, output_file: Path):
    try:
        text = input_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"⚠️ File not found: {input_file}")
        return

    rows = parse_text(text)
    write_csv(rows, output_file)
    print(f"✅ Cleaned data written to {output_file}")

input_file = Path("contacts_raw.txt")
output_file = Path("contact_clean.csv")
process_file(input_file, output_file)