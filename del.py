import logging
import os
import hashlib

from modules.Infrastructure import exceptions

from utils.General import parse_config
from utils.extra import create_pool

information = {
    'description' : 'Borrar un usuario',
    'commands'    : [
        {
            'positionals' : [
                {
                    'args' : ('user',),
                    'help' : 'El nombre de usuario a eliminar'

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

async def MainParser(args):
    user = args.user

    server_conf = parse_config.parse()['Server']

    db = await create_pool.create(server_conf.get('mysql_db'))

    logging.warning('Borrando usuario "%s" :-(', user)

    userid = await db.extract_userid(user)

    if not (userid):
        raise exceptions.UserNotExists('El usuario "%s" no existe' % user)

    await db.delete_user(userid)

    public_key_dst = '%s/pubkeys/%s' % (
        server_conf.get('init_path'), hashlib.sha3_224(user.encode()).hexdigest()

    )

    logging.debug('Borrando clave pública: %s', public_key_dst)

    if (os.path.isfile(public_key_dst)):
        os.remove(public_key_dst)

    else:
        raise exceptions.PublicKeyNotFound('No se pudo eliminar la clave pública "%s" porque no existe' % (
            public_key_dst

        ))

    logging.info('Usuario "%s" eliminado.', user)
