import os
import logging
import tornado.iostream
import uteslaclient

from modules.Infrastructure import client
from modules.Infrastructure import options
from utils.extra import netparse
from utils.extra import create_translation

_ = create_translation.create(
    "renew",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    network = args.network
    token = args.token
    username = args.username
    password = args.password
    server_key = args.server_key
    public_key = args.public_key
    private_key = args.private_key

    try:
        (addr, port, path) = netparse.parse(network, default_path="/generate_token")

    except Exception as err:
        logging.error(_("La dirección '%s' no es válida: %s"), network, err)
        return

    try:
        (UControl, UClient, __) = await client.simple_client(
            addr,
            port,
            username,
            server_key.read(options.KEY_LENGTH),
            public_key = public_key.read(options.KEY_LENGTH),
            private_key = private_key.read(options.KEY_LENGTH),
            uteslaclient = uteslaclient.UTeslaClient()

        )
    
    except tornado.iostream.StreamClosedError as err:
        logging.error(_("Hubo un error conectado a %s:%d: %s"), addr, port, err)
        return

    else:
        UClient.set_stream_control(UControl)
        UControl.set_token(token)

    try:
        token = await UClient.renew_token(password, path)

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
            print(_("Nuevo Token:"), token)

        else:
            logging.warning(_("Se obtuvo un código de estado diferente a 0."))
            logging.warning(_("Código de estado: %d"), status_code)
            logging.warning(_("Estado: %s"), status)
