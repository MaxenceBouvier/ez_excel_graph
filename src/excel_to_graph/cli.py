"""
Command-line interface for excel_to_graph.

This provides a simple CLI for quick graph generation,
though the main interface is through Claude Code natural language prompts.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from excel_to_graph.reader import ExcelReader
from excel_to_graph.visualizer import GraphVisualizer
from excel_to_graph.utils import setup_output_dir, generate_filename


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate graphs from Excel timeline data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all standard charts from an Excel file
  excel-to-graph resources/data.xlsx --all

  # Generate only timeline chart as PNG
  excel-to-graph resources/data.xlsx --timeline --format png

  # Generate bar chart as interactive HTML
  excel-to-graph resources/data.xlsx --bar --format html

  # Generate charts from specific sheet
  excel-to-graph resources/data.xlsx --sheet "Sheet1" --all

For more advanced usage, use Claude Code with natural language:
  claude
  > "Generate a timeline chart from my Excel data"
        """
    )

    parser.add_argument(
        "file",
        type=str,
        help="Path to Excel file"
    )

    parser.add_argument(
        "-s", "--sheet",
        type=str,
        default=None,
        help="Sheet name to process (default: first sheet)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="outputs",
        help="Output directory (default: outputs)"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["png", "pdf", "html"],
        default="png",
        help="Output format (default: png)"
    )

    # Chart type options
    chart_group = parser.add_argument_group("chart types")
    chart_group.add_argument(
        "--timeline",
        action="store_true",
        help="Generate timeline/Gantt chart"
    )
    chart_group.add_argument(
        "--bar",
        action="store_true",
        help="Generate bar chart of speaking time"
    )
    chart_group.add_argument(
        "--distribution",
        action="store_true",
        help="Generate distribution plot"
    )
    chart_group.add_argument(
        "--heatmap",
        action="store_true",
        help="Generate heatmap"
    )
    chart_group.add_argument(
        "--all",
        action="store_true",
        help="Generate all chart types"
    )

    args = parser.parse_args()

    # Validate file exists
    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    try:
        # Setup output directory
        setup_output_dir(args.output)

        # Load Excel data
        print(f"Loading Excel file: {args.file}")
        reader = ExcelReader(args.file)
        reader.load_all_sheets()

        # Get data from specified sheet
        df = reader.get_timeline_data(args.sheet)

        print(f"Loaded {len(df)} rows from sheet: {args.sheet or reader.sheet_names[0]}")

        # Show summary stats
        stats = reader.get_summary_stats(df)
        print(f"  - {stats['unique_speakers']} unique speakers")
        print(f"  - {stats['unique_times']} time periods")
        print(f"  - {stats['num_idea_columns']} idea columns")
        print()

        # Create visualizer
        visualizer = GraphVisualizer(df, args.output)

        # Determine which charts to generate
        generate_all = args.all or not any([args.timeline, args.bar, args.distribution, args.heatmap])

        generated_files = []

        # Generate timeline chart
        if args.timeline or generate_all:
            print("Generating timeline chart...")
            output_file = visualizer.timeline_chart(format=args.format)
            generated_files.append(output_file)
            print(f"  ✓ Saved: {output_file}")

        # Generate bar chart
        if args.bar or generate_all:
            print("Generating bar chart...")
            output_file = visualizer.bar_chart_speaking_time(format=args.format)
            generated_files.append(output_file)
            print(f"  ✓ Saved: {output_file}")

        # Generate distribution plot
        if args.distribution or generate_all:
            print("Generating distribution plot...")
            output_file = visualizer.distribution_plot(format=args.format)
            generated_files.append(output_file)
            print(f"  ✓ Saved: {output_file}")

        # Generate heatmap
        if args.heatmap or generate_all:
            print("Generating heatmap...")
            output_file = visualizer.heatmap_person_time(format=args.format)
            generated_files.append(output_file)
            print(f"  ✓ Saved: {output_file}")

        print()
        print(f"✓ Successfully generated {len(generated_files)} chart(s)")
        print(f"  Output directory: {args.output}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
