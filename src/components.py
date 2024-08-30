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
    def __init__(
        self, name, depositAsset, totalShares, totalAssets, reserveRatio=0, maxDelta=0
    ):
        super().__init__(name, depositAsset, totalShares, totalAssets)
        self.sub_vaults = {}
        self.cash = 0
        self.reserveRatio = reserveRatio
        self.maxDelta = maxDelta

    def add_vault(self, vault, ratio):
        if vault not in self.sub_vaults:
            self.sub_vaults[vault] = {"shares": 0, "ratio": ratio}

    def invest(self, vault, assets, cost=0):
        if vault in self.sub_vaults:
            shares = vault.deposit(assets - cost)
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

    def simple_rebalance(self, cost=0):
        required_reserve = self.totalAssets * self.reserveRatio / 100
        available_cash = max(0, self.cash - required_reserve)

        if available_cash > 0:
            for vault, data in self.sub_vaults.items():
                target_investment = self.totalAssets * data["ratio"] / 100
                current_investment = self.value_position(vault)
                investment_needed = max(0, target_investment - current_investment)

                investment_amount = min(investment_needed, available_cash)
                if investment_amount > 0:
                    self.invest(vault, investment_amount, cost)
                    available_cash -= investment_amount

    def smart_rebalance(self, cost=0):
        required_reserve = self.totalAssets * self.reserveRatio / 100
        available_cash = max(0, self.cash - required_reserve)
        if available_cash > 0:
            rebalances = {}
            for vault, data in self.sub_vaults.items():
                current_holdings = self.value_position(vault)
                target_holdings = self.totalAssets * data["ratio"] / 100
                delta = target_holdings - current_holdings
                if delta > 0 and delta > self.totalAssets * self.maxDelta / 100:
                    rebalances[vault] = min(delta, available_cash)

            sorted_rebalances = sorted(
                rebalances.items(), key=lambda x: x[1], reverse=True
            )

            for vault, amount in sorted_rebalances:
                if available_cash >= amount:
                    self.invest(vault, amount, cost)
                    available_cash -= amount
                else:
                    self.invest(vault, available_cash, cost)
                    break

    #### OVERRIDES ####

    def deposit(self, assets):
        self.cash += assets
        shares = ERC4626.deposit(self, assets)
        self.update_total_assets()
        return shares

    # implement withdrawals later when you want to test that logic
    def withdraw(self):
        pass


####################   FUND   ####################
##################################################


class Fund(Portal):
    def __init__(
        self, name, depositAsset, totalShares, totalAssets, reserveRatio, maxDelta=0
    ):
        super().__init__(
            name, depositAsset, totalShares, totalAssets, reserveRatio, maxDelta
        )


##################   RESERVE   ###################
##################################################


# class Reserve:
#     def __init__(self, cash, reserveRatio):
#         pass
