import os
from utils.extra import create_translation

_ = create_translation.create(
    "del_network-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Borrar una red"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args" : ("network",),
                    "help" : _("La red a borrar")

                }

            ]

        }

    ],
    "version"     : "1.1.0"

}
