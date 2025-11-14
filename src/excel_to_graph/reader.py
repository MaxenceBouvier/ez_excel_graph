"""
Excel file reader module.

This module handles reading Excel files with proper UTF-8 encoding
to support international characters (French accents: é, è, à, ô, etc.).
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional


class ExcelReader:
    """
    Read and parse Excel files for data analysis.

    Supports reading Excel files with multiple sheets and provides
    utilities for data inspection and preprocessing.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Excel reader.

        Args:
            file_path: Path to the Excel file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")

        self.workbook_data: Dict[str, pd.DataFrame] = {}
        self.sheet_names: List[str] = []

    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """
        Load all sheets from the Excel file.

        Returns:
            Dictionary mapping sheet names to DataFrames
        """
        # Read all sheets with proper encoding
        self.workbook_data = pd.read_excel(
            self.file_path, sheet_name=None, engine="openpyxl"  # Load all sheets
        )
        self.sheet_names = list(self.workbook_data.keys())
        return self.workbook_data

    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        """
        Load a specific sheet from the Excel file.

        Args:
            sheet_name: Name of the sheet to load

        Returns:
            DataFrame containing the sheet data
        """
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, engine="openpyxl")
        return df

    def get_data(
        self, sheet_name: Optional[str] = None, normalize_columns: bool = True
    ) -> pd.DataFrame:
        """
        Get data from a sheet with optional column name normalization.

        Args:
            sheet_name: Name of the sheet to process (if None, uses first sheet)
            normalize_columns: Whether to normalize column names (lowercase, strip whitespace)

        Returns:
            DataFrame with the sheet data
        """
        if sheet_name is None:
            if not self.workbook_data:
                self.load_all_sheets()
            sheet_name = self.sheet_names[0]

        df = self.workbook_data.get(sheet_name) or self.load_sheet(sheet_name)

        if normalize_columns:
            # Normalize column names (lowercase, strip whitespace)
            df.columns = df.columns.str.strip().str.lower()

        return df

    def get_timeline_data(self, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Get data from a sheet and format for timeline analysis.

        This is a specialized method that assumes a specific data structure:
        - Column 1: time/period data
        - Column 2: person/entity data
        - Remaining columns: additional attributes

        The first two columns will be renamed to 'speak_time' and 'speak_person'.

        Args:
            sheet_name: Name of the sheet to process (if None, uses first sheet)

        Returns:
            DataFrame with normalized and renamed columns
        """
        if sheet_name is None:
            if not self.workbook_data:
                self.load_all_sheets()
            sheet_name = self.sheet_names[0]

        df = self.workbook_data.get(sheet_name) or self.load_sheet(sheet_name)

        # Normalize column names (lowercase, strip whitespace)
        df.columns = df.columns.str.strip().str.lower()

        # Detect column structure
        # Expected: first column is time, second is person, rest are ideas
        if len(df.columns) >= 2:
            cols = list(df.columns)
            # Rename first two columns to standard names
            df = df.rename(columns={cols[0]: "speak_time", cols[1]: "speak_person"})

        return df

    def get_idea_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of idea column names from a DataFrame.

        Args:
            df: DataFrame to analyze

        Returns:
            List of column names that contain ideas
        """
        # All columns except speak_time and speak_person are idea columns
        idea_cols = [col for col in df.columns if col not in ["speak_time", "speak_person"]]
        return idea_cols

    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics about the data.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with summary statistics
        """
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_names": df.columns.tolist(),
        }

        # Add timeline-specific stats if columns exist
        if "speak_person" in df.columns:
            stats["unique_speakers"] = df["speak_person"].nunique()
            stats["speakers"] = df["speak_person"].unique().tolist()

        if "speak_time" in df.columns:
            stats["unique_times"] = df["speak_time"].nunique()
            stats["time_range"] = df["speak_time"].unique().tolist()

        if "speak_person" in df.columns or "speak_time" in df.columns:
            stats["idea_columns"] = self.get_idea_columns(df)
            stats["num_idea_columns"] = len(self.get_idea_columns(df))

        return stats

    def __repr__(self) -> str:
        return f"ExcelReader('{self.file_path}', sheets={len(self.sheet_names)})"
