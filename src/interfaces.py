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
    10101: Item("Chocolate Almonds", 12, 0.5),
    102: Item("Butter Toffee Peanuts", 10, 0.5),
    10201: Item("Butter Toffee Peanuts", 12, 0.5),
    103: Item("Cranberry Fitness Mix", 10, 0.5),
    10301: Item("Cranberry Fitness Mix", 12, 0.5),
    104: Item("Mixed Nuts", 10, 0.5),
    105: Item("Hot & Spicy Nuts", 10, 0.5),
    10501: Item("Hot & Spicy Nuts", 12, 0.5),
    10502: Item("Hot & Spicy Nuts Big Bag", 22, 0.5),
    1051: Item("Hot & Spicy Nuts Big Bag", 20, 0.5),
    106: Item("Sweet N Crunchy Trail Mix", 10, 0.5),
    10601: Item("Sweet N Crunchy Trail Mix", 12, 0.5),
    1061: Item("Sweet N Crunchy Trail Mix Big Bag", 20, 0.5),
    107: Item("Gummi Bears", 10, 0.5),
    10701: Item("Gummi Bears", 12, 0.5),
    1071: Item("Gummi Bears Big Bag", 20, 0.5),
    108: Item("Neon Sour Gummi Worms", 10, 0.5),
    10801: Item("Neon Sour Gummi Worms", 12, 0.5),
    10802: Item("Neon Sour Gummi Worms Big Bag", 22, 0.5),
    1081: Item("Neon Sour Gummi Worms Big Bag", 20, 0.5),
    109: Item("Fruit Slices", 10, 0.5),
    10901: Item("Fruit Slices", 12, 0.5),
    1091: Item("Fruit Slices Big Bag", 20, 0.5),
    110: Item("Peanut Butter Bears", 14, 0.5),
    11001: Item("Peanut Butter Bears", 15, 0.5),
    111: Item("English Butter Toffee", 14, 0.5),
    11101: Item("English Butter Toffee", 15, 0.5),
    112: Item("Pecan Buds", 14, 0.5),
    11201: Item("Pecan Buds", 15, 0.5),
    113: Item("Chocolate Covered Pretzels", 10, 0.5),
    11301: Item("Chocolate Covered Pretzels", 12, 0.5),
    114: Item("Chocolate Covered Raisins", 10, 0.5),
    11401: Item("Chocolate Covered Raisins", 12, 0.5),
    115: Item("Cracked Pepper & Sea Salt Cashews", 10, 0.5),
    11501: Item("Cracked Pepper & Sea Salt Cashews", 12, 0.5),
    116: Item("Honey Roasted Peanuts", 10, 0.5),
    11601: Item("Honey Roasted Peanuts", 12, 0.5),
    11602: Item("Honey Roaste Peanuts Big Bag", 22, 0.5),
    1161: Item("Honey Roaste Peanuts Big Bag", 20, 0.5),
    117: Item("Hawaiian Delight", 10, 0.5),
    11701: Item("Hawaiian Delight", 12, 0.5),
    118: Item("Cashew Snack Mix", 10, 0.5),
    11801: Item("Cashew Snack Mix", 12, 0.5),
    1181: Item("Cashew Snack Mix Big Bag", 20, 0.5),
    119: Item("Cashew Halves", 10, 0.5),
    11901: Item("Cashew Halves", 12, 0.5),
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
    211: Item("White Cheddar", 20, 0.5),
    301: Item("Chocolate Chip Cookies", 25, 0.5),
    302: Item("Peanut Butter Cookies", 25, 0.5),
    303: Item("Cinnabon Cookies", 25, 0.5),
    304: Item("White Chocolate Mac", 25, 0.5),
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
    611: Item("40 oz Red Travel Mug - Organization Bottle", 45, 0.4),
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
    801: Item("Donation", 20, 0.8),
    901: Item("Blue Bubble Gun", 20, 0.4),
    902: Item("Blue Bubble Gun", 20, 0.4),
    903: Item("Hello Kitty Pop-it Toy", 20, 0.4),
    904: Item("Kuromi Pop-it Toy", 20, 0.4),
    905: Item("Pikachu Pop-it Toy", 20, 0.4),
    906: Item("Stitch Pop-it Toy", 20, 0.4),
    1001: Item("Red Christmas Blanket", 35, 0.4),
    1002: Item("White Christmas Blanket", 35, 0.4),
    1003: Item("Combo Christmas Blanket", 60, 0.4),
    1004: Item("Red & White Christmas Thermal Sock", 12, 0.4),
    1005: Item("Light Red & White Christmas Thermal Sock", 12, 0.4),
    1006: Item("Pink & White Christmas Thermal Sock", 12, 0.4),
    1007: Item("Hot Pink & White Christmas Thermal Sock", 12, 0.4),
    1008: Item("Burgundy & White Christmas Thermal Sock", 12, 0.4),
    1009: Item("Grey & Burgundy Christmas Thermal Sock", 12, 0.4),
    1010: Item("Thermal Sock Set", 48, 0.4),
    1101: Item("Medium Holiday Christmas Bags", 15, 0.4),
    1102: Item("Medium Ornament Christmas Bags", 15, 0.4),
    1103: Item("XL Holiday Christmas Bags", 20, 0.4),
    1104: Item("XL 'Merry Christmas' Christmas Bags", 20, 0.4),
    1105: Item("XL Ornament Christmas Bags", 20, 0.4),
    1106: Item("XL Santa/Reindeer Christmas Bags", 20, 0.4),
    1201: Item("XL Birthday Bags", 20, 0.4),
    1201: Item("XL Colorful Bags", 20, 0.4),
    1201: Item("XL Food & Fun Bags", 20, 0.4),

}
