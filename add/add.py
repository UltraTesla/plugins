import logging
import hashlib
import time
import shutil
import os
import pymysql

from utils.General import parse_config

from utils.extra import generate_hash
from utils.extra import create_pool
from utils.extra import create_translation

from config import defaults

_ = create_translation.create(
    "add",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    user = args.user
    password = args.password
    token_limit = args.token_limit
    public_key = args.import_public_key
    overwrite = args.overwrite
    time_cost = args.time_cost
    memory_cost = args.memory_cost
    parallelism = args.parallelism
    guest_user = args.guest_user

    if (len(user) > defaults.user_length):
        logging.error(_("La longitud del nombre de usuario es muy larga para poder continuar"))
        return

    config = parse_config.parse()
    
    server_conf = config["Server"]
    crypt_limits = config["Crypt Limits"]

    db = await create_pool.create(
        server_conf.get("mysql_db")

    )

    userid = await db.return_first_result("extract_userid", user)

    if (userid is not None):
        logging.error(_("El usuario '%s' ya existe"), user)
        return

    logging.info(_("Creando usuario: %s"), user)

    user_hash = hashlib.sha3_224(user.encode()).hexdigest()

    public_key_dst = os.path.join(
        server_conf.get("init_path"),
        server_conf.get("user_data"),
        user_hash
            
    )

    time_init = time.time()

    logging.debug(_("Generando hash..."))

    time_end = time.time()-time_init

    pass2hash = generate_hash.generate(
        password, time_cost, memory_cost, parallelism, crypt_limits

    )

    logging.debug(_("Copiando clave pública '%s' a '%s'"),
        public_key, public_key_dst

    )

    if not (os.path.isfile(public_key)):
        logging.error(_("La clave pública de origen '%s' no existe"), public_key)
        return

    if (os.path.isfile(public_key_dst)) and not (overwrite):
        logging.error(_("¡La clave pública '%s' ya existe!"), public_key_dst)
        return

    logging.debug(
        _("Creando nuevo usuario: Username=%s, Password=%s, Token-Limit=%d, Guest=%i"),
        user, len(password)*"*", token_limit, guest_user

    )

    try:
        await db.return_first_result("insert_user",
            user, pass2hash, token_limit, guest_user
            
        )

    except pymysql.err.IntegrityError as err:
        logging.error(_("Ocurrió un error agregando al usuario %s: %s"), user, err)

    else:
        shutil.copy(public_key, public_key_dst)

        logging.info(_("Se creó con éxito: %s"), user)
