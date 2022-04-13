from dotenv import load_dotenv
import os
import click
import utils


load_dotenv()

TOKEN = os.getenv("DIGITAL_OCEAN_PAT")
FW_ID = os.getenv("DIGITAL_OCEAN_FIREWALL_ID")
AUTH = {"Authorization": f"Bearer {TOKEN}"}


@click.group()
def cli():
    pass


@cli.command()
def fw_open():
    current_firewall_rules = utils.get_current_inboud_rules_for_firewall(
        firewall_id=FW_ID, auth=AUTH
    )
    utils.delete_firewall_rules(
        firewall_id=FW_ID, auth=AUTH, rules=current_firewall_rules
    )
    utils.add_current_ip_to_firewall_opening(firewall_id=FW_ID, auth=AUTH)


@cli.command()
def fw_close():
    current_firewall_rules = utils.get_current_inboud_rules_for_firewall(
        firewall_id=FW_ID, auth=AUTH
    )
    utils.delete_firewall_rules(
        firewall_id=FW_ID, auth=AUTH, rules=current_firewall_rules
    )


if __name__ == "__main__":
    cli()
