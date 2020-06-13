import argparse

from modules.Crypt import rsa

default_bit_size = 3072

information = {
    'description' : 'Generar el par de claves para el usuario',
    'commands'    : [
        {
            'Configuración del par de claves' : [
                {
                    'args'    : ('-bit_size',),
                    'help'    : 'El tamaño de la clave en bit\'s',
                    'type'    : int,
                    'default' : default_bit_size

                }

            ],

            'optionals'   : [
                {
                    'args'    : ('-out-public-key',),
                    'help'    : 'El nombre del archivo para almacenar la clave pública',
                    'type'    : argparse.FileType('wb')

                },

                {
                    'args'    : ('-out-private-key',),
                    'help'    : 'El nombre del archivo para almacenar la clave privada',
                    'type'    : argparse.FileType('wb')

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

def MainParser(args):
    bit_size = args.bit_size
    out_public_key = args.out_public_key
    out_private_key = args.out_private_key

    Rsa = rsa.Rsa()
    
    if (bit_size < 1024):
        logging.error('No es posible establecer una clave menor a 1024 bit\'s')

        return

    Rsa.generate(bit_size)
    public_key = Rsa.export_public_key()
    private_key = Rsa.export_private_key()

    if (out_public_key):
        out_public_key.write(
            public_key

        )

    else:
        print(public_key.decode(), end='\n\n')

    if (out_private_key):
        out_private_key.write(
            private_key

        )

    else:
        print(private_key.decode(), end='\n\n')
