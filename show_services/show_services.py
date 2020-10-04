import os
import logging
import tornado.iostream
import table
import uteslaclient

from modules.Infrastructure import client
from modules.Infrastructure import dbConnector
from utils.extra import create_pool
from utils.extra import create_translation
from utils.extra import netparse

_ = create_translation.create(
    "show_services",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

async def MainParser(args):
    limit = args.limit
    only = args.only
    remote = args.remote
    network = args.network
    token = args.token
    username = args.username
    server_key = args.server_key
    public_key = args.public_key
    private_key = args.private_key
    n = 1

    if (remote):
        if (network is None):
            logging.error(_("Es necesario definir la dirección de la red"))
            return

        if (token is None):
            logging.error(_("Es necesario definir el token de acceso"))
            return

        if (username is None):
            logging.error(_("Es necesario definir el nombre de usuario"))
            return

        if (server_key is None):
            logging.error(_("Es necesario definir la clave pública del servidor"))
            return

        if (public_key is None):
            logging.error(_("Es necesario definir la clave pública del usuario"))
            return

        if (private_key is None):
            logging.error(_("Es necesario definir la clave privada del usuario"))
            return

        try:
            (addr, port, path) = netparse.parse(network, default_path="/get_services")

        except Exception as err:
            logging.error(_("La dirección '%s' no es válida: %s"), network, err)
            return

        try:
            (UControl, UClient, __) = await client.simple_client(
                addr,
                port,
                username,
                server_key.read(32),
                public_key = public_key.read(32),
                private_key = private_key.read(32),
                uteslaclient = uteslaclient.UTeslaClient()

            )
        
        except tornado.iostream.StreamClosedError as err:
            logging.error(_("Hubo un error conectado a %s:%d: %s"), addr, port, err)
            return

        UClient.set_stream_control(UControl)
        UControl.set_token(token)

        services = UClient.get_services(path)

        logging.warning(_("Obteniendo servicios..."))

        async for service in services:
            service_number = " %d " % (n)
            n += 1;

            headers = [
                _("Nombre del servicio"),
                _("Ruta de acceso")
                    
            ]

            values = [
                service, "%s:%d/%s" % (addr, port, service)
                    
            ]

            print(service_number.center(50, "="))

            table.print_table(headers, values)

        if (UControl.request.get_status_code() != -1) and (UControl.request.get_status_code() != 0):
            logging.error(_("Error obteniendo los servicios: %s"), UControl.request.get_status())

    else:
        db = await create_pool.create()
        services = db.execute_command("get_services",
            limit, only=only, basic=False
            
        )
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
