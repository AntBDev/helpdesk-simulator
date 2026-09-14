from enum import Enum


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TicketStatus(str, Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_ON_USER = "WAITING_ON_USER"
    WAITING_ON_VENDOR = "WAITING_ON_VENDOR"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class DeviceType(str, Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    PRINTER = "PRINTER"
    PHONE = "PHONE"
    TABLET = "TABLET"
    OTHER = "OTHER"


class DeviceStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    REPAIR = "REPAIR"
    RETIRED = "RETIRED"
