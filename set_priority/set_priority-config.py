import os
from utils.extra import create_translation

_ = create_translation.create(
    "set_priority-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Cambiar la prioridad de uno o más servicios"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"     : ("identificator",),
                    "help"     : _("El identificador del nodo o del servicio"),
                    "type"     : int
                    
                },

                {
                    "args"     : ("-p", "--priority"),
                    "help"     : _("La prioridad de o el servicio"),
                    "type"     : int,
                    "required" : True
                    
                }
                
            ],

            "optionals" : [
                {
                    "args"   : ("--use-only-networks",),
                    "help"   : _("Usar ``IDENTIFICATOR`` como identificador de una red y cambiar la "
                               "prioridad de todos los servicios a la cual le pertenezcan."),
                    "action" : "store_true",
                    "dest"   : "only_networks"
                    
                }
                
            ]
            
        }
        
    ],
    "version"     : "1.0.0"
        
}
