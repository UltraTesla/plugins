import os
from utils.extra import create_translation

_ = create_translation.create(
    "show-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Mostrar los usuarios registrados"),
    "commands"    : [
        {
            "optionals" : [
                {
                    "args"    : ("-limit",),
                    "help"    : _("Mostrar sólo N cantidad de usuarios. Cero es infinito."),
                    "type"    : int,
                    "default" : 0

                }

            ]

        }

    ],
    "version"     : "1.1.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]

}
