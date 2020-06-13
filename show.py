from utils.extra import create_pool

information = {
    'description' : 'Mostrar los usuarios registrados',
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

    users = await db.show_users(show_limit)

    if (len(users) == 0):
        print('Aún no hay usuarios registrados :-(')

    else:
        for n, (userid, username, token_limit) in enumerate(users, 1):
            n = ' %d ' % (n)

            print(n.center(50, '='))
            print('    Identificador :', userid)
            print('Nombre de usuario :', username)
            print(' Límite de tokens :', token_limit)
