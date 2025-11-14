"""
Utility functions for the excel_to_graph package.

Provides helpers for file management, output organization, and naming.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import re


def setup_output_dir(base_dir: str = "outputs") -> Path:
    """
    Create and organize the output directory structure.

    Args:
        base_dir: Base directory for outputs

    Returns:
        Path object for the output directory
    """
    output_path = Path(base_dir)
    output_path.mkdir(exist_ok=True)

    # Create subdirectories for different output types
    (output_path / "png").mkdir(exist_ok=True)
    (output_path / "pdf").mkdir(exist_ok=True)
    (output_path / "html").mkdir(exist_ok=True)

    return output_path


def generate_filename(
    base_name: str,
    chart_type: str = "",
    format: str = "png",
    include_timestamp: bool = True
) -> str:
    """
    Generate a meaningful filename for output files.

    Args:
        base_name: Base name for the file (e.g., "timeline", "speakers")
        chart_type: Type of chart (e.g., "bar", "line", "heatmap")
        format: File format extension
        include_timestamp: Whether to include timestamp in filename

    Returns:
        Complete filename with proper formatting

    Examples:
        >>> generate_filename("timeline", "gantt", "png")
        'timeline_gantt_2025-11-14_10-30-45.png'

        >>> generate_filename("speakers", "bar", "pdf", include_timestamp=False)
        'speakers_bar.pdf'
    """
    # Sanitize base_name
    base_name = sanitize_filename(base_name)

    # Build filename parts
    parts = [base_name]

    if chart_type:
        parts.append(sanitize_filename(chart_type))

    if include_timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        parts.append(timestamp)

    # Join parts and add extension
    filename = "_".join(parts)
    if not filename.endswith(f".{format}"):
        filename += f".{format}"

    return filename


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.

    Args:
        name: String to sanitize

    Returns:
        Sanitized string safe for filenames

    Examples:
        >>> sanitize_filename("My Chart: Timeline #1")
        'my_chart_timeline_1'
    """
    # Convert to lowercase
    name = name.lower()

    # Replace spaces and special characters with underscores
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s-]+', '_', name)

    # Remove leading/trailing underscores
    name = name.strip('_')

    return name


def organize_output_file(
    file_path: str,
    organize_by_type: bool = True
) -> str:
    """
    Move an output file to the appropriate subdirectory.

    Args:
        file_path: Path to the file to organize
        organize_by_type: Whether to organize into subdirectories by file type

    Returns:
        New path to the organized file
    """
    path = Path(file_path)

    if not organize_by_type or not path.exists():
        return str(path)

    # Determine subdirectory based on extension
    ext = path.suffix.lstrip('.')
    if ext in ['png', 'pdf', 'html']:
        subdir = path.parent / ext
        subdir.mkdir(exist_ok=True)

        new_path = subdir / path.name

        # Move file if not already in subdirectory
        if path.parent != subdir:
            path.rename(new_path)
            return str(new_path)

    return str(path)


def get_file_info(file_path: str) -> dict:
    """
    Get information about a file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file information
    """
    path = Path(file_path)

    if not path.exists():
        return {"exists": False}

    return {
        "exists": True,
        "name": path.name,
        "size_bytes": path.stat().st_size,
        "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
        "extension": path.suffix,
        "created": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
    }


def format_size(size_bytes: int) -> str:
    """
    Format a file size in bytes to human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'

        >>> format_size(1048576)
        '1.0 MB'
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def list_output_files(output_dir: str = "outputs", format: Optional[str] = None) -> list:
    """
    List all output files in the output directory.

    Args:
        output_dir: Output directory to search
        format: Filter by file format (e.g., "png", "pdf")

    Returns:
        List of file paths
    """
    output_path = Path(output_dir)

    if not output_path.exists():
        return []

    if format:
        pattern = f"**/*.{format}"
    else:
        pattern = "**/*.*"

    files = sorted(output_path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)

    return [str(f) for f in files]
