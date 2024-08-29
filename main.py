from src.components import *
from src.simulation import *
import random

random.seed(42)
USDC = "USDC"

# NOTES

# the goal of the sim is to maximize capital efficiency
# capital efficiency is achieved by returning the greatest possible return
# for the invested capital after transaction costs

# the protocol is a fund type structure that invests in a number of different interest-baring vaults
# it executes a diversified strategy according to the goals of the asset manager
# it receives capital from users that accumulates in a reserve and deposits them to into the 
# yield baring vaults on the users behalf according to an algo
# we want to make that algo as efficient as possible

# there is a tradeoff between transaction cost, and lost interest due to idle capital
# it should be a problem that has an optimal min/max
# the optimal point will move depeding on market conditions and the state of the Fund
# things like gas cost for transacting and trading fees/slippage influence costs

# COMMENTS

# initialize a number of vaults on 3 example protocols
# each protocol has a number of vaults
# these are bundled together in a Portal contract on a per protocol basis
# the Portal stores data about what ratio to invest funds into each of the 
# vaults on the protocol

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

    # a Fund contract is created that sits above the Portal
    # it has data about:
    # 1. a certain % of reserve cash it needs to maintain for fast withdrawal
    # 2. a certain % max delta that assets are allowed to deviate from their defined ratios

    fund = Fund("USab", USDC, 0, 0, 10, 1)

    fund.add_vault(cfg_portal, 30)
    fund.add_vault(morpho_portal, 30)
    fund.add_vault(yearn_portal, 30)

    # we initialize by deposited 1000 to the fund
    fund.deposit(1000)

    # we call simple rebalance to distribute funds to each Portal according to their ratios
    fund.simple_rebalance()

    # within each portal we call simple rebalance to deposit funds into each vault according to their ratios
    for portal in portals.values():
        portal.simple_rebalance()


    #### SIMULATION ####

    # assume 5 years of rebalancing
    days = 365 * 5

    print(f"Starting long-term simulation for {days} days...")

    # every day the fund gets a random deposit of between 1,000 and 100,000
    # this is distributed to each portal by a smart rebalance algo
    # smart rebalance will only deposit to a portal when it's actual value has deviated 
    # from the defined ratio by more than the maxDelta 
    for day in range(days):
        daily_deposit = random.randint(1_000, 100_000)
        fund.deposit(daily_deposit)
        fund.smart_rebalance()
        
        # simple rebalance from the portals into the vaults
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
