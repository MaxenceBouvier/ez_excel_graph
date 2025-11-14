"""
Excel to Graph - Generate beautiful graphs from Excel timeline data.

This package helps you visualize timeline data from Excel spreadsheets,
specifically designed for data with speak_time, speak_person, and idea columns.
"""

__version__ = "0.1.0"

from excel_to_graph.reader import ExcelReader
from excel_to_graph.visualizer import GraphVisualizer
from excel_to_graph.utils import setup_output_dir, generate_filename

__all__ = [
    "ExcelReader",
    "GraphVisualizer",
    "setup_output_dir",
    "generate_filename",
]
