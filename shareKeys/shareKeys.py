import os
import sys
import pathlib
import logging
import tornado.web
import tornado.httpserver
import tornado.template
import aiofiles

from utils.General import parse_config
from utils.extra import netparse
from utils.extra import create_translation

_ = create_translation.create(
    "shareKeys",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

def listdir(path, regex="*"):
    for file in pathlib.Path(path).glob(regex):
        file = os.path.basename(str(file))

        if (os.path.isfile(os.path.join(path, file))) and (file[:1] != "."):
            yield os.path.basename(file)

class ServerHandler(tornado.web.RequestHandler):
    def initialize(
        self,
        path,
        key,
        index,
        title,
        subtitle,
        key_limit_size,
        glob_exp
        
    ):
        self.path = path
        self.key = key
        self.index = index
        self.title = title
        self.subtitle = subtitle
        self.key_limit_size = key_limit_size
        self.glob_exp = glob_exp

    def __replace_str(self, string):
        string = string.replace("{key}", os.path.basename(self.key), 1)
        string = string.replace("{path}", self.request.path, 1)

        return string

    async def get(self, *args, **kwargs):
        path = self.request.path
        title = self.__replace_str(self.title)
        subtitle = self.__replace_str(self.subtitle)

        if (path == "/"):
            if (os.path.isfile(self.key)):
                key = [os.path.basename(self.key)]

            elif (os.path.isdir(self.key)):
                key = listdir(self.path, self.glob_exp)

            else:
                self.set_status(404)
                return

            self.render(
                self.index,
                title = title,
                subtitle = subtitle,
                keys = key
                
            )

        else:
            if (os.path.isfile(self.path)):
                base_path = os.path.basename(self.path)
                file = self.path

            else:
                base_path = os.path.basename(path[1:])
                file = "%s/%s" % (
                    self.path,
                    tornado.template.escape.xhtml_unescape(base_path)

                )

            if (os.path.isfile(file)):
                self.set_header("Content-Type", "application/octet-stream")
                self.set_header("Content-Disposition", "attachment; filename='%s'" % (
                    tornado.template.escape.xhtml_escape(base_path)
                    
                ))

                async with aiofiles.open(file, "rb") as fd:
                    key = await fd.read(self.key_limit_size)

                self.set_header("Content-Length", str(len(key)))
                self.write(key)
                await self.flush()

            else:
                self.set_status(404)

async def MainParser(args):
    keyfile = args.keyfile
    title = args.title
    subtitle = args.subtitle
    html_file = args.html_file
    key_limit_size = args.key_limit_size
    glob_exp = args.glob_pattern

    workspace = args.__OPTIONS__["workspaces"][args.__OPTIONS__["index"]]
    
    try:
        (address, port, __) = netparse.parse(args.listen)

    except Exception as err:
        logging.error(_("La dirección '%s' no es válida: %s"), args.listen, err)
        sys.exit(1)
        return

    if not (os.path.exists(keyfile)):
        config = parse_config.parse()["Server"]

        if (keyfile.lower() == "server"):
            keyfile = config["pub_key"]
            path = os.path.dirname(keyfile)

        elif (keyfile.lower() == "users"):
            keyfile = "%s/%s" % (
                config["init_path"], config["user_data"]
                    
            )

            path = keyfile

        elif (keyfile.lower() == "nodes"):
            keyfile = "%s/%s" % (
                config["init_path"], config["server_data"]
                    
            )
            path = os.path.dirname(keyfile) or "."

        else:
            logging.error(_("El archivo '%s' no existe"), keyfile)
            sys.exit(1)
            return

    else:
        path = keyfile

    index = "%s/%s" % (workspace, html_file)

    if not (os.path.isfile(index)):
        logging.error(_("La plantilla '%s' no existe"))
        sys.exit(1)
        return

    app = tornado.web.Application([
        (
            r"/(.*)",
            ServerHandler,
            {
                "path"           : path,
                "key"            : keyfile,
                "index"          : index,
                "title"          : title,
                "subtitle"       : subtitle,
                "key_limit_size" : key_limit_size,
                "glob_exp"       : glob_exp
                
            }
            
        )
        
    ], template_path=".")
    httpd = tornado.httpserver.HTTPServer(app)
    httpd.listen(port, address)

    logging.info(_("Escuchando en http://%s:%d"), address, port)
