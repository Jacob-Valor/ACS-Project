"""
Service payloads and port mappings for service detection.
"""

# Common port to service mappings
COMMON_PORTS = {
    21: 'ftp',
    22: 'ssh',
    23: 'telnet',
    25: 'smtp',
    53: 'dns',
    80: 'http',
    110: 'pop3',
    143: 'imap',
    443: 'https',
    993: 'imaps',
    995: 'pop3s',
    3306: 'mysql',
    5432: 'postgresql',
    6379: 'redis',
    8080: 'http-alt',
    8443: 'https-alt'
}

# Service-specific payloads for probing
SERVICE_PAYLOADS = {
    'http': b'GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n',
    'https': b'GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n',
    'ftp': b'USER anonymous\r\n',
    'ssh': b'\n',
    'smtp': b'EHLO localhost\r\n',
    'pop3': b'USER test\r\n',
    'imap': b'A001 CAPABILITY\r\n',
    'mysql': b'\x3a\x00\x00\x00\x85\xa2\x1e\x00\x00\x00\x00\x40\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x72\x6f\x6f\x74\x00\x00',
    'redis': b'*1\r\n$4\r\nINFO\r\n'
}

# Generic payloads to try when service is unknown
GENERIC_PAYLOADS = [
    b'HEAD / HTTP/1.0\r\n\r\n',
    b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n',
    b'OPTIONS * HTTP/1.1\r\nHost: localhost\r\n\r\n',
    b'\r\n',
    b'\n'
]