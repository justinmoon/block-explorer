import ssl
import toml

from bitcoinrpc.authproxy import AuthServiceProxy

from flask import request


class RPC:
    url_template = "http://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    
    def __init__(self, node='bitcoind', network=None):
        assert node in ('bitcoind', 'btcd')
        self.node = node
        assert network in (None, 'mainnet', 'testnet')
        self.network = network
        self.settings = toml.load('settings.toml')

    def url(self):
        # a dirty hack to avoid storing global state
        if self.network is None:
            network = 'testnet' if 'testnet' in request.path else 'mainnet'
        params = self.settings[self.node][network]
        return self.url_template.format(**params)
    
    def __getattr__(self, name):
        """Hack to establish a new AuthServiceProxy every time this is called"""
        context = None
        if self.node == 'btcd':
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        rpc = AuthServiceProxy(self.url(), context=context)
        return getattr(rpc, name)

