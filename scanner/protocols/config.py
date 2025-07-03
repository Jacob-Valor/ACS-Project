"""
Protocol configurations and service payloads
"""

# Common ports mapping
COMMON_PORTS = {
    21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 53: 'dns',
    80: 'http', 110: 'pop3', 143: 'imap', 443: 'https', 445: 'smb',
    993: 'imap', 995: 'pop3', 1433: 'mssql', 3306: 'mysql', 3389: 'rdp',
    5432: 'postgresql', 5900: 'vnc', 5901: 'vnc', 6379: 'redis',
    8080: 'http', 8443: 'https', 161: 'snmp', 162: 'snmp'
}

# Service detection payloads
SERVICE_PAYLOADS = {
    'http': {
        'payload': b'GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n',
        'expected': [b'HTTP/', b'html', b'<html'],
        'port': 80
    },
    'https': {
        'payload': b'GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n',
        'expected': [b'HTTP/', b'html', b'<html'],
        'port': 443,
        'ssl': True
    },
    'ftp': {
        'payload': b'USER anonymous\r\n',
        'expected': [b'220', b'FTP', b'530', b'331'],
        'port': 21
    },
    'ssh': {
        'payload': b'SSH-2.0-Scanner\r\n',
        'expected': [b'SSH-', b'Protocol mismatch'],
        'port': 22
    },
    'smtp': {
        'payload': b'EHLO scanner.local\r\n',
        'expected': [b'220', b'250', b'SMTP', b'mail'],
        'port': 25
    },
    'pop3': {
        'payload': b'USER test\r\n',
        'expected': [b'+OK', b'POP3', b'-ERR'],
        'port': 110
    },
    'imap': {
        'payload': b'A001 CAPABILITY\r\n',
        'expected': [b'* OK', b'IMAP', b'CAPABILITY'],
        'port': 143
    },
    'telnet': {
        'payload': b'\xFF\xFB\x01\xFF\xFB\x03\xFF\xFC\x27',
        'expected': [b'\xFF', b'login:', b'Username:', b'Password:'],
        'port': 23
    },
    'smb': {
        'payload': b'\x00\x00\x00\x85\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfe\x00\x00\x00\x00\x00\x62\x00\x02\x50\x43\x20\x4e\x45\x54\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31\x2e\x30\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00',
        'expected': [b'SMB', b'\xff\x53\x4d\x42'],
        'port': 445
    },
    'dns': {
        'payload': b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01',
        'expected': [b'\x12\x34', b'\x81\x80', b'\x81\x83'],
        'port': 53,
        'udp': True
    },
    'rdp': {
        'payload': b'\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00',
        'expected': [b'\x03\x00\x00\x0b\x06\xd0', b'\x03\x00\x00\x13'],
        'port': 3389
    },
    'vnc': {
        'payload': b'RFB 003.008\n',
        'expected': [b'RFB ', b'003.'],
        'port': 5900
    },
    'mysql': {
        'payload': b'',
        'expected': [b'\x0a', b'mysql', b'\x00\x00\x00\x0a'],
        'port': 3306
    },
    'postgresql': {
        'payload': b'\x00\x00\x00\x08\x04\xd2\x16\x2f',
        'expected': [b'SCRAM-SHA-256', b'md5', b'trust'],
        'port': 5432
    },
    'redis': {
        'payload': b'*1\r\n$4\r\nINFO\r\n',
        'expected': [b'redis_version', b'$', b'+PONG', b'-NOAUTH'],
        'port': 6379
    },
    'snmp': {
        'payload': b'\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa0\x19\x02\x04\x00\x00\x00\x01\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00',
        'expected': [b'\x30', b'\x02\x01\x01'],
        'port': 161,
        'udp': True
    }
}