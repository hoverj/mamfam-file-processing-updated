import pandas as pd
from interfaces import (
    ITEM_COSTS,
    Item,
    Product,
    Participant,
    PrimaryDivision,
    Organization,
    OnlineLineDetails,
    OrgWriteUp,
    initalize_participant,
)
from typing import Dict
from collections import Counter

columns_to_return = [
    "billing_first_name",
    "billing_last_name",
    "shipping_method_title",
    "USER_user_registration_grade_division",
    "USER_user_registration_coach_teacher",
    "USER_user_registration_customer_participant",
    "products",
]


def online_line_parser(online_line_item):
    # Get primary division and set to unknown if blank
    primary_division = str(
        online_line_item["USER_user_registration_grade_division"]
    ).lower()
    primary_division = primary_division if primary_division != "" else "Unknown"

    # Get secondary division and set to unknown if blank
    secondary_division = str(
        online_line_item["USER_user_registration_coach_teacher"]
    ).lower()
    secondary_division = secondary_division if secondary_division != "" else "Unknown"

    # Get online_line_item details
    customer_name = (
        online_line_item["billing_first_name"]
        + " "
        + online_line_item["billing_last_name"]
    )
    partipant_name = online_line_item[
        "USER_user_registration_customer_participant"
    ].lower()

    return OnlineLineDetails(
        primary_div_name=primary_division,
        secondary_div_name=secondary_division,
        customer_name=customer_name,
        participant_name=partipant_name,
    )


def online_match_definer(order_details: OnlineLineDetails, organization: Organization):
    "Returns a string of the deepest level match found"
    pri_div = order_details.primary_div_name
    sec_div = order_details.secondary_div_name
    participant = order_details.participant_name

    # FOR NOW PRIMARY AND SECONDARY WILL BE UNKNOWN
    # CAN BE REMOVED AFTER RELIABLE WAY TO GET INFO IS DISCOVERED
    pri_div = "Unknown"
    sec_div = "Unknown"

    if pri_div in organization.primary_divisions.keys():
        # Primary Match exists, check secondary Match
        if sec_div in organization.primary_divisions[pri_div].keys():
            # Secondary Match Exists, check partcipant
            if participant in organization.primary_divisions[pri_div][sec_div].keys():
                return "participant_match"
            else:
                return "secondary_match"
        else:
            # Primary Match Exists, but Secondary Doesn't
            return "primary_match"
    else:
        return "no_match"


def get_data_frame(online_file):
    dataframe = pd.read_json(online_file)
    dataframe = dataframe.loc[:, dataframe.columns.intersection(columns_to_return)]
    dataframe = dataframe.dropna(how="all")
    return dataframe


def get_desgin(pr_line) -> str:
    desgin = (
        pr_line["music-design"]
        + pr_line["occupational-design"]
        + pr_line["general-design"]
        + pr_line["baseball-design"]
        + pr_line["basketball-design"]
        + pr_line["dance-design"]
        + pr_line["football-design"]
        + pr_line["soccer-design"]
        + pr_line["softball-design"]
        + pr_line["cheer-design"]
    )
    start_index = desgin.find("title=")
    end_index = desgin.find("><img class")
    return desgin[start_index + 7 : end_index - 1]


def iterate_products(
    participant_orders: Dict[str, Dict[int, Product]],
    online_details: OnlineLineDetails,
    products_ordered,
):
    customer_name = online_details.customer_name
    order_total = 0
    item_total = 0
    profit_total = 0
    product_dict = {}
    if customer_name not in participant_orders:
        participant_orders[customer_name] = []

    for product in products_ordered:
        name = product["name"]
        design = get_desgin(product) if get_desgin(product) != "" else "N/A"
        size = product["size"] if product["size"] != "" else "N/A"
        font = product["font"] if product["font"] != "" else "N/A"
        qty = int(product["qty"])
        color = (
            product["attribute_color"] if product["attribute_color"] != "" else "N/A"
        )
        sku = int(product["sku"])
        item_price = product["item_price"]
        profit = ITEM_COSTS[sku].percent_profit * qty * item_price
        product = Product(
            sku=sku,
            item_name=name,
            qty=qty,
            total_cost=qty * item_price,
            notes=f"Design: {design}~Font: {font}~Size: {size}~Color: {color}",
        )
        item_total += qty
        order_total += qty * item_price
        profit_total += profit
        if sku in product_dict:
            product_dict[sku] += qty
        else:
            product_dict[sku] = qty
        (participant_orders[customer_name]).append(product)
    return order_total, item_total, profit_total, product_dict


def add_order_to_participant(
    organization: Organization,
    order_details: OnlineLineDetails,
    order_type: str,
    products,
):
    pri_div = order_details.primary_div_name
    sec_div = order_details.secondary_div_name
    participant = order_details.participant_name

    # FOR NOW PRIMARY AND SECONDARY WILL BE UNKNOWN
    # CAN BE REMOVED AFTER RELIABLE WAY TO GET INFO IS DISCOVERED
    pri_div = "Unknown"
    sec_div = "Unknown"

    if order_type == "Home":
        participant_orders = organization.primary_divisions[pri_div][sec_div][
            participant
        ].ship_to_home
        totals_reference = organization.primary_divisions[pri_div][sec_div][
            participant
        ].ship_to_home_total
        return_totals = iterate_products(
            participant_orders=participant_orders,
            online_details=order_details,
            products_ordered=products,
        )
        totals_reference.money += return_totals[0]
        totals_reference.item_cnt += return_totals[1]
        totals_reference.profit_generated += return_totals[2]

    elif order_type == "Org":
        participant_orders = organization.primary_divisions[pri_div][sec_div][
            participant
        ].ship_to_org
        totals_reference = organization.primary_divisions[pri_div][sec_div][
            participant
        ].ship_to_org_total
        return_totals = iterate_products(
            participant_orders=participant_orders,
            online_details=order_details,
            products_ordered=products,
        )
        totals_reference.money += return_totals[0]
        totals_reference.item_cnt += return_totals[1]
        totals_reference.profit_generated += return_totals[2]
        quick_pull = organization.primary_divisions[pri_div][sec_div][
            participant
        ].quick_pull
        quick_pull = dict(Counter(quick_pull) + Counter(return_totals[3]))
        organization.primary_divisions[pri_div][sec_div][
            participant
        ].quick_pull = quick_pull

    else:
        raise NameError("Unknown order type Error")
    return Counter(return_totals[3])


def make_participant_entry(
    organization: Organization, order_details: OnlineLineDetails
):
    pri_div = order_details.primary_div_name
    sec_div = order_details.secondary_div_name
    participant = order_details.participant_name

    # FOR NOW PRIMARY AND SECONDARY WILL BE UNKNOWN
    # CAN BE REMOVED AFTER RELIABLE WAY TO GET INFO IS DISCOVERED
    pri_div = "Unknown"
    sec_div = "Unknown"

    organization.primary_divisions[pri_div][sec_div][
        participant
    ] = initalize_participant()


def make_secondary_entry(organization: Organization, order_details: OnlineLineDetails):
    pri_div = order_details.primary_div_name
    sec_div = order_details.secondary_div_name

    # FOR NOW PRIMARY AND SECONDARY WILL BE UNKNOWN
    # CAN BE REMOVED AFTER RELIABLE WAY TO GET INFO IS DISCOVERED
    pri_div = "Unknown"
    sec_div = "Unknown"

    organization.primary_divisions[pri_div][sec_div] = {}


def make_primary_entry(organization: Organization, order_details: OnlineLineDetails):
    pri_div = order_details.primary_div_name

    # FOR NOW PRIMARY AND SECONDARY WILL BE UNKNOWN
    # CAN BE REMOVED AFTER RELIABLE WAY TO GET INFO IS DISCOVERED
    pri_div = "Unknown"

    organization.primary_divisions[pri_div] = {}


def ship_to_home_order(
    organization: Organization,
    order_details: OnlineLineDetails,
    order,
):
    match online_match_definer(order_details=order_details, organization=organization):
        case "no_match":
            make_primary_entry(organization, order_details)
            make_secondary_entry(organization, order_details)
            make_participant_entry(organization, order_details)
        case "primary_match":
            make_secondary_entry(organization, order_details)
            make_participant_entry(organization, order_details)
        case "secondary_match":
            make_participant_entry(organization, order_details)
        case "participant_match":
            pass
        case _:
            raise NameError("Match Not Found")
    return add_order_to_participant(
        organization=organization,
        order_details=order_details,
        order_type="Home",
        products=order,
    )


def ship_to_org_order(
    organization: Organization,
    order_details: OnlineLineDetails,
    order,
):
    match online_match_definer(order_details=order_details, organization=organization):
        case "no_match":
            make_primary_entry(organization, order_details)
            make_secondary_entry(organization, order_details)
            make_participant_entry(organization, order_details)
        case "primary_match":
            make_secondary_entry(organization, order_details)
            make_participant_entry(organization, order_details)
        case "secondary_match":
            make_participant_entry(organization, order_details)
        case "participant_match":
            pass
        case _:
            raise NameError("Match Not Found")
    return add_order_to_participant(
        organization=organization,
        order_details=order_details,
        order_type="Org",
        products=order,
    )


def iterate_orders(organization: Organization, org_write_up: OrgWriteUp, dataframe):
    for _, line in dataframe.iterrows():
        online_details: OnlineLineDetails = online_line_parser(line)
        if line["shipping_method_title"] == "Ship to Organization" or line["shipping_method_title"] == "Ship to Organizaton":
            old_ship = Counter(org_write_up.ship_to_org)
            new_dict = (
                ship_to_org_order(organization, online_details, line["products"])
                + old_ship
            )
            org_write_up.ship_to_org = dict(new_dict)
        else:
            old_ship = Counter(org_write_up.ship_to_home)
            new_dict = (
                ship_to_home_order(organization, online_details, line["products"])
                + old_ship
            )
            org_write_up.ship_to_home = dict(new_dict)


def parse_online(file: str, organization: Organization, org_write_up: OrgWriteUp):
    dataframe = get_data_frame(file)
    iterate_orders(organization, org_write_up, dataframe)
