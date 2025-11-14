"""
Graph visualization module for timeline data.

This module creates various types of visualizations using matplotlib and plotly,
with proper support for French text and accents.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from typing import Optional, List, Literal
import seaborn as sns

# Set matplotlib to use a font that supports French characters
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False


class GraphVisualizer:
    """
    Create visualizations from timeline data.

    Supports multiple output formats: PNG, PDF, HTML (interactive)
    """

    def __init__(self, data: pd.DataFrame, output_dir: str = "outputs"):
        """
        Initialize the visualizer.

        Args:
            data: DataFrame with timeline data (must have speak_time, speak_person columns)
            output_dir: Directory to save output files
        """
        self.data = data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Verify required columns
        if 'speak_time' not in data.columns or 'speak_person' not in data.columns:
            raise ValueError("Data must contain 'speak_time' and 'speak_person' columns")

    def timeline_chart(
        self,
        title: str = "Timeline - Interventions par Personne",
        output_name: Optional[str] = None,
        format: Literal["png", "pdf", "html"] = "png"
    ) -> str:
        """
        Create a timeline/Gantt-style chart showing when each person spoke.

        Args:
            title: Chart title
            output_name: Output filename (without extension)
            format: Output format (png, pdf, or html)

        Returns:
            Path to the saved file
        """
        if format == "html":
            return self._timeline_chart_plotly(title, output_name)
        else:
            return self._timeline_chart_matplotlib(title, output_name, format)

    def _timeline_chart_matplotlib(
        self,
        title: str,
        output_name: Optional[str],
        format: str
    ) -> str:
        """Create timeline chart using matplotlib."""
        fig, ax = plt.subplots(figsize=(14, 8))

        # Prepare data: group by person and time
        timeline_data = self.data.groupby(['speak_person', 'speak_time']).size().reset_index(name='count')

        # Create y-positions for each person
        persons = timeline_data['speak_person'].unique()
        person_positions = {person: i for i, person in enumerate(persons)}

        # Plot each intervention
        for _, row in timeline_data.iterrows():
            person = row['speak_person']
            time = row['speak_time']
            y_pos = person_positions[person]

            ax.scatter(time, y_pos, s=200, alpha=0.6, c=f'C{y_pos % 10}')

        ax.set_yticks(range(len(persons)))
        ax.set_yticklabels(persons)
        ax.set_xlabel('Temps de Parole', fontsize=12)
        ax.set_ylabel('Personne', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save file
        if output_name is None:
            output_name = "timeline_chart"
        output_path = self.output_dir / f"{output_name}.{format}"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def _timeline_chart_plotly(self, title: str, output_name: Optional[str]) -> str:
        """Create interactive timeline chart using plotly."""
        # Prepare data
        timeline_data = self.data.groupby(['speak_person', 'speak_time']).size().reset_index(name='count')

        fig = px.scatter(
            timeline_data,
            x='speak_time',
            y='speak_person',
            size='count',
            color='speak_person',
            title=title,
            labels={'speak_time': 'Temps de Parole', 'speak_person': 'Personne'},
            hover_data=['count']
        )

        fig.update_layout(
            showlegend=True,
            height=600,
            font=dict(size=12)
        )

        # Save file
        if output_name is None:
            output_name = "timeline_chart"
        output_path = self.output_dir / f"{output_name}.html"
        fig.write_html(str(output_path))

        return str(output_path)

    def bar_chart_speaking_time(
        self,
        title: str = "Nombre d'Interventions par Personne",
        output_name: Optional[str] = None,
        format: Literal["png", "pdf", "html"] = "png"
    ) -> str:
        """
        Create a bar chart showing speaking frequency per person.

        Args:
            title: Chart title
            output_name: Output filename (without extension)
            format: Output format

        Returns:
            Path to the saved file
        """
        # Count interventions per person
        speaking_counts = self.data.groupby('speak_person').size().reset_index(name='count')
        speaking_counts = speaking_counts.sort_values('count', ascending=False)

        if format == "html":
            fig = px.bar(
                speaking_counts,
                x='speak_person',
                y='count',
                title=title,
                labels={'speak_person': 'Personne', 'count': 'Nombre d\'Interventions'},
                color='count',
                color_continuous_scale='Viridis'
            )

            if output_name is None:
                output_name = "bar_chart_speaking_time"
            output_path = self.output_dir / f"{output_name}.html"
            fig.write_html(str(output_path))
        else:
            fig, ax = plt.subplots(figsize=(12, 6))

            bars = ax.bar(speaking_counts['speak_person'], speaking_counts['count'])

            # Color bars with gradient
            colors = plt.cm.viridis(speaking_counts['count'] / speaking_counts['count'].max())
            for bar, color in zip(bars, colors):
                bar.set_color(color)

            ax.set_xlabel('Personne', fontsize=12)
            ax.set_ylabel('Nombre d\'Interventions', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            if output_name is None:
                output_name = "bar_chart_speaking_time"
            output_path = self.output_dir / f"{output_name}.{format}"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()

        return str(output_path)

    def distribution_plot(
        self,
        title: str = "Distribution des Interventions par Temps",
        output_name: Optional[str] = None,
        format: Literal["png", "pdf", "html"] = "png"
    ) -> str:
        """
        Create a distribution plot showing intervention patterns over time.

        Args:
            title: Chart title
            output_name: Output filename (without extension)
            format: Output format

        Returns:
            Path to the saved file
        """
        # Count interventions per time period
        time_counts = self.data.groupby('speak_time').size().reset_index(name='count')

        if format == "html":
            fig = px.line(
                time_counts,
                x='speak_time',
                y='count',
                title=title,
                labels={'speak_time': 'Temps', 'count': 'Nombre d\'Interventions'},
                markers=True
            )

            if output_name is None:
                output_name = "distribution_plot"
            output_path = self.output_dir / f"{output_name}.html"
            fig.write_html(str(output_path))
        else:
            fig, ax = plt.subplots(figsize=(12, 6))

            ax.plot(time_counts['speak_time'], time_counts['count'], marker='o', linewidth=2, markersize=8)
            ax.fill_between(time_counts['speak_time'], time_counts['count'], alpha=0.3)

            ax.set_xlabel('Temps', fontsize=12)
            ax.set_ylabel('Nombre d\'Interventions', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()

            if output_name is None:
                output_name = "distribution_plot"
            output_path = self.output_dir / f"{output_name}.{format}"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()

        return str(output_path)

    def heatmap_person_time(
        self,
        title: str = "Carte Thermique - Personne × Temps",
        output_name: Optional[str] = None,
        format: Literal["png", "pdf", "html"] = "png"
    ) -> str:
        """
        Create a heatmap showing intervention intensity per person over time.

        Args:
            title: Chart title
            output_name: Output filename (without extension)
            format: Output format

        Returns:
            Path to the saved file
        """
        # Create pivot table
        heatmap_data = self.data.groupby(['speak_person', 'speak_time']).size().reset_index(name='count')
        pivot_data = heatmap_data.pivot(index='speak_person', columns='speak_time', values='count').fillna(0)

        if format == "html":
            fig = px.imshow(
                pivot_data,
                title=title,
                labels=dict(x="Temps", y="Personne", color="Interventions"),
                color_continuous_scale="YlOrRd"
            )

            if output_name is None:
                output_name = "heatmap_person_time"
            output_path = self.output_dir / f"{output_name}.html"
            fig.write_html(str(output_path))
        else:
            fig, ax = plt.subplots(figsize=(14, 8))

            sns.heatmap(
                pivot_data,
                annot=True,
                fmt='.0f',
                cmap='YlOrRd',
                ax=ax,
                cbar_kws={'label': 'Nombre d\'Interventions'}
            )

            ax.set_xlabel('Temps', fontsize=12)
            ax.set_ylabel('Personne', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            plt.tight_layout()

            if output_name is None:
                output_name = "heatmap_person_time"
            output_path = self.output_dir / f"{output_name}.{format}"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()

        return str(output_path)
