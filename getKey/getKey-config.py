import os
from utils.extra import create_translation

_ = create_translation.create(
    "getKey-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Obtener una clave pública"),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args" : ("network",),
                    "help" : _("La dirección de la red junto con el nombre de la clave. "
                             "P. ej.: localhost:17000/ed25519.pub")
                    
                },

                {
                    "args"    : ("-o", "--outfile"),
                    "help"    : _("El nombre de salida del archivo. Usar 'nodes' para almacenar "
                                "la clave pública en la carpeta de los nodos; usar 'users' para "
                                "almacenar la clave pública en la carpeta de los usuarios; o usar "
                                "la ruta de una carpeta arbitraria."),
                    "default" : "."
                    
                },

                {
                    "args"    : ("-O", "--overwrite"),
                    "help"    : _("Si la clave existe y tiene el mismo contenido que la clave descargada "
                                "se sobre-escribe si se usa esta opción."),
                    "action"  : "store_false"
                    
                }
                
            ]
            
        },

        {
            "optionals"  : [
                {
                    "args"   : ("-c", "--convert"),
                    "help"   : _("Convertir el nombre de la clave en un identificador. P. ej.: SHA3_224(USERNAME/NODE) -> ID"),
                    "action" : "store_true"
                    
                },

                {
                    "args"    : ("-L", "--key-limit-size"),
                    "help"    : _("La longitud límite para la transferencia de claves."),
                    "type"    : int,
                    "default" : 32
                    
                }
                
            ]
            
        },

        {
            "Configuración del cliente" : [
                {
                    "args"    : ("-connect-timeout",),
                    "help"    : _("El tiempo de espera para conectar"),
                    "type"    : float,
                    "default" : 15.0
                    
                },

                {
                    "args"    : ("-request-timeout",),
                    "help"    : _("El tiempo de espera de la petición"),
                    "type"    : float,
                    "default" : 15.0
                    
                },

                {
                    "args"    : ("-user-agent",),
                    "help"    : _("El agente de usuario"),
                    "default" : "UTesla Client"
                    
                },

                {
                    "args"    : ("-max_redirects",),
                    "help"    : _("El límite máximo de redirecciones"),
                    "type"    : int,
                    "default" : 5
                    
                },

                {
                    "args"    : ("-follow_redirects",),
                    "help"    : _("Habilitar la redirección"),
                    "action"  : "store_true"
                    
                }
                
            ]
            
        }
        
    ],
    "version"     : "1.0.0"
        
}
