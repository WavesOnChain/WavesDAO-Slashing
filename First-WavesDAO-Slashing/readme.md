# First WavesDAO participation & Slashing Implementation Report

## Overview
This report summarizes the analysis and implementation of participation-based slashing mechanics for WavesDAO governance, conducted between November 2023 and November 27, 2024.

## Analysis Contributors
- [**WavesOnChain**](https://wavesonchain.com/): Provided on-chain data analysis & wallet participation research
- [**WavesFunnyNode**](https://wavesfunnynode.com/): Collaborated on wallet participation research

## Implementation Details

### Participation Requirements
- **Minimum Quorum**: 30% participation in proposals per epoch
- **Slashing Penalty**: 20% of committed PWR tokens for non-compliant wallets

### Analysis Period
- **Start Date**: November 2023
- **End Date**: November 27, 2024
- **Total Proposals Analyzed**: 79

## Calculation Logic
The slashing mechanism uses this core logic:

1. **Quorum Calculation**:
   - Required votes = Total proposals × 30%

2. **Wallet Evaluation**:
   - For each wallet:
     - If voted_count ≥ required_votes AND participation_percentage ≥ 30%:
       - Wallet passes
     - Otherwise:
       - Slash amount = committed_tokens × 20%
       - Remaining = committed_tokens - slash_amount

## Implementation Process

### Data Processing Logic
The implementation follows these key steps:
1. Calculates minimum required votes for each wallet based on 30% of total proposals
2. Tracks individual wallet participation across all proposals
3. Evaluates wallets against quorum requirements
4. Applies 20% slashing to non-compliant wallets
5. Generates reports for passed and failed wallets

### Output Reports
The process generates detailed reports containing:
- List of compliant wallets
- List of wallets subject to slashing
- Overall participation statistics
- Total PWR tokens affected
