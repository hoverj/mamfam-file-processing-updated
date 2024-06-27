import pandas as pd
from interfaces import (
    ITEM_COSTS,
    Item,
    Product,
    Participant,
    PrimaryDivision,
    Organization,
    OrgWriteUp,
    initalize_participant,
)
from typing import List
from collections import Counter

columns_to_return = [
    "Name",
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    201,
    202,
    203,
    204,
    205,
    206,
    301,
    302,
    303,
]


def add_primary_div(primary_div: str, org: Organization):
    org.primary_divisions[primary_div] = {}


def add_secondary_div(primary_div: str, secondary_div: str, org: Organization):
    org.primary_divisions[primary_div][secondary_div] = {}


def add_participant_to_org(
    primary_div: str, secondary_div: str, participant: str, org: Organization
):
    org.primary_divisions[primary_div][secondary_div][
        participant
    ] = initalize_participant()


def find_secondary_divs(df):
    return df.loc[df.drop(columns="Name").isnull().all(axis=1), "Name"].tolist()


def get_partiicpant_name(excel_line):
    participant_name = excel_line["Name"].lower().strip()
    participant_name = participant_name.split(",")

    if len(participant_name) > 1:
        return f"{participant_name[1]} {participant_name[0]}"
    return participant_name[0]


def add_participant_excel_to_org(
    organization: Organization,
    org_write_up: OrgWriteUp,
    primary_div: str,
    secondary_div: str,
    excel_line,
):
    partipant_dict = {}
    participant_name = get_partiicpant_name(excel_line).strip()

    if primary_div not in organization.primary_divisions:
        add_primary_div(primary_div=primary_div, org=organization)

    if secondary_div not in organization.primary_divisions[primary_div]:
        add_secondary_div(
            primary_div=primary_div, secondary_div=secondary_div, org=organization
        )
    if (
        participant_name
        not in organization.primary_divisions[primary_div][secondary_div]
    ):
        add_participant_to_org(
            primary_div=primary_div,
            secondary_div=secondary_div,
            participant=participant_name,
            org=organization,
        )
    excel_row = excel_line.dropna(how="any")
    partipant_dict = excel_row.to_dict()

    for sku in partipant_dict:
        try:
            partipant_dict[sku] = int(partipant_dict[sku])
        except:
            partipant_dict[sku] = 0

    partipant_dict.pop("Name")
    money_total = 0
    item_total = 0
    for sku, item_cnt in partipant_dict.items():
        item_total += item_cnt
        money_total += item_cnt * ITEM_COSTS[sku].price

    partipant = organization.primary_divisions[primary_div][secondary_div][
        participant_name
    ]

    # Update organization brochure
    old_dict = Counter(org_write_up.brochure)
    new_dict = Counter(partipant_dict) + old_dict
    org_write_up.brochure = dict(new_dict)

    partipant.brochure = partipant_dict
    partipant.quick_pull = dict(Counter(partipant.quick_pull) + Counter(partipant_dict))
    partipant.brochure_total.money = money_total
    partipant.brochure_total.item_cnt = item_total


def iterate_primary_div(
    primary_div: str,
    organization: Organization,
    org_write_up: OrgWriteUp,
    secondary_divs: List[str],
    current_df,
):
    current_second_div = "Unknown"
    for _, line in current_df.iterrows():
        if line["Name"] in secondary_divs:
            current_second_div = line["Name"]
            continue

        add_participant_excel_to_org(
            organization=organization,
            org_write_up=org_write_up,
            primary_div=primary_div,
            secondary_div=current_second_div,
            excel_line=line,
        )


def parse_excel(file: str, organization: Organization, org_write_up: OrgWriteUp):
    sheets_dict = pd.read_excel(file, header=3, sheet_name=None)
    for primary_div, df in sheets_dict.items():
        if df.empty:
            continue
        df.rename(columns={"Unnamed: 0": "Name"}, inplace=True)
        dataframe = df.loc[:, df.columns.intersection(columns_to_return)]
        dataframe = dataframe.dropna(how="all")
        dataframe = dataframe[dataframe["Name"] != "Total"]
        secondary_divs = find_secondary_divs(dataframe)
        secondary_divs = secondary_divs if secondary_divs else ["Unknown"]
        iterate_primary_div(
            primary_div=primary_div,
            organization=organization,
            org_write_up=org_write_up,
            secondary_divs=secondary_divs,
            current_df=dataframe,
        )
