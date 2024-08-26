# modules
import sys
import os
from src.components import ERC4626, Portal
import random

random.seed(42)
USDC = "USDC"



def initialize_vaults(protocols):
    vaults = []
    for protocol in protocols:
        protocol_name = protocol["name"]
        num_vaults = protocol["vaults"]

        for i in range(num_vaults):
            vault_name = f"{protocol_name} Vault {chr(65 + i)}"  # A, B, C, ...
            vault = ERC4626(vault_name, "USDC", 0, 0)
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
    

protocols = [
    {"name": "Centrifuge", "vaults": 3, "ratios": [40, 30, 30]},
    {"name": "Morpho", "vaults": 2, "ratios": [60, 40]},
    {"name": "Yearn", "vaults": 2, "ratios": [50, 50]},
]


def run_simulation():
    vaults = initialize_vaults(protocols)

    for vault in vaults:
        print(f"Vault: {vault.name}")
        print(f"  Total Assets: {vault.totalAssets}")
        print(f"  Total Shares: {vault.totalShares}")


if __name__ == "__main__":
    run_simulation()
