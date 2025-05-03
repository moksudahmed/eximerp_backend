from enum import Enum
import enum

# Enum for AccountType
class AccountTypeEnum(str, Enum):
    ASSET = 'asset'
    LIABILITY = 'liability'
    EQUITY = 'equity'
    REVENUE = 'revenue'
    EXPENSE = 'expense'


# Enum for transaction payment methods
class PaymentMethod(enum.Enum):
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"


class ActionType(enum.Enum):
    ADD = 'ADD'
    DEDUCT = 'DEDUCT'
    DAMAGED = 'DAMAGED'


class AccountAction(enum.Enum):
    dr='DEBIT'
    cr='CREDIT'

class OrderStatusEnum(Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
