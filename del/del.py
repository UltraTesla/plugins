import logging
import os
import hashlib

from utils.General import parse_config

from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "del",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    user = args.user

    server_conf = parse_config.parse()["Server"]

    db = await create_pool.create(server_conf.get("mysql_db"))

    logging.warning(_("Borrando usuario '%s' :-("), user)

    userid = await db.return_first_result("extract_userid", user)

    if (userid is None):
        logging.error(_("El usuario no existe"))
        return

    else:
        (userid,) = userid

    await db.return_first_result("delete_user", userid)

    public_key_dst = "%s/pubkeys/%s" % (
        server_conf.get("init_path"), hashlib.sha3_224(user.encode()).hexdigest()

    )

    logging.debug(_("Borrando clave pública: %s"), public_key_dst)

    if (os.path.isfile(public_key_dst)):
        os.remove(public_key_dst)

    else:
        logging.warning(_("No se pudo eliminar la clave pública porque no existe"))

    logging.info(_("Usuario '%s' eliminado."), user)
