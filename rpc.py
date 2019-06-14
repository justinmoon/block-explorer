from bitcoinrpc.authproxy import AuthServiceProxy
from dynaconf import settings


class RPC:
    
    def __getattr__(self, name):
        """Hack to establish a new AuthServiceProxy every time this is called"""
        rpc_uri = f"http://{settings.RPC_USERNAME}:{settings.RPC_PASSWORD}@{settings.RPC_IP}:{settings.RPC_PORT}"
        rpc = AuthServiceProxy(rpc_uri)
        return getattr(rpc, name)

