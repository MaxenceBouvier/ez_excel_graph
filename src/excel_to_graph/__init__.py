"""
Excel to Graph - Generate beautiful graphs from Excel data with AI assistance.

This package helps you visualize data from Excel spreadsheets using
natural language commands through Claude Code CLI.
"""

__version__ = "0.1.0"

from excel_to_graph.reader import ExcelReader
from excel_to_graph.visualizer import GraphVisualizer
from excel_to_graph.analyzer import StatisticalAnalyzer
from excel_to_graph.converter import convert_excel_to_csv, convert_directory
from excel_to_graph.utils import (
    setup_output_dir,
    generate_filename,
    validate_project_name,
    create_project_structure,
    list_projects,
    detect_project_from_path,
    get_output_dir_for_project,
)

__all__ = [
    "ExcelReader",
    "GraphVisualizer",
    "StatisticalAnalyzer",
    "convert_excel_to_csv",
    "convert_directory",
    "setup_output_dir",
    "generate_filename",
    "validate_project_name",
    "create_project_structure",
    "list_projects",
    "detect_project_from_path",
    "get_output_dir_for_project",
]
