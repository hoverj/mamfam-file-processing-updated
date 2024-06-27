from src.online_processing import online_line_parser


class TestOnlineDetailParser:
    def test_online_parser():
        some_json = {
            "order_number": "2021",
            "order_status": "Processing",
            "order_date": "2024-03-11 11:14",
            "billing_first_name": "Sophia",
            "billing_last_name": "Sosa",
            "billing_email": "sophiaxsosa@gmail.com",
            "billing_phone": "6615833030",
            "shipping_method_title": "Ship to Organization",
            "order_subtotal": 70,
            "order_total": "76.12",
            "shipping_address_1": "1212 East Avenue R-6",
            "shipping_address_2": "",
            "shipping_citystatezip": "Palmdale, CA, 93550",
            "USER_user_registration_customer_organization": "AV Rise Basketball",
            "USER_user_registration_customer_participant": "Mateo Sosa",
            "USER_user_registration_coach_teacher": "Eric Castillo",
            "USER_user_registration_grade_division": "11u",
            "products": [
                {
                    "sku": "510",
                    "line_id": 1,
                    "name": "40 oz Water Bottle - Organization Logo - Black",
                    "item_price": 35,
                    "qty": "1",
                    "attribute_color": "Black",
                    "size": "",
                    "attribute_bottle-color": "",
                    "font": "Elegant (Sosa)",
                    "music-design": "",
                    "occupational-design": "",
                    "general-design": "",
                    "baseball-design": "",
                    "basketball-design": "",
                    "dance-design": "",
                    "football-design": "",
                    "soccer-design": "",
                    "softball-design": "",
                    "cheer-design": "",
                },
                {
                    "sku": "511",
                    "line_id": 2,
                    "name": "40 oz Water Bottle - Organization Logo - Burgundy",
                    "item_price": 35,
                    "qty": "1",
                    "attribute_color": "Burgundy",
                    "size": "",
                    "attribute_bottle-color": "",
                    "font": "Elegant (Sosa)",
                    "music-design": "",
                    "occupational-design": "",
                    "general-design": "",
                    "baseball-design": "",
                    "basketball-design": "",
                    "dance-design": "",
                    "football-design": "",
                    "soccer-design": "",
                    "softball-design": "",
                    "cheer-design": "",
                },
            ],
        }
        line_detail_object = online_line_parser(some_json)
        assert line_detail_object.customer_name == "sophia sosa"
        assert line_detail_object.participant_name == "mateo sosa"
        assert line_detail_object.primary_div_name == "11u"
        assert line_detail_object.secondary_div_name == "eric castillo"
