import os
import logging

from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "set_priority",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    identificator = args.identificator
    priority = args.priority
    only_networks = args.only_networks

    db = await create_pool.create()

    logging.debug(_("Cambiando prioridad del identificador '%d'"), identificator)

    if (only_networks):
        exists = await db.return_first_result("is_network_exists_for_id", identificator)

    else:
        exists = await db.return_first_result("is_service_exists_for_id", identificator)

    if not (exists):
        logging.error(_("¡El identificador '%d' no existe!"), identificator)
        return

    await db.return_first_result("set_priority",
        identificator, priority, only_networks=only_networks
            
    )

    logging.debug(_("Hecho."))
