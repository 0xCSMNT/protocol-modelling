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

    fund1 = Fund("Smart Fund", USDC, 0, 0, 10, 1)
    fund2 = Fund("Simple Fund", USDC, 0, 0, 10, 1)
    fund3 = Fund("Smart Fund without Gas Cost", USDC, 0, 0, 10, 1)
    fund4 = Fund("Simple Fund without Gas Cost", USDC, 0, 0, 10, 1)

    for fund in [fund1, fund2, fund3, fund4]:
        fund.add_vault(initialized_vaults[0], 40)
        fund.add_vault(initialized_vaults[1], 30)
        fund.add_vault(initialized_vaults[2], 30)
        fund.deposit(1000)
        fund.simple_rebalance()

    days = 365 * 5   
    transaction_cost = 0.005811 

    for day in range(days):
        daily_deposit = random.randint(1_000, 100_000)
        
        for fund in [fund1, fund2, fund3, fund4]:
            fund.deposit(daily_deposit)
        
        fund1.smart_rebalance(transaction_cost)
        fund2.simple_rebalance(transaction_cost)
        fund3.smart_rebalance()
        fund4.simple_rebalance()

        for vault in fund1.sub_vaults:
            daily_interest = random.randint(1, 10) / 365 / 10
            vault.earn_interest(daily_interest)

    funds = [fund1, fund2, fund3, fund4]

    
    fund_names = ["Smart Fund 1", "Simple Fund 2", "Smart Fund without Gas Cost 3", "Simple Fund without Gas Cost 4"]
    ranked_funds = sorted(funds, key=lambda x: x.totalAssets, reverse=True)

    print("\nFunds Ranked by Total Assets:")
    for rank, fund in enumerate(ranked_funds, start=1):
        print(f"{rank}. {fund.name}")

    for fund, name in zip(funds, fund_names):
        print(f"\n{name}:")
        print(f"Fund total assets: {fund.totalAssets:,.2f}")
        print(f"Fund cash: {fund.cash:,.2f}")
        print(f"Percentage: {fund.cash / fund.totalAssets:.18f}")
    
    funds = [fund2, fund3, fund4]  

    for i, fund in enumerate(funds, start=2): 
        print(f"\nDelta vs {fund.name}:") 
        print(f"\nDelta abs: {fund.totalAssets - fund1.totalAssets:.2f}")
        print(f"Delta %: {(fund.totalAssets - fund1.totalAssets) / fund.totalAssets * 100:.18f}")

    print("\n")

if __name__ == "__main__":
    main()