import ssl

from bitcoinrpc.authproxy import AuthServiceProxy

from dynaconf import settings

class RPC:
    
    def __getattr__(self, name):
        """Hack to establish a new AuthServiceProxy every time this is called"""
        rpc_uri = f"http://{settings.RPC_USERNAME}:{settings.RPC_PASSWORD}@{settings.RPC_IP}:{settings.RPC_PORT}"
        rpc = AuthServiceProxy(rpc_uri)
        return getattr(rpc, name)


class BTCD:
    
    def __getattr__(self, name):
        """Hack to establish a new AuthServiceProxy every time this is called"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        rpc_uri = f"https://{settings.BTCD_USERNAME}:{settings.BTCD_PASSWORD}@{settings.BTCD_IP}:{settings.BTCD_PORT}"
        rpc = AuthServiceProxy(rpc_uri, context=context)
        return getattr(rpc, name)

