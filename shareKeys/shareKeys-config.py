import os
from utils.extra import create_translation

_ = create_translation.create(
    "shareKeys-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Compartir las claves públicas de los usuarios, de los nodos o del servidor"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"    : ("keyfile",),
                    "help"    : _("La clave pública a compartir. Usar 'server' para compartir la  "
                                "clave pública del servidor; usar 'nodes' para compartir todas  "
                                "las claves de los nodos; usar 'users' para compartir todas las "
                                "claves de los usuarios; usar la ruta de un archivo y pretender "
                                "que es una clave pública."),
                    
                }
                
            ]
            
        },

        {
            "optionals" : [
                {
                    "args"    : ("-l", "--listen"),
                    "help"    : _("La dirección a escuchar"),
                    "default" : "0.0.0.0:8080"
                    
                },

                {
                    "args"    : ("-t", "--title"),
                    "help"    : _("El título del documento"),
                    "default" : "Descargar: {key}"
                    
                },

                {
                    "args"    : ("-s", "--subtitle"),
                    "help"    : _("El sub-título del documento"),
                    "default" : "Descargar: {key}"
                    
                },

                {
                    "args"    : ("-H", "--html-file"),
                    "help"    : _("El nombre de la plantilla HTML"),
                    "default" : "index.html"
                    
                },

                {
                    "args"    : ("-L", "--key-limit-size"),
                    "help"    : _("La longitud límite para la transferencia de claves."),
                    "type"    : int,
                    "default" : 32
                    
                },

                {
                    "args"    : ("-g", "--glob-pattern"),
                    "help"    : _("El comodín a utilizar para encontrar las claves públicas "
                                "(si ``KEYFILE`` es un archivo, se ignora)"),
                    "default" : "*"
                    
                }
                
            ]
            
        }
        
    ],
    "version"     : "1.0.0",
    "persist"     : True
        
}
