import os
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

            ]

        }
        
    ],
    "version"     : "1.0.0",
    "workspaces"  : ["modules/Cmd/modules-shared"]
        
}
