from enum import Enum

# Define general user group permissions

engineer = {
    "company_view": True,
    "company_edit": True,
    "company_delete": True,
    "device_view": True,
    "device_edit": True,
    "device_delete": True,
    "product_view": True,
    "product_edit": True,
    "product_delete": True,
    "users_view": False,
    "users_edit": False,
    "users_delete": False,
    "administration_dashboard": True

}

supervisor = {
    "company_view": True,
    "company_edit": True,
    "company_delete": True,
    "device_view": True,
    "device_edit": True,
    "device_delete": True,
    "product_view": True,
    "product_edit": True,
    "product_delete": True,
    "users_view": False,
    "users_edit": False,
    "users_delete": False,
    "administration_dashboard": True

}

operator = {
    "company_view": False,
    "company_edit": False,
    "company_delete": False,
    "device_view": False,
    "device_edit": False,
    "device_delete": False,
    "product_view": False,
    "product_edit": False,
    "product_delete": False,
    "users_view": False,
    "users_edit": False,
    "users_delete": False,
    "administration_dashboard": False
}


class UserRolePermissions(Enum):
    ENGINEER = engineer
    SUPERVISOR = supervisor
    OPERATOR = operator
