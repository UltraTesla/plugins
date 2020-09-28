import os
from utils.extra import create_translation

_ = create_translation.create(
    "gen_onodo-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Crear un gráfico que representa a la red junto a sus nodos"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"     : ("-output",),
                    "help"     : _("El nombre del archivo .xlsx que representará la red. "
                                 "Use ``stdout`` para imprimir el resultado en la "
                                 "salido (exceptuando al formato xlsx)"),
                    "default"  : "onodo.xlsx"

                }

            ]

        },

        {
            "optionals"   : [
                {
                    "args"     : ("-local-machine",),
                    "help"     : _("El nombre de la máquina actual"),
                    "default"  : "<Local Machine>"

                },

                {
                    "args"     : ("-format",),
                    "help"     : _("El formato del resultado"),
                    "default"  : "xlsx"

                },

                {
                    "args"     : ("-list",),
                    "help"     : _("Listar los formatos disponibles"),
                    "action"   : "store_true"

                }

            ]

        }

    ],
    "version"     : "1.1.0"

}
