from typing import Any


def to_table(data: dict[str, dict[str, Any]]) -> str:
    """
    Convert a nested dictionary to a markdown table.

    Args:
        data (dict[str, dict[str, Any]]): The nested dictionary to convert. The first level keys will be the row names, the second level keys will be the column names, and the values will be the cell values.

    Returns:
        str: A string containing the markdown table representation of the input data.
    """

    # Extract names
    rows = list(data.keys())
    cols = list(data[rows[0]].keys())
    max_row_len = max([ len(row) for row in rows ])

    # Create header
    table = "|" + " " * max_row_len + "|" + "|".join(cols) + "|\n"
    table += "|" + "-" * max_row_len + "|" + "|".join(["-" * len(col) for col in cols]) + "|\n"

    # Create rows
    for row in rows:
        table += "|" + row + " " * (max_row_len - len(row)) + "|"
        for col in cols:
            value = data[row][col]
            table += str(value) + " " * (len(col) - len(str(value))) + "|"
        table += "\n"

    return table