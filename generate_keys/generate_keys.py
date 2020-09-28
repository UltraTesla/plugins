import os
import argparse
import logging

from modules.Crypt import ed25519
from utils.extra import create_translation

_ = create_translation.create(
    "generate_keys",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

def MainParser(args):
    out_public_key = args.public_key
    out_private_key = args.private_key

    logging.debug(_("Generando claves..."))

    (public_key, private_key) = ed25519.to_raw()
    
    logging.debug(_("Escribiendo clave pública..."))

    out_public_key.write(
        public_key

    )

    logging.debug(_("Escribiendo la clave privada..."))

    out_private_key.write(
        private_key

    )

    logging.debug(_("Hecho."))
