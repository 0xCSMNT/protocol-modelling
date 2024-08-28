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

        self.portal = Portal("Test Portal", USDC, 0, 0)

        self.portal.add_vault(self.vault_a, 40)
        self.portal.add_vault(self.vault_b, 30)
        self.portal.add_vault(self.vault_c, 30)

    def test_portal_init(self):
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

        # shares should equal deposit as vault is new
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

    def test_portal_invest(self):
        deposit = 100
        self.portal.deposit(deposit)

        vault_a_assets = self.vault_a.seed()
        vault_b_assets = self.vault_b.seed()
        vault_c_assets = self.vault_c.seed()

        amount_to_invest = deposit
        for vault, data in self.portal.sub_vaults.items():
            investment = amount_to_invest * data["ratio"] / 100
            self.portal.invest(vault, investment)

        # assert all vault got the right amout of cash
        self.assertEqual(self.vault_a.totalAssets, vault_a_assets + 40)
        self.assertEqual(self.vault_b.totalAssets, vault_b_assets + 30)
        self.assertEqual(self.vault_c.totalAssets, vault_c_assets + 30)

        # assert portal has the right shares in each vault
        for vault, data in self.portal.sub_vaults.items():
            expected_investment = deposit * data["ratio"] / 100
            self.assertAlmostEqual(
                vault.convert_to_assets(data["shares"]), expected_investment
            )

        # assert portal has invested all cash
        self.assertEqual(self.portal.cash, 0)

        # check interal accounting functions
        self.assertEqual(self.portal.value_position(self.vault_a), 40)
        self.assertEqual(self.portal.totalAssets, 100)
        self.assertEqual(self.portal.value_portal_investments(), deposit)


if __name__ == "__main__":
    unittest.main()
