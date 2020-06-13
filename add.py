import logging
import hashlib
import time
import shutil
import os

from modules.Infrastructure import exceptions

from utils.General import parse_config

from utils.extra import generate_hash
from utils.extra import create_pool

information = {
    'description' : 'Agregar un usuario',
    'commands'    : [
        {
            'Credenciales' : [
                {
                    'args'     : ('-u', '--user'),
                    'help'     : 'El nombre de usuario',
                    'required' : True

                },

                {
                    'args'     : ('-p', '--password'),
                    'help'     : 'La contraseña del usuario',
                    'required' : True

                },

                {
                    'args'     : ('-i', '--import-public-key'),
                    'help'     : 'La clave pública del usuario a registrar',
                    'required' : True

                }

            ]

        },

        {
            'optionals'    :  [
                {
                    'args'    : ('-l', '--token-limit'),
                    'help'    : 'Límites del token por usuario',
                    'type'    : int,
                    'default' : 1

                },

                {
                    'args'    : ('-o', '--overwrite'),
                    'help'    : 'Sobre-escribir la clave pública (en caso de que exista)',
                    'action'  : 'store_true'

                },

                {
                    'args'    : ('-t', '--time-cost'),
                    'help'    : 'La cantidad del cálculo realizado, y por lo tanto, el tiempo de ejecución dado el número de iteraciones',
                    'type'    : int,
                    'default' : 2

                },

                {
                    'args'    : ('-m', '--memory-cost'),
                    'help'    : 'La cantidad de memoria a utilizar',
                    'type'    : int,
                    'default' : 102400

                },

                {
                    'args'    : ('-S', '--parallelism'),
                    'help'    : 'La cantidad de subprocesos paralelos',
                    'type'    : int,
                    'default' : 8

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

async def MainParser(args):
    user = args.user
    password = args.password
    token_limit = args.token_limit
    public_key = args.import_public_key
    overwrite = args.overwrite
    time_cost = args.time_cost
    memory_cost = args.memory_cost
    parallelism = args.parallelism

    config = parse_config.parse()
    
    server_conf = config['Server']
    crypt_limits = config['Crypt Limits']

    db = await create_pool.create(
        server_conf.get('mysql_db')

    )

    logging.info('Creando usuario: %s', user)

    user_hash = hashlib.sha3_224(user.encode()).hexdigest()

    public_key_dst = "%s/pubkeys/%s" % (
        server_conf.get('init_path'), user_hash

    )

    time_init = time.time()

    logging.debug('Generando hash...')

    time_end = time.time()-time_init

    pass2hash = generate_hash.generate(
        password, time_cost, memory_cost, parallelism, crypt_limits

    )

    logging.debug('Hash generado "%s" en %.2f',
        pass2hash, round(time_end, 2)

    )

    logging.debug('Copiando clave pública "%s" a "%s"',
        public_key, public_key_dst

    )

    if not (os.path.isfile(public_key)):
        raise FileNotFoundError('La clave pública de origen "%s" no existe' % (public_key))

    if (os.path.isfile(public_key_dst)) and not (overwrite):
        raise FileExistsError('¡La clave pública "%s" ya existe!' % (public_key_dst))

    shutil.copy(public_key, public_key_dst)

    logging.debug('Creando nuevo usuario: '
                  'Username=%s, Password=%s, Token-Limit=%d',
        user, len(password)*'*', token_limit

    )

    await db.insert_user(user,
                         pass2hash,
                         token_limit)

    logging.info('Se creó con éxito: %s', user)
