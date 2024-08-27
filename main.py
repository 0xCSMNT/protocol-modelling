from src.components import ERC4626, Portal, Fund
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
            vault = ERC4626(vault_name, USDC, 0, 0)
            vault.seed()
            vaults.append(vault)

    return vaults


def create_portals(vaults, protocols):
    portals = {}
    vault_dict = {vault.name: vault for vault in vaults}

    for protocol in protocols:
        protocol_name = protocol["name"]
        protocol_vault_names = [
            f"{protocol_name} Vault {chr(65 + i)}" for i in range(protocol["vaults"])
        ]
        protocol_vaults = [vault_dict[name] for name in protocol_vault_names]
        protocol_ratios = protocol["ratios"]

        portal = create_portal(protocol_vaults, protocol_name, protocol_ratios)
        portals[protocol_name] = portal

    return portals


def create_portal(vaults, name, ratios):
    if sum(ratios) != 100:
        raise ValueError("Ratios do not sum to 100")

    portal = Portal(name, USDC, 0, 0)
    for vault, ratio in zip(vaults, ratios):
        portal.add_vault(vault, ratio)

    return portal


protocols = [
    {"name": "Centrifuge", "vaults": 3, "ratios": [40, 30, 30]},
    {"name": "Morpho", "vaults": 2, "ratios": [60, 40]},
    {"name": "Yearn", "vaults": 2, "ratios": [50, 50]},
]


def run_simulation():
    initialized_vaults = initialize_vaults(protocols)
    portals = create_portals(initialized_vaults, protocols)

    cfg_portal = portals["Centrifuge"]
    morpho_portal = portals["Morpho"]
    yearn_portal = portals["Yearn"]

    fund = Fund("USab", USDC, 0, 0, 10)

    fund.add_vault(cfg_portal, 25)
    fund.add_vault(morpho_portal, 25)
    fund.add_vault(yearn_portal, 50)

    fund.deposit(1000)

    print(f"Fund total assets: {fund.totalAssets} {USDC}")
    print(f"Fund cash: {fund.cash} {USDC}")

    cash_to_invest = fund.cash
    for vault in fund.sub_vaults:
        ratio = fund.sub_vaults[vault]["ratio"]
        amount_to_invest = cash_to_invest * (ratio / 100)
        fund.invest(vault, amount_to_invest)

    print(f"Fund cash after investing: {fund.cash:.2f} {USDC}")
    print(f"Fund total assets: {fund.totalAssets:.2f} {USDC}")

    for portal_name, portal in portals.items():
        print(f"\n{portal_name} Portal:")
        print(f"  Total Assets: {portal.totalAssets:.2f} {USDC}")
        print(f"  Cash: {portal.cash:.2f} {USDC}")
        print(f"  Total Shares: {portal.totalShares:.2f}")
        fund_shares = fund.sub_vaults[portal]["shares"]
        print(f"  Fund's Shares: {fund_shares:.2f}")
        fund_ratio = fund.sub_vaults[portal]["ratio"]
        print(f"  Fund's Allocation Ratio: {fund_ratio}%")
        portal_value = fund.value_position(portal)
        print(f"  Fund's Position Value: {portal_value:.2f} {USDC}")


if __name__ == "__main__":
    run_simulation()
