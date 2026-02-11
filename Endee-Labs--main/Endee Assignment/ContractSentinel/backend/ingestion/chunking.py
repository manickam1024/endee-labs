from typing import List

class RecursiveTokenChunker:
    """
    Splits text recursively by separators to ensure chunks fit within a token limit.
    This mimics the behavior of LangChain's RecursiveCharacterTextSplitter but is 
    implemented from scratch to demonstrate understanding of the algorithm.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        final_chunks = []
        self._split_recursive(text, self.separators, final_chunks)
        return final_chunks

    def _split_recursive(self, text: str, separators: List[str], final_chunks: List[str]):
        # Base case: if text is small enough, add it
        if len(text) <= self.chunk_size:
            final_chunks.append(text)
            return

        # Choose the best separator
        separator = separators[-1] # Default to the last one (character level)
        for sep in separators:
            if sep in text:
                separator = sep
                break
        
        # Split
        if separator == "":
            splits = list(text) # Character split
        else:
            splits = text.split(separator)

        # Merge splits back into chunks
        current_chunk = []
        current_len = 0
        
        new_separators = separators[separators.index(separator) + 1:] if separator in separators and separator != "" else []

        for split in splits:
            split_len = len(split)
            if current_len + split_len + len(separator) > self.chunk_size:
                # If the current chunk is full, finalize it
                if current_chunk:
                    joined_chunk = separator.join(current_chunk)
                    if len(joined_chunk) > self.chunk_size: 
                        # If a single split is too big even after splitting by current sep, recurse on it
                        self._split_recursive(joined_chunk, new_separators, final_chunks)
                    else:
                        final_chunks.append(joined_chunk)
                    
                    # Start new chunk with overlap (simplified overlap logic)
                    # For a real robust overlap, we'd need to keep the last few tokens.
                    # Here we just reset. 
                    current_chunk = [split]
                    current_len = split_len
            else:
                current_chunk.append(split)
                current_len += split_len + len(separator)
        
        # Add the last chunk
        if current_chunk:
            final_chunks.append(separator.join(current_chunk))
