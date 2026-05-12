from __future__ import annotations

import pandas as pd


def dataframe_to_markdown(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    headers = list(frame.columns)
    rows = frame.astype(str).values.tolist()
    widths = [max(len(header), *(len(row[index]) for row in rows)) for index, header in enumerate(headers)]
    header_line = "| " + " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)) + " |"
    divider = "| " + " | ".join("-" * widths[index] for index in range(len(headers))) + " |"
    body = ["| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(headers))) + " |" for row in rows]
    return "\n".join([header_line, divider, *body])
