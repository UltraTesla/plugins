import os
import logging
import hashlib
import table

from utils.General import parse_config
from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "show",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    show_limit = args.limit

    server_conf = parse_config.parse()["Server"]
    init_path = server_conf["init_path"]
    user_data = server_conf["user_data"]

    db = await create_pool.create()
    users = db.execute_command("show_users", show_limit)
    n = 1
    init = False

    async for userid, username, token_limit, guest_user in users:
        if not (init):
            init = True

        headers = [
            _("Identificador"),
            _("Nombre de usuario"),
            _("Límite de tokens"),
            _("¿Es invitado?")
            
        ]
        values = [userid, username, token_limit, guest_user]        

        user_number = " %d " % (n)
        n += 1

        pubkey = os.path.join(init_path, user_data, hashlib.sha3_224(username.encode()).hexdigest())

        print(user_number.center(50, "="))

        if (os.path.isfile(pubkey)):
            headers.append(_("Clave pública"))
            values.append(pubkey)

        else:
            logging.warning(_("No se encuentra la clave pública de %s"), username)

        table.print_table(headers, values)

    if not (init):
        print(_("Aún no hay usuarios registrados :-("))
