import click
from extractor import extract_text
from chunker import chunk_text
from db import index_chunks, retrieve
from utils import generate_answer

@click.group()
def cli():
    """PDF RAG Chat CLI"""
    pass

@cli.command()
@click.argument('pdf_path')
def index(pdf_path):
    """Index a PDF into ChromaDB."""
    # Extract text as Chunk objects
    chunks = extract_text(pdf_path)
    # Further chunk the text if needed
    chunked = chunk_text(chunks)
    # Generate unique IDs for each chunk
    ids = [f"chunk_{i}" for i in range(len(chunked))]
    # Index the chunks
    index_chunks(ids, chunked)
    click.echo(f"Indexed {len(chunked)} chunks from {pdf_path}")

@cli.command()
def chat():
    """Enter interactive chat mode."""
    click.echo("Entering chat. Type 'exit' to quit.")
    while True:
        q = click.prompt("Question")
        if q.lower() in ('exit', 'quit'):
            break
        docs = retrieve(q)
        context = "\n---\n".join(docs)
        ans = generate_answer(context, q)
        click.echo(f"\nAnswer:\n{ans}\n")

if __name__ == '__main__':
    cli()