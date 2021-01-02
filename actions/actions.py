import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

currency_rates = {
    'usd': (23000, 23500),
    'gbp': (30000, 31600),
    'yen': (200, 250)
}

bank_addresses = {
    'hà nội': ['108 Trần Hưng Đạo', '126 Đội Cấn', '183 Nguyễn Lương Bằng'],
    'đà nẵng': ['36 Trần Quốc Toản', '218 Nguyễn Văn Linh', '381 Nguyễn Lương Bằng'],
    'sài gòn': ['Tầng 14&15, 93-95 Hàm Nghi', '222-224 Phan Đình Phùng', '461-465 Nguyễn Đình Chiểu']
}


class ActionExchangeRate(Action):
    def name(self) -> Text:
        return "action_exchange_rate"

    @staticmethod
    def get_exchange_rate(currency):
        if currency in currency_rates:
            return random.randrange(currency_rates[currency][0], currency_rates[currency][1])
        return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        currencies = tracker.get_slot('currency')
        if type(currencies) is str:
            currencies = [currencies]
        currencies = set(currencies)
        for currency in currencies:
            rate = self.get_exchange_rate(currency)
            if rate:
                dispatcher.utter_message(text=f'1 {currency.upper()} = {rate} VND')
            else:
                dispatcher.utter_message(text=f'Xin lỗi, tôi không tìm thấy tỉ giá của {currency.upper()}')


class ActionBankAddresses(Action):
    def name(self) -> Text:
        return "action_bank_addresses"

    @staticmethod
    def get_addresses(city):
        city = city.lower()
        if city in bank_addresses:
            return '\n'.join(bank_addresses[city])
        return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cities = tracker.get_slot('city')
        if type(cities) is str:
            cities = [cities]
        cities = set(cities)
        for city in cities:
            addresses = self.get_addresses(city)
            if addresses:
                dispatcher.utter_message(text=f'Các chi nhánh Vietinbank ở {city}:\n{addresses}')
            else:
                dispatcher.utter_message(text=f'Xin lỗi, tôi không tìm thấy chi nhanh Vietinbank ở {city}')


class ValidateAddressForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_address_form"

    def validate_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if type(slot_value) is str:
            slot_value = [slot_value]
        slot_value = set(slot_value)
        ret = []
        for slot in slot_value:
            if slot.lower() in bank_addresses:
                ret.append(slot)
        if ret:
            return {'city': ret}
        return {'city': None}


class ValidateExchangeRateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_exchange_rate_form"

    def validate_currency(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if type(slot_value) is str:
            slot_value = [slot_value]
        slot_value = set(slot_value)
        ret = []
        for slot in slot_value:
            if slot.lower() in currency_rates:
                ret.append(slot)
        if ret:
            return {'currency': ret}
        return {'currency': None}
