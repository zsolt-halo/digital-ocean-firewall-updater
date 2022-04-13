import requests
import json
from updates import get_inbound_rule_dict_for_ip


def get_public_ip():
    return requests.get("https://api.ipify.org").text


def get_current_inboud_rules_for_firewall(firewall_id, auth):
    current_firewall_rules = requests.get(
        f"https://api.digitalocean.com/v2/firewalls/{firewall_id}",
        headers=auth,
    ).json()
    current_inbound_rules = current_firewall_rules.get("firewall").get(
        "inbound_rules", {}
    )
    return current_inbound_rules


def delete_firewall_rules(firewall_id, auth, rules):
    if len(rules) == 0:
        print("[+] No rules to delete")
        return
    rsp = requests.delete(
        f"https://api.digitalocean.com/v2/firewalls/{firewall_id}/rules",
        headers=auth,
        json={"inbound_rules": rules},
    )
    if rsp.status_code == 204:
        print("[+] Successfully deleted current inbound rules")
    else:
        print(f"[x] Failed to delete current inbound rules: {rsp.status_code}")
        print(f"[x] Failed to delete current inbound rules, response: {rsp.text}")


def add_current_ip_to_firewall_opening(firewall_id, auth):
    my_current_public_ip = get_public_ip()
    new_inbound_rule = get_inbound_rule_dict_for_ip(my_current_public_ip)

    print(
        f"[+] Creating new inbound rules: \n {json.dumps(new_inbound_rule, indent=2)}"
    )
    rsp = requests.post(
        f"https://api.digitalocean.com/v2/firewalls/{firewall_id}/rules",
        headers=auth,
        json=new_inbound_rule,
    )
    if rsp.status_code == 204:
        print("[+] Successfully deleted current inbound rules")
    else:
        print(
            f"[x] Failed to delete current inbound rules, status code: {rsp.status_code}"
        )
        print(f"[x] Failed to delete current inbound rules, response: {rsp.text}")
