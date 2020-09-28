import os
import time
import logging
import tornado.iostream
import uteslaclient

from modules.Infrastructure import client
from utils.General import parse_config
from utils.extra import netparse
from utils.extra import generate_hash
from utils.extra import create_pool
from utils.extra import create_translation

_ = create_translation.create(
    "change_passwd-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    user = args.user
    password = args.password
    new_password = args.new_password
    token_limit = args.token_limit
    time_cost = args.time_cost
    memory_cost = args.memory_cost
    parallelism = args.parallelism
    remote = args.remote
    network = args.network
    server_key = args.server_key
    public_key = args.public_key
    private_key = args.private_key

    if not (remote):
        config = parse_config.parse()

        server_conf = config["Server"]
        crypt_limits = config["Crypt Limits"]

        db = await create_pool.create(
            server_conf.get("mysql_db")

        )

        userid = await db.return_first_result("extract_userid", user)

        if (userid is None):
            logging.error(_("El usuario '%s' no existe"), user)
            return

        else:
            (userid,) = userid

        logging.warning(_("Cambiando contraseña del usuario: %s"), user)

        logging.debug(_("Generando hash..."))

        time_init = time.time()

        logging.debug(_("Generando hash..."))

        time_end = time.time()-time_init

        pass2hash = generate_hash.generate(
            new_password, time_cost, memory_cost, parallelism, crypt_limits

        )

        await db.return_first_result("change_password", pass2hash, userid)
        
        if (token_limit is not None):
            logging.warning(
                _("Cambiando el límite de token's permitidos para el usuario: %s (%d)"),
                user, userid
                
            )

            await db.return_first_result("change_token_limit", token_limit, userid)

        logging.info(_("Hecho."))

    else:
        if (password is None):
            logging.error(_("Es necesario definir la contraseña actual"))
            return

        if (network is None):
            logging.error(_("Es necesario definir la dirección de la red"))
            return

        try:
            (addr, port, path) = netparse.parse(network, default_path="/generate_token")

        except Exception as err:
            logging.error(_("La dirección '%s' no es válida: %s"), network, err)
            return

        if (server_key is None) or (public_key is None) or (private_key is None):
            logging.error(_("Se debe definir absolutamente todas las claves para poder continuar"))
            return

        if not (os.path.isfile(server_key)):
            logging.error(_("¡La clave pública del servidor no existe!"))
            return

        elif not (os.path.isfile(public_key)) or not (os.path.isfile(private_key)):
            logging.error(_("¡La clave pública o privada del usuario no existe!"))
            return

        else:
            with open(server_key, "rb") as fd:
                server_key = fd.read()

            with open(public_key, "rb") as fd:
                public_key = fd.read()

            with open(private_key, "rb") as fd:
                private_key = fd.read()

        try:
            (UControl, UClient, __) = await client.simple_client(
                addr,
                port,
                user,
                server_key,
                public_key = public_key,
                private_key = private_key,
                uteslaclient = uteslaclient.UTeslaClient()

            )
        
        except tornado.iostream.StreamClosedError as err:
            logging.error(
                _("Hubo un error conectado a %s:%d: %s"),
                addr, port, err
                
            )
            return

        UClient.set_stream_control(UControl)

        try:
            await UClient.change_passwd(
                password, new_password, token_limit, path

            )

        except tornado.iostream.StreamClosedError as err:
            logging.error(_("Hubo un error interpretando los datos: %s"), err)

            if (UControl.request.get_status_code() != 0) and (UControl.request.get_status_code() != -1):
                logging.error(_("Posible error: %s"), UControl.request.get_status())

        else:
            status = UControl.request.get_status()
            status_code = UControl.request.get_status_code()

            if (status is None) or (status_code == -1):
                logging.error(_("Error, no se definió correctamente el estado."))
                return

            if (status_code == 0):
                logging.info(_("Contraseña cambiada satisfactoriamente"))

            else:
                logging.warning(_("Se obtuvo un código de estado diferente a 0."))
                logging.warning(_("Código de estado: %d"), status_code)
                logging.warning(_("Estado: %s"), status)
