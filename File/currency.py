from enum import Enum

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    RUB = "RUB"
    CNY = "CNY"
    JPY = "JPY"
    KZT = "KZT"
    UAH = "UAH"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    INR = "INR"

    @property
    def display_name(self) -> str:
        names = {
            "USD": "🇺🇸 US Dollar",
            "EUR": "🇪🇺 Euro",
            "GBP": "🇬🇧 British Pound",
            "RUB": "🇷🇺 Russian Ruble",
            "CNY": "🇨🇳 Chinese Yuan",
            "JPY": "🇯🇵 Japanese Yen",
            "KZT": "🇰🇿 Kazakhstani Tenge",
            "UAH": "🇺🇦 Ukrainian Hryvnia",
            "CAD": "🇨🇦 Canadian Dollar",
            "AUD": "🇦🇺 Australian Dollar",
            "CHF": "🇨🇭 Swiss Franc",
            "INR": "🇮🇳 Indian Rupee"
        }
        return names.get(self.value, self.value)
