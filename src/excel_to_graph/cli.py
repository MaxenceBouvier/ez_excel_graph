"""
Command-line interface for excel_to_graph.

This provides a simple CLI for quick operations,
though the main interface is through Claude Code natural language prompts.
"""

import sys
import argparse
from pathlib import Path

import pandas as pd

from excel_to_graph.reader import ExcelReader
from excel_to_graph.visualizer import GraphVisualizer
from excel_to_graph.analyzer import StatisticalAnalyzer
from excel_to_graph.converter import convert_excel_to_csv, convert_directory
from excel_to_graph.utils import (
    setup_output_dir,
    create_project_structure,
    list_projects,
    detect_project_from_path,
    get_output_dir_for_project,
)


def cmd_init(args):
    """Handle the init command to create a new project."""
    try:
        paths = create_project_structure(args.project_name)

        print(f"✓ Created project: {args.project_name}")
        print("\nDirectories created:")
        for dir_type, path in paths.items():
            print(f"  - {dir_type}: {path}")

        print("\nNext steps:")
        print(f"  1. Add your Excel files to: resources/{args.project_name}/")
        print(f"  2. Convert to CSV: excel-to-graph convert resources/{args.project_name}")
        print("  3. Use Claude Code to generate visualizations")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


def cmd_convert(args):
    """Handle the convert command to convert Excel to CSV."""
    input_path = Path(args.path)

    if not input_path.exists():
        print(f"Error: Path not found: {input_path}", file=sys.stderr)
        return 1

    try:
        if input_path.is_file():
            # Convert single file
            print(f"Converting: {input_path.name}")
            output_dir = Path(args.output) if args.output else None
            csv_files = convert_excel_to_csv(input_path, output_dir, verbose=True)
            print(f"\n✓ Created {len(csv_files)} CSV file(s)")

        elif input_path.is_dir():
            # Convert all files in directory
            print(f"Converting Excel files in: {input_path}")
            output_dir = Path(args.output) if args.output else None
            results = convert_directory(input_path, output_dir, verbose=True)

            total_csv = sum(len(csvs) for csvs in results.values())
            print(f"\n✓ Converted {len(results)} Excel file(s) to {total_csv} CSV file(s)")

        else:
            print(f"Error: Invalid path: {input_path}", file=sys.stderr)
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args):
    """Handle the list command to show all projects."""
    projects = list_projects()

    if not projects:
        print("No projects found.")
        print("\nCreate a new project with:")
        print("  excel-to-graph init <project_name>")
        return 0

    print(f"Found {len(projects)} project(s):\n")
    for project in projects:
        print(f"  - {project}")

    print("\nTo work with a project:")
    print("  1. Add Excel files to resources/<project_name>/")
    print("  2. Convert: excel-to-graph convert resources/<project_name>")
    print("  3. Use Claude Code for visualizations")

    return 0


def cmd_analyze(args):
    """Handle the analyze command for statistical analysis."""
    # Validate file exists
    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return 1

    try:
        # Detect project and determine output directory
        project_name = detect_project_from_path(str(input_path))
        if project_name and args.output == "outputs/analyses":  # Using default
            output_dir = Path(get_output_dir_for_project(project_name)) / "analyses"
            print(f"Detected project: {project_name}")
            print(f"Analysis outputs will be saved to: {output_dir}")
        else:
            output_dir = Path(args.output)

        # Load data (supports both Excel and CSV)
        print(f"Loading data from: {input_path}")
        if input_path.suffix.lower() in [".xlsx", ".xls"]:
            reader = ExcelReader(str(input_path))
            reader.load_all_sheets()
            df = reader.get_data(args.sheet)
            sheet_name = args.sheet or reader.sheet_names[0]
            print(f"Loaded {len(df)} rows from sheet: {sheet_name}")
        elif input_path.suffix.lower() == ".csv":
            df = pd.read_csv(input_path, encoding="utf-8")
            print(f"Loaded {len(df)} rows from CSV")
        else:
            print(f"Error: Unsupported file format: {input_path.suffix}", file=sys.stderr)
            print("Supported formats: .xlsx, .xls, .csv", file=sys.stderr)
            return 1

        # Show basic info
        print(f"  - {len(df)} rows")
        print(f"  - {len(df.columns)} columns: {', '.join(df.columns[:5])}"
              f"{'...' if len(df.columns) > 5 else ''}")
        print()

        # Create analyzer
        analyzer = StatisticalAnalyzer(df, output_dir)

        # Interactive mode - prompt user to use Claude
        print("=" * 70)
        print("Statistical Analysis Ready!")
        print("=" * 70)
        print()
        print("This command is designed for use with Claude Code's natural language")
        print("interface. You can now ask Claude to perform various analyses:")
        print()
        print("Examples:")
        print('  • "Run a correlation analysis on all numeric variables"')
        print('  • "Perform an ANOVA comparing groups in column X"')
        print('  • "Do a t-test between group A and B for variable Y"')
        print('  • "Test if column Z follows a normal distribution"')
        print('  • "Run a chi-square test between categorical variables"')
        print()
        print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"Output directory: {output_dir}")
        print()

        # If specific analysis requested via command line, run it
        if args.describe:
            print("Running descriptive statistics...")
            stats = analyzer.describe()
            report_path = analyzer.save_report(
                stats,
                f"descriptive_stats_{input_path.stem}",
                "Descriptive Statistics"
            )
            print(f"✓ Report saved: {report_path}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_visualize(args):
    """Handle the visualize command (backward compatibility)."""
    # Validate file exists
    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    try:
        # Detect project and determine output directory
        project_name = detect_project_from_path(args.file)
        if project_name and args.output == "outputs":  # Only auto-organize if using default
            output_dir = get_output_dir_for_project(project_name)
            print(f"Detected project: {project_name}")
            print(f"Outputs will be saved to: {output_dir}")
        else:
            output_dir = args.output

        # Setup output directory
        setup_output_dir(output_dir)

        # Load Excel data
        print(f"Loading Excel file: {args.file}")
        reader = ExcelReader(args.file)
        reader.load_all_sheets()

        # Get data from specified sheet
        df = reader.get_data(args.sheet)

        print(f"Loaded {len(df)} rows from sheet: {args.sheet or reader.sheet_names[0]}")

        # Show summary stats
        stats = reader.get_summary_stats(df)
        print(f"  - {stats['total_rows']} rows")
        print(f"  - {len(df.columns)} columns")
        print()

        # Create visualizer
        visualizer = GraphVisualizer(df, output_dir)

        # Determine which charts to generate
        generate_all = args.all or not any(
            [args.timeline, args.bar, args.distribution, args.heatmap]
        )

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
        print(f"  Output directory: {output_dir}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="excel-to-graph",
        description="AI-assisted Excel data visualization tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
For more advanced usage, use Claude Code with natural language:
  claude
  > "Generate visualizations from my Excel data"
  > "Convert all Excel files in resources/my_project to CSV"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    parser_init = subparsers.add_parser(
        "init",
        help="Initialize a new project",
        description="Create a new project with organized directory structure",
    )
    parser_init.add_argument(
        "project_name",
        type=str,
        help="Name of the project (letters, numbers, hyphens, underscores only)",
    )
    parser_init.set_defaults(func=cmd_init)

    # Convert command
    parser_convert = subparsers.add_parser(
        "convert",
        help="Convert Excel files to CSV",
        description="Convert Excel files to CSV for easier inspection by Claude",
    )
    parser_convert.add_argument(
        "path", type=str, help="Path to Excel file or directory containing Excel files"
    )
    parser_convert.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output directory for CSV files (default: same as source)",
    )
    parser_convert.set_defaults(func=cmd_convert)

    # List command
    parser_list = subparsers.add_parser(
        "list", help="List all projects", description="Show all initialized projects"
    )
    parser_list.set_defaults(func=cmd_list)

    # Analyze command
    parser_analyze = subparsers.add_parser(
        "analyze",
        help="Perform statistical analysis on data",
        description="Advanced statistical analysis (ANOVA, correlations, t-tests, etc.)",
    )
    parser_analyze.add_argument("file", type=str, help="Path to Excel or CSV file")
    parser_analyze.add_argument(
        "-s",
        "--sheet",
        type=str,
        default=None,
        help="Sheet name to process (for Excel files, default: first sheet)",
    )
    parser_analyze.add_argument(
        "-o",
        "--output",
        type=str,
        default="outputs/analyses",
        help="Output directory for analysis reports (default: outputs/analyses)",
    )
    parser_analyze.add_argument(
        "--describe",
        action="store_true",
        help="Run descriptive statistics immediately",
    )
    parser_analyze.set_defaults(func=cmd_analyze)

    # Visualize command (for backward compatibility, can also be default)
    parser_viz = subparsers.add_parser(
        "visualize",
        help="Generate visualizations from Excel data",
        description="Generate charts and graphs from Excel data",
    )
    parser_viz.add_argument("file", type=str, help="Path to Excel file")
    parser_viz.add_argument(
        "-s", "--sheet", type=str, default=None, help="Sheet name to process (default: first sheet)"
    )
    parser_viz.add_argument(
        "-o", "--output", type=str, default="outputs", help="Output directory (default: outputs)"
    )
    parser_viz.add_argument(
        "-f",
        "--format",
        choices=["png", "pdf", "html"],
        default="png",
        help="Output format (default: png)",
    )

    # Chart type options for visualize
    chart_group = parser_viz.add_argument_group("chart types")
    chart_group.add_argument("--timeline", action="store_true", help="Generate timeline chart")
    chart_group.add_argument("--bar", action="store_true", help="Generate bar chart")
    chart_group.add_argument(
        "--distribution", action="store_true", help="Generate distribution plot"
    )
    chart_group.add_argument("--heatmap", action="store_true", help="Generate heatmap")
    chart_group.add_argument("--all", action="store_true", help="Generate all chart types")
    parser_viz.set_defaults(func=cmd_visualize)

    # Parse arguments
    args = parser.parse_args()

    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return 0

    # Execute the appropriate command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
