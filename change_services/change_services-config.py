import os
import argparse
from utils.extra import create_translation

_ = create_translation.create(
    "change_services-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Cambiar los servicios permitidos de un token"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args" : ("services",),
                    "help" : _("Una expresión regular que indica qué servicios se usarán con el token")
                    
                },

                {
                    "args"     : ("-n", "--network"),
                    "help"     : _("La red a conectar"),
                    "required" : True
                    
                },

                {
                    "args"     : ("-t", "--token"),
                    "help"     : _("El token de acceso"),
                    "required" : True
                    
                }
                
            ],

            _("Credenciales") : [
                {
                    "args"     : ("-u", "--username"),
                    "help"     : _("El nombre de usuario"),
                    "required" : True

                },

                {
                    "args"     : ("-p", "--password"),
                    "help"     : _("La contraseña del usuario"),
                    "required" : True

                }

            ],

            _("Claves")       : [
                {
                    "args"     : ("-s", "--server-key"),
                    "help"     : _("La clave pública del servidor"),
                    "required" : True,
                    "type"     : argparse.FileType("rb")

                },

                {
                    "args"     : ("-i", "--import-public-key"),
                    "help"     : _("La clave pública del usuario"),
                    "required" : True,
                    "dest"     : "public_key",
                    "type"     : argparse.FileType("rb")

                },

                {
                    "args"     : ("-I", "--import-private-key"),
                    "help"     : _("La clave privada del usuario"),
                    "required" : True,
                    "dest"     : "private_key",
                    "type"     : argparse.FileType("rb")

                }

            ]
            
        }
        
    ],
    "version"     : "1.0.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]
        
}
