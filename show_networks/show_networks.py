import os
import hashlib
import table

from utils.General import parse_config
from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "show_networks",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    show_limit = args.limit

    server_conf = parse_config.parse()["Server"]
    init_path = server_conf["init_path"]
    server_data = server_conf["server_data"]

    db = await create_pool.create()
    networks = db.execute_command("get_networks", show_limit, use_options=True)
    n = 1
    init = False

    async for networkid, network, token in networks:
        if not (init):
            init = True

        headers = [
            _("Identificador"),
            _("Dirección de red"),
            _("Token")
            
        ]
        values = [networkid, network, token]

        network_number = " %d " % (n)
        n += 1

        pubkey = os.path.join(
            init_path, server_data, hashlib.sha3_224(network.encode()).hexdigest()
                
        )

        print(network_number.center(50, "="))

        if (os.path.isfile(pubkey)):
            headers.append(_("Clave pública"))
            values.append(pubkey)

        else:
            logging.warning(_("No se encuentra la clave pública de %s"), network)

        table.print_table(headers, values)

    if not (init):
        print(_("Aún no hay redes registradas :-("))
