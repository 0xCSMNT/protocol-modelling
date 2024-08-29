from src.components import *
from src.simulation import *
import random

random.seed(42)
USDC = "USDC"

protocols = [
    {"name": "Centrifuge", "vaults": 3, "ratios": [40, 30, 30]},
    {"name": "Morpho", "vaults": 2, "ratios": [60, 40]},
    {"name": "Yearn", "vaults": 2, "ratios": [50, 50]},
]

def main():
    initialized_vaults = initialize_vaults(protocols)
    portals = create_portals(initialized_vaults, protocols)

    cfg_portal = portals["Centrifuge"]
    morpho_portal = portals["Morpho"]
    yearn_portal = portals["Yearn"]

    fund = Fund("USab", USDC, 0, 0, 10, 1)

    fund.add_vault(cfg_portal, 30)
    fund.add_vault(morpho_portal, 30)
    fund.add_vault(yearn_portal, 30)

    fund.deposit(1000)

    fund.simple_rebalance()

    for portal in portals.values():
        portal.simple_rebalance()


    days = 365 * 5

    print(f"Starting long-term simulation for {days} days...")

    for day in range(days):
        daily_deposit = random.randint(1_000, 100_000)
        fund.deposit(daily_deposit)
        fund.smart_rebalance()
        
        for portal in portals.values():
            portal.simple_rebalance()
        
        for vault in initialized_vaults:
            vault.earn_interest(random.randint(1, 10) / 365 / 10)

        if day % 30 == 0:  # Print update every 30 days
            print(f"Day {day}: Fund total assets: {fund.totalAssets:.2f}")

    print("\nFinal state after long-term simulation:")
    print(f"Fund total assets: {fund.totalAssets:.2f}")
    print(f"Fund cash: {fund.cash:.2f}")
    for portal, data in fund.sub_vaults.items():
        print(f"  {portal.name} value: {fund.value_position(portal):.2f}")


if __name__ == "__main__":
    main()
