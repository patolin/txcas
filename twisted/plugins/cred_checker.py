
# Application modules
import txcas.settings

_scp = txcas.settings.load_settings('cas', syspath='/etc/cas')

if txcas.settings.has_options(_scp, {'LDAP': ['host', 'port', 'basedn', 'binddn', 'bindpw']}):
    from txcas.ldap_cred_checker import LDAPSimpleBindChecker
    ldap_simple_bind_cred_checker = LDAPSimpleBindChecker(
                                    host=_scp.get('LDAP', 'host'),
                                    port=_scp.getint('LDAP', 'port'),
                                    basedn=_scp.get('LDAP', 'basedn'),
                                    binddn=_scp.get('LDAP', 'binddn'),
                                    bindpw=_scp.get('LDAP', 'bindpw'))
del _scp

