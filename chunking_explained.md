# How Text Chunking & Overlap Works in RAG

## What is Chunking?

Chunking is the process of **splitting a large text into smaller pieces** (called chunks) so that an AI model can process them. Large Language Models (LLMs) have a limited context window, so we can't feed them an entire document at once. Instead, we break it into manageable chunks.

## Key Parameters

| Parameter       | Default Value | Description                                              |
|-----------------|---------------|----------------------------------------------------------|
| `chunk_size`    | 900           | Maximum number of characters per chunk                   |
| `chunk_overlap` | 150           | Number of characters shared between consecutive chunks   |

---

## Step-by-Step: Simple Example

Imagine this is your full text (**30 characters**):

```
ABCDEFGHIJ KLMNOPQRST UVWXYZ!!
```

Settings: `chunk_size = 15`, `chunk_overlap = 5`

### Round 1 — Chunk 1

```
ABCDEFGHIJ KLMNOPQRST UVWXYZ!!
|______________|
start=0        end=15
```

- Takes position **0 to 15** → `"ABCDEFGHIJ KLMN"`
- This is **Chunk 1**
- Next start = `end - overlap` = `15 - 5` = **10**     

### Round 2 — Chunk 2

```
ABCDEFGHIJ KLMNOPQRST UVWXYZ!!
          |______________|
          start=10       end=25
```

- Takes position **10 to 25** → `" KLMNOPQRST UVWX"`
- This is **Chunk 2**

**The overlap:**

```
Chunk 1:  A B C D E F G H I J [ K L M N]
Chunk 2:                      [ K L M N] O P Q R S T   U V W X
                               ^^^^^^^^
                         These 5 chars appear in BOTH chunks!
```

- Next start = `25 - 5` = **20**

### Round 3 — Chunk 3

```
ABCDEFGHIJ KLMNOPQRST UVWXYZ!!
                    |__________|
                    start=20   end=30 (end of text, loop ends)
```

- Takes position **20 to 30** → `"T UVWXYZ!!"`
- This is **Chunk 3** (last chunk)

### Summary of Simple Example

| Chunk # | Start | End | Text             | Length |
|---------|-------|-----|------------------|--------|
| 1       | 0     | 15  | ABCDEFGHIJ KLMN  | 15     |
| 2       | 10    | 25  | KLMNOPQRST UVWX  | 15     |
| 3       | 20    | 30  | T UVWXYZ!!        | 10     |

- Overlap between Chunk 1 & 2: positions **10–15** → `" KLMN"`
- Overlap between Chunk 2 & 3: positions **20–25** → `"T UVW"`

---

## Real-World Example: Your Payslip

Your payslip full text is **1271 characters**.

Settings: `chunk_size = 900`, `chunk_overlap = 150`

### Round 1 — Chunk 1

```
Position:  0 .................................................. 900
           |--- Chunk 1 --------------------------------------|
```

- Window: position **0 to 900** (900 characters)
- After `.strip()` (removing whitespace): **~850 characters**
- Content: `"ebm-papst India Private Limited ... VEHICLE FUEL REIMBURSEMENT 5,000.00 5"`
- Next start = `900 - 150` = **750**

### Round 2 — Chunk 2

```
Position:  0 ............. 750 ......... 900 ................. 1271
                            |--- Chunk 2 ----------------------|
```

- Window: position **750 to 1271** (521 characters)
- Content: `"108.00\nMEDICAL ALLOWANCE ... Signature of the Employee"`
- End of text reached → loop stops

### The Overlap Zone (Position 750 to 900)

```
|--- Chunk 1 (pos 0 to 900) ---------------------------------------------------|
                                                     |<--- 150 chars --->|
                                                     |--- Chunk 2 (pos 750 to 1271) ----------|
                                                  pos 750              pos 900
```

The text from **position 750 to 900** appears in **BOTH** chunks. This overlap text contains something like:

```
"...5,000.00
TELEPHONE REIMBURSEMENT 3,000.00 3,000.00
DEDUCTIONS
AMOUNT RS.
PROVIDENT FUND 2,179.00
PROFESSIONAL TAX 418.00..."
```

This exact same text is at the **end of Chunk 1** and the **beginning of Chunk 2**.

---

## Why is `.strip()` Used?

The code does:

```python
chunk = full_text[start:end].strip()
```

`.strip()` removes leading/trailing **whitespace** (spaces, newlines, tabs). This is why Chunk 1 is **850 characters** instead of 900 — about 50 characters of whitespace were trimmed.

> **Important:** The overlap calculation uses the **original window position** (900), NOT the stripped length (850).

---

## Why Do We Need Overlap?

### Without Overlap (Bad)

```
Chunk 1: "...VEHICLE FUEL REIMBURSEMENT 5,000.00 5"
Chunk 2: ",000.00\nTELEPHONE REIMBURSEMENT..."
```

The sentence `"VEHICLE FUEL REIMBURSEMENT 5,000.00"` is **cut in half**!  
If you ask: *"What is the Vehicle Fuel Reimbursement amount?"* — neither chunk alone has the complete answer.

### With 150-char Overlap (Good)

```
Chunk 1: "...VEHICLE FUEL REIMBURSEMENT 5,000.00 5,000.00\nTELEPHONE REIMBURSEMENT 3,000.00..."
Chunk 2: "...VEHICLE FUEL REIMBURSEMENT 5,000.00 5,000.00\nTELEPHONE REIMBURSEMENT 3,000.00..."
```

**Both chunks** contain the full sentence. The AI can find the answer from **either** chunk.

### Real-World Analogy

Think of a **book with overlapping pages**. When you tear pages apart, you'd want each page to repeat a few lines from the previous page — so you don't lose any meaning at the page break. That's exactly what chunk overlap does.

---

## The Formula

```
next_start = current_end - chunk_overlap
```

| Step | Start | End                          | Chunk Size | Next Start          |
|------|-------|------------------------------|------------|---------------------|
| 1    | 0     | min(0+900, 1271) = 900       | 900        | 900 - 150 = **750** |
| 2    | 750   | min(750+900, 1271) = 1271    | 521        | End of text (stop)  |

---

## Code Walkthrough

```python
def chunk_pages(pages, chunk_size=900, chunk_overlap=150):
    chunks = []                          # Empty list to store results
    full_text = " ".join(pages)          # Combine all pages into one string
    text_length = len(full_text)         # Total length of text
    start = 0                            # Starting position

    while start < text_length:
        end = min(start + chunk_size, text_length)   # Don't go past the end
        chunk = full_text[start:end].strip()          # Extract & clean chunk

        if chunk:
            chunks.append(chunk)         # Store the chunk

        if end >= text_length:
            break                        # We've reached the end, stop

        start = end - chunk_overlap      # Slide window back by overlap amount

    return chunks
```

### What Each Line Does:

1. **`full_text = " ".join(pages)`** — Combines all PDF pages into one continuous string
2. **`end = min(start + chunk_size, text_length)`** — Ensures we don't read past the end of text
3. **`chunk = full_text[start:end].strip()`** — Extracts the text slice and removes whitespace
4. **`start = end - chunk_overlap`** — Moves the window forward, but slides back 150 chars for overlap

---

## Summary

| Concept         | Value | Meaning                                                    |
|-----------------|-------|------------------------------------------------------------|
| `chunk_size`    | 900   | Max characters per chunk (before stripping whitespace)     |
| `chunk_overlap` | 150   | Characters shared between adjacent chunks                  |
| Total text      | 1271  | Your payslip text length                                   |
| Chunks created  | 2     | Number of pieces your text was split into                  |
| Chunk 1         | ~850  | Characters 0–900 (after strip)                             |
| Chunk 2         | ~521  | Characters 750–1271 (after strip)                          |
| Overlap zone    | 150   | Characters 750–900 appear in both Chunk 1 and Chunk 2     |
