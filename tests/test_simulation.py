import unittest
from src.simulation import *
from src.components import *


class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.protocols = [
            {"name": "Centrifuge", "vaults": 3, "ratios": [40, 30, 30]},
            {"name": "Morpho", "vaults": 2, "ratios": [60, 40]},
            {"name": "Yearn", "vaults": 2, "ratios": [50, 50]},
        ]

        self.initialized_vaults = initialize_vaults(self.protocols)
        self.portals = create_portals(self.initialized_vaults, self.protocols)

        self.cfg_portal = self.portals["Centrifuge"]
        self.morpho_portal = self.portals["Morpho"]
        self.yearn_portal = self.portals["Yearn"]

        self.fund = Fund("USab", USDC, 0, 0, 10)

        self.fund.add_vault(self.cfg_portal, 25)
        self.fund.add_vault(self.morpho_portal, 25)
        self.fund.add_vault(self.yearn_portal, 40)

        self.fund.deposit(1000)

    def test_fund_initialization(self):
        self.assertEqual(self.fund.name, "USab")
        self.assertEqual(self.fund.depositAsset, USDC)
        self.assertEqual(self.fund.totalAssets, 1000)
        self.assertEqual(self.fund.totalShares, 1000)
        self.assertEqual(self.fund.reserveRatio, 10)
        self.assertEqual(len(self.fund.sub_vaults), 3)

    def test_fund_vault_allocation(self):
        self.assertEqual(self.fund.sub_vaults[self.cfg_portal]["ratio"], 25)
        self.assertEqual(self.fund.sub_vaults[self.morpho_portal]["ratio"], 25)
        self.assertEqual(self.fund.sub_vaults[self.yearn_portal]["ratio"], 40)

    def test_fund_rebalance(self):
        pass

    def test_portal_initialization(self):
        for portal in [self.cfg_portal, self.morpho_portal, self.yearn_portal]:
            self.assertEqual(portal.depositAsset, USDC)
            self.assertEqual(portal.totalAssets, 0)
            self.assertEqual(portal.totalShares, 0)
            self.assertEqual(portal.reserveRatio, 0)

    def test_portal_vault_allocation(self):
        self.assertEqual(len(self.cfg_portal.sub_vaults), 3)
        self.assertEqual(len(self.morpho_portal.sub_vaults), 2)
        self.assertEqual(len(self.yearn_portal.sub_vaults), 2)

        cfg_ratios = [data["ratio"] for data in self.cfg_portal.sub_vaults.values()]
        self.assertEqual(cfg_ratios, [40, 30, 30])

        morpho_ratios = [
            data["ratio"] for data in self.morpho_portal.sub_vaults.values()
        ]
        self.assertEqual(morpho_ratios, [60, 40])

        yearn_ratios = [data["ratio"] for data in self.yearn_portal.sub_vaults.values()]
        self.assertEqual(yearn_ratios, [50, 50])

    def test_portal_rebalance(self):
        self.fund.simple_rebalance()  # Invest in portals
        initial_portal_assets = {
            portal: portal.totalAssets for portal in self.portals.values()
        }

        for portal in self.portals.values():
            portal.simple_rebalance()

        for portal in self.portals.values():
            self.assertEqual(portal.cash, 0)  # All cash should be invested
            for vault, data in portal.sub_vaults.items():
                expected_investment = (
                    initial_portal_assets[portal] * data["ratio"] / 100
                )
                self.assertAlmostEqual(
                    portal.value_position(vault), expected_investment, places=2
                )
