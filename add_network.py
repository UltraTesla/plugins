import logging
import hashlib
import shutil

from modules.Infrastructure import client

from utils.General import parse_config

from utils.extra import create_pool
from utils.extra import get_url
from utils.extra import array_strip

information = {
    'description' : 'Agregar una red',
    'commands'        : [
        {
            'positionals'  : [
                {
                    'args'     : ('network',),
                    'help'     : 'La red a conectar'

                }

            ]

        },

        {
            'Claves' : [
                {
                    'args'     : ('-s', '--server-key'),
                    'help'     : 'La clave pública del servidor',
                    'required' : True

                },
                
                {
                    'args'     : ('-p', '--import-public-key'),
                    'help'     : 'La clave pública del usuario',
                    'required' : True

                },

                {
                    'args'     : ('-P', '--import-private-key'),
                    'help'     : 'La clave privada del usuario',
                    'required' : True

                }

            ]

        },

        {
            'Identificación' : [
                {
                    'args'     : ('-u', '--username'),
                    'help'     : 'El nombre de usuario',
                    'required' : True

                },

                {
                    'args'     : ('-t', '--token'),
                    'help'     : 'El token de acceso',
                    'required' : True

                }

            ]

        },

        {
            'Servicios'       : [
                {
                    'args'    : ('-o', '--only'),
                    'help'    : 'En caso de que se conozcan los servicios, se pueden escribir '
                                'repitiendo el mismo parámetro con su argumento correspondiente. '
                                'Si se elige esta opción, no se hará una petición para obtener '
                                'los servicios actuales de la red.',
                    'action'  : 'append',
                    'default' : []

                },

                {
                    'args'    : ('-e', '--exclude'),
                    'help'    : 'Excluir ciertos servicios repitiendo la operación con su argumento '
                                'correspondiente',
                    'action'  : 'append',
                    'default' : []

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

async def MainParser(args):
    network = args.network
    token = args.token
    username = args.username
    server_key = args.server_key
    public_key = args.import_public_key
    private_key = args.import_private_key
    only = array_strip.strip(args.only)
    exclude = array_strip.strip(args.exclude)

    config = parse_config.parse()
    server_conf = config.get('Server')

    url = get_url.get(network)
    url_hash = hashlib.sha3_224(
        url.encode()
    ).hexdigest()
    db = await create_pool.create(
        server_conf.get('mysql_db')

    )
    init_path = server_conf.get('init_path')
    server_key_dst = '%s/servkeys/%s' % (
        init_path, url_hash

    )
    
    UClient = client.CoreClient(url, username)
    await UClient.set_server_key(server_key)
    await UClient.set_user_keys(public_key, private_key)

    logging.warning('Obteniendo servicios...')

    request = await UClient.get_services()
    response = UClient.get_message(request.body)

    if not (response.get('error')):
        (status, message) = list(response.get('message').values())

        if (status == 200):
            logging.warning('Petición satisfactoria, almacenando servicios...')

            for _ in range(2):
                networkid = await db.extract_networkid(url)

                if (networkid is None):
                    logging.debug('La red "%s" no existe, pero se agregará...',
                                  url)

                    await db.insert_network(url, token)

                else:
                    break

            for service_name, service_info in message.items():
                mtime = int(service_info.get('mtime'))
                current_mtime = await db.get_service_mtime(networkid)

                if (mtime != current_mtime):
                    if (service_name in exclude):
                        logging.warning('El servicio "%s" no se agregará o actualizará porque está en la'
                                        'lista de exclusión',
                                        service_name)

                    elif (only != []) and not (service_name in only):
                        logging.debug('No se incluirá el servicio %s porque sólo se prefieren'
                                      'algunos servicios y éste no está incluido ahí',
                                      service_name)

                    else:
                        serviceid = await db.extract_serviceid(service_name)

                        if (serviceid is None):
                            logging.debug('Agregando servicio "%s" de la red "%s"',
                                          service_name, url)

                            await db.insert_service(networkid, service_name, mtime)

                        else:
                            logging.debug('Actualizando servicio "%s" de la red "%s"',
                                          service_name, url)

                            await db.update_service_mtime(serviceid, mtime)

                else:
                    logging.warning('El servicio "%s" no se agregará o actualizará ya que no se ha modificado',
                                    service_name)

            logging.debug('Copiando "%s" a "%s"...',
                          server_key, server_key_dst)

            shutil.copy(server_key, server_key_dst)

            logging.info('Hecho.')

        else:
            logging.error('El código de estado no es el correspndiente: %s', message)

    else:
        logging.error('Ocurrió un error con la petición: %s', response.get('message'))
