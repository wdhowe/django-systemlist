from django.db import models

# Asset Inventory
class AssetEntry(models.Model):

    ##-- Tuples for Use in Field Choices --##

    # asset_type choices
    DEVICE_TYPES = (
        ("Firewalls", "Firewalls"),
        ("Routers", "Routers"),
        ("Servers", "Servers"),
        ("Storage", "Storage"),
        ("Switches", "Switches"),
        ("Workstations", "Workstations"),
    )

    # asset_env choices
    ENV_NAMES = (("Dev", "Development"), ("Test", "Testing"), ("Prod", "Production"))

    # Linux OS List
    OS_NAMES_LINUX = (
        ("CentOS 7", "CentOS 7"),
        ("CentOS 8", "CentOS 8"),
        ("RHEL 7", "Red Hat Enterprise Linux 7"),
        ("RHEL 8", "Red Hat Enterprise Linux 8"),
        ("Ubuntu 16.04", "Ubuntu 16.04"),
        ("Ubuntu 18.04", "Ubuntu 18.04"),
    )

    # Windows OS List
    OS_NAMES_WINDOWS = (
        ("Win 2012", "Windows 2012"),
        ("Win 2016", "Windows 2016"),
        ("Win 2019", "Windows 2019"),
        ("Win 7", "Windows 7"),
        ("Win 10", "Windows 10"),
    )

    # Other OS List
    OS_NAMES_OTHER = (
        ("Cisco IOS", "Cisco IOS"),
        ("Extreme XOS", "Extreme XOS"),
        ("Juniper JunOS", "Juniper JunOS"),
        ("NA", "None"),
        ("Other", "Other"),
        ("VMware ESXi", "VMware ESXi"),
    )

    # Combined OS List - for asset_os choices
    OS_NAMES = OS_NAMES_LINUX + OS_NAMES_WINDOWS + OS_NAMES_OTHER

    # asset_hardware choices
    HW_TYPES = (("Virtual", "Virtual"), ("Physical", "Physical"))

    ##-- AssetEntry Fields --##
    asset_name = models.CharField("Name", max_length=50)

    asset_type = models.CharField("Device Type", max_length=15, choices=DEVICE_TYPES)

    asset_description = models.CharField("Description", max_length=100)

    asset_env = models.CharField("Environment", max_length=15, choices=ENV_NAMES)

    asset_os = models.CharField("OS Name/Version", max_length=20, choices=OS_NAMES)

    asset_hardware = models.CharField(
        "Hardware: Virtual or Physical", max_length=15, choices=HW_TYPES
    )

    # Object representation - display the name in the portal
    def __str__(self):
        return self.asset_name
