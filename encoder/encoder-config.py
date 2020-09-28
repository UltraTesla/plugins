import os
import sys
import argparse
from utils.extra import create_translation

_ = create_translation.create(
    "encoder-config",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

information = {
    "description" : _("Codificar archivos para la legibilidad humana. Creado para transmitir "
                      "claves en medios que no aceptan una codificación textual."),
    "commands"    : [
        {
            "positionals" : [
                {
                    "args"    : ("-e", "--encoder"),
                    "help"    : _("La codificación de salida del par de claves"),
                    "default" : "base64"
                    
                }

            ]

        },

        {
            _("Opciones generales") : [
                {
                    "args"     : ("-f", "--file"),
                    "help"     : _("El archivo de entrada. Si no se específica se usa la entrada"),
                    "type"     : argparse.FileType("rb"),
                    "default"  : sys.stdin
                    
                },

                {
                    "args"     : ("-o", "--out"),
                    "help"     : _("El archivo de salida. Si no se específica se usa la salida"),
                    "type"     : argparse.FileType("wb"),
                    "default"  : sys.stdout
                    
                },

                {
                    "args"     : ("-O", "--option"),
                    "help"     : _("Codificar o descodificar"),
                    "choices"  : ("encode", "decode")
                    
                }
                
                
            ]
            
        },

        {
            "optionals" : [
                {
                    "args"       : ("--show-formats",),
                    "help"       : _("Mostrar los formatos disponibles"),
                    "action"     : "store_true"
                    
                },

                {
                    "args"       : ("--limit-size",),
                    "help"       : _("El tamaño máximo de lectura"),
                    "type"       : int,
                    "default"    : 2**10*64 # 64 KiB
                    
                }
                
            ]
            
        }
        
    ],
    "version"     : "1.0.0"
        
}
