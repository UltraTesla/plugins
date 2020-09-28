import os
import nacl.encoding

from utils.extra import create_translation

_ = create_translation.create(
    "FormatEncode",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

DEFAULT_FORMAT = "base64"

ENCODE = 1
DECODE = 2

encoders = {
    "base16"  : nacl.encoding.Base16Encoder(),
    "base32"  : nacl.encoding.Base32Encoder(),
    "base64"  : nacl.encoding.Base64Encoder(),
    "hex"     : nacl.encoding.HexEncoder(),
    "urlsafe" : nacl.encoding.URLSafeBase64Encoder()
        
}

def __execute(data, obj, cmd):
    if (cmd == ENCODE):
        return obj.encode(data)

    else:
        return obj.decode(data)

def __get_algo(format):
    algo = encoders.get(format)

    if (algo is None):
        raise ValueError(_("El algoritmo '{}' no existe").format(format))

    return algo

def encode(data, format=DEFAULT_FORMAT):
    algo = __get_algo(format)

    return __execute(data, algo, ENCODE)

def decode(data, format=DEFAULT_FORMAT):
    algo = __get_algo(format)

    return __execute(data, algo, DECODE)
