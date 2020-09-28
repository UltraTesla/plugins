import os
from utils.extra import create_translation

_ = create_translation.create(
    "add_network-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description"     : _("Agregar una red"),
    "commands"        : [
        {
            "positionals"  : [
                {
                    "args"     : ("network",),
                    "help"     : _("La red a conectar")

                }

            ]

        },

        {
            _("Claves") : [
                {
                    "args"     : ("-s", "--server-key"),
                    "help"     : _("La clave pública del servidor"),
                    "required" : True

                },
                
                {
                    "args"     : ("-p", "--import-public-key"),
                    "help"     : _("La clave pública del usuario"),
                    "required" : True

                },

                {
                    "args"     : ("-P", "--import-private-key"),
                    "help"     : _("La clave privada del usuario"),
                    "required" : True

                }

            ]

        },

        {
            _("Identificación") : [
                {
                    "args"     : ("-u", "--username"),
                    "help"     : _("El nombre de usuario"),
                    "required" : True

                },

                {
                    "args"     : ("-t", "--token"),
                    "help"     : _("El token de acceso"),
                    "required" : True

                }

            ]

        },

        {
            _("Servicios") : [
                {
                    "args"    : ("-o", "--only"),
                    "help"    : _("En caso de que se conozcan los servicios, se pueden escribir "
                                "repitiendo el mismo parámetro con su argumento correspondiente. "
                                "Si se elige esta opción, no se hará una petición para obtener "
                                "los servicios actuales de la red."),
                    "action"  : "append",
                    "default" : []

                },

                {
                    "args"    : ("-e", "--exclude"),
                    "help"    : _("Excluir ciertos servicios repitiendo la operación con su argumento "
                                "correspondiente"),
                    "action"  : "append",
                    "default" : []

                }

            ]

        },

        {
            "optionals" : [
                {
                    "args"    : ("--priority",),
                    "help"    : _("La prioridad de la red (útil para una mejor organización en la jerarquía)"),
                    "type"    : int,
                    "default" : 0
                    
                }
                
            ]
                
        }

    ],
    "version"     : "1.1.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]

}
