import numpy as np

def format_table(headers, columns, values, ruler='-'):
    printable_rows = []

    table = np.empty((len(values), len(columns)), dtype=object)

    for row, value in enumerate(values):
        table[row] = [str(getattr(value, column)) for column in columns]

    column_widths = [
        max(len(headers[col]), len(max(table[:, col], key=len)))
        for col in range(len(columns))]

    # print header
    printable_rows.append('  '.join([header.ljust(column_widths[col])
                    for col, header in enumerate(headers)]))

    printable_rows.append('  '.join(['-' * width for width in column_widths]))

    for row in table:
        printable_rows.append('  '.join([col.ljust(column_widths[idx])
                                         for idx, col in enumerate(row)]))

    return printable_rows
