import os
import argparse

from utils.extra import create_translation

_ = create_translation.create(
    "generate_token-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

default_expire = 604800 # 7 días

information = {
    "description" : _("Generar un token de acceso"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"      : ("network",),
                    "help"      : _("La red a conectar")

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
                    "type"     : argparse.FileType("rb")

                },

                {
                    "args"     : ("-I", "--import-private-key"),
                    "help"     : _("La clave privada del usuario"),
                    "required" : True,
                    "type"     : argparse.FileType("rb")

                }

            ],

            "optionals"    : [
                {
                    "args"     : ("-e", "--expire"),
                    "help"     : _("La fecha de expiración expresada en segundos"),
                    "type"     : int,
                    "default"  : default_expire

                },

                {
                    "args"     : ("-S", "--services"),
                    "help"     : _("Una expresión regular que indica qué servicios se usarán con el token"),
                    "default"  : "(.*)"
                    
                }

            ]

        }

    ],
    "version"     : "1.1.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]

}
