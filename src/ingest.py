from collections import Counter

from pathlib import Path

from pypdf import PdfReader

DATA_DIR = Path("data")
CHUNK_SIZE = 200   # words per chunk
OVERLAP = 40       # words shared between neighbouring chunks


def load_pdfs(folder):
    """Read every PDF in the folder and return its text page by page."""
    pages = []
    for pdf_path in folder.glob("*.pdf"):
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_num,
                })
    return pages


def load_txts(folder):
    """Read every .txt file in the folder."""
    pages = []
    for txt_path in folder.glob("*.txt"):
        text = txt_path.read_text(encoding="utf-8")
        if text.strip():
            pages.append({
                "text": text,
                "source": txt_path.name,
                "page": 1,
            })
    return pages


def get_checked_date(filename):
    """'ssa_ssn_2026-11-26.pdf' -> '2026-11-26'"""
    return Path(filename).stem.split("_")[-1]


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split text into overlapping chunks of words."""
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_size]))
        if start + chunk_size >= len(words):
            break
    return chunks


def main():
    pages = load_pdfs(DATA_DIR) + load_txts(DATA_DIR)
    print(f"Loaded {len(pages)} pages")

    all_chunks = []
    for page in pages:
        for i, chunk in enumerate(chunk_text(page["text"])):
            all_chunks.append({
                "id": f"{page['source']}-p{page['page']}-c{i}",
                "text": chunk,
                "source": page["source"],
                "page": page["page"],
                "checked": get_checked_date(page["source"]),
            })

    print(f"Created {len(all_chunks)} chunks\n")

    counts = Counter(chunk["source"] for chunk in all_chunks)
    print("Chunks per source:")
    for source, count in counts.items():
        date = get_checked_date(source)
        print(f"  {source}: {count} chunks (checked {date})")


if __name__ == "__main__":
    main() 