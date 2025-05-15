import tiktoken
from db import Chunk

ENC = tiktoken.get_encoding("cl100k_base")
CHUNK_MAX_TOKENS = 500
OVERLAP = 50

def chunk_text(chunks: list) -> list:
    """
    Takes a list of Chunk objects and further splits them into smaller chunks
    by token count while preserving source and page metadata.
    """
    result = []
    
    for chunk in chunks:
        tokens = ENC.encode(chunk.text)
        
        # If the chunk is small enough, keep it as is
        if len(tokens) <= CHUNK_MAX_TOKENS:
            result.append(chunk)
            continue
        
        # Otherwise, split it into smaller chunks
        for i in range(0, len(tokens), CHUNK_MAX_TOKENS - OVERLAP):
            chunk_tokens = tokens[i:i + CHUNK_MAX_TOKENS]
            chunk_text = ENC.decode(chunk_tokens)
            
            # Create a new chunk with the same metadata
            result.append(Chunk(
                text=chunk_text,
                source=chunk.source,
                page=chunk.page
            ))
    
    return result