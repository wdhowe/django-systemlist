from django.shortcuts import render

# Render http response+templates
from django.shortcuts import render

# Object or 404
from django.shortcuts import get_object_or_404

# HTTP Response
from django.http import HttpResponse

# Logging
import logging

logger = logging.getLogger(__name__)

# Systemlist model
from .models import AssetEntry

# /systemlist/  -  All Devices, All Environments (the index)
def index(request):
    # Get all asset objects
    all_asset_list = AssetEntry.objects.order_by(
        "asset_type", "asset_env", "asset_name"
    )
    # Get all asset device types
    asset_type_list = [key for key, value in AssetEntry.DEVICE_TYPES]

    # Get number of assets in list
    number_assets = len(all_asset_list)

    # Map template variable names (1st) to Python variables (2nd) for use in html templates
    context = {
        "all_asset_list": all_asset_list,
        "asset_count": number_assets,
        "asset_type_list": asset_type_list,
    }

    # Logging
    logger.info("Rendering index.html - All Devices, All Environments")

    # Render the http request, using the template, passing the context
    return render(request, "systemlist/index.html", context)


# /systemlist/stats  -  All Devices, Statistics
def stats(request):
    # Get all asset objects
    all_asset_list = AssetEntry.objects.order_by(
        "asset_type", "asset_env", "asset_name"
    )

    # Get all asset device types
    asset_type_list = [key for key, value in AssetEntry.DEVICE_TYPES]

    # Get all os names, Linux only, Windows only
    os_list = [key for key, value in AssetEntry.OS_NAMES]
    os_list_linux = [key for key, value in AssetEntry.OS_NAMES_LINUX]
    os_list_windows = [key for key, value in AssetEntry.OS_NAMES_WINDOWS]

    # - Build Statistics -#
    # Initialize Stats list (will be a list of dictionaries)
    stats_list = []

    ####---- Asset Counts Table: Grand Total Row ----####
    sysstats_grand_total = 0
    sysstats_grand_physical = 0
    sysstats_grand_physical_linux = 0
    sysstats_grand_physical_windows = 0
    sysstats_grand_physical_other = 0
    sysstats_grand_virtual = 0
    sysstats_grand_virtual_linux = 0
    sysstats_grand_virtual_windows = 0
    sysstats_grand_virtual_other = 0
    sysstats_grand_vmware = 0

    # Calculate stats for each type of device
    for device_type in asset_type_list:
        device_stats = []

        # Add node to the device_stats list if a node from the all_asset_list matches the current device type
        for node in all_asset_list:
            if "".join(node.asset_type.lower().split()) == device_type.lower():
                device_stats.append(node)

        ####---- Asset Counts Table ----####
        # Total Count
        count_total = len(device_stats)

        # - Add to grand total
        sysstats_grand_total += count_total

        # Physical and Virtual Counts
        count_physical = 0
        count_physical_linux = 0
        count_physical_windows = 0
        count_physical_other = 0
        count_virtual = 0
        count_virtual_linux = 0
        count_virtual_windows = 0
        count_virtual_other = 0
        for node in device_stats:
            if node.asset_hardware == "Physical":
                count_physical += 1

                if node.asset_os in os_list_linux:
                    # Physical+Linux Count
                    count_physical_linux += 1
                elif node.asset_os in os_list_windows:
                    # Physical+Windows Count
                    count_physical_windows += 1
                else:
                    # Physical+Other OS
                    count_physical_other += 1

            elif node.asset_hardware == "Virtual":
                # Virtual Count
                count_virtual += 1

                if node.asset_os in os_list_linux:
                    # Virtual+Linux Count
                    count_virtual_linux += 1
                elif node.asset_os in os_list_windows:
                    # Virtual+Windows Count
                    count_virtual_windows += 1
                else:
                    # Virtual+Other OS
                    count_virtual_other += 1

        # - Add to grand total physical
        sysstats_grand_physical += count_physical
        sysstats_grand_physical_linux += count_physical_linux
        sysstats_grand_physical_windows += count_physical_windows
        sysstats_grand_physical_other += count_physical_other

        # - Add to grand total virtual
        sysstats_grand_virtual += count_virtual
        sysstats_grand_virtual_linux += count_virtual_linux
        sysstats_grand_virtual_windows += count_virtual_windows
        sysstats_grand_virtual_other += count_virtual_other

        ####---- OS Counts Table ----####
        os_counts = []

        # Add all the os names and an initial count of 0
        for name in os_list:
            os_counts.append({"os_name": name, "count": 0})

        # Check each node in the devices specific stats
        for node in device_stats:
            # Compare node's OS against each os name in the os_counts list and increment count if a match is found
            for os_entry in os_counts:
                if os_entry["os_name"] == node.asset_os:
                    os_entry["count"] += 1

        ####---- After All Stats Calculations: Add Device Stats to stats_list ----####
        # Add device statistics to stats_list
        stats_list.append(
            {
                "asset_type": device_type,
                "total": count_total,
                "physical": count_physical,
                "physical_linux": count_physical_linux,
                "physical_windows": count_physical_windows,
                "physical_other": count_physical_other,
                "virtual": count_virtual,
                "virtual_linux": count_virtual_linux,
                "virtual_windows": count_virtual_windows,
                "virtual_other": count_virtual_other,
                "os_count_stats": os_counts,
            }
        )

        # Grand Total Only: VMware ESXi Host Count
        for node in device_stats:
            if node.asset_os.startswith("VMware"):
                sysstats_grand_vmware += 1
    # -- END OF Calculate Device Type Stats loop --#

    ##-- Calculate OS stats grand totals --##
    os_counts_total = []

    # Add all the os names and an initial count of 0
    for name in os_list:
        os_counts_total.append({"os_name": name, "count": 0})

    # For each device specific stats entry, add up grand total os counts
    for device_entry in stats_list:
        # For each device_entry in the stats_list, go through its os_count_stats value, which is a list of os_names and counts
        for os_device_entry in device_entry["os_count_stats"]:
            # Check each os_count_stats os_name against the os_counts_total os_name list
            for os_entry_total in os_counts_total:
                # If we have an os_name match, add the device's os count to the total os count
                if os_entry_total["os_name"] == os_device_entry["os_name"]:
                    os_entry_total["count"] += os_device_entry["count"]

    ####---- Add grand totals to stats_list ----####
    stats_list.append(
        {
            "asset_type": "Total",
            "total": sysstats_grand_total,
            "physical": sysstats_grand_physical,
            "physical_linux": sysstats_grand_physical_linux,
            "physical_windows": sysstats_grand_physical_windows,
            "physical_other": sysstats_grand_physical_other,
            "virtual": sysstats_grand_virtual,
            "virtual_linux": sysstats_grand_virtual_linux,
            "virtual_windows": sysstats_grand_virtual_windows,
            "virtual_other": sysstats_grand_virtual_other,
            "os_count_stats": os_counts_total,
        }
    )

    # - Other Grand Totals: Calculate -#
    sysstats_grand_linux = sysstats_grand_physical_linux + sysstats_grand_virtual_linux
    sysstats_grand_windows = (
        sysstats_grand_physical_windows + sysstats_grand_virtual_windows
    )
    sysstats_grand_other = sysstats_grand_physical_other + sysstats_grand_virtual_other

    # Map template variable names (1st) to the Python variables (2nd) for use in templates
    context = {
        "device_stats": stats_list,
        "total_linux": sysstats_grand_linux,
        "total_windows": sysstats_grand_windows,
        "total_other": sysstats_grand_other,
        "total_vmware": sysstats_grand_vmware,
        "os_list": os_list,
    }

    # Logging
    logger.info("Rendering stats.html")

    # Render the HTTP request, using the template, passing the context
    return render(request, "systemlist/stats.html", context)


# /systemlist/env_name  -  All Devices, Specific Environment
def env(request, env_name):
    # Get all asset objects
    all_asset_list = AssetEntry.objects.order_by(
        "asset_type", "asset_env", "asset_name"
    )
    # Get all asset device types
    asset_type_list = [key for key, value in AssetEntry.DEVICE_TYPES]

    # New List for the asset types in the passed environment only
    assets_by_env = []

    # Check each asset, add to new list if it matches the requested environment name
    for node in all_asset_list:
        if "".join(node.asset_env.lower().split()) == env_name.lower():
            assets_by_env.append(node)

    # Get number of assets in list
    number_assets = len(assets_by_env)

    # Map template variable names (1st) to Python variables (2nd) for use in html templates
    context = {
        "all_asset_list": assets_by_env,
        "env": env_name,
        "asset_count": number_assets,
        "asset_type_list": asset_type_list,
    }

    # Logging
    logger.info("Rendering index.html - All Devices, " + env_name)

    # Render the http request, using the template, passing the context
    return render(request, "systemlist/index.html", context)


# /systemlist/device/  - Specific Device, All Environments
def type_all_env(request, device_type):
    # Get all asset objects
    all_asset_list = AssetEntry.objects.order_by(
        "asset_type", "asset_env", "asset_name"
    )
    # Get all asset device types
    asset_type_list = [key for key, value in AssetEntry.DEVICE_TYPES]

    # New List for specific devices only
    assets_by_type = []

    # Check each asset, add to new list if it matches the requested device type
    for node in all_asset_list:
        if "".join(node.asset_type.lower().split()) == device_type.lower():
            assets_by_type.append(node)

    # Get number of assets in list
    number_assets = len(assets_by_type)

    # Map template variable names (1st) to Python variables (2nd) for use in html templates
    context = {
        "all_asset_list": assets_by_type,
        "asset_type": device_type,
        "asset_count": number_assets,
        "asset_type_list": asset_type_list,
    }

    # Logging
    logger.info("Rendering index.html - Devices: " + device_type + ", All Environments")

    # Render the http request, using the template, passing the context
    return render(request, "systemlist/index.html", context)


# /systemlist/device/env_name  -  Specific Device, Specific Environment
def type_env(request, device_type, env_name):
    # Get all asset objects
    all_asset_list = AssetEntry.objects.order_by(
        "asset_type", "asset_env", "asset_name"
    )
    # Get all asset device types
    asset_type_list = [key for key, value in AssetEntry.DEVICE_TYPES]

    # New List for specific devices and environment only
    assets_by_type_env = []

    # Check each asset, add to new list if it matches the requested device and environment
    for node in all_asset_list:
        if "".join(node.asset_type.lower().split()) == device_type.lower():
            if "".join(node.asset_env.lower().split()) == env_name.lower():
                assets_by_type_env.append(node)

    # Get number of assets in list
    number_assets = len(assets_by_type_env)

    # Map template variable names (1st) to Python variables (2nd) for use in html templates
    context = {
        "all_asset_list": assets_by_type_env,
        "asset_type": device_type,
        "env": env_name,
        "asset_count": number_assets,
        "asset_type_list": asset_type_list,
    }

    # Logging
    logger.info("Rendering index.html - Devices: " + device_type + ", Env: " + env_name)

    # Render the http request, using the template, passing the context
    return render(request, "systemlist/index.html", context)


# /systemlist/<asset_hardware>/  - Physical or Virtual
def asset_hardware(request, asset_hardware):
    # Get all asset objects
    all_asset_list = AssetEntry.objects.order_by(
        "asset_type", "asset_env", "asset_name"
    )
    # Get all asset device types
    asset_type_list = [key for key, value in AssetEntry.DEVICE_TYPES]

    # New List for asset_hardware (physical or virtual)
    assets_by_hw = []

    # Check each asset, add to new list if it matches the requested hardware type
    for node in all_asset_list:
        if "".join(node.asset_hardware.lower().split()) == asset_hardware.lower():
            assets_by_hw.append(node)

    # Get number of assets in list
    number_assets = len(assets_by_hw)

    # Map template variable names (1st) to the Python variables (2nd) for use in templates
    context = {
        "all_asset_list": assets_by_hw,
        "asset_hardware": asset_hardware,
        "asset_count": number_assets,
        "asset_type_list": asset_type_list,
    }

    # Logging
    logger.info("Rendering index.html - All Devices, " + asset_hardware)

    # Render the HTTP request, using the template, passing the context
    return render(request, "systemlist/index.html", context)
