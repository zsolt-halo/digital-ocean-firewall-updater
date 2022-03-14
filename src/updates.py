def get_inbound_rule_dict_for_ip(ip):
    return {
        "inbound_rules": [
            {
                "protocol": "tcp",
                "ports": "22",
                "sources": {"addresses": [ip]},
            }
        ],
    }


def get_outboudn_rule_allow_all():
    return {
        "outbound_rules": [
            {
                "protocol": "icmp",
                "ports": "0",
                "destinations": {"addresses": ["0.0.0.0/0", "::/0"]},
            },
            {
                "protocol": "tcp",
                "ports": "0",
                "destinations": {"addresses": ["0.0.0.0/0", "::/0"]},
            },
            {
                "protocol": "udp",
                "ports": "0",
                "destinations": {"addresses": ["0.0.0.0/0", "::/0"]},
            },
        ],
    }
