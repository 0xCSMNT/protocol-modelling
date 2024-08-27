import unittest
from src.components import ERC4626

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
        expected_shares = self.vault.convert_to_assets(deposit)
        print(f"expected_shares :{expected_shares}")

        total_assets = self.vault.totalAssets

        shares = self.vault.deposit(deposit)
        self.assertEqual(shares, expected_shares)

        new_total_assets = self.vault.totalAssets

        assets = self.vault.withdraw(shares)
        self.assertEqual(assets, new_total_assets - total_assets)


if __name__ == "__main__":
    unittest.main()
