from enum import Enum, auto


class TicketCategory(Enum):
    ACCOUNT_ACCESS = 'account_access'
    BATTERY_LIFE = 'battery_life'
    CANCELLATION_REQUEST = 'cancellation_request'
    DATA_LOSS = 'data_loss'
    DELIVERY_PROBLEM = 'delivery_problem'
    DISPLAY_ISSUE = 'display_issue'
    HARDWARE_ISSUE = 'hardware_issue'
    INSTALLATION_SUPPORT = 'installation_support'
    NETWORK_PROBLEM = 'network_problem'
    PAYMENT_ISSUE = 'payment_issue'
    PERIPHERAL_COMPATIBILITY = 'peripheral_compatibility'
    PRODUCT_COMPATIBILITY = 'product_compatibility'
    PRODUCT_RECOMMENDATION = 'product_recommendation'
    PRODUCT_SETUP = 'product_setup'
    REFUND_REQUEST = 'refund_request'
    SOFTWARE_BUG = 'software_bug'
    OTHER = 'other'
