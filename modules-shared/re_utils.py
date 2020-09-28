import re
import os
from utils.extra import create_translation

_ = create_translation.create(
    "re_utils",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

def to_raw(regex):
    if not (isinstance(regex, str)):
        raise TypeError(_("La expresión regular no es un tipo de dato válido"))

    return regex.encode("unicode-escape").decode()

def is_regex(regex):
    try:
        re.compile(regex)

    except re.error:
        return False

    else:
        return True
