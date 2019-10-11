"""
Test cases for views
Run via: ./manage.py test
"""
# TestCase class
from django.test import TestCase

# Import the systemlist app model
from systemlist.models import AssetEntry

# Allow named url references instead of hardcoded
from django.urls import reverse


class ViewsTestCase(TestCase):
    """Class to test the AssetEntry views"""

    def create_asset(self):
        """Create an asset"""

        return AssetEntry.objects.create(
            asset_name="server01",
            asset_type="Servers",
            asset_description="My dev centos 8 server",
            asset_env="Dev",
            asset_os="CentOS 8",
            asset_hardware="Virtual",
        )

    def test_view_index_no_assets(self):
        """Index, no assets should exist yet"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["asset_count"], 0)

    def test_view_index_one_asset(self):
        """Index, create one asset and test"""
        self.create_asset()

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["asset_count"], 1)

    def test_view_stats(self):
        """Stats view"""
        self.create_asset()

        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)

        # device_stats list item 2 is "servers"
        self.assertEqual(response.context["device_stats"][2]["total"], 1)
        self.assertEqual(response.context["device_stats"][2]["virtual_linux"], 1)

        # os_count_stats list item 1 is "CentOS 8"
        self.assertEqual(
            response.context["device_stats"][2]["os_count_stats"][1]["count"], 1
        )

    def test_view_all_types_env(self):
        """All device types, specific environment"""
        self.create_asset()

        # Get all environment names for url tests
        env_list = [key.lower() for key, value in AssetEntry.ENV_NAMES]

        for env_name in env_list:
            print(f"Checking {env_name}...", end="")
            response = self.client.get(reverse("env", args=(env_name,)))
            self.assertEqual(response.status_code, 200)
            print(f"[{response.status_code}]")

            if env_name == "dev":
                self.assertEqual(response.context["asset_count"], 1)
            else:
                self.assertEqual(response.context["asset_count"], 0)

    def test_view_type_all_env(self):
        """Specific device type, all environments"""
        self.create_asset()

        # Get all device types lowercased for url tests
        asset_type_list = [key.lower() for key, value in AssetEntry.DEVICE_TYPES]

        for asset_type in asset_type_list:
            print(f"Checking {asset_type}...", end="")
            response = self.client.get(reverse("type_all_env", args=(asset_type,)))
            self.assertEqual(response.status_code, 200)
            print(f"[{response.status_code}]")

            if asset_type == "servers":
                self.assertEqual(response.context["asset_count"], 1)

    def test_view_type_env(self):
        """Specific device type, specific environment"""
        self.create_asset()

        # Get all device types lowercased for url tests
        asset_type_list = [key.lower() for key, value in AssetEntry.DEVICE_TYPES]

        for asset_type in asset_type_list:
            print(f"Checking {asset_type}, dev...", end="")
            response = self.client.get(reverse("type_env", args=(asset_type, "dev")))
            self.assertEqual(response.status_code, 200)
            print(f"[{response.status_code}]")

            if asset_type == "servers":
                self.assertEqual(response.context["asset_count"], 1)

    def test_view_hardware(self):
        """Physical/Virtual hardware"""
        self.create_asset()

        # The test asset should be a virtual hardware type
        response = self.client.get(reverse("asset_hardware", args=("virtual",)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["asset_count"], 1)
