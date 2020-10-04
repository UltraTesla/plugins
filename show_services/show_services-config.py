import os
import argparse
from utils.extra import create_translation

_ = create_translation.create(
    "show_services-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Mostrar los servicios de los nodos registrados"),
    "commands"    : [
        {
            "optionals" : [
                {
                    "args"    : ("-limit",),
                    "help"    : _("Mostrar sólo N cantidad de servicios. Cero es infinito."),
                    "type"    : int,
                    "default" : 0

                },

                {
                    "args"    : ("--only",),
                    "help"    : _("Mostrar sólo los servicios de un nodo específico."),
                    "type"    : int
                    
                }

            ],

            _("Argumentos remotos") : [
                {
                    "args"    : ("-r", "--remote"),
                    "help"    : _("Mostrar los servicios de forma remota."),
                    "action"  : "store_true"
                    
                },

                {
                    "args"    : ("-n", "--network"),
                    "help"    : _("La dirección de la red")
                    
                },

                {
                    "args"    : ("-t", "--token"),
                    "help"    : _("El token de acceso")
                    
                },

                {
                    "args"    : ("-u", "--username"),
                    "help"    : _("El nombre de usuario")
                    
                }
                
            ],

            _("Claves") : [
                {
                    "args"     : ("-s", "--server-key"),
                    "help"     : _("La clave pública del servidor"),
                    "type"     : argparse.FileType("rb")

                },
                
                {
                    "args"     : ("-p", "--import-public-key"),
                    "help"     : _("La clave pública del usuario"),
                    "dest"     : "public_key",
                    "type"     : argparse.FileType("rb")

                },

                {
                    "args"     : ("-P", "--import-private-key"),
                    "help"     : _("La clave privada del usuario"),
                    "dest"     : "private_key",
                    "type"     : argparse.FileType("rb")

                }
                
            ]

        }
        
    ],
    "version"     : "1.1.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]
        
}
