# DeFi Protocol Optimization

## Project Overview

This project simulates a DeFi (Decentralized Finance) protocol designed to optimize capital efficiency in a multi-vault investment strategy. The goal is to maximize returns on invested capital while minimizing transaction costs and idle capital.

## Key Concepts

- **Vault**: A smart contract that accepts deposits and generates yield.
- **Portal**: A contract that manages multiple vaults from a single protocol.
- **Fund**: The main contract that manages multiple portals and implements the investment strategy.

## Class Hierarchy

1. **ERC4626** (Base class)
   - Represents a standard yield-bearing vault
   - Methods: deposit, withdraw, convert_to_shares, convert_to_assets, earn_interest

2. **Portal** (Inherits from ERC4626)
   - Manages multiple ERC4626 vaults
   - Additional attributes: sub_vaults, cash, reserveRatio, maxDelta
   - Methods: add_vault, invest, value_position, simple_rebalance, smart_rebalance

3. **Fund** (Inherits from Portal)
   - Manages multiple Portals
   - Implements the high-level investment strategy

Note: The Portal and Fund contracts will probably be combined in the final design. They are functionally identical right now

## Optimization Problem

The core challenge is to balance two competing factors:

1. Transaction costs: Each rebalance operation incurs a cost.
2. Opportunity cost of idle capital: Cash sitting in reserves doesn't earn yield.

The optimal solution minimizes the sum of these two costs, which varies based on:
- Current market conditions (e.g., gas prices, interest rates)
- The state of the Fund (e.g., total assets, current allocations)

## Simulation Approach

1. Initialize vaults for multiple protocols
2. Create portals to manage these vaults
3. Set up a fund to manage the portals
4. Run a multi-year simulation:
   - Daily random deposits
   - Rebalance using smart and simple algorithms
   - Apply daily interest to vaults

## Key Parameters

- `reserveRatio`: Percentage of assets to keep as cash for withdrawals
- `maxDelta`: Maximum allowed deviation from target allocation before rebalancing

## Optimization Opportunities

1. **Rebalancing Frequency**: Determine the optimal frequency to minimize transaction costs while maintaining target allocations.
2. **Allocation Strategy**: Develop algorithms to dynamically adjust target allocations based on market conditions and vault performance.
3. **Reserve Management**: Optimize the reserve ratio to balance liquidity needs with yield generation.
4. **Transaction Batching**: Group multiple rebalancing operations to reduce overall transaction costs.

## Getting Started

1. Review the `src/components.py` file to understand the core classes and their methods.
2. Examine `src/simulation.py` to see how the simulation is set up and run.
3. Run the main simulation script to see the protocol in action.
4. Modify parameters and algorithms in the `Fund` and `Portal` classes to experiment with different optimization strategies.

## Next Steps

[ ] Add in DS libs for analysis.
[x] Develop performance metrics to evaluate different strategies.
[ ] Add realistic transaction cost models - price depth on DEXs, swaps between collateral.
[ ] Introduce market volatility and liquidity constraints to the simulation.
[ ] Optimize the rebalancing algo, reserve ratio and add max tx size if neccessary
[ ] Add in multiple funds and solver role that is looking for profitable opportunities to rebalance multiple funds
[ ] Add in withdrawals and behavioural assumptions:
    - e.g if the market goes down x amount, we expected y withdrawals across all funds


Expertise in optimization algorithms would be particularly valuable in refining the `smart_rebalance` method and developing more advanced allocation strategies that can adapt to changing market conditions.