"""
Test cases for models
Run via: ./manage.py test
"""
from django.test import TestCase

# Import the systemlist app model
from systemlist.models import AssetEntry


class ModelsTestCase(TestCase):
    """Class to test the AssetEntry models"""

    def setUp(self):
        """Create some objects for testing"""

        AssetEntry.objects.create(
            asset_name="server01",
            asset_type="Servers",
            asset_description="My dev centos 8 server",
            asset_env="Dev",
            asset_os="CentOS 8",
            asset_hardware="Virtual",
        )
        AssetEntry.objects.create(
            asset_name="server02",
            asset_type="Servers",
            asset_description="My prod centos 7 server",
            asset_env="Prod",
            asset_os="CentOS 7",
            asset_hardware="Physical",
        )

    def test_model_object_retrieval(self):
        """
        Test retrieval of objects from the
        AssetEntry model info.
        """
        # Retrieve two objects
        node01 = AssetEntry.objects.get(asset_name="server01")
        node02 = AssetEntry.objects.get(asset_name="server02")

        # Ensure object properties are correct
        # node01
        self.assertEqual(node01.asset_type, "Servers")
        self.assertEqual(node01.asset_env, "Dev")
        self.assertEqual(node01.asset_os, "CentOS 8")
        self.assertEqual(node01.asset_hardware, "Virtual")

        # node02
        self.assertEqual(node02.asset_type, "Servers")
        self.assertEqual(node02.asset_env, "Prod")
        self.assertEqual(node02.asset_os, "CentOS 7")
        self.assertEqual(node02.asset_hardware, "Physical")

        # Retrieve all objects
        all_nodes = AssetEntry.objects.order_by("asset_type", "asset_env", "asset_name")
        number_of_nodes = len(all_nodes)
        self.assertEqual(number_of_nodes, 2)
