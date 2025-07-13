"""
TextSplitter service for splitting text into documents based on token limits.

This module provides functionality to split large text documents into smaller documents
while preserving metadata such as headers, URLs, and images.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
import tiktoken
from app.API.Src.Document.models.document import Document

logger = logging.getLogger(__name__)


class Headers:
    """Represents headers extracted from text documents."""
    
    def __init__(self):
        self._headers: Dict[str, List[str]] = {}
    
    def __getitem__(self, key: str) -> List[str]:
        return self._headers.get(key, [])
    
    def __setitem__(self, key: str, value: List[str]):
        self._headers[key] = value
    
    def get(self, key: str, default: List[str] = None) -> List[str]:
        return self._headers.get(key, default or [])
    
    def keys(self):
        return self._headers.keys()
    
    def items(self):
        return self._headers.items()
    
    def copy(self) -> 'Headers':
        new_headers = Headers()
        new_headers._headers = self._headers.copy()
        return new_headers
    
    def __contains__(self, key: str) -> bool:
        return key in self._headers
    
    def __delitem__(self, key: str):
        del self._headers[key]


# IDoc class removed - using Document model directly


class TextSplitter:
    """
    Service for splitting text into documents based on token limits.
    
    This class handles text splitting while preserving document structure,
    extracting headers, URLs, and images from text documents.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize TextSplitter with specified model.
        
        Args:
            model_name: The model name for tokenization (default: "gpt-4o")
        """
        self.model_name = model_name
        self.tokenizer: Optional[tiktoken.Encoding] = None
        
        # Special tokens mapping
        self.special_tokens = {
            "<|im_start|>": 100264,
            "<|im_end|>": 100265,
            "<|im_sep|>": 100266,
        }
    
    def _initialize_tokenizer(self) -> None:
        """Initialize the tokenizer if not already initialized."""
        if self.tokenizer is None:
            try:
                # Map model names to tiktoken encodings
                model_mapping = {
                    "gpt-4o": "cl100k_base",
                    "gpt-4": "cl100k_base", 
                    "gpt-3.5-turbo": "cl100k_base",
                    "gpt-3.5-turbo-16k": "cl100k_base",
                    "text-embedding-ada-002": "cl100k_base",
                    "text-davinci-003": "p50k_base",
                    "text-davinci-002": "p50k_base",
                    "text-davinci-001": "r50k_base",
                    "text-curie-001": "r50k_base",
                    "text-babbage-001": "r50k_base",
                    "text-ada-001": "r50k_base",
                    "davinci": "r50k_base",
                    "curie": "r50k_base",
                    "babbage": "r50k_base",
                    "ada": "r50k_base",
                }
                
                encoding_name = model_mapping.get(self.model_name, "cl100k_base")
                self.tokenizer = tiktoken.get_encoding(encoding_name)
                logger.info(f"Tokenizer initialized for model: {self.model_name}")
                
            except Exception as e:
                logger.error(f"Failed to initialize tokenizer: {e}")
                raise RuntimeError(f"Tokenizer initialization failed: {e}")
    
    def _count_tokens(self, text: str) -> int:
        """
        Count tokens in the given text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
            
        Raises:
            RuntimeError: If tokenizer is not initialized
        """
        if self.tokenizer is None:
            raise RuntimeError("Tokenizer not initialized")
        
        formatted_content = self._format_for_tokenization(text)
        tokens = self.tokenizer.encode(formatted_content)
        return len(tokens)
    
    def _format_for_tokenization(self, text: str) -> str:
        """
        Format text for tokenization with special tokens.
        
        Args:
            text: Text to format
            
        Returns:
            Formatted text with special tokens
        """
        return f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant<|im_end|>"
    
    async def split(self, text: str, limit: int) -> List[Document]:
        """
        Split text into documents based on token limit.
        
        Args:
            text: Text to split
            limit: Maximum tokens per document
            
        Returns:
            List of documents with metadata
        """
        logger.info(f"Starting split process with limit: {limit} tokens")
        
        self._initialize_tokenizer()
        documents: List[Document] = []
        position = 0
        total_length = len(text)
        current_headers = Headers()
        
        while position < total_length:
            logger.info(f"Processing document starting at position: {position}")
            
            document_text, document_end = self._get_document(text, position, limit)
            tokens = self._count_tokens(document_text)
            logger.info(f"Document tokens: {tokens}")
            
            headers_in_document = self._extract_headers(document_text)
            self._update_current_headers(current_headers, headers_in_document)
            
            content, urls, images = self._extract_urls_and_images(document_text)
            
            documents.append(Document(
                content=content,
                metadata={
                    "tokens": tokens,
                    "headers": {k: v for k, v in current_headers.items()},
                    "urls": urls,
                    "images": images,
                }
            ))
            
            logger.info(f"Document processed. New position: {document_end}")
            position = document_end
        
        logger.info(f"Split process completed. Total documents: {len(documents)}")
        return documents
    
    def _get_document(self, text: str, start: int, limit: int) -> Tuple[str, int]:
        """
        Get a single document of text within token limit.
        
        Args:
            text: Full text to split into documents
            start: Starting position
            limit: Token limit
            
        Returns:
            Tuple of (document_text, document_end_position)
        """
        logger.info(f"Getting document starting at {start} with limit {limit}")
        
        # Account for token overhead due to formatting
        overhead = self._count_tokens(self._format_for_tokenization("")) - self._count_tokens("")
        
        # Initial tentative end position
        if start >= len(text):
            return "", start
        
        # Estimate end position based on token density
        remaining_text = text[start:]
        if not remaining_text:
            return "", start
        
        estimated_tokens = self._count_tokens(remaining_text)
        if estimated_tokens == 0:
            return "", start
        
        # Calculate approximate end position
        end = min(
            start + int((len(remaining_text) * limit) / estimated_tokens),
            len(text)
        )
        
        # Adjust end to avoid exceeding token limit
        document_text = text[start:end]
        tokens = self._count_tokens(document_text)
        
        while tokens + overhead > limit and end > start:
            logger.info(f"Document exceeds limit with {tokens + overhead} tokens. Adjusting end position...")
            end = self._find_new_document_end(text, start, end)
            document_text = text[start:end]
            tokens = self._count_tokens(document_text)
        
        # Adjust document end to align with newlines
        end = self._adjust_document_end(text, start, end, tokens + overhead, limit)
        
        document_text = text[start:end]
        tokens = self._count_tokens(document_text)
        logger.info(f"Final document end: {end}")
        
        return document_text, end
    
    def _adjust_document_end(self, text: str, start: int, end: int, current_tokens: int, limit: int) -> int:
        """
        Adjust document end to align with newlines when possible.
        
        Args:
            text: Full text
            start: Document start position
            end: Current document end position
            current_tokens: Current token count
            limit: Token limit
            
        Returns:
            Adjusted end position
        """
        min_document_tokens = int(limit * 0.8)  # Minimum document size is 80% of limit
        
        next_newline = text.find('\n', end)
        prev_newline = text.rfind('\n', start, end)
        
        # Try extending to next newline
        if next_newline != -1 and next_newline < len(text):
            extended_end = next_newline + 1
            document_text = text[start:extended_end]
            tokens = self._count_tokens(document_text)
            if tokens <= limit and tokens >= min_document_tokens:
                logger.info(f"Extending document to next newline at position {extended_end}")
                return extended_end
        
        # Try reducing to previous newline
        if prev_newline > start:
            reduced_end = prev_newline + 1
            document_text = text[start:reduced_end]
            tokens = self._count_tokens(document_text)
            if tokens <= limit and tokens >= min_document_tokens:
                logger.info(f"Reducing document to previous newline at position {reduced_end}")
                return reduced_end
        
        # Return original end if adjustments aren't suitable
        return end
    
    def _find_new_document_end(self, text: str, start: int, end: int) -> int:
        """
        Find new document end position by reducing current end.
        
        Args:
            text: Full text
            start: Document start position
            end: Current document end position
            
        Returns:
            New end position
        """
        # Reduce end position to try to fit within token limit
        new_end = end - int((end - start) / 10)  # Reduce by 10% each iteration
        if new_end <= start:
            new_end = start + 1  # Ensure at least one character is included
        return new_end
    
    def _extract_headers(self, text: str) -> Headers:
        """
        Extract headers from text using regex.
        
        Args:
            text: Text to extract headers from
            
        Returns:
            Headers object with extracted headers
        """
        headers = Headers()
        header_regex = r'(^|\n)(#{1,6})\s+(.*)'
        
        for match in re.finditer(header_regex, text, re.MULTILINE):
            level = len(match.group(2))
            content = match.group(3).strip()
            key = f"h{level}"
            
            if key not in headers:
                headers[key] = []
            headers[key].append(content)
        
        return headers
    
    def _update_current_headers(self, current: Headers, extracted: Headers) -> None:
        """
        Update current headers with newly extracted headers.
        
        Args:
            current: Current headers to update
            extracted: Newly extracted headers
        """
        for level in range(1, 7):
            key = f"h{level}"
            if key in extracted:
                current[key] = extracted[key]
                self._clear_lower_headers(current, level)
    
    def _clear_lower_headers(self, headers: Headers, level: int) -> None:
        """
        Clear headers of lower levels when a higher level header is found.
        
        Args:
            headers: Headers to modify
            level: Current header level
        """
        for l in range(level + 1, 7):
            key = f"h{l}"
            if key in headers:
                del headers[key]
    
    def _extract_urls_and_images(self, text: str) -> Tuple[str, List[str], List[str]]:
        """
        Extract URLs and images from text, replacing them with placeholders.
        
        Args:
            text: Text to process
            
        Returns:
            Tuple of (processed_content, urls, images)
        """
        urls: List[str] = []
        images: List[str] = []
        url_index = 0
        image_index = 0
        
        # Replace images with placeholders
        def replace_image(match):
            nonlocal image_index
            alt_text, url = match.groups()
            images.append(url)
            placeholder = f"![{alt_text}]({{{{$img{image_index}}}}})"
            image_index += 1
            return placeholder
        
        # Replace links with placeholders
        def replace_link(match):
            nonlocal url_index
            link_text, url = match.groups()
            urls.append(url)
            placeholder = f"[{link_text}]({{{{$url{url_index}}}}})"
            url_index += 1
            return placeholder
        
        # Process images first, then links
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, text)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
        
        return content, urls, images