from utils.extra import create_pool

information = {
    'description' : 'Mostrar los nodos de la red',
    'commands'    : [
        {
            'positionals' : [
                {
                    'args'    : ('-limit',),
                    'help'    : 'Mostrar sólo N cantidad de usuarios. Cero es infinito.',
                    'type'    : int,
                    'default' : 0

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

async def MainParser(args):
    show_limit = args.limit

    db = await create_pool.create()

    networks = await db.get_networks(show_limit, show_all=True)

    if (len(networks) == 0):
        print('Aún no hay redes registradas :-(')

    else:
        for n, (networkid, network, token) in enumerate(networks, 1):
            n = ' %d ' % (n)

            print(n.center(50, '='))
            print('    Identificador :', networkid)
            print(' Dirección de red :', network)
            print('            Token :', token)
