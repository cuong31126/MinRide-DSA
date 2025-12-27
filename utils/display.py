# utils/display.py

def print_line(widths):
    print("+" + "+".join("-" * w for w in widths) + "+")


def print_row(values, widths):
    row = "|"
    for val, w in zip(values, widths):
        row += str(val).ljust(w) + "|"
    print(row)


def print_table(headers, rows):
    """
    headers: list[str]
    rows: list[list]
    """
    widths = [max(len(str(h)), 12) for h in headers]

    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)) + 2)

    print_line(widths)
    print_row(headers, widths)
    print_line(widths)

    for row in rows:
        print_row(row, widths)

    print_line(widths)
