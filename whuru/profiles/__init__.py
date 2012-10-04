from webfinger import rel
import datetime
from xrd import XRD, Link

def webfinger_handler(acct, xrd):
    # acct.userinfo is the username
    # acct.host is the host
    xrd.aliases.append('http://example.com/profile/%s/' % acct.userinfo)
    xrd.expires = datetime.datetime.utcnow() + datetime.timedelta(0, 10)
    xrd.links.append(Link(
        rel=rel.AUTHOR,
        href='http://jeremy.carbauja.com',
        type_='text/html',
    ))
