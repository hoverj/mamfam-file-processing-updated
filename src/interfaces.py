from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Item:
    name: str
    price: float
    percent_profit: float


@dataclass
class Product:
    sku: int
    item_name: str
    qty: int
    total_cost: float
    notes: str


@dataclass
class OrderMethodTotals:
    money: float
    profit_generated: float
    item_cnt: int


@dataclass
class Participant:
    ship_to_home: Dict[str, List[Product]]
    ship_to_home_total: OrderMethodTotals
    ship_to_org: Dict[str, List[Product]]
    ship_to_org_total: OrderMethodTotals
    brochure: Dict[int, int]
    brochure_total: OrderMethodTotals
    quick_pull: Dict[int, int]


@dataclass
class PrimaryDivision:
    """
    Primary Division is for when groups need to divided up
    among divisions among leagues or grades within a school
    """

    secondary_divisions: Dict[str, Dict[str, Participant]]


@dataclass
class Organization:
    organization_name: str
    primary_divisions: Dict[str, PrimaryDivision]


@dataclass
class OnlineLineDetails:
    primary_div_name: str
    secondary_div_name: str
    customer_name: str
    participant_name: str


@dataclass
class OrgWriteUp:
    quick_pull: Dict[int, int]
    brochure: Dict[int, int]
    ship_to_home: Dict[int, int]
    ship_to_org: Dict[int, int]
    ship_to_home_total: OrderMethodTotals
    ship_to_org_total: OrderMethodTotals
    brochure_total: OrderMethodTotals


def initalize_participant():
    return Participant(
        ship_to_home={},
        ship_to_home_total=OrderMethodTotals(0, 0, 0),
        ship_to_org={},
        ship_to_org_total=OrderMethodTotals(0, 0, 0),
        brochure={},
        brochure_total=OrderMethodTotals(0, 0, 0),
        quick_pull={},
    )


ITEM_COSTS = {
    101: Item("Chocolate Almonds", 10, 0.5),
    102: Item("Butter Toffee Peanuts", 10, 0.5),
    103: Item("Cranberry Fitness Mix", 10, 0.5),
    104: Item("Mixed Nuts", 10, 0.5),
    105: Item("Hot & Spicy Nuts", 10, 0.5),
    106: Item("Sweet N Crunchy Trail Mix", 10, 0.5),
    107: Item("Gummi Bears", 10, 0.5),
    108: Item("Neon Sour Gummi Worms", 10, 0.5),
    109: Item("Fruit Slices", 10, 0.5),
    110: Item("Peanut Butter Bears", 14, 0.5),
    111: Item("English Butter Toffee", 14, 0.5),
    112: Item("Pecan Buds", 14, 0.5),
    113: Item("Chocolate Covered Pretzels", 10, 0.5),
    114: Item("Chocolate Covered Raisins", 10, 0.5),
    115: Item("Cracked Pepper & Sea Salt Cashews", 10, 0.5),
    116: Item("Honey Roasted Peanuts", 10, 0.5),
    201: Item("Kettle Popcorn", 20, 0.5),
    202: Item("Buttery Caramel", 20, 0.5),
    203: Item("Cheesy Cheddar", 20, 0.5),
    204: Item("Chicago", 20, 0.5),
    205: Item("Fruity", 20, 0.5),
    206: Item("Jalapeno Cheddar", 20, 0.5),
    207: Item("Chocolate Delight", 20, 0.5),
    208: Item("Movie Theater Popcorn", 20, 0.5),
    209: Item("Cookies & Cream", 20, 0.5),
    210: Item("Texas Cheddar Habanero", 20, 0.5),
    301: Item("Chocolate Chip Cookies", 25, 0.5),
    302: Item("Peanut Butter Cookies", 25, 0.5),
    303: Item("Cinnabon Cookies", 25, 0.5),
    401: Item("Customized Bear", 25, 0.4),
    402: Item("Graduation Bear", 30, 0.4),
    403: Item("Extra Bear Shirt", 13, 0.4),
    404: Item("Custom Shirt - Black", 25, 0.4),
    405: Item("Custom Shirt - Grey", 25, 0.4),
    406: Item("Custom Shirt - Navy Blue", 25, 0.4),
    407: Item("Custom Shirt - Red", 25, 0.4),
    408: Item("Custom Shirt - Royal Blue", 25, 0.4),
    409: Item("Custom Shirt - White", 25, 0.4),
    410: Item("Custom Hoodie - Black", 55, 0.4),
    411: Item("Custom Hoodie - Grey", 55, 0.4),
    412: Item("Custom Hoodie - Navy Blue", 55, 0.4),
    413: Item("Custom Hoodie - Red", 55, 0.4),
    414: Item("Custom Hoodie - Royal Blue", 55, 0.4),
    415: Item("Custom Hoodie - White", 55, 0.4),
    501: Item("20 oz Black Bottle", 30, 0.4),
    502: Item("40 oz Black", 35, 0.4),
    503: Item("40 oz Burgundy", 35, 0.4),
    504: Item("40 oz Green", 35, 0.4),
    505: Item("40 oz Navy", 35, 0.4),
    506: Item("40 oz Purple", 35, 0.4),
    507: Item("40 oz Red", 35, 0.4),
    508: Item("40 oz Royal", 35, 0.4),
    509: Item("20 oz Black Bottle - Organization Bottle", 30, 0.4),
    510: Item("40 oz Black - Organization Bottle", 35, 0.4),
    511: Item("40 oz Burgundy - Organization Bottle", 35, 0.4),
    512: Item("40 oz Green - Organization Bottle", 35, 0.4),
    513: Item("40 oz Navy - Organization Bottle", 35, 0.4),
    514: Item("40 oz Purple - Organization Bottle", 35, 0.4),
    515: Item("40 oz Red - Organization Bottle", 35, 0.4),
    516: Item("40 oz Royal - Organization Bottle", 35, 0.4),
    601: Item("40 oz Black Travel Mug", 45, 0.4),
    602: Item("40 oz Light Blue Travel Mug", 45, 0.4),
    603: Item("40 oz Pink Travel Mug", 45, 0.4),
    604: Item("40 oz Purple Travel Mug", 45, 0.4),
    605: Item("40 oz White Travel Mug", 45, 0.4),
    606: Item("40 oz Black Travel Mug - Organization Bottle", 45, 0.4),
    607: Item("40 oz Light Blue Travel Mug - Organization Bottle", 45, 0.4),
    608: Item("40 oz Pink Travel Mug - Organization Bottle", 45, 0.4),
    609: Item("40 oz Purple Travel Mug - Organization Bottle", 45, 0.4),
    610: Item("40 oz White Travel Mug - Organization Bottle", 45, 0.4),
    701: Item("30 oz Black", 35, 0.4),
    702: Item("30 oz Green", 35, 0.4),
    703: Item("30 oz Navy", 35, 0.4),
    704: Item("30 oz Red", 35, 0.4),
    705: Item("30 oz Royal", 35, 0.4),
    706: Item("30 oz White", 35, 0.4),
    707: Item("30 oz Black - Organization Bottle", 35, 0.4),
    708: Item("30 oz Green - Organization Bottle", 35, 0.4),
    709: Item("30 oz Navy - Organization Bottle", 35, 0.4),
    710: Item("30 oz Red - Organization Bottle", 3, 0.4),
    711: Item("30 oz Royal - Organization Bottle", 35, 0.4),
    712: Item("30 oz White - Organization Bottle", 35, 0.4),
    3249: Item("Donation", 20, 0.8),
}
