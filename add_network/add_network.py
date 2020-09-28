import logging
import os
import hashlib
import shutil
import tornado.iostream
import array_strip
import uteslaclient

from modules.Infrastructure import client

from utils.General import parse_config

from utils.extra import create_pool
from utils.extra import netparse
from utils.extra import create_translation

async def MainParser(args):
    _ = create_translation.create(
        "add_network",
        os.getenv("UTESLA_LOCALES_PLUGINS") or \
        "modules/Cmd/locales-shared"
        
    )
    network = args.network
    token = args.token
    username = args.username
    server_key = args.server_key
    public_key = args.import_public_key
    private_key = args.import_private_key
    only = array_strip.strip(args.only)
    exclude = array_strip.strip(args.exclude)
    priority = args.priority

    if not (os.path.isfile(server_key)):
        logging.error(_("¡La clave pública del servidor no existe!"))
        return

    elif not (os.path.isfile(public_key)) or not (os.path.isfile(private_key)):
        logging.error(_("¡La clave pública o privada del usuario no existe!"))
        return

    else:
        with open(server_key, "rb") as fd:
            server_key_data = fd.read()

        with open(public_key, "rb") as fd:
            public_key_data = fd.read()

        with open(private_key, "rb") as fd:
            private_key_data = fd.read()

    config = parse_config.parse()
    server_conf = config.get("Server")

    try:
        (addr, port, path) = netparse.parse(network, default_path="/get_services")

    except Exception as err:
        logging.error(_("La dirección '%s' no es válida: %s"), network, err)
        return

    net = "%s:%d" % (addr, port)
    net_hash = hashlib.sha3_224(
        net.encode()
    ).hexdigest()
    db = await create_pool.create(
        server_conf.get("mysql_db")

    )
    init_path = server_conf.get("init_path")
    server_key_dst = "%s/servkeys/%s" % (
        init_path, net_hash

    )
    service_path = server_conf["services"]
    networkid = await db.return_first_result("extract_networkid", net)

    try:
        (UControl, UClient, __) = await client.simple_client(
            addr,
            port,
            username,
            server_key_data,
            public_key = public_key_data,
            private_key = private_key_data,
            uteslaclient = uteslaclient.UTeslaClient()

        )
    
    except tornado.iostream.StreamClosedError as err:
        logging.error(_("Hubo un error conectado a %s:%d: %s"), addr, port, err)
        return

    UClient.set_stream_control(UControl)
    UControl.set_token(token)

    services = UClient.get_services(path)
    
    logging.warning(_("Obteniendo servicios..."))

    try:
        async for service_name in services:
            status_code = UControl.request.get_status_code()
            status = UControl.request.get_status()

            if (status_code == 0):
                service_name = os.path.basename(service_name)
                service_abs = "%(service_path)s/%(service_name)s/%(service_name)s.py" % {
                    "service_path" : service_path,
                    "service_name" : service_name
                        
                }

                for __ in range(2):
                    if (networkid is None):
                        logging.debug(
                            _("La red '%s' no existe, pero se agregará..."), net

                        )

                        await db.return_first_result("insert_network", net, token, username)
                        networkid = await db.return_first_result("extract_networkid", net)

                    else:
                        break

                if (networkid is None):
                    logging.error(
                        _("¡No se pudo obtener el identificador de la red '%s' en la base de datos!"),
                        net
                        
                    )
                    continue

                else:
                    if (isinstance(networkid, tuple)):
                        (networkid,) = networkid

                if (os.path.isfile(service_abs)):
                    logging.warning(
                        _("El servicio '%s' ya existe de manera local. No se agregará."),
                        service_name
                        
                    )
                    continue

                if (service_name in exclude):
                    logging.warning(
                        _("El servicio '%s' no se agregará o actualizará porque está en la lista de exclusión"),
                        service_name

                    )

                elif (only != []) and not (service_name in only):
                    logging.warning(
                        _("No se incluirá el servicio %s porque sólo se prefieren algunos servicios y éste no está incluido ahí"),
                        service_name

                    )

                else:
                    serviceid = await db.return_first_result("extract_serviceid", service_name)

                    if (serviceid is None) or not (await db.return_first_result("network_in_service", networkid, *serviceid)):
                        logging.info(
                            _("Agregando servicio '%s' de la red '%s'"),
                            service_name, net

                        )

                        await db.return_first_result(
                            "insert_service", networkid, service_name, priority

                        )

                    else:
                        logging.warning(
                            _("'%s' ya está registrado en la red '%s'"), service_name, net
                                
                        )

            else:
                logging.error(_("Ocurrió un error con la petición: %s"), status)
                break

        if (UControl.request.get_status_code() != -1) and (UControl.request.get_status_code() != 0):
            logging.error(_("Error obteniendo los servicios: %s"), UControl.request.get_status())

    except tornado.iostream.StreamClosedError as err:
        logging.error(_("Hubo un error interpretando los datos: %s"), err)

        if (UControl.request.get_status_code() != 0) and (UControl.request.get_status_code() != -1):
            logging.error(_("Posible error: %s"), UControl.request.get_status())

    else:
        if not (os.path.isfile(server_key_dst)):
            logging.debug(
                _("Copiando '%s' a '%s'..."),
                server_key, server_key_dst

            )

            shutil.copy(server_key, server_key_dst)

        logging.info(_("Hecho."))
