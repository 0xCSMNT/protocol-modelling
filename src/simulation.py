from src.components import ERC4626, Portal

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
