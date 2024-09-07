import os
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text


# Function to embed and store documents in the FAISS vector database
def build_faiss_index(text_chunks):
    embeddings = embedding_model.encode(text_chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Create a flat (brute-force) index
    index.add(np.array(embeddings))  # Add embeddings to the index
    return index, embeddings


# Function to query the vector database for the most relevant content
def query_faiss_index(query, index, text_chunks, k=5):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)  # Get top-k results
    return [text_chunks[i] for i in indices[0]]


# Function to generate content using OpenAI's GPT model
def generate_content(objective, context):
    prompt = f"Based on the following content:\n\n{context}\n\n Generate content for the following objective: {objective}"
    # Define the system prompt
    system_prompt = f"Based on the following content:\n\n{context}\n\n Generate content for the following objective: {objective}"

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        }
                    ]
                },
                # {
                #     "role": "user",
                #     "content": [
                #         {
                #             "type": "text",
                #             "text": content
                #         }
                #     ]
                # },

            ],
            temperature=0,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        llm_response = response.choices[0].message.content

        return llm_response
    except Exception as e:
        return f"Error: {str(e)}"


# Main function to handle RAG workflow
def rag_workflow(file, objective):
    # Extract content based on the file type (PDF or URL)
    text = extract_text_from_pdf(file)

    # Chunk the extracted text for better retrieval (split into paragraphs)
    text_chunks = text.split('\n\n')

    # Build FAISS index
    index, embeddings = build_faiss_index(text_chunks)

    # Retrieve relevant content based on the objective
    relevant_content = query_faiss_index(objective, index, text_chunks)

    # Generate new content using the relevant context and objective
    generated_content = generate_content(objective, '\n'.join(relevant_content))

    return generated_content


# Example Usage
if __name__ == "__main__":
    file_or_url = 'report-migration-program-2022-23.pdf'  # Replace with your file path or URL
    # file_or_url = 'https://www.vic.gov.au/education'  # Replace with your file path or URL
    objective = "Write a summary for a blog post"

    result = rag_workflow(file_or_url, objective)
    print(result)
