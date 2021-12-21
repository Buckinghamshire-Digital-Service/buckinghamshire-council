def typedtableblock_to_alignedtypedtableblock(block):
    if not (block and block.get("value")):
        return {
            "type": "table",
            "value": {"caption": "", "table": {"columns": [], "rows": []}},
        }

    new_columns = []
    new_rows = []
    column_types = [column["type"] for column in block["value"]["table"]["columns"]]

    for ind in range(len(block["value"]["table"]["columns"])):
        new_row_values = []
        for row in block["value"]["table"]["rows"]:
            new_row_values.append(
                {"type": column_types[ind], "value": row["values"][ind]}
            )
        new_rows.append(new_row_values)

    for column in block["value"]["table"]["columns"]:
        if column["type"] == "numeric":
            new_column_type = "right_aligned_column"
        else:
            new_column_type = "left_aligned_column"
        new_columns.append({"type": new_column_type, "heading": column["heading"]})

    return {
        "type": "table",
        "value": {
            "caption": block["value"]["caption"],
            "table": {"columns": new_columns, "rows": [{"values": new_rows}]},
        },
    }


def alignedtypedtableblock_to_typedtableblock(block):
    # this assumes that all cells of a single column will have same datatype,
    # and all columns have equals number of rows
    if not (block and block.get("value")):
        return {
            "type": "table",
            "value": {"caption": "", "table": {"columns": [], "rows": []}},
        }

    column_types = [
        row_value[0]["type"]
        for row_value in block["value"]["table"]["rows"][0]["values"]
    ]

    new_columns = []
    new_rows = []

    for ind, column in enumerate(block["value"]["table"]["columns"]):
        new_columns.append({"type": column_types[ind], "heading": column["heading"]})

    for ind in range(len(block["value"]["table"]["rows"][0]["values"][0])):
        new_row_values = []
        for row in block["value"]["table"]["rows"][0]["values"]:
            # here row is the values in each column
            new_row_values.append(row[ind]["value"])
        new_rows.append({"values": new_row_values})

    return {
        "type": "table",
        "value": {
            "caption": block["value"]["caption"],
            "table": {"columns": new_columns, "rows": new_rows},
        },
    }
