import random

##################   ERC4626   ###################
##################################################


class ERC4626:
    def __init__(self, name, depositAsset, totalShares, totalAssets):
        self.name = name
        self.depositAsset = depositAsset
        self.totalShares = totalShares
        self.totalAssets = totalAssets

    def deposit(self, assets):
        shares = self.convert_to_shares(assets)
        self.totalAssets += assets
        self.totalShares += shares
        return shares

    def withdraw(self, shares):
        if shares > self.totalShares:
            raise ValueError("Insufficient shares")

        assets = self.convert_to_assets(shares)
        self.totalShares -= shares
        self.totalAssets -= assets
        return assets

    def convert_to_shares(self, assets):
        a = assets
        b = self.totalAssets
        t = self.totalShares

        if b == 0 and t == 0:
            shares = a
            return shares

        else:

            shares = a * t / b if b > 0 else a  # avoid division by zero
            return shares

    def convert_to_assets(self, shares):
        s = shares
        b = self.totalAssets
        t = self.totalShares

        assets = s * b / t if t > 0 else s
        return assets

    def seed(self):
        starting_balance = random.uniform(1_000, 1_000_000)
        self.totalAssets = starting_balance
        self.totalShares = starting_balance
        operations = random.randint(1, 10)

        for i in range(operations):
            if i % 2 == 0:
                self.deposit(random.randint(1, 10))
            else:
                self.earn_interest(random.uniform(0, 1))

        return self.totalAssets

    def earn_interest(self, percent):
        amount = self.totalAssets * percent / 100
        self.totalAssets += amount


###################   PORTAL   ###################
##################################################


class Portal(ERC4626):
    def __init__(self, name, depositAsset, totalShares, totalAssets):
        super().__init__(name, depositAsset, totalShares, totalAssets)
        self.sub_vaults = {}
        self.cash = 0

    def add_vault(self, vault, ratio):
        if vault not in self.sub_vaults:
            self.sub_vaults[vault] = {"shares": 0, "ratio": ratio}

    def invest(self, vault, assets):
        if vault in self.sub_vaults:
            shares = vault.deposit(assets)
            self.sub_vaults[vault]["shares"] += shares
            self.cash -= assets
            self.update_total_assets()
            return shares
        else:
            raise ValueError("Vault not found in investments")

    def value_position(self, vault):
        if vault in self.sub_vaults:
            assets = vault.convert_to_assets(self.sub_vaults[vault]["shares"])
            return assets

    def value_portal_investments(self):
        total_investments = 0
        for vault in self.sub_vaults:
            total_investments += self.value_position(vault)
        return total_investments

    def update_total_assets(self):
        self.totalAssets = self.value_portal_investments() + self.cash
        return self.totalAssets

    def simple_rebalance(self):
        excess_cash = self.cash
        for vault, data in self.sub_vaults.items():
            investment = excess_cash * data["ratio"] / 100
            self.invest(vault, investment)

    #### OVERRIDES ####

    def deposit(self, assets):
        self.cash += assets
        shares = ERC4626.deposit(self, assets)
        self.update_total_assets()
        return shares

    # implement withdrawals later when you want to test that logic
    def withdraw(self):
        pass


# connect Fund to Reserve later when you want to have multiple funds operating
class Fund(Portal):
    def __init__(self, name, depositAsset, totalShares, totalAssets, reserveRatio):
        super().__init__(name, depositAsset, totalShares, totalAssets)
        self.reserveRatio = reserveRatio


class Reserve:
    def __init__(self, cash):
        self.cash = cash
