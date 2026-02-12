"""Utility functions for file operations and data validation."""

import csv
import json
from pathlib import Path
from typing import Any


def read_json_file(path: str) -> dict:
    """Read and parse JSON files.

    Args:
        path: Path to the JSON file.

    Returns:
        Dictionary containing the JSON data.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def write_json_file(path: str, data: dict) -> None:
    """Write data to JSON files.

    Args:
        path: Path where the JSON file will be written.
        data: Dictionary to write to the JSON file.

    Raises:
        OSError: If the file cannot be written.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def read_csv_file(path: str) -> list[dict[str, Any]]:
    """Read CSV files and return list of dictionaries.

    Args:
        path: Path to the CSV file.

    Returns:
        List of dictionaries. Each dictionary represents a row.

    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv_file(path: str, data: list[dict[str, Any]]) -> None:
    """Write list of dictionaries to CSV.

    Args:
        path: Path where the CSV file will be written.
        data: List of dictionaries to write to the CSV file.
              The first dictionary's keys will be used as column headers.

    Raises:
        OSError: If the file cannot be written.
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("Cannot write empty data to CSV file")

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = data[0].keys()

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def append_csv_file(path: str, data: list[dict[str, Any]]) -> None:
    """Append data to an existing CSV file or create a new one."""
    if not data:
        return

    file_path = Path(path)
    file_exists = file_path.exists()
    fieldnames = data[0].keys()

    # Use "a" for append
    with open(file_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Write the header only if the file is new
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)


def validate_amount(amount: float) -> bool:
    """Validate that amount is positive.

    Args:
        amount: The amount to validate.

    Returns:
        True if amount is positive, False otherwise.
    """
    return amount > 0
