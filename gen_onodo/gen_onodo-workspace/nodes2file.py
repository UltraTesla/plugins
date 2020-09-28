import os
import logging
import pandas
from utils.extra import create_translation

_ = create_translation.create(
    "nodes2file",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

def write_xlsx(filename, nodes, relations):
    df_nodes = pandas.DataFrame(nodes)
    df_relations = pandas.DataFrame(relations)

    writer = pandas.ExcelWriter(filename, engine="xlsxwriter")

    df_nodes.to_excel(writer, index=False, sheet_name="Nodes")
    df_relations.to_excel(writer, index=False, sheet_name="Relations")

    writer.save()

def write(output, format, nodes, relations):
    df = pandas.DataFrame(
        {
            "nodes"     : nodes,
            "relations" : relations

        }

    )

    if (output is not None) and (format in ("dict", "markdown")):
        logging.warning(_("No se puede guardar el resultado como un archivo usando este formato"))

    if (format == "csv"):
        return df.to_csv(output)

    elif (format == "dict"):
        return df.to_dict()

    elif (format == "html"):
        return df.to_html(output)

    elif (format == "json"):
        return df.to_json(output)

    elif (format == "latex"):
        return df.to_latex(output)

    elif (format == "markdown"):
        return df.to_markdown()

    elif (format == "string"):
        return df.to_string(output)

    else:
        raise ValueError(_("El formato es irreconocible"))
