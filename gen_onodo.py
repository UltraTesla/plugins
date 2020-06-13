import zipfile
import defusedxml.minidom
import re
import logging
import random
import time
import copy

from utils.General import show_complements
from utils.extra import create_pool

information = {
    'description' : 'Crear un gráfico que representa a la red junto a sus nodos',
    'commands'    : [
        {
            'positionals' : [
                {
                    'args'     : ('output',),
                    'help'     : 'El nombre del archivo .xlsx que representará la red'

                }

            ]

        },

        {
            'optionals'   : [
                {
                    'args'     : ('-a', '--author'),
                    'help'     : 'Cambiar el autor de la hoja de cálculo. Sólo se aceptarán '
                                 'letras y números',
                    'default'  : 'UTesla'

                }

            ]
    

        }

    ],
    'version'     : '1.0.0'

}

def generate_random_int(string):
    return random.random() + 5 + len(string)

async def MainParser(args):
    output = args.output
    workspace = information['workspaces'][0]
    regex = re.match(r'[a-zA-Z0-9]', args.author)

    logging.info('Generando "%s"...', output)

    if not (regex):
        raise ValueError('El nombre del autor es inaceptable')

    author = args.author[regex.start():regex.end()]

    db = await create_pool.create()
    networks = await db.get_networks()
    aux = list(show_complements.show(False).keys())
    nodes2add = [(x, 'Service') for x in aux]
    local_services = copy.copy(aux)
    local_machine_name = '&lt;Local Machine&gt;'
    k = 2
    tracked = {}
    nod_column = []
    rel_column = []

    column_template = '<col min="%(n_node)d" max="%(n_node)d" bestFit="1" customWidth="1" width="%(width)f" />'

    with open('%s/xl/worksheets/sheet1.xml' % (workspace), 'r') as fd:
        xml_nodes_main = fd.read()

    with open('%s/xl/worksheets/sheet2.xml' % (workspace), 'r') as fd:
        xml_relations_main = fd.read()

    with open('%s/docProps/core.xml' % (workspace), 'r') as fd:
        xml_core_main = fd.read()

    nodes = ['<row r="1">'
             '<c r="A1" s="3" t="inlineStr">'
             '<is><t>Name</t></is>'
             '</c>'
             '<c r="B1" s="3" t="inlineStr">'
             '<is><t>Type</t></is>'
             '</c>'
             '<c r="C1" s="3" t="inlineStr">'
             '<is><t>Description</t></is>'
             '</c>'
             '<c r="D1" s="3" t="inlineStr">'
             '<is><t>Visible</t></is>'
             '</c>'
             '</row>']

    relations = ['<row r="1">'
		 '<c r="A1" s="3" t="inlineStr">'
		 '<is><t>Source</t></is>'
                 '</c>'
                 '<c r="B1" s="3" t="inlineStr">'
                 '<is><t>Type</t></is>'
                 '</c>'
                 '<c r="C1" s="3" t="inlineStr">'
                 '<is><t>Target</t></is>'
                 '</c>'
                 '<c r="D1" s="3" t="inlineStr">'
                 '<is><t>Directed</t></is>'
                 '</c>'
                 '<c r="E1" s="3" t="inlineStr">'
                 '<is><t>At</t></is>'
                 '</c>'
                 '<c r="F1" s="3" t="inlineStr">'
                 '<is><t>From</t></is>'
                 '</c>'
                 '<c r="G1" s="3" t="inlineStr">'
                 '<is><t>To</t></is>'
                 '</c>'
		'</row>']

    node_template = '<row r="%(n_node)d">' \
                    '<c r="A%(n_node)d" s="0" t="inlineStr">' \
                    '<is><t>%(node)s</t></is>' \
                    '</c>' \
                    '<c r="B%(n_node)d" s="0" t="inlineStr">' \
                    '<is><t>%(node_type)s</t></is>' \
                    '</c>' \
                    '<c r="C%(n_node)d" s="0"/>' \
                    '<c r="D%(n_node)d" s="0"/>' \
                    '</row>'

    relation_template = '<row r="%(n_node)d">' \
                        '<c r="A%(n_node)d" s="0" t="inlineStr">' \
                        '<is><t>%(nodefrom)s</t></is>' \
                        '</c>' \
                        '<c r="B%(n_node)d" s="0" t="inlineStr">' \
                        '<is><t>%(node_type)s</t></is>' \
                        '</c>' \
                        '<c r="C%(n_node)d" s="0" t="inlineStr">' \
                        '<is><t>%(nodeto)s</t></is>' \
                        '</c>' \
                        '<c r="D%(n_node)d" s="0"/>' \
                        '<c r="E%(n_node)d" s="0"/>' \
                        '<c r="F%(n_node)d" s="0"/>' \
                        '<c r="G%(n_node)d" s="0"/>' \
                        '</row>'

    def rename_node(node, type, add=True):
        node_format = (node, type)
        if (add):
            aux.append(node)

        if (node in aux):
            node = '%s (%d)' % (node, aux.count(node)-1)
            node_format = (node, type)

        return node_format

    def addnode(node, type, add=True):
        node_format = rename_node(node, type, add)

        nodes2add.append(node_format)

        return node_format[0]

    def add_rel_column(n_node, service):
        rel_column.append(
            column_template % {
                'n_node' : n_node,
                'width'  : generate_random_int(service)

            }

        )

    for _ in networks:
        network = _[0]
        networkid = await db.extract_networkid(network)

        services = await db.url2services(networkid)

        tracked[network] = []

        addnode(network, 'Network', False)

        for _ in services:
            service = addnode(_[0], 'Service')

            tracked[network].append(service)

    tracked[local_machine_name] = local_services + list(tracked.keys())
    addnode(local_machine_name, 'Main', False)

    for n, (node, node_type) in enumerate(nodes2add, 2):
        nod_column.append(
            column_template % {
                'n_node' : n,
                'width'  : generate_random_int(node)

            }

        )

        nodes.append(
            node_template % {
                'node'      : node,
                'node_type' : node_type,
                'n_node'    : n

            }

        )

    for network, services in tracked.items():
        for service in services:
            if (service == local_machine_name):
                node_type = 'El centro de esta red'

            elif (service in tracked):
                node_type = 'Proporciona sus servicios'

            else:
                node_type = 'Servicio'

            add_rel_column(k, service)

            relations.append(
                relation_template % {
                    'nodefrom'  : service,
                    'nodeto'    : network,
                    'n_node'    : k,
                    'node_type' : node_type

                }

            )

            k += 1

    xml_nodes_output = xml_nodes_main % {
        'nodes_column' : ''.join(nod_column),
        'nodes'        : ''.join(nodes)

    }

    xml_relations_output = xml_relations_main % {
        'relation_column' : ''.join(rel_column),
        'relations'       : ''.join(relations)

    }

    xml_core_output = xml_core_main % {
        'author'   : author,
        'datetime' : time.strftime('%Y-%m-%dT%H-%M-%SZ')

    }

    xml_nodes_parsed = defusedxml.minidom.parseString(
        xml_nodes_output.replace('\n', '').replace('\t', '')

    ).toprettyxml()
    xml_relations_parsed = defusedxml.minidom.parseString(
        xml_relations_output.replace('\n', '').replace('\t', '')

    ).toprettyxml()
    xml_core_parsed = defusedxml.minidom.parseString(
        xml_core_output.replace('\n', '').replace('\t', '')

    ).toprettyxml()

    files = [
        '_rels/.rels',
        '[Content_Types].xml',
        'docProps/app.xml',
        'xl/_rels/workbook.xml.rels',
        'xl/styles.xml',
        'xl/workbook.xml',
        'xl/worksheets/_rels/sheet1.xml.rels',
        'xl/worksheets/_rels/sheet2.xml.rels'

    ]

    with zipfile.ZipFile(output, 'w') as fd:
        for file in files:
            filename = '%s/%s' % (
                workspace, file

            )
            
            with open(filename, 'r') as file_fd:
                fd.writestr(file, file_fd.read())

        fd.writestr('xl/worksheets/sheet1.xml', xml_nodes_parsed)
        fd.writestr('xl/worksheets/sheet2.xml', xml_relations_parsed)
        fd.writestr('docProps/core.xml', xml_core_parsed)

    logging.info('Hecho.')
