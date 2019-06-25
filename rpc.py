import ssl
import toml

from flask import current_app, request

from bitcoinrpc.authproxy import AuthServiceProxy


class RPCWrapper:
    
    template = "{TRANSPORT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    
    def __init__(self, node, network):
        self.node = node
        self.network = network
        self.url = self.template.format(**toml.load('settings.toml')[node][network])

    def proxy(self):
        return AuthServiceProxy(self.url, context=self.context())

    def context(self):
        if self.node == 'btcd':
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        else:
            context = None
        return context

    def __getattr__(self, name):
        """Hack to establish a new AuthServiceProxy every time this is called"""
        return getattr(self.proxy(), name)


class RPCRouter:

    def __init__(self, node):
        self.node = node
        self.testnet = RPCWrapper(node, 'testnet')
        self.mainnet = RPCWrapper(node, 'mainnet')

    def __getattr__(self, name):
        if current_app and 'testnet' in request.path:
            return getattr(self.testnet, name)
        else:
            return getattr(self.mainnet, name)
