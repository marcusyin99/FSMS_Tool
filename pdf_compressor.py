import fitz  # PyMuPDF
import os

def compress_pdf(input_path: str, output_path: str, compression_level: int = 0) -> dict:
    """
    Compresses a PDF file using PyMuPDF (fitz) with optimal balance of size and quality.
    
    Args:
    - input_path (str): The file path of the original PDF.
    - output_path (str): The file path where the compressed PDF will be saved.
    - compression_level (int): 0 for Lossless. 1: 150 DPI (90q), 2: 100 DPI (75q), 3: 72 DPI (50q)
    
    Returns:
    - dict: A dictionary containing 'original_size', 'new_size', 'percentage_reduction', and 'status'.
    """
    try:
        if not os.path.exists(input_path):
            return {"status": "error", "message": f"Input file not found: {input_path}"}
            
        original_size = os.path.getsize(input_path)
        
        doc = fitz.open(input_path)
        
        # Applied lossy image re-sampling if requested
        if compression_level > 0:
            quality_map = {1: 90, 2: 75, 3: 50}
            dpi_map = {1: 150, 2: 100, 3: 72}
            
            target_q = quality_map.get(compression_level, 75)
            target_dpi = dpi_map.get(compression_level, 100)
            
            try:
                doc.rewrite_images(dpi_target=target_dpi, quality=target_q)
            except AttributeError:
                pass # Graceful fallback if library version lacks rewrite_images
        
        # Save output with full garbage structural optimization
        doc.save(
            output_path, 
            garbage=3, 
            deflate=True, 
            deflate_images=True,
            deflate_fonts=True,
            clean=True,
            incremental=False, 
            encryption=0
        )
        
        doc.close()
        
        new_size = os.path.getsize(output_path)
        reduction = 0.0
        
        if original_size > 0:
            reduction = ((original_size - new_size) / original_size) * 100
            
        return {
            "status": "success",
            "original_size": original_size,
            "new_size": new_size,
            "percentage_reduction": round(reduction, 2)
        }
        
    except fitz.FileDataError as e:
        return {"status": "error", "message": f"Corrupted or invalid PDF file: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred during compression: {e}"}
