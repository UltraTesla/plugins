import os
import argparse

from utils.extra import create_translation

_ = create_translation.create(
    "generate_keys-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Generar el par de claves para el usuario"),
    "commands"    : [
        {

            "optionals"   : [
                {
                    "args"     : ("-out-public-key",),
                    "help"     : _("El nombre del archivo para almacenar la clave pública"),
                    "type"     : argparse.FileType("wb"),
                    "dest"     : "public_key",
                    "required" : True

                },

                {
                    "args"     : ("-out-private-key",),
                    "help"     : _("El nombre del archivo para almacenar la clave privada"),
                    "type"     : argparse.FileType("wb"),
                    "dest"     : "private_key",
                    "required" : True

                },


            ]

        }

    ],
    "version"     : "1.0.0"

}
