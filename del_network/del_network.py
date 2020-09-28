import os
import logging
import hashlib

from utils.General import parse_config
from utils.extra import create_pool
from utils.extra import netparse
from utils.extra import create_translation

_ = create_translation.create(
    "del_network",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    try:
        (network, port, __) = netparse.parse(args.network)

    except Exception as err:
        logging.error(_("La dirección '%s' no es válida: %s"), args.network, err)
        return

    net = "%s:%d" % (network, port)

    server_conf = parse_config.parse()["Server"]

    db = await create_pool.create(server_conf.get("mysql_db"))

    logging.warning(_("Borrando red '%s' :-("), net)

    networkid = await db.return_first_result("extract_networkid", net)

    if (networkid is None):
        logging.error(_("La red no existe"))
        return

    else:
        (networkid,) = networkid

    await db.return_first_result("delete_network", networkid)

    public_key_dst = "%s/servkeys/%s" % (
        server_conf.get("init_path"), hashlib.sha3_224(net.encode()).hexdigest()

    )

    logging.debug(_("Borrando clave pública: %s"), public_key_dst)

    if (os.path.isfile(public_key_dst)):
        os.remove(public_key_dst)

    else:
        logging.warning(_("No se pudo eliminar la clave pública porque no existe"))

    logging.info(_("Red '%s' eliminada."), network)
