import os
from utils.extra import create_translation

_ = create_translation.create(
    "change_passwd-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Cambiar la contraseña de un usuario"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"     : ("-user",),
                    "help"     : _("El nombre de usuario"),
                    "required" : True
                    
                },

                {
                    "args"     : ("-password",),
                    "help"     : _("La contraseña a verificar (si la operación es local, se ignora)")
                    
                },

                {
                    "args"     : ("-new_password",),
                    "help"     : _("La contraseña nueva"),
                    "required" : True
                    
                }
                
            ]
            
        },

        {
            "optionals"    :  [
                {
                    "args"    : ("-l", "--token-limit"),
                    "help"    : _("Límites del token por usuario"),
                    "type"    : int

                },

                {
                    "args"    : ("-t", "--time-cost"),
                    "help"    : _("La cantidad del cálculo realizado, y por lo tanto, el tiempo de ejecución "
                                "dado el número de iteraciones"),
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

                }

            ],

            _("Opciones remotas") : [
                {
                    "args"    : ("-r", "--remote"),
                    "action"  : "store_true",
                    "help"    : _("Cambiar la contraseña remotamente en vez de forma local")
                    
                },

                {
                    "args"    : ("-n", "--network"),
                    "help"    : _("La dirección de la red"),
                    
                }
                
            ],

            _("Claves")       : [
                {
                    "args"     : ("-s", "--server-key"),
                    "help"     : _("La clave pública del servidor")

                },

                {
                    "args"     : ("-i", "--import-public-key"),
                    "help"     : _("La clave pública del usuario"),
                    "dest"     : "public_key"

                },

                {
                    "args"     : ("-I", "--import-private-key"),
                    "help"     : _("La clave privada del usuario"),
                    "dest"     : "private_key"

                }

            ],

        }

    ],
    "version"     : "1.0.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]
        
}
