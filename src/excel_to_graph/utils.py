"""
Utility functions for the excel_to_graph package.

Provides helpers for file management, output organization, and naming.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import re


def detect_project_from_path(file_path: str) -> Optional[str]:
    """
    Detect project name from a file path.

    If the file is in resources/<project_name>/, returns the project name.
    Otherwise returns None.

    Args:
        file_path: Path to check

    Returns:
        Project name or None

    Examples:
        >>> detect_project_from_path("resources/my-project/data.xlsx")
        "my-project"

        >>> detect_project_from_path("resources/data.xlsx")
        None
    """
    path = Path(file_path)

    # Check if path is under resources/
    try:
        # Get parts relative to resources directory
        parts = path.parts

        if "resources" in parts:
            resources_idx = parts.index("resources")
            # Check if there's a subdirectory after resources
            if len(parts) > resources_idx + 1:
                potential_project = parts[resources_idx + 1]
                # Verify it's not a file
                project_path = Path("resources") / potential_project
                if project_path.is_dir():
                    return potential_project

        return None
    except (ValueError, IndexError):
        return None


def get_output_dir_for_project(
    project_name: Optional[str] = None, base_dir: str = "outputs"
) -> str:
    """
    Get the appropriate output directory for a project.

    Args:
        project_name: Project name (if None, uses base_dir)
        base_dir: Base output directory

    Returns:
        Output directory path as string
    """
    if project_name:
        return f"{base_dir}/{project_name}"
    return base_dir


def setup_output_dir(base_dir: str = "outputs") -> Path:
    """
    Create and organize the output directory structure.

    Args:
        base_dir: Base directory for outputs

    Returns:
        Path object for the output directory
    """
    output_path = Path(base_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories for different output types
    (output_path / "png").mkdir(exist_ok=True)
    (output_path / "pdf").mkdir(exist_ok=True)
    (output_path / "html").mkdir(exist_ok=True)

    return output_path


def generate_filename(
    base_name: str, chart_type: str = "", format: str = "png", include_timestamp: bool = True
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
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s-]+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    return name


def organize_output_file(file_path: str, organize_by_type: bool = True) -> str:
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
    ext = path.suffix.lstrip(".")
    if ext in ["png", "pdf", "html"]:
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
    for unit in ["B", "KB", "MB", "GB"]:
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


def validate_project_name(name: str) -> tuple[bool, str]:
    """
    Validate a project name for file system safety.

    Project names can only contain:
    - Alphanumeric characters (a-z, A-Z, 0-9)
    - Hyphens (-)
    - Underscores (_)

    Args:
        name: Project name to validate

    Returns:
        Tuple of (is_valid, error_message)

    Examples:
        >>> validate_project_name("my-project_2024")
        (True, "")

        >>> validate_project_name("my project!")
        (False, "Project name can only contain letters, numbers, hyphens, and underscores")
    """
    if not name:
        return False, "Project name cannot be empty"

    if len(name) > 100:
        return False, "Project name is too long (max 100 characters)"

    # Check for valid characters only
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        return (
            False,
            "Project name can only contain letters, numbers, hyphens (-), and underscores (_)",
        )

    # Check it doesn't start/end with special characters
    if name[0] in ["-", "_"] or name[-1] in ["-", "_"]:
        return False, "Project name cannot start or end with hyphens or underscores"

    # Reserved names
    reserved = ["con", "prn", "aux", "nul", "com1", "com2", "lpt1", "lpt2"]
    if name.lower() in reserved:
        return False, f"'{name}' is a reserved name and cannot be used"

    return True, ""


def create_project_structure(project_name: str, base_dir: str = ".") -> dict:
    """
    Create the directory structure for a new project.

    Creates:
    - resources/<project_name>/
    - outputs/<project_name>/
    - scripts/<project_name>/

    Args:
        project_name: Name of the project
        base_dir: Base directory (default: current directory)

    Returns:
        Dictionary with created paths

    Raises:
        ValueError: If project name is invalid or project already exists
    """
    # Validate project name
    is_valid, error_msg = validate_project_name(project_name)
    if not is_valid:
        raise ValueError(error_msg)

    base_path = Path(base_dir)

    # Define project paths
    project_paths = {
        "resources": base_path / "resources" / project_name,
        "outputs": base_path / "outputs" / project_name,
        "scripts": base_path / "scripts" / project_name,
    }

    # Check if project already exists
    if any(path.exists() for path in project_paths.values()):
        raise ValueError(f"Project '{project_name}' already exists")

    # Create directories
    for path in project_paths.values():
        path.mkdir(parents=True, exist_ok=True)

    # Create README in resources directory
    resources_readme = project_paths["resources"] / "README.md"
    resources_readme.write_text(
        f"""# {project_name}

This directory contains Excel files for the **{project_name}** project.

## Usage

1. Place your Excel files (.xlsx, .xls) in this directory
2. Convert them to CSV for easier inspection:
   ```bash
   excel-to-graph convert resources/{project_name}
   ```
3. Generate visualizations using Claude Code or the CLI

## Files

Add your Excel data files here. They will not be committed to git (protected by .gitignore).

Generated CSV files will also appear here for easier data inspection.
"""
    )

    return {k: str(v) for k, v in project_paths.items()}


def list_projects(base_dir: str = ".") -> list[str]:
    """
    List all initialized projects.

    Args:
        base_dir: Base directory to search

    Returns:
        List of project names
    """
    base_path = Path(base_dir)
    resources_dir = base_path / "resources"

    if not resources_dir.exists():
        return []

    # Find all subdirectories in resources (these are projects)
    projects = [
        d.name for d in resources_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]

    return sorted(projects)
