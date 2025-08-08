#!/usr/bin/env python3
"""
Basic usage example for NeuroSei Python SDK
"""

import asyncio
from neurosei import AI

async def main():
    # Initialize AI assistant
    ai = AI()
    
    # Example shard data
    shard_data = {
        "shard_id": "shard_001",
        "transactions": 1000,
        "gas_used": 50000,
        "block_time": 2.5
    }
    
    # Analyze shard performance
    analysis = await ai.analyze_shard(shard_data)
    print(f"Shard analysis: {analysis}")
    
    # Predict optimal fees
    network_state = {
        "total_validators": 100,
        "network_load": 0.75,
        "gas_price": 0.001
    }
    
    optimal_fee = await ai.predict_optimal_fees(network_state)
    print(f"Optimal fee rate: {optimal_fee}")

if __name__ == "__main__":
    asyncio.run(main()) 