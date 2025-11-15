"""
Statistical analysis module for excel_to_graph.

Provides advanced statistical analysis capabilities for social science research,
including ANOVA, correlations, t-tests, and more.
"""

import warnings
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr, chi2_contingency, shapiro
import matplotlib.pyplot as plt
import seaborn as sns

# Configure matplotlib for international characters
plt.rcParams["font.family"] = "DejaVu Sans"

# Suppress future warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)


class StatisticalAnalyzer:
    """
    Performs statistical analyses on DataFrame data.

    Designed for social science researchers who need common statistical tests
    like ANOVA, correlations, t-tests, and chi-square tests.
    """

    def __init__(self, data: pd.DataFrame, output_dir: str | Path = "outputs/analyses"):
        """
        Initialize the analyzer with data.

        Args:
            data: DataFrame to analyze
            output_dir: Directory to save analysis reports and plots
        """
        self.data = data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for organization
        (self.output_dir / "reports").mkdir(exist_ok=True)
        (self.output_dir / "plots").mkdir(exist_ok=True)

    def describe(self, columns: list[str] | None = None) -> dict[str, Any]:
        """
        Get descriptive statistics for specified columns or all numeric columns.

        Args:
            columns: List of column names to describe (default: all numeric)

        Returns:
            Dictionary with descriptive statistics
        """
        if columns:
            subset = self.data[columns]
        else:
            subset = self.data.select_dtypes(include=[np.number])

        stats_dict = {
            "count": subset.count().to_dict(),
            "mean": subset.mean().to_dict(),
            "std": subset.std().to_dict(),
            "min": subset.min().to_dict(),
            "25%": subset.quantile(0.25).to_dict(),
            "50%": subset.median().to_dict(),
            "75%": subset.quantile(0.75).to_dict(),
            "max": subset.max().to_dict(),
        }

        return stats_dict

    def correlation_analysis(
        self,
        columns: list[str] | None = None,
        method: str = "pearson",
        save_plot: bool = True,
    ) -> dict[str, Any]:
        """
        Perform correlation analysis between variables.

        Args:
            columns: Columns to correlate (default: all numeric)
            method: 'pearson' or 'spearman'
            save_plot: Whether to save a correlation heatmap

        Returns:
            Dictionary with correlation matrix and p-values
        """
        if columns:
            subset = self.data[columns]
        else:
            subset = self.data.select_dtypes(include=[np.number])

        if subset.shape[1] < 2:
            raise ValueError("Need at least 2 numeric columns for correlation analysis")

        # Calculate correlation matrix
        if method == "pearson":
            corr_matrix = subset.corr(method="pearson")
        elif method == "spearman":
            corr_matrix = subset.corr(method="spearman")
        else:
            raise ValueError(f"Unknown correlation method: {method}")

        # Calculate p-values
        p_values = pd.DataFrame(
            np.zeros_like(corr_matrix), columns=corr_matrix.columns, index=corr_matrix.index
        )

        for i, col1 in enumerate(subset.columns):
            for j, col2 in enumerate(subset.columns):
                if i != j:
                    # Drop NaN values jointly to keep arrays aligned
                    valid_data = subset[[col1, col2]].dropna()
                    if len(valid_data) > 2:  # Need at least 3 points for correlation
                        if method == "pearson":
                            _, p = pearsonr(valid_data[col1], valid_data[col2])
                        else:
                            _, p = spearmanr(valid_data[col1], valid_data[col2])
                        p_values.iloc[i, j] = p
                    else:
                        p_values.iloc[i, j] = np.nan

        # Create heatmap
        if save_plot:
            plt.figure(figsize=(10, 8))
            sns.heatmap(
                corr_matrix,
                annot=True,
                cmap="coolwarm",
                center=0,
                vmin=-1,
                vmax=1,
                fmt=".2f",
                square=True,
            )
            plt.title(f"{method.capitalize()} Correlation Matrix")
            plt.tight_layout()

            plot_path = self.output_dir / "plots" / f"correlation_{method}.png"
            plt.savefig(plot_path, dpi=300, bbox_inches="tight")
            plt.close()

        return {
            "method": method,
            "correlation_matrix": corr_matrix.to_dict(),
            "p_values": p_values.to_dict(),
            "plot_path": str(plot_path) if save_plot else None,
        }

    def t_test(
        self,
        group_column: str,
        value_column: str,
        group1: Any = None,
        group2: Any = None,
    ) -> dict[str, Any]:
        """
        Perform independent samples t-test between two groups.

        Args:
            group_column: Column containing group labels
            value_column: Column containing values to compare
            group1: First group value (default: first unique value)
            group2: Second group value (default: second unique value)

        Returns:
            Dictionary with t-test results
        """
        groups = self.data[group_column].unique()

        if group1 is None:
            group1 = groups[0]
        if group2 is None:
            group2 = groups[1] if len(groups) > 1 else groups[0]

        data1 = self.data[self.data[group_column] == group1][value_column].dropna()
        data2 = self.data[self.data[group_column] == group2][value_column].dropna()

        # Perform t-test
        t_stat, p_value = stats.ttest_ind(data1, data2)

        # Check normality assumption
        _, p_norm1 = shapiro(data1) if len(data1) > 3 else (None, None)
        _, p_norm2 = shapiro(data2) if len(data2) > 3 else (None, None)

        return {
            "group1": str(group1),
            "group2": str(group2),
            "group1_mean": float(data1.mean()),
            "group1_std": float(data1.std()),
            "group1_n": int(len(data1)),
            "group2_mean": float(data2.mean()),
            "group2_std": float(data2.std()),
            "group2_n": int(len(data2)),
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "significant_at_0.05": p_value < 0.05,
            "normality_group1_p": float(p_norm1) if p_norm1 is not None else None,
            "normality_group2_p": float(p_norm2) if p_norm2 is not None else None,
        }

    def anova(self, group_column: str, value_column: str, posthoc: bool = False) -> dict[str, Any]:
        """
        Perform one-way ANOVA to compare means across multiple groups.

        Args:
            group_column: Column containing group labels
            value_column: Column containing values to compare
            posthoc: Whether to perform post-hoc pairwise comparisons

        Returns:
            Dictionary with ANOVA results
        """
        groups = self.data[group_column].unique()

        if len(groups) < 2:
            raise ValueError("Need at least 2 groups for ANOVA")

        # Prepare data for each group
        group_data = [
            self.data[self.data[group_column] == group][value_column].dropna() for group in groups
        ]

        # Perform one-way ANOVA
        f_stat, p_value = stats.f_oneway(*group_data)

        result = {
            "groups": [str(g) for g in groups],
            "group_means": {
                str(groups[i]): float(data.mean()) for i, data in enumerate(group_data)
            },
            "group_stds": {str(groups[i]): float(data.std()) for i, data in enumerate(group_data)},
            "group_ns": {str(groups[i]): int(len(data)) for i, data in enumerate(group_data)},
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "significant_at_0.05": p_value < 0.05,
        }

        # Post-hoc pairwise t-tests (Bonferroni correction)
        if posthoc and p_value < 0.05:
            pairwise = {}
            n_comparisons = len(groups) * (len(groups) - 1) / 2
            alpha_corrected = 0.05 / n_comparisons  # Bonferroni correction

            for i, group1 in enumerate(groups):
                for group2 in groups[i + 1 :]:
                    data1 = self.data[self.data[group_column] == group1][value_column].dropna()
                    data2 = self.data[self.data[group_column] == group2][value_column].dropna()
                    t_stat, p_val = stats.ttest_ind(data1, data2)

                    pair_key = f"{group1}_vs_{group2}"
                    pairwise[pair_key] = {
                        "t_statistic": float(t_stat),
                        "p_value": float(p_val),
                        "significant_bonferroni": p_val < alpha_corrected,
                    }

            result["posthoc_pairwise"] = pairwise
            result["bonferroni_alpha"] = alpha_corrected

        return result

    def chi_square_test(self, column1: str, column2: str) -> dict[str, Any]:
        """
        Perform chi-square test of independence between two categorical variables.

        Args:
            column1: First categorical column
            column2: Second categorical column

        Returns:
            Dictionary with chi-square test results
        """
        # Create contingency table
        contingency = pd.crosstab(self.data[column1], self.data[column2])

        # Perform chi-square test
        chi2, p_value, dof, expected = chi2_contingency(contingency)

        return {
            "column1": column1,
            "column2": column2,
            "contingency_table": contingency.to_dict(),
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "significant_at_0.05": p_value < 0.05,
            "expected_frequencies": pd.DataFrame(
                expected, index=contingency.index, columns=contingency.columns
            ).to_dict(),
        }

    def normality_test(self, column: str) -> dict[str, Any]:
        """
        Test if a variable follows a normal distribution using Shapiro-Wilk test.

        Args:
            column: Column name to test

        Returns:
            Dictionary with normality test results
        """
        data = self.data[column].dropna()

        if len(data) < 3:
            raise ValueError("Need at least 3 observations for normality test")

        # Shapiro-Wilk test
        stat, p_value = shapiro(data)

        return {
            "column": column,
            "n": int(len(data)),
            "shapiro_statistic": float(stat),
            "p_value": float(p_value),
            "normally_distributed_at_0.05": p_value >= 0.05,
            "interpretation": (
                "Data appears normally distributed"
                if p_value >= 0.05
                else "Data deviates from normal distribution"
            ),
        }

    def save_report(
        self, results: dict[str, Any], filename: str, title: str = "Statistical Analysis"
    ) -> Path:
        """
        Save analysis results to a formatted text report.

        Args:
            results: Dictionary of analysis results
            filename: Output filename (without extension)
            title: Report title

        Returns:
            Path to saved report
        """
        report_path = self.output_dir / "reports" / f"{filename}.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"{title}\n")
            f.write("=" * 80 + "\n\n")

            self._write_dict_recursive(f, results)

        return report_path

    def _write_dict_recursive(self, f, data: dict[str, Any], indent: int = 0):
        """Helper to recursively write dictionary to file."""
        for key, value in data.items():
            if isinstance(value, dict):
                f.write("  " * indent + f"{key}:\n")
                self._write_dict_recursive(f, value, indent + 1)
            elif isinstance(value, (list, tuple)):
                f.write("  " * indent + f"{key}: {', '.join(map(str, value))}\n")
            else:
                f.write("  " * indent + f"{key}: {value}\n")
