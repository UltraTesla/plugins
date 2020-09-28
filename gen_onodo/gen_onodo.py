import os
import re
import logging

# Workspace modules
import nodes2file
from nodes import Nodes

from utils.General import show_services
from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "gen_onodo",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    output = args.output.lower()
    local_machine_name = args.local_machine
    file_format = args.format
    list_formats = args.list

    if (list_formats):
        print("*", "xlsx")
        print("*", "csv")
        print("*", "dict")
        print("*", "html")
        print("*", "json")
        print("*", "latex")
        print("*", "markdown")
        print("*", "string")

    else:
        db = await create_pool.create()
        networks = db.execute_command("get_networks")
        services = show_services.show(sub_service=False, only_name=True)

        nodes = {
            "Name"        : Nodes(),
            "Type"        : []

        }
        relations = {
            "Source"      : [],
            "Type"        : [],
            "Target"      : []

        }

        logging.info(_("Generando '%s'..."), output)

        # Empezamos con la máquina local
        nodes["Name"].append(local_machine_name)
        nodes["Type"].append("Main")
        
        # Ahora con los servidores secundarios
        async for network in networks:
            (network,) = network

            network_name_tmp = nodes["Name"].append(network)
            nodes["Type"].append("Server")

            relations["Source"].append(network_name_tmp)
            relations["Type"].append("Server")
            relations["Target"].append(local_machine_name)

            networkid = await db.return_first_result("extract_networkid", network)

            if (networkid is None):
                logging.error(_("No se pudo obtener el identificador de red de '%s'"), network)
                return

            else:
                (networkid,) = networkid

            remote_services = db.execute_command("net2services", networkid)

            async for service in remote_services:
                (service,) = service

                # Agregamos los servicios como nodos
                service_name_tmp = nodes["Name"].append(service)
                nodes["Type"].append("Service")

                # Y ahora los relacionamos
                relations["Source"].append(service_name_tmp)
                relations["Type"].append("Service")
                relations["Target"].append(network_name_tmp)

        # Por último relacionamos los servicios locales
        for service in services:
            name_tmp = nodes["Name"].append(service)
            nodes["Type"].append("Service")
            
            relations["Source"].append(name_tmp)
            relations["Type"].append("Service")
            relations["Target"].append(local_machine_name)

        # Y escribimos :D
        try:
            if (file_format == "xlsx"):
                nodes2file.write_xlsx(output, nodes, relations)

            else:
                if (output == "stdout"):
                    output = None

                if (text := nodes2file.write(output, file_format, nodes, relations)):
                    print(text)

        except ImportError as err:
            logging.error(_("Ocurrió un error, probablemente se requiere una dependencia para pandas: %s"), err)

        else:
            logging.info(_("Hecho: %s"), output)
