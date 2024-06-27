from online_processing import parse_online
from excel_processing import parse_excel
from interfaces import (
    ITEM_COSTS,
    Item,
    Product,
    Participant,
    PrimaryDivision,
    Organization,
    OrgWriteUp,
    OrderMethodTotals,
)
from typing import List, Dict
from html_generation.html_file_generation import create_detailed_files
import time


# items need to be initalized to 1. The counter function used to combine dictionaries drops keys where values are 0
# So in order for items to stay in the list, they need to be ininitalized to 1.
# This is accounted for by subrtracting 1 when printing them to the html file
def __initialize_item_dict():
    item_dict: Dict[int, int] = {}
    for sku in ITEM_COSTS:
        item_dict[sku] = 1
    return item_dict


def _print_items(orders):
    for customer_name, order in orders.items():
        print(" " * 8 + f"Customer Name: {customer_name}")
        for item in order:
            print(" " * 10 + f"ItemName: {item.item_name}")
            print(" " * 10 + f"Qty: {item.qty}")
            print(" " * 10 + f"Total Cost: {item.total_cost}")
            print(" " * 10 + f"Notes: {item.notes}")


def _print_partipant(participants):
    for partipant_name, orders in participants.items():
        print(" " * 4 + f"PARTICIPANT {partipant_name}")
        print(" " * 6 + f"SHIP_to_Home ORDERS:")
        print(
            " " * 6
            + f"SHIP_TO_HOME_TOTAL: ${orders.ship_to_home_total.money} {orders.ship_to_home_total.item_cnt}"
        )
        _print_items(orders.ship_to_home)
        print(" " * 6 + f"SHIP_to_Org ORDERS")
        print(
            " " * 6
            + f"SHIP_TO_Org_TOTAL: ${orders.ship_to_org_total.money} {orders.ship_to_org_total.item_cnt}"
        )
        _print_items(orders.ship_to_org)
        print(" " * 6 + f"BROCHURE ORDERS")
        print(
            " " * 6
            + f"Brochure_TOTAL: ${orders.brochure_total.money} {orders.brochure_total.item_cnt}"
        )
        print(" " * 10 + str(orders.brochure))
        print(" " * 6 + "Brochure+Ship2Org:")
        print(" " * 10 + str(orders.quick_pull))


def pretty_print(organization: Organization):
    for primary_div, secondary_divs in organization.primary_divisions.items():
        print(f"PRIMARY DIV {primary_div}")
        for secondary_div, participants in secondary_divs.items():
            print(" " * 2 + f"SECONDARY DIV {secondary_div}")
            _print_partipant(participants)


if __name__ == "__main__":
    organization = Organization("Montclair12u", {})
    org_write_up: OrgWriteUp = OrgWriteUp(
        {},
        __initialize_item_dict(),
        __initialize_item_dict(),
        __initialize_item_dict(),
        OrderMethodTotals(0, 0),
        OrderMethodTotals(0, 0),
        OrderMethodTotals(0, 0),
    )

    # PC
    # excel_file = r"C:/Users/jeffb/OneDrive\Desktop/Projects/mam-fam-file-processing\sample_data/MultiplePrimary.xlsx"
    # excel_file = "../sample_data/CarterHighSchool/CarterCheer.xlsx"
    online_file = "../sample_data/Montclair/Montclair12u.json"

    # MAC
    # excel_file = r"sample_data/MultiplePrimary.xlsx"
    # online_file = r"/Users/jeffreyhover/Desktop/Programs/mam-fam-file-processing/sample_data/Blackshear/Blackshear.json"

    # parse_excel(organization=organization, file=excel_file, org_write_up=org_write_up)
    parse_online(organization=organization, file=online_file, org_write_up=org_write_up)
    # pretty_print(organization)
    create_detailed_files(organization, org_write_up)
