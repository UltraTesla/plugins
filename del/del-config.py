import os
from utils.extra import create_translation

_ = create_translation.create(
    "del-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Borrar un usuario"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args" : ("user",),
                    "help" : _("El nombre de usuario a eliminar")

                }

            ]

        }

    ],
    "version"     : "1.1.0"

}
