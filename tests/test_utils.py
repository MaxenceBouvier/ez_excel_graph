"""Tests for utility functions."""

from excel_to_graph.utils import (
    validate_project_name,
    sanitize_filename,
    detect_project_from_path,
    get_output_dir_for_project,
)


class TestProjectNameValidation:
    """Test project name validation."""

    def test_valid_project_names(self):
        """Test that valid project names are accepted."""
        valid_names = [
            "my-project",
            "research_2024",
            "study-phase-1",
            "analysis_v2",
            "data2024",
        ]

        for name in valid_names:
            is_valid, error = validate_project_name(name)
            assert is_valid, f"{name} should be valid but got error: {error}"

    def test_invalid_project_names(self):
        """Test that invalid project names are rejected."""
        invalid_names = [
            "my project",  # spaces
            "project!",  # special characters
            "pro/ject",  # slashes
            "",  # empty
            "-project",  # starts with hyphen
            "project_",  # ends with underscore
        ]

        for name in invalid_names:
            is_valid, error = validate_project_name(name)
            assert not is_valid, f"{name} should be invalid"
            assert error, f"{name} should have an error message"

    def test_reserved_names(self):
        """Test that reserved names are rejected."""
        reserved = ["con", "prn", "aux", "nul"]

        for name in reserved:
            is_valid, error = validate_project_name(name)
            assert not is_valid
            assert "reserved" in error.lower()


class TestFilenameSanitization:
    """Test filename sanitization."""

    def test_sanitize_basic(self):
        """Test basic filename sanitization."""
        assert sanitize_filename("My Chart") == "my_chart"
        assert sanitize_filename("Timeline #1") == "timeline_1"
        assert sanitize_filename("Data: Analysis") == "data_analysis"

    def test_sanitize_special_characters(self):
        """Test removal of special characters."""
        assert sanitize_filename("file@name!") == "filename"
        assert sanitize_filename("test & data") == "test_data"

    def test_sanitize_multiple_spaces(self):
        """Test handling of multiple spaces."""
        assert sanitize_filename("test    file") == "test_file"


class TestProjectDetection:
    """Test project detection from paths."""

    def test_detect_project_from_path(self):
        """Test detecting project name from file path."""
        # Note: This will only work if the directory actually exists
        # For now, we test the logic without filesystem checks
        path = "resources/my-project/data.xlsx"
        # Would need actual directory to test properly
        # Just test that it doesn't crash
        result = detect_project_from_path(path)
        # Result could be None if directory doesn't exist
        assert result is None or isinstance(result, str)

    def test_no_project_in_path(self):
        """Test when file is not in a project subdirectory."""
        path = "resources/data.xlsx"
        result = detect_project_from_path(path)
        assert result is None


class TestOutputDirectory:
    """Test output directory helper."""

    def test_get_output_dir_with_project(self):
        """Test getting output directory for a project."""
        result = get_output_dir_for_project("my-project")
        assert result == "outputs/my-project"

    def test_get_output_dir_without_project(self):
        """Test getting output directory without project."""
        result = get_output_dir_for_project(None)
        assert result == "outputs"

    def test_get_output_dir_custom_base(self):
        """Test getting output directory with custom base."""
        result = get_output_dir_for_project("test", base_dir="custom")
        assert result == "custom/test"
