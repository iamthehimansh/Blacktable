"""
Utility functions for Resume Parser
"""
import os
from pathlib import Path
from docling.document_converter import DocumentConverter


class DocumentProcessor:
    """Document processing utilities"""
    
    def __init__(self):
        self.converter = DocumentConverter()
    
    def convert_to_markdown(self, file_path: str) -> str:
        """
        Convert document to markdown using Docling
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Markdown content of the document
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = Path(file_path).suffix.lower()
        
        # For text files, read directly
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        # For other formats, use Docling
        try:
            result = self.converter.convert(file_path)
            return result.document.export_to_markdown()
        except Exception as e:
            raise ValueError(f"Failed to convert document {file_path}: {e}")
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Check if file format is supported
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if format is supported
        """
        supported_extensions = {'.pdf', '.doc', '.docx', '.txt'}
        file_extension = Path(file_path).suffix.lower()
        return file_extension in supported_extensions
