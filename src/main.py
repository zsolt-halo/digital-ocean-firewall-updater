from dotenv import load_dotenv
import os
import json
import requests
from updates import get_inbound_rule_dict_for_ip

load_dotenv()


def main():
    token = os.getenv("DIGITAL_OCEAN_PAT")
    auth = {"Authorization": f"Bearer {token}"}

    my_current_public_ip = requests.get("https://api.ipify.org").text

    current_firewall_rules = requests.get(
        "https://api.digitalocean.com/v2/firewalls/bd8e9abd-4000-4b1f-94da-0c570ad896f2",
        headers=auth,
    ).json()
    current_inbound_rules = current_firewall_rules.get("firewall").get(
        "inbound_rules", {}
    )

    if len(current_inbound_rules) != 0:
        print(
            f"[+] Deleting current inbound rules: \n {json.dumps(current_inbound_rules, indent=2)}"
        )
        rsp = requests.delete(
            "https://api.digitalocean.com/v2/firewalls/bd8e9abd-4000-4b1f-94da-0c570ad896f2/rules",
            headers=auth,
            json={"inbound_rules": current_inbound_rules},
        )
        if rsp.status_code == 204:
            print("[+] Successfully deleted current inbound rules")
        else:
            print(f"[x] Failed to delete current inbound rules: {rsp.status_code}")

    new_inbound_rule = get_inbound_rule_dict_for_ip(my_current_public_ip)

    print(
        f"[+] Creating new inbound rules: \n {json.dumps(new_inbound_rule, indent=2)}"
    )
    rsp = requests.post(
        "https://api.digitalocean.com/v2/firewalls/bd8e9abd-4000-4b1f-94da-0c570ad896f2/rules",
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


if __name__ == "__main__":
    main()
