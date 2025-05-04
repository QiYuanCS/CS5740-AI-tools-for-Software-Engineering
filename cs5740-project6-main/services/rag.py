import asyncio
import csv
import os
from typing import List, Tuple
import tiktoken as tkn
from PyPDF2 import PdfReader
from openai import OpenAI
from sklearn.neighbors import NearestNeighbors
import numpy as np
import services.llm

from pdf2image import convert_from_path
from PIL import Image
import io
from openai import APITimeoutError
import time

# Global configuration
EMBEDDING_MODEL = "text-embedding-3-small"
CSV_FILE_PATH = "data/ThePragmaticProgrammer.embeddings.csv"


async def ask_book(query: str, return_image: bool = False):
    """
    Main RAG (Retrieval Augmented Generation) implementation.
    Takes a query about the book and returns relevant information with optional page image.
    """
    # OpenAI client configuration with increased timeout
    client = OpenAI(
        base_url=os.getenv('OPENAI_API_BASE_URL', 'http://aitools.cs.vt.edu:7860/openai/v1'),
        api_key=os.getenv('OPENAI_API_KEY', "c3RldmU3Mjo4OTU2"),
        timeout=60  # Increase timeout to 60 seconds
    )

    # Source PDF path
    pdf_path = "data/ThePragmaticProgrammer.pdf"
    print(f"Checking PDF path: {pdf_path}")

    # Embedding management
    if os.path.exists(CSV_FILE_PATH):
        print(f"CSV file exists at {CSV_FILE_PATH}, loading embeddings...")
        embeddings_data = load_embeddings_from_csv(CSV_FILE_PATH)
    else:
        print(f"CSV file not found at {CSV_FILE_PATH}, generating embeddings...")
        # Check if PDF exists
        if not os.path.exists(pdf_path):
            return {
                "answer": f"Error: PDF file not found at {pdf_path}",
                "page_number": -1,
                "context": "",
                "image_data": None
            }

        # Extract text from PDF
        pages_text = __extract_text_from_pdf(pdf_path)
        if not pages_text:
            return {
                "answer": "Error: No text extracted from PDF.",
                "page_number": -1,
                "context": "",
                "image_data": None
            }

        try:
            chunks, embeddings = await asyncio.gather(
                __chunk_prompt(pages_text),
                __calculate_embeddings(client, [pt[1] for pt in pages_text], batch_size=5)
                # Use page text for embeddings
            )
        except APITimeoutError as e:
            print(f"API timeout error: {e}. Retrying with smaller batch size.")
            chunks = await __chunk_prompt(pages_text)
            documents = [chunk[1] for chunk in chunks]
            embeddings = await __calculate_embeddings(client, documents, batch_size=1)

        documents = [chunk[1] for chunk in chunks]
        print(f"Generated {len(embeddings)} embeddings for {len(documents)} documents.")
        save_embeddings_to_csv(CSV_FILE_PATH, "ThePragmaticProgrammer", [chunk[0] for chunk in chunks], embeddings,
                               documents)
        embeddings_data = [{"page_number": chunk[0], "embedding": emb, "context": doc} for chunk, emb, doc in
                           zip(chunks, embeddings, documents)]

    # Validate embeddings_data
    if not embeddings_data or "context" not in embeddings_data[0]:
        return {
            "answer": "Error: No valid embedding data available.",
            "page_number": -1,
            "context": "",
            "image_data": None
        }

    # Semantic search
    try:
        query_embedding = (await __calculate_embeddings(client, [query], batch_size=1))[0]
        print("Query embedding generated successfully.")
    except APITimeoutError as e:
        return {
            "answer": "Error: Unable to process query due to API timeout.",
            "page_number": -1,
            "context": "",
            "image_data": None
        }

    # Perform nearest neighbors search
    embeddings = np.array([item["embedding"] for item in embeddings_data])
    if embeddings.size == 0:
        return {
            "answer": "Error: No embeddings available for search.",
            "page_number": -1,
            "context": "",
            "image_data": None
        }

    nbrs = NearestNeighbors(n_neighbors=1, metric="cosine").fit(embeddings)
    distances, indices = nbrs.kneighbors([query_embedding])
    best_match_idx = indices[0][0]
    print(f"Best match found at index {best_match_idx}, distance: {distances[0][0]}")

    # Define context and page_number from the best match
    page_number = embeddings_data[best_match_idx]["page_number"]
    context = embeddings_data[best_match_idx]["context"]

    # Answer generation
    messages = services.llm.create_conversation_starter(
        f"Based on this context from 'The Pragmatic Programmer':\n\n{context}\n\nAnswer the following question: {query}"
    )
    answer_chunks = services.llm.converse(messages)
    answer = ""
    async for chunk in answer_chunks:
        answer += chunk
    print(f"Answer generated: {answer[:50]}...")

    # Optional image extraction
    image_data = None
    if return_image:
        image_data = __extract_page_as_image(pdf_path, page_number)
        print(f"Image extracted for page {page_number}: {len(image_data) if image_data else 'None'} bytes")

    return {
        "answer": answer,
        "page_number": page_number,
        "context": context,
        "image_data": image_data
    }


def __extract_text_from_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """Extract text content from each page of the PDF."""
    reader = PdfReader(pdf_path)
    pages_text = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        print(f"Extracted text from page {i}: {text[:50]}...")
        pages_text.append((i, text.strip()))
    return pages_text


def __extract_page_as_image(pdf_path: str, page_number: int) -> bytes:
    """Convert a specific PDF page to a PNG image."""
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    if images:
        img_byte_arr = io.BytesIO()
        images[0].save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    return None


async def __chunk_prompt(pages_text: List[Tuple[int, str]], chunk_size: int = 1500, overlap: int = 50) -> List[
    Tuple[int, str]]:
    """Split text into chunks suitable for embedding. One chunk per page for simplicity."""
    return pages_text  # For now, one chunk per page


async def __calculate_embeddings(client, documents, batch_size=5):
    """Generate embeddings for a list of documents."""
    embeddings = []
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch = [doc.strip() for doc in batch if isinstance(doc, str) and doc.strip()]
        if not batch:
            print(f"Warning: Skipping empty or invalid batch at index {i}. Input: {documents[i:i + batch_size]}")
            continue
        try:
            response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
            batch_embeddings = [emb.embedding for emb in response.data]
            embeddings.extend(batch_embeddings)
            print(f"Batch {i} processed: {len(batch_embeddings)} embeddings")
        except Exception as e:
            print(f"Error processing batch at index {i}: {str(e)}")
            raise ValueError(f"Embedding generation failed: {str(e)}")
    return embeddings


def save_embeddings_to_csv(file_path: str, document_name: str, page_numbers: List[int], embeddings: List[List[float]],
                           contexts: List[str]):
    """Cache embeddings to CSV for faster future lookups."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print(f"Saving embeddings to {file_path}")
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["document_name", "page_number", "embedding", "context"])
        for pn, emb, ctx in zip(page_numbers, embeddings, contexts):
            writer.writerow([document_name, pn, str(emb), ctx])
    print(f"Wrote {len(page_numbers)} rows to {file_path}")


def load_embeddings_from_csv(file_path: str) -> List[dict]:
    """Load previously cached embeddings from CSV."""
    results = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            embedding = eval(row["embedding"])  # Convert string back to list
            results.append({
                "document_name": row["document_name"],
                "page_number": int(row["page_number"]),
                "embedding": embedding,
                "context": row["context"]
            })
    print(f"Loaded {len(results)} embeddings from {file_path}")
    return results



