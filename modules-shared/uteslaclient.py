import os
from modules.Infrastructure import client
from utils.extra import create_translation

_ = create_translation.create(
    "uteslaclient",
    os.getenv("UTESLA_LOCALES_PLUGINS") or \
    "modules/Cmd/locales-shared"
    
)

class UTeslaClient(client.UTeslaClient):
    def __init__(self, stream_control=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_stream_control(stream_control)

    def set_stream_control(self, stream_control):
        self.__stream_control = stream_control

    @property
    def stream_control(self):
        if (self.__stream_control is None):
            raise RuntimeError(_("El controlador no ha sido definido"))

        return self.__stream_control

    @stream_control.setter
    def stream_control(self, stream_control):
        self.set_stream_control(stream_control)

    async def generate_token(
        self,
        password,
        expire = 604800,
        services = "(.*)",
        path = "/generate_token",
        action = "generate"

    ):
        self.stream_control.set_path(path, action)
        self.stream_control.set_init_parameter("password", password)
        self.stream_control.set_parameter("expire", expire)
        self.stream_control.set_parameter("services", services)
        await self.stream_control.write(None)

        return await self.stream_control.read()

    async def change_passwd(
        self,
        password,
        new_password,
        token_limit = None,
        path = "/generate_token",
        action = "change_passwd"
            
    ):
        self.stream_control.set_path(path, action)
        self.stream_control.set_init_parameter("password", password)
        self.stream_control.set_parameter("new_password", new_password)
        self.stream_control.set_parameter("token_limit", token_limit)
        await self.stream_control.write(None)

        return await self.stream_control.read()

    async def change_services(
        self,
        password,
        services,
        path = "/generate_token",
        action = "change_services"
            
    ):
        self.stream_control.set_path(path, action)
        self.stream_control.set_init_parameter("password", password)
        self.stream_control.set_parameter("services", services)
        await self.stream_control.write(None)

        return await self.stream_control.read()

    async def get_services(
        self,
        path = "/get_services",
        action = "get"

    ):
        self.stream_control.set_path(path, action)
        await self.stream_control.write(None)

        while (service := await self.stream_control.read()):
            yield service

    async def renew_token(
        self,
        password,
        path = "/generate_token",
        action = "renew"
            
    ):
        self.stream_control.set_path(path, action)
        self.stream_control.set_init_parameter("password", password)
        await self.stream_control.write(None)

        return await self.stream_control.read()
