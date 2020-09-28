import os
from utils.extra import create_translation

_ = create_translation.create(
    "add-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Agregar un usuario"),
    "commands"    : [
        {
            _("Credenciales") : [
                {
                    "args"     : ("-u", "--user"),
                    "help"     : _("El nombre de usuario"),
                    "required" : True

                },

                {
                    "args"     : ("-p", "--password"),
                    "help"     : _("La contraseña del usuario"),
                    "required" : True

                },

                {
                    "args"     : ("-i", "--import-public-key"),
                    "help"     : _("La clave pública del usuario a registrar"),
                    "required" : True

                }

            ]

        },

        {
            "optionals"    :  [
                {
                    "args"    : ("-l", "--token-limit"),
                    "help"    : _("Límites del token por usuario"),
                    "type"    : int,
                    "default" : 1

                },

                {
                    "args"    : ("-o", "--overwrite"),
                    "help"    : _("Sobre-escribir la clave pública (en caso de que exista)"),
                    "action"  : "store_true"

                },

                {
                    "args"    : ("-t", "--time-cost"),
                    "help"    : _("La cantidad del cálculo realizado, y por lo tanto, el tiempo de ejecución dado el número de iteraciones"),
                    "type"    : int,
                    "default" : 2

                },

                {
                    "args"    : ("-m", "--memory-cost"),
                    "help"    : _("La cantidad de memoria a utilizar"),
                    "type"    : int,
                    "default" : 102400

                },

                {
                    "args"    : ("-S", "--parallelism"),
                    "help"    : _("La cantidad de subprocesos paralelos"),
                    "type"    : int,
                    "default" : 8

                },

                {
                    "args"    : ("-g", "--guest-user"),
                    "help"    : _("Agregar como un usuario invitado"),
                    "action"  : "store_true"
                    
                }

            ]

        }

    ],
    "version"     : "1.1.0"

}
