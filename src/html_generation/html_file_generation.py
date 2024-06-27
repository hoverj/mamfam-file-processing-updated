import os
from weasyprint import HTML
from typing import Dict, List
from interfaces import (
    ITEM_COSTS,
    Item,
    Product,
    Participant,
    PrimaryDivision,
    Organization,
    OrgWriteUp,
    OnlineLineDetails,
    initalize_participant,
)
from collections import Counter
from html_generation.html_constants import *

OUTPUT_FILE = os.path.abspath("../output")
HTML_STYLE = os.path.abspath("../src/html_generation/file_generation.css")
LOGO = os.path.abspath("../src/html_generation/Logo.png")


def create_folder(path_to_org: str, folder_to_create: str):
    os.makedirs(f"{path_to_org}/{folder_to_create}", exist_ok=True)


def create_organization_folder(org_name: str):
    os.makedirs(f"{OUTPUT_FILE}/{org_name}", exist_ok=True)


def _update_org_pulling(participant: Participant, org_pulling: OrgWriteUp):
    # Add the current participants totals to the org total
    org_pulling.ship_to_home_total.item_cnt += participant.ship_to_home_total.item_cnt
    org_pulling.ship_to_home_total.money += participant.ship_to_home_total.money

    # Add the current participants totals to the org total
    org_pulling.ship_to_org_total.item_cnt += participant.ship_to_org_total.item_cnt
    org_pulling.ship_to_org_total.money += participant.ship_to_org_total.money

    org_pulling.brochure_total.money += participant.brochure_total.money
    org_pulling.brochure_total.item_cnt += participant.brochure_total.item_cnt

    temp_dict = org_pulling.quick_pull
    new_dict = dict(Counter(temp_dict) + Counter(participant.quick_pull))
    org_pulling.quick_pull = new_dict


def _make_ship_to_home_table(participant: Participant):
    ship_to_home_table = SHIP_TO_HOME_TABLE_START

    ship_to_home = participant.ship_to_home
    for orderer, items_ordered in ship_to_home.items():
        for product in items_ordered:
            note_array = product.notes.split("~")
            ship_to_home_table += f"""
            <tr>
            <td>{orderer}</td>
            <td>{product.item_name}</td>
            <td>{product.qty}</td>
            <td>${product.total_cost}</td>
            <td>{note_array[0]} {note_array[1]} {note_array[2]}</td>
            </tr>
            """
    ship_to_home_table += END_TABLE
    return ship_to_home_table


def _make_ship_to_org_table(participant: Participant):
    ship_to_org_table = SHIP_TO_ORG_TABLE_START

    ship_to_org = participant.ship_to_org

    for orderer, items_ordered in ship_to_org.items():
        for product in items_ordered:
            note_array = product.notes.split("~")
            ship_to_org_table += f"""
            <tr>
            <td>{orderer}</td>
            <td>{product.item_name}</td>
            <td>{product.qty}</td>
            <td>${product.total_cost}</td>
            <td>{note_array[0]} {note_array[1]} {note_array[2]}</td>
            </tr>
            """
    ship_to_org_table += END_TABLE
    return ship_to_org_table


def _make_brochure_table(participant: Participant):
    brochure_table = BROCHURE_TABLE_START

    for sku, qty in participant.brochure.items():
        brochure_table += f"""
        <tr>
        <td>{ITEM_COSTS[sku].name}</td>
        <td>{int(qty)}</td>
        <td>${ITEM_COSTS[sku].price*qty}</td>
        </tr>
        """

    brochure_table += END_TABLE
    return brochure_table


def items_sold_page(org_write_up: OrgWriteUp, org_name: str):
    org_sold = HTML_BOILER_PLATE_ORG_LEVEL_START
    org_sold += f"""
        <header>
            <div class="center">
        <p>{org_name} Organization Summary</p>
            </div>
        </header>
        <br>
    """
    org_sold += ORG_ITEMS_SOLD_TABLE_START
    for sku in ITEM_COSTS:
        total_items = (
            org_write_up.brochure[sku]
            + org_write_up.ship_to_home[sku]
            + org_write_up.ship_to_org[sku]
        ) - 3
        org_sold += f"""
        <tr>
        <td>{ITEM_COSTS[sku].name}</td>
        <td>{int(org_write_up.ship_to_org[sku] - 1)}</td>
        <td>{int(org_write_up.ship_to_home[sku] - 1)}</td>
        <td>{int(org_write_up.brochure[sku] - 1)}</td>
        <td>{int(total_items)}</td>
        </tr>
    """

    org_sold += END_TABLE
    org_sold += HTML_END

    output_file = f"{OUTPUT_FILE}/{org_name}/Organization/items_sold.pdf"

    HTML(string=org_sold).write_pdf(
        output_file,
        stylesheets=[f"{HTML_STYLE}"],
        presentational_hints=True,
        zoom=1.0,
        resolution=300,
        enable_hinting=True,
        embed_fonts=True,
        font_config=None,
        base_url=None,
        attachments=None,
        **{"page-size": "Letter", "orientation": "portrait"},
    )


def _make_total_table(participant: Participant):
    total_table = PARTICIPANT_DETAILED_TOTAL_TABLE_START

    home = participant.ship_to_home_total
    org = participant.ship_to_org_total
    brochure = participant.brochure_total

    money_total = home.money + org.money + brochure.money
    item_total = home.item_cnt + org.item_cnt + brochure.item_cnt

    total_table += f"""
    <tr>
    <td>Ship to Organization</td>
    <td>{int(org.item_cnt)}</td>
    <td>${org.money}</td>
    </tr>
    <tr>
    <td>Brochure Sales</td>
    <td>{int(brochure.item_cnt)}</td>
    <td>${brochure.money}</td>
    </tr>
    <tr>
    <td>Ship To Home</td>
    <td>{int(home.item_cnt)}</td>
    <td>${home.money}</td>
    </tr>
    <tr>
    <td>Order Totals</td>
    <td>{int(item_total)}</td>
    <td>${money_total}</td>
    </tr>
    """
    total_table += END_TABLE
    return total_table


def _get_total_items_from_participant(participant: Participant):
    return (
        participant.ship_to_home_total.item_cnt
        + participant.ship_to_org_total.item_cnt
        + participant.brochure_total.item_cnt
    )


def _get_total_money_from_participant(participant: Participant):
    return (
        participant.ship_to_home_total.money
        + participant.ship_to_org_total.money
        + participant.brochure_total.money
    )


def _create_participant_header(
    org_name: str,
    primary_div: str,
    secondary_div: str,
    participant_name: str,
    document_type: str,
    participant_order: Participant,
):
    participant_header = HTML_BOILER_PLATE_START

    participant_header += f"""
    <header>
        <div class="center">
     <p>{document_type} Student Summary</p>
        </div>
    </header>
    <br>
<div>
    <div style="flex: 1;">
        <span class="file_header"><b>Participant Name:</b> <u>{participant_name}</u></span>
        <span class="file_header"><b>Total Items Sold:</b> <u>{_get_total_items_from_participant(participant_order)}</u></span>
        <span class="file_header"><b>Total Collected:</b> <u>${_get_total_money_from_participant(participant_order)}</u></span>

    </div>
    <div style="flex: 1;">
        <span class="file_header"><b>Organization:</b> <u>{org_name}</u></span>
        <span class="file_header"><b>Primary Div:</b> <u>{primary_div}</u></span>
        <span class="file_header"><b>Secondary Div:</b> <u>{secondary_div}</u></span>
        
    </div>
</div>

    """
    return participant_header


def create_quick_table_body(quick_pull: Dict[int, int]):
    table_body = ""
    for sku, qty in quick_pull.items():
        table_body += f"""
        <tr>
        <td>{ITEM_COSTS[sku].name}</td>
        <td>{int(qty)}</td>
        <td>${ITEM_COSTS[sku].price*qty}</td>
        </tr>
        """
    return table_body


def create_quick_par_file(
    org_name: str,
    primary_div: str,
    secondary_div: str,
    participant_name: str,
    participant_order: Participant,
):
    participant_quick = _create_participant_header(
        org_name=org_name,
        primary_div=primary_div,
        secondary_div=secondary_div,
        participant_name=participant_name,
        document_type="Quick",
        participant_order=participant_order,
    )
    participant_quick += PARTICIPANT_QUICK_TABLE_START
    participant_quick += create_quick_table_body(
        dict(sorted(participant_order.quick_pull.items()))
    )

    participant_quick += HTML_END
    output_file = f"{OUTPUT_FILE}/{org_name}/{primary_div}/{secondary_div}/{participant_name}/{participant_name}-quick.pdf"

    HTML(string=participant_quick).write_pdf(
        output_file,
        stylesheets=[f"{HTML_STYLE}"],
        presentational_hints=True,
        zoom=1.0,
        resolution=300,
        enable_hinting=True,
        embed_fonts=True,
        font_config=None,
        base_url=None,
        attachments=None,
        **{"page-size": "Letter", "orientation": "portrait"},
    )
    # with open(output_file, "w") as f:
    #     f.write(participant_quick)


def create_detailed_par_file(
    org_name: str,
    primary_div: str,
    secondary_div: str,
    participant_name: str,
    participant_order: Participant,
):
    participant_detailed = _create_participant_header(
        org_name=org_name,
        primary_div=primary_div,
        secondary_div=secondary_div,
        participant_name=participant_name,
        document_type="Detailed",
        participant_order=participant_order,
    )

    ship_to_home = _make_ship_to_home_table(participant_order)
    ship_to_org = _make_ship_to_org_table(participant_order)
    brochure = _make_brochure_table(participant_order)
    total_table = _make_total_table(participant_order)

    participant_detailed += ship_to_org
    participant_detailed += brochure
    participant_detailed += ship_to_home
    participant_detailed += total_table

    participant_detailed += HTML_END
    output_file = f"{OUTPUT_FILE}/{org_name}/{primary_div}/{secondary_div}/{participant_name}/{participant_name}-detailed.pdf"

    HTML(string=participant_detailed).write_pdf(
        output_file,
        stylesheets=[f"{HTML_STYLE}"],
        presentational_hints=True,
        zoom=1.0,
        resolution=300,
        enable_hinting=True,
        embed_fonts=True,
        font_config=None,
        base_url=None,
        attachments=None,
        **{"page-size": "Letter", "orientation": "portrait"},
    )


def quick_organization_pull(org_name: str, org_pull: OrgWriteUp):
    create_folder(f"{OUTPUT_FILE}/{org_name}", "Organization")

    org_file = HTML_BOILER_PLATE_ORG_LEVEL_START
    org_file += f"""
        <header>
            <div class="center">
        <p>{org_name} Organization Summary</p>
            </div>
        </header>
        <br>
    """

    org_file += PARTICIPANT_QUICK_TABLE_START
    org_file += create_quick_table_body(dict(sorted(org_pull.quick_pull.items())))

    org_file += HTML_END
    output_file = f"{OUTPUT_FILE}/{org_name}/Organization/quick_pull.pdf"

    HTML(string=org_file).write_pdf(
        output_file,
        stylesheets=[f"{HTML_STYLE}"],
        presentational_hints=True,
        zoom=1.0,
        resolution=300,
        enable_hinting=True,
        embed_fonts=True,
        font_config=None,
        base_url=None,
        attachments=None,
        **{"page-size": "Letter", "orientation": "portrait"},
    )


def iterate_primary_divs(organization: Organization, org_pulling: OrgWriteUp):
    output_origin = f"{OUTPUT_FILE}/{organization.organization_name}"
    for primary_div, secondary_div_list in organization.primary_divisions.items():
        # Create primary div folder
        create_folder(output_origin, primary_div)
        for secondary_div, participants in secondary_div_list.items():
            # Create secondary div folder
            create_folder(f"{output_origin}/{primary_div}", secondary_div)
            for participant, order in participants.items():
                # Create participant folder
                create_folder(
                    f"{output_origin}/{primary_div}/{secondary_div}", participant
                )
                create_detailed_par_file(
                    org_name=organization.organization_name,
                    primary_div=primary_div,
                    secondary_div=secondary_div,
                    participant_name=participant,
                    participant_order=order,
                )
                create_quick_par_file(
                    org_name=organization.organization_name,
                    primary_div=primary_div,
                    secondary_div=secondary_div,
                    participant_name=participant,
                    participant_order=order,
                )
                _update_org_pulling(order, org_pulling)


def organization_student_writeup(organization: Organization, org_write_up: OrgWriteUp):
    organization_total_money = 0
    organization_total_items = 0
    primary_total_money = 0
    primary_total_item = 0
    secondary_total_money = 0
    secondary_total_item = 0

    participant_table = ""
    secondary_div_table = ""
    primary_div_table = ""

    org_writeup = HTML_BOILER_PLATE_ORG_LEVEL_START
    org_writeup += """<div class="horizontal">"""
    org_writeup += f"""
        <header>
            <div class="center">
        <p>{organization.organization_name} Organization Summary</p>
            </div>
 
        </header>
        <br>
    """
    org_writeup += ORG_PARTICIPANT_WRITEUP_START

    for primary_div in organization.primary_divisions:
        prim_ref = organization.primary_divisions[primary_div]
        primary_total_item = 0
        primary_total_money = 0
        secondary_div_table = ""
        for secondary_div in prim_ref:
            second_ref = prim_ref[secondary_div]
            secondary_total_item = 0
            secondary_total_money = 0
            participant_table = ""
            for partcipant_name, part_orders in second_ref.items():
                part_money = _get_total_money_from_participant(part_orders)
                part_item = _get_total_items_from_participant(part_orders)

                secondary_total_item += part_item
                secondary_total_money += part_money
                participant_table += f"""
                <tr>
                <td></td>
                <td></td>
                <td>{partcipant_name}</td>
                <td>{int(part_orders.ship_to_home_total.item_cnt)}</td>
                <td>${part_orders.ship_to_home_total.money}</td>
                <td>{int(part_orders.ship_to_org_total.item_cnt)}</td>
                <td>${part_orders.ship_to_org_total.money}</td>
                <td>{int(part_orders.brochure_total.item_cnt)}</td>
                <td>${part_orders.brochure_total.money}</td>
                <td>{int(part_item)}</td>
                <td>${"{:.2f}".format(part_money)}</td>
                <td>${"{:.2f}".format(part_money * 0.4)}</td>
                </tr> 
                """
            # End of participant for loop, add to second div
            secondary_div_table += f"""
            <tr>
                <td></td>
                <td>{secondary_div}</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>{int(secondary_total_item)}</td>
                <td>${"{:.2f}".format(secondary_total_money)}</td>
                <td>${"{:.2f}".format(secondary_total_money * 0.4)}</td>
                </tr> 
            """
            secondary_div_table += participant_table
            primary_total_item += secondary_total_item
            primary_total_money += secondary_total_money
        # Secondary Div is Done
        primary_div_table += f"""
            <tr>
                <td>{primary_div}</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>{int(primary_total_item)}</td>
                <td>${"{:.2f}".format(primary_total_money)}</td>
                <td>${"{:.2f}".format(primary_total_money * 0.4)}</td>
                </tr> 
        """
        primary_div_table += secondary_div_table
        organization_total_items += primary_total_item
        organization_total_money += primary_total_money

    # Now All loops should be done
    org_writeup += primary_div_table

    org_writeup += f"""
            <tr>
                <td>Organization Total</td>
                <td></td>
                <td></td>
                <td>{int(org_write_up.ship_to_home_total.item_cnt)}</td>
                <td>${int(org_write_up.ship_to_home_total.money)}</td>
                <td>{org_write_up.ship_to_org_total.item_cnt}</td>
                <td>${org_write_up.ship_to_org_total.money}</td>
                <td>{int(org_write_up.brochure_total.item_cnt)}</td>
                <td>${org_write_up.brochure_total.money}</td>
                <td>{int(organization_total_items)}</td>
                <td>${"{:.2f}".format(organization_total_money)}</td>
                <td>${"{:.2f}".format(organization_total_money*0.4)}</td>
                </tr> 
    """

    org_writeup += END_TABLE
    org_writeup += "</div>"

    org_writeup += HTML_END
    output_file = f"{OUTPUT_FILE}/{organization.organization_name}/Organization/org_student_rundown.pdf"

    HTML(string=org_writeup).write_pdf(
        output_file,
        stylesheets=[f"{HTML_STYLE}"],
        presentational_hints=True,
        zoom=1.0,
        resolution=300,
        enable_hinting=True,
        embed_fonts=True,
        font_config=None,
        base_url=None,
        attachments=None,
        **{"page-size": "Letter", "orientation": "landscape"},
    )


def create_detailed_files(organization: Organization, org_write_up: OrgWriteUp):
    # Create the Organization folder if it doesn't exist
    create_organization_folder(org_name=organization.organization_name)
    iterate_primary_divs(organization, org_write_up)
    quick_organization_pull(organization.organization_name, org_write_up)
    organization_student_writeup(organization, org_write_up)
    items_sold_page(org_write_up, organization.organization_name)


# def create_pdf(file):
#     path_to_save = file[:-4] + "pdf"

#     print(path_to_save)
#     HTML(file).write_pdf(path_to_save)
