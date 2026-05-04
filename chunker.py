# Import type hints for better code readability
from typing import List, Tuple

def chunk_pages(pages: List[str], chunk_size: int = 900, chunk_overlap: int = 150) -> List[str]:
    """
    Splits a list of page texts into smaller overlapping chunks.

    Args:
        pages (List[str]): List of text strings, one per PDF page.
        chunk_size (int): Maximum number of characters per chunk (default: 900).
        chunk_overlap (int): Number of overlapping characters between consecutive chunks (default: 150).

    Returns:
        List[str]: A list of text chunks ready for embedding.
    """

    # Initialize an empty list to store the resulting chunks
    chunks: List[str] = []
    print(f"Chunking pages into chunks of size {chunk_size} with an overlap of {chunk_overlap}...")
    print("chunks:",chunks)  # Debug: Print the initial empty chunks list
    # Combine all page texts into one single continuous string
    full_text = " ".join(pages)
    print("full_text:",full_text)
    # Get the total length of the combined text
    text_length = len(full_text)
    print("text_length:",text_length)

    # If there's no text, return the empty list immediately
    if text_length == 0:
        return chunks

    # Start position of the sliding window
    start = 0

    # Slide a window across the text to create overlapping chunks
    while start < text_length:

        # Calculate the end position (don't go past the end of the text)
        end = min(start + chunk_size, text_length)

        # Extract the chunk from start to end, and remove leading/trailing whitespace
        chunk = full_text[start:end].strip()

        # Only add the chunk if it's not empty
        if chunk:
            chunks.append(chunk)

        # If we've reached the end of the text, stop the loop
        if end >= text_length:
            break

        # Move the window forward, but step back by chunk_overlap
        # so the next chunk shares some text with the current one.
        # This prevents losing context at chunk boundaries.
        start = end - chunk_overlap
        
    # Print each chunk separately
    print(f"\n{'='*60}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"{'='*60}")
    for i, c in enumerate(chunks, 1):
        print(f"\n{'*'*60}")
        print(f"  CHUNK {i} of {len(chunks)}  |  Length: {len(c)} chars")
        print(f"{'*'*60}")
        print(c)

    # Show overlapping text between consecutive chunks
    if len(chunks) > 1:
        print(f"\n{'#'*60}")
        print(f"  OVERLAP VISUALIZATION")
        print(f"{'#'*60}")
        for i in range(len(chunks) - 1):
            overlap_text = chunks[i][-chunk_overlap:]
            print(f"\n--- Overlap between Chunk {i+1} and Chunk {i+2} ---")
            print(f"Chunk {i+1} ENDS with:")
            print(f"  ...{chunks[i][-200:]}")
            print(f"\n>>>>> OVERLAPPING TEXT ({len(overlap_text)} chars) <<<<<")
            print(f'  "{overlap_text}"')
            print(f"\nChunk {i+2} STARTS with:")
            print(f"  {chunks[i+1][:200]}...")
        print(f"\n{'#'*60}\n")

    # Return the final list of text chunks
    return chunks