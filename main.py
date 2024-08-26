# modules
import sys
import os
from src.components import ERC4626, Portal
import random

random.seed(42)
USDC = "USDC"


def initialize_vaults(num_vaults):
    vaults = []
    for i in range(num_vaults):
        vault_name = f"Morpho Vault {chr(65 + i)}"  # A, B, C, ...
        vault = ERC4626(vault_name, USDC, 0, 0)
        vault.seed()
        vaults.append(vault)
    return vaults

def create_portal(vaults, name, ratios):
    if sum(ratios) == 100:
        portal = Portal(name, USDC, 0, 0)
        for i in range(len(vaults)):
            portal.add_vault(vaults[i], ratios[i])
        
        return portal
    
    else:
        raise ValueError("Ratios do not sum to 100") 


def run_simulation():
    vaults = initialize_vaults(3)
    ratios = [40, 30, 30]
    portal = create_portal(vaults, "Morpho Vault", ratios)


    # Test investments
    portal.deposit(100)
    cash_to_invest = portal.cash
    for vault in portal.sub_vaults:
        ratio = portal.sub_vaults[vault]['ratio']
        amount_to_invest = cash_to_invest * (ratio / 100)
        portal.invest(vault, amount_to_invest)

    # print state
    print("\nOverall State:")
    for vault in vaults:
        print(f"\n{vault.name}:")
        print(f"  Total Assets: {vault.totalAssets:.2f} {USDC}")
        print(f"  Total Shares: {vault.totalShares:.2f}")
        print(f"  Portal's Shares: {portal.sub_vaults[vault]['shares']:.2f}")
        print(f"  Portal's Ratio: {portal.sub_vaults[vault]['ratio']}%")
        portal_value = portal.value_position(vault)
        print(f"  Portal's Position Value: {portal_value:.2f} {USDC}")

    total_portal_value = sum(portal.value_position(vault) for vault in vaults)
    print(f"\nTotal Portal Investments: {total_portal_value:.2f} {USDC}")

    # Check remaining cash
    print(f"Remaining cash in portal: {portal.cash:.2f} {USDC}")


if __name__ == "__main__":
    run_simulation()