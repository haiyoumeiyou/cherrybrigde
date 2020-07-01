from typing import List

import ssl
import ldap3
from ldap3 import Connection, Server, ALL, NTLM, Tls
import instance.ldap_conf as def_conf 


if_not = lambda x, y: x if x is not None else y

class LdapHandler(object):
    def __init__(self, conf=None):
        self.conf = if_not(conf, def_conf)
        self.tls_config = Tls(
            validate=ssl.CERT_NONE,
            version=ssl.PROTOCOL_TLSv1
        )
        self.server = Server(
            self.conf.LDAP_DOMAIN,
            get_info=ALL,
            use_ssl=conf.LDAP_USE_SSL,
            tls=self.tls_config
        )

    def _create_conn(self, uname:str=None, upass:str=None):
        return Connection(
            self.server,
            user=if_not(uname, self.conf.LDAP_BIND_USER_DN),
            password=if_not(upass, self.conf.LDAP_BIND_USER_PASSWORD),
            authentication=NTLM,
            auto_range=True
        )

    def _close_conn(self, conn):
        conn.unbind()

    def get_selve(self, search_base:str=None, search_string:str=None, attrs:List=[], size_limit:int=None):
        with self._create_conn() as conn:
            try:
                conn.search(
                    search_base=if_not(search_base, self.conf.LDAP_BASE_DN),
                    search_filter=search_string,
                    attributes=attrs,
                    size_limit=if_not(size_limit, 50)
                )
                if len(conn.entries) > 0:
                    return True, conn.entries
                return False, None
            except Exception as Err:
                return False, Err

    def remove_self(self, search_base:str=None, search_string:str=None, x_attrs:List=[]):
        d_attrs = ['distinguishedName']
        attrs = list(set(d_attrs)|set(x_attrs))
        with self._create_conn() as conn:
            try:
                conn.search(
                    if_not(search_base, self.conf.LDAP_BASE_DN),
                    search_string,
                    attributes=attrs
                )
                if len(conn.entries) == 1:
                    entry = conn.entries[0]
                    try:
                        conn.delete(str(entry[d_attrs[0]]))
                        return True, conn.result
                    except Exception as Err:
                        return False, Err
            except Exception as Err:
                return False, Err


class OnPremADHandler(object):
    def __init__(self, onprem_conf=def_conf):
        self.onprem_ad = LdapHandler(onprem_conf)

    def find_devices(self, device_name, search_base):
        search_base = 'OU={},DC=hlpusd,DC=k12,DC=ca,DC=us'.format(search_base)
        search_string = '(&(objectClass=computer)(sAMAccountName={}*))'.format(device_name)
        attributes=['name','distinguishedName','lastLogon','operatingSystem']
        # print(search_string, search_base, attributes)
        return self.onprem_ad.get_selve(search_base, search_string, attributes, 10)


# ad = OnPremADHandler()

# devices = ad.find_devices('103', '_Workstations')

# print(devices)
