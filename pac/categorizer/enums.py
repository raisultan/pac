from enum import Enum, auto


class TicketCategory(Enum):
    ACCOUNT_ACCESS = auto()
    BATTERY_LIFE = auto()
    CANCELLATION_REQUEST = auto()
    DATA_LOSS = auto()
    DELIVERY_PROBLEM = auto()
    DISPLAY_ISSUE = auto()
    HARDWARE_ISSUE = auto()
    INSTALLATION_SUPPORT = auto()
    NETWORK_PROBLEM = auto()
    PAYMENT_ISSUE = auto()
    PERIPHERAL_COMPATIBILITY = auto()
    PRODUCT_COMPATIBILITY = auto()
    PRODUCT_RECOMMENDATION = auto()
    PRODUCT_SETUP = auto()
    REFUND_REQUEST = auto()
    SOFTWARE_BUG = auto()
    OTHER = auto()
