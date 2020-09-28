import os
import argparse
from utils.extra import create_translation

_ = create_translation.create(
    "renew-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Renovar un token de acceso"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"      : ("network",),
                    "help"      : _("La red a conectar")

                },

                {
                    "args"     : ("-t", "--token"),
                    "help"     : _("El token de acceso"),
                    "required" : True
                    
                }

            ]

        },

        {
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
                    "type"     : argparse.FileType("rb"),
                    "dest"     : "public_key"

                },

                {
                    "args"     : ("-I", "--import-private-key"),
                    "help"     : _("La clave privada del usuario"),
                    "required" : True,
                    "type"     : argparse.FileType("rb"),
                    "dest"     : "private_key"

                }

            ]

        }
        
    ],
    "version"     : "1.0.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]
        
}
