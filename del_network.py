import logging
import os
import hashlib

from modules.Infrastructure import exceptions

from utils.General import parse_config
from utils.extra import create_pool
from utils.extra import get_url

information = {
    'description' : 'Borrar una red',
    'commands'    : [
        {
            'positionals' : [
                {
                    'args' : ('network',),
                    'help' : 'La red a borrar'

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

async def MainParser(args):
    url = args.network
    network = get_url.get(url)

    server_conf = parse_config.parse()['Server']

    db = await create_pool.create(server_conf.get('mysql_db'))

    logging.warning('Borrando red "%s" :-(', network)

    networkid = await db.extract_networkid(network) 

    if not (networkid):
        raise exceptions.NetworkNotExists('La red "%s" no existe' % network)

    await db.delete_network(networkid)

    public_key_dst = '%s/servkeys/%s' % (
        server_conf.get('init_path'), hashlib.sha3_224(network.encode()).hexdigest()

    )

    logging.debug('Borrando clave pública: %s', public_key_dst)

    if (os.path.isfile(public_key_dst)):
        os.remove(public_key_dst)

    else:
        raise exceptions.PublicKeyNotFound('No se pudo eliminar la clave pública "%s" porque no existe' % (
            public_key_dst

        ))

    logging.info('Red "%s" eliminada.', network)
