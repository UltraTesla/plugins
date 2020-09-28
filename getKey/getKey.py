import os
import hashlib
import logging
import tornado.httpclient

from utils.General import parse_config
from utils.extra import netparse
from utils.extra import create_translation

_ = create_translation.create(
    "getKey",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

class IncorrectLength(Exception):
    """
    Usado cuando la longitud de la clave pública
    es diferente a la requerida.
    
    """

# La clave pública obtenida
key = b""

# El límite de la clave pública
key_limit_size = None

def on_received(data):
    global key

    key += data

    if (len(key) > key_limit_size):
        raise IncorrectLength(_("La longitud de la clave obtenida sobrepasa los límites propuestos"))

async def getKey(url, **config):
    httpclient = tornado.httpclient.AsyncHTTPClient()
    httprequest = await httpclient.fetch(
        url, streaming_callback=on_received, **config
        
    )

    if (len(key) != key_limit_size):
        raise IncorrectLength(_("La longitud de la clave no es correcta"))

    return key

async def MainParser(args):
    global key_limit_size

    try:
        (net, port, path) = netparse.parse(args.network, default_port=8080)

    except Exception as err:
        logging.error(_("La dirección '%s' no es válida: %s"), args.network, err)
        return

    if (path == "/"):
        logging.error(_("Debe colocar el nombre de la clave a descargar"))
        return

    else:
        path = path[1:]

    outfile = args.outfile
    convert = args.convert
    overwrite = args.overwrite
    key_limit_size = args.key_limit_size
    client_options = {
        "connect_timeout"  : args.connect_timeout,
        "request_timeout"  : args.request_timeout,
        "user_agent"       : args.user_agent,
        "max_redirects"    : args.max_redirects,
        "follow_redirects" : args.follow_redirects
            
    }

    if not (os.path.isdir(outfile)):
        config = parse_config.parse()["Server"]

        if (outfile.lower() == "nodes"):
            outfile = "%s/%s" % (
                config["init_path"], config["server_data"]
                    
            )

        elif (outfile.lower() == "users"):
            outfile = "%s/%s" % (
                config["init_path"], config["user_data"]
                    
            )

        else:
            logging.error(_("El directorio '%s' no existe"), outfile)
            return

    if (convert):
        path = hashlib.sha3_224(path.encode()).hexdigest()

    try:
        key = await getKey(
            "http://%s:%d/%s" % (net, port, path),
            **client_options
            
        )

    except tornado.httpclient.HTTPClientError as err:
        logging.error(_("Ocurrió un error inesperado en la petición: %s"), err)
        return

    except IncorrectLength as err:
        logging.error(str(err))
        return

    else:
        fingerprint = hashlib.sha3_256(key).hexdigest()

        output = os.path.join(outfile, path)
        prompt = _("¿Deseas continuar con la operación (sí/no)? ")
        prompt_error = _("Por favor teclea 'sí' o 'no': ")

        if (os.path.isfile(output)) and (overwrite):
            logging.warning(_("¡La clave '%s' ya existe!"), path)

            with open(output, "rb") as fd:
                original = fd.read()
                original_fingerprint = hashlib.sha3_256(key).hexdigest()

                if (fingerprint == original_fingerprint):
                    print(_("La clave ya ha sido almacenada: {}").format(output))
                    return

    print(_("La huella de la clave es SHA3_256:{}").format(fingerprint))

    while (True):
        question = input(prompt).lower()

        if not (question):
            prompt = prompt_error
            continue

        if (question == "sí"):
            with open(output, "wb") as fd:
                fd.write(key)

            print(_("Guardada: {}").format(output))
            break

        elif (question == "no"):
            print(_("Verificación de la clave fallida"))
            break

        else:
            prompt = prompt_error
