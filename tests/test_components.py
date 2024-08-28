import unittest
from src.components import ERC4626, Portal

USDC = "USDC"


class TestERC4626(unittest.TestCase):
    def setUp(self):
        self.vault = ERC4626("Test Vault", USDC, 0, 0)

    def test_initialization(self):
        self.assertEqual(self.vault.name, "Test Vault")
        self.assertEqual(self.vault.depositAsset, "USDC")
        self.assertEqual(self.vault.totalShares, 0)
        self.assertEqual(self.vault.totalAssets, 0)

    def test_deposit(self):
        deposit = 100
        self.vault.deposit(deposit)
        self.assertEqual(deposit, self.vault.totalAssets)

        shares = self.vault.convert_to_shares(deposit)
        self.assertEqual(shares, deposit)

        interest = 10
        self.vault.earn_interest(interest)
        expected_balance = deposit + (deposit * interest / 100)
        self.assertEqual(expected_balance, self.vault.totalAssets)

        holdings = self.vault.convert_to_assets(shares)
        self.assertEqual(holdings, expected_balance)

        self.vault.withdraw(shares)
        self.assertEqual(self.vault.totalAssets, 0)

    def test_vault_shares(self):
        deposit = 100
        self.vault.seed()
        expected_shares = self.vault.convert_to_shares(deposit)

        total_assets = self.vault.totalAssets

        shares = self.vault.deposit(deposit)
        self.assertEqual(shares, expected_shares)

        new_total_assets = self.vault.totalAssets

        assets = self.vault.withdraw(shares)
        self.assertAlmostEqual(assets, new_total_assets - total_assets, places=7)


class TestPortal(unittest.TestCase):
    def setUp(self):
        self.vault_a = ERC4626("Test Vault A", USDC, 0, 0)
        self.vault_b = ERC4626("Test Vault B", USDC, 0, 0)
        self.vault_c = ERC4626("Test Vault C", USDC, 0, 0)

        vault_a_assets = self.vault_a.seed()
        vault_b_assets = self.vault_b.seed()
        vault_c_assets = self.vault_c.seed()

        self.portal = Portal("Test Portal", USDC, 0, 0)

    def test_portal_init(self):
        self.portal.add_vault(self.vault_a, 40)
        self.portal.add_vault(self.vault_b, 30)
        self.portal.add_vault(self.vault_c, 30)

        self.assertEqual(len(self.portal.sub_vaults), 3)
        expected_vaults = [self.vault_a, self.vault_b, self.vault_c]
        expected_ratios = [40, 30, 30]

        for (vault, data), expected_vault, expected_ratio in zip(
            self.portal.sub_vaults.items(), expected_vaults, expected_ratios
        ):
            self.assertIn(vault, expected_vaults)
            self.assertEqual(vault, expected_vault)
            self.assertEqual(data["ratio"], expected_ratio)

    def test_portal_deposits(self):
        deposit = 1234
        expected_shares = self.portal.convert_to_shares(deposit)
        
        # shares should equal deposit as new vault
        self.assertEqual(deposit, expected_shares)

        self.portal.deposit(deposit)
        self.assertEqual(deposit, self.portal.totalAssets)
        self.assertEqual(deposit, self.portal.totalShares)
        self.assertEqual(deposit, self.portal.cash)

        deposit2 = 5678
        expected_shares2 = self.portal.convert_to_shares(deposit2)
        self.assertEqual(deposit2, expected_shares2)

        self.portal.deposit(deposit2)
        self.assertEqual(deposit + deposit2, self.portal.totalAssets)
        self.assertEqual(deposit + deposit2, self.portal.totalShares)
        self.assertEqual(deposit + deposit2, self.portal.cash)


if __name__ == "__main__":
    unittest.main()
