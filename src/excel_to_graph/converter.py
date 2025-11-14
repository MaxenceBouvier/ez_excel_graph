"""
Excel to CSV converter module.

Converts Excel files to CSV format for easier inspection by Claude Code
and other text-based tools.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
import sys


def convert_excel_to_csv(
    excel_file: Path, output_dir: Optional[Path] = None, verbose: bool = True
) -> List[Path]:
    """
    Convert an Excel file to CSV format(s).

    Each sheet in the Excel file is converted to a separate CSV file
    named: <filename>_<sheetname>.csv

    Args:
        excel_file: Path to the Excel file
        output_dir: Directory to save CSV files (default: same as Excel file)
        verbose: Print progress messages

    Returns:
        List of paths to created CSV files

    Raises:
        FileNotFoundError: If Excel file doesn't exist
        ValueError: If file is not an Excel file
    """
    if not excel_file.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_file}")

    if excel_file.suffix.lower() not in [".xlsx", ".xls", ".xlsm", ".xlsb"]:
        raise ValueError(f"Not an Excel file: {excel_file}")

    # Determine output directory
    if output_dir is None:
        output_dir = excel_file.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Read all sheets from Excel file
    try:
        excel_data = pd.read_excel(excel_file, sheet_name=None, engine="openpyxl")
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {e}")

    # Base name for CSV files (without extension)
    base_name = excel_file.stem

    created_files = []

    # Convert each sheet to CSV
    for sheet_name, df in excel_data.items():
        # Sanitize sheet name for filename
        safe_sheet_name = sanitize_sheet_name(sheet_name)

        # Create CSV filename
        csv_filename = f"{base_name}_{safe_sheet_name}.csv"
        csv_path = output_dir / csv_filename

        # Save to CSV
        df.to_csv(csv_path, index=False, encoding="utf-8")
        created_files.append(csv_path)

        if verbose:
            print(f"  ✓ Created: {csv_path}")
            print(f"    Rows: {len(df)}, Columns: {len(df.columns)}")

    return created_files


def sanitize_sheet_name(name: str) -> str:
    """
    Sanitize a sheet name for use in filenames.

    Args:
        name: Sheet name to sanitize

    Returns:
        Sanitized name safe for filenames
    """
    # Replace problematic characters with underscores
    safe_chars = []
    for char in name:
        if char.isalnum() or char in ["-", "_"]:
            safe_chars.append(char)
        elif char == " ":
            safe_chars.append("_")
        # Skip other characters

    result = "".join(safe_chars)

    # Remove multiple consecutive underscores
    while "__" in result:
        result = result.replace("__", "_")

    # Remove leading/trailing underscores
    result = result.strip("_")

    # Ensure not empty
    if not result:
        result = "sheet"

    return result


def convert_directory(
    directory: Path, output_dir: Optional[Path] = None, verbose: bool = True
) -> dict:
    """
    Convert all Excel files in a directory to CSV.

    Args:
        directory: Directory containing Excel files
        output_dir: Directory to save CSV files (default: same as source)
        verbose: Print progress messages

    Returns:
        Dictionary mapping Excel files to lists of created CSV files

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    # Find all Excel files
    excel_extensions = ["*.xlsx", "*.xls", "*.xlsm", "*.xlsb"]
    excel_files = []

    for ext in excel_extensions:
        excel_files.extend(directory.glob(ext))
        excel_files.extend(directory.glob(ext.upper()))

    if not excel_files:
        if verbose:
            print(f"No Excel files found in {directory}")
        return {}

    results = {}

    for excel_file in sorted(excel_files):
        if verbose:
            print(f"\nConverting: {excel_file.name}")

        try:
            csv_files = convert_excel_to_csv(excel_file, output_dir, verbose)
            results[excel_file] = csv_files
        except Exception as e:
            if verbose:
                print(f"  ✗ Error: {e}")
            results[excel_file] = []

    return results


def main():
    """Command-line entry point for standalone usage."""
    if len(sys.argv) < 2:
        print("Usage: python -m excel_to_graph.converter <path>")
        print("  <path> can be an Excel file or directory")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if input_path.is_file():
        print(f"Converting Excel file: {input_path}")
        csv_files = convert_excel_to_csv(input_path)
        print(f"\n✓ Created {len(csv_files)} CSV file(s)")

    elif input_path.is_dir():
        print(f"Converting all Excel files in: {input_path}")
        results = convert_directory(input_path)
        total_csv = sum(len(csvs) for csvs in results.values())
        print(f"\n✓ Converted {len(results)} Excel file(s) to {total_csv} CSV file(s)")

    else:
        print(f"Error: Path not found: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
