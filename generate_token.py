import logging

from modules.Infrastructure import client

from utils.extra import get_url
from utils.extra import create_pool

default_expire = 604800 # 7 días

information = {
    'description' : 'Generar un token de acceso',
    'commands'    : [
        {
            'positionals'      : [
                {
                    'args'      : ('network',),
                    'help'      : 'La red a conectar'

                }

            ]

        },

        {
            'Credenciales' : [
                {
                    'args'     : ('-u', '--username'),
                    'help'     : 'El nombre de usuario',
                    'required' : True

                },

                {
                    'args'     : ('-p', '--password'),
                    'help'     : 'La contraseña del usuario',
                    'required' : True

                }

            ],

            'Claves'       : [
                {
                    'args'     : ('-s', '--server-key'),
                    'help'     : 'La clave pública del servidor',
                    'required' : True

                },

                {
                    'args'     : ('-i', '--import-public-key'),
                    'help'     : 'La clave pública del usuario',
                    'required' : True

                },

                {
                    'args'     : ('-I', '--import-private-key'),
                    'help'     : 'La clave privada del usuario',
                    'required' : True

                }

            ],

            'optionals'    : [
                {
                    'args'     : ('-e', '--expire'),
                    'help'     : 'La fecha de expiración expresada en segundos',
                    'type'     : int,
                    'default'  : default_expire

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

async def MainParser(args):
    username = args.username
    password = args.password
    network = args.network
    expire = args.expire
    server_key = args.server_key
    public_key = args.import_public_key
    private_key = args.import_private_key

    url = get_url.get(network)
    db = await create_pool.create()
    UClient = client.CoreClient(network, username)
    await UClient.set_server_key(server_key)
    await UClient.set_user_keys(public_key, private_key)

    request = await UClient.generate_token(password, expire)
    response = UClient.get_message(request.body)

    if not (response.get('error')):
        (status, message) = list(response.get('message').values())

        if (status == 201):
            logging.info('Token generado con éxito: %s', message)

        elif (status == 202):
            logging.warning('No se pudo crear el token, puede ser que haya expirado: %s', message)

        else:
            logging.error('Ocurrió un error con la petición: %s', message)

    else:
        logging.error('Error en la respuesta: %s', response.get('message'))
