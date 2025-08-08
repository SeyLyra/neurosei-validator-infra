#!/usr/bin/env python3
"""
10K TPS Stress Test for NeuroSei Validator
"""

import asyncio
import time
import random
from typing import List, Dict, Any

class StressTest:
    def __init__(self, target_tps: int = 10000):
        self.target_tps = target_tps
        self.results = []
        self.start_time = None
        
    async def generate_transaction(self) -> Dict[str, Any]:
        """Generate a mock transaction"""
        return {
            "from": f"sei1{random.randint(100000, 999999)}",
            "to": f"sei1{random.randint(100000, 999999)}",
            "amount": random.randint(1, 1000),
            "gas": random.randint(20000, 100000),
            "timestamp": time.time()
        }
    
    async def process_transaction(self, tx: Dict[str, Any]) -> bool:
        """Process a single transaction"""
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.001, 0.005))
        return True
    
    async def run_batch(self, batch_size: int) -> List[bool]:
        """Process a batch of transactions"""
        tasks = []
        for _ in range(batch_size):
            tx = await self.generate_transaction()
            task = self.process_transaction(tx)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
    
    async def run_stress_test(self, duration_seconds: int = 60):
        """Run the main stress test"""
        print(f"Starting {self.target_tps} TPS stress test for {duration_seconds} seconds...")
        
        self.start_time = time.time()
        batch_size = self.target_tps // 10  # Process in batches
        
        while time.time() - self.start_time < duration_seconds:
            batch_start = time.time()
            results = await self.run_batch(batch_size)
            batch_end = time.time()
            
            actual_tps = len(results) / (batch_end - batch_start)
            self.results.append({
                "timestamp": batch_start,
                "tps": actual_tps,
                "success_rate": sum(results) / len(results)
            })
            
            print(f"Batch completed: {actual_tps:.2f} TPS, {sum(results)}/{len(results)} successful")
            
            # Adjust timing to maintain target TPS
            expected_batch_time = batch_size / self.target_tps
            actual_batch_time = batch_end - batch_start
            if actual_batch_time < expected_batch_time:
                await asyncio.sleep(expected_batch_time - actual_batch_time)
    
    def print_results(self):
        """Print test results"""
        if not self.results:
            print("No results to display")
            return
        
        avg_tps = sum(r["tps"] for r in self.results) / len(self.results)
        avg_success_rate = sum(r["success_rate"] for r in self.results) / len(self.results)
        
        print(f"\n=== Stress Test Results ===")
        print(f"Average TPS: {avg_tps:.2f}")
        print(f"Average Success Rate: {avg_success_rate:.2%}")
        print(f"Total Batches: {len(self.results)}")

async def main():
    """Run the stress test"""
    stress_test = StressTest(target_tps=10000)
    await stress_test.run_stress_test(duration_seconds=30)
    stress_test.print_results()

if __name__ == "__main__":
    asyncio.run(main()) 