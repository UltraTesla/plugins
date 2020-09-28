import os
import logging
import FormatEncode

from utils.extra import create_translation

_ = create_translation.create(
    "encoder",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

def MainParser(args):
    encoder = args.encoder
    file = args.file
    out = args.out
    option = args.option
    show_formats = args.show_formats
    limit_size = args.limit_size

    if (show_formats):
        for format in FormatEncode.encoders.keys():
            print("*", format)

    else:
        if not (encoder in FormatEncode.encoders):
            logging.error(_("¡Debe seleccionar un codificador disponible!"))
            return

        if (option is None):
            logging.error(_("¡Debe decidir si codificar o decodificar!"))
            return

        else:
            option = option.lower()

        # La entrada no puede ser leída en modo binario, así que se hace esta magia
        if (file.mode == "r"):
            buff_in = file.buffer

        else:
            buff_in = file

        # Y la salida no puede ser escrita en modo binario...
        if (out.mode == "w"):
            buff_out = out.buffer

        else:
            buff_out = out

        data = buff_in.read(limit_size)

        if (option == "encode"):
            result = FormatEncode.encode(data, encoder)

        else:
            result = FormatEncode.decode(data, encoder)

        buff_out.write(result)
