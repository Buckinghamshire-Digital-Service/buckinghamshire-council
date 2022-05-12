def tableblock_to_typedtableblock(block):
    if not (block and block.get("value")):
        return {
            "type": "table",
            "value": {
                "caption": "",
                "table": {"columns": [], "rows": []},
            },
        }
    has_table_header = block["value"]["first_row_is_table_header"]
    new_rows = []
    new_columns = []
    if len(block["value"]["data"]) > 0:
        for row_index, row in enumerate(block["value"]["data"]):
            current_row = []
            if row_index == 0:
                for col_index, cell in enumerate(row):
                    new_columns.append(
                        {
                            "heading": cell if has_table_header else "",
                            "type": "rich_text",
                        }
                    )
                if has_table_header:
                    continue
            for col_index, cell in enumerate(row):
                # If column header, set as bold.
                if block["value"]["first_col_is_header"] and col_index == 0:
                    current_row.append(f'<p class="row-header"><b>{cell}</b></p>')
                else:
                    current_row.append(f"<p>{cell}</p>")
            new_rows.append({"values": current_row})
    return {
        "type": "table",
        "value": {
            "caption": block["value"]["table_caption"],
            "table": {"columns": new_columns, "rows": new_rows},
        },
    }
