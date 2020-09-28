import os
import logging
import table

from modules.Infrastructure import dbConnector
from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "show_services",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    limit = args.limit
    only = args.only

    db = await create_pool.create()
    services = db.execute_command("get_services",
        limit, only=only, basic=False
        
    )
    n = 1
    init = False

    async for id_service, id_network, service, priority in services:
        if not (init):
            init = True

        headers = [       
            _("Identificador"),
            _("Le pertenece a"),
            _("Nombre del servicio"),
            _("Prioridad")
                
        ]

        (network,) = await db.return_first_result("id2network", id_network)

        values = [
            id_service, "%d (%s)" % (id_network, network), service, priority
                
        ]

        service_number = " %d " % (n)
        n += 1

        print(service_number.center(50, "="))

        table.print_table(headers, values)

    if only is not None and not init:
        logging.error(_("No se pudo encontrar ningún servicio que le pertenezca al nodo '%d'"), only)

    elif not (init):
        print(_("Aún no hay servicios registrados :-("))
