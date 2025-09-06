import random
import asyncio
from pydantic import BaseModel
from collections import defaultdict

# Simulate a global state for resource contention and active tasks
_resource_locked = False
_active_tasks = defaultdict(int) # Tracks how many tasks each protocol is currently handling
_PROTOCOL_CAPACITY = {
    "Code Generation": 2,
    "Security Scan": 1,
    "Infrastructure Generation": 1,
    "Automated Testing": 3,
    "Automated Deployment": 1,
    "External Service Integration": 2
}

class NexusCheckResult(BaseModel):
    status: str  # e.g., "ok", "conflict_detected", "waiting_on_dependency", "capacity_exceeded"
    message: str

async def perform_nexus_check(protocol_name: str, action: str) -> NexusCheckResult:
    """Placeholder for Nexus Protocol's inter-protocol communication and conflict resolution logic."""
    global _resource_locked
    global _active_tasks

    print(f"[NEXUS_MANAGER] Performing check for {protocol_name} before {action}...")
    
    # Simulate capacity check
    if _active_tasks[protocol_name] >= _PROTOCOL_CAPACITY.get(protocol_name, 1):
        return NexusCheckResult(
            status="capacity_exceeded",
            message=f"Nexus: {protocol_name} capacity exceeded. Waiting for resources to free up."
        )

    # Simulate different outcomes
    # Higher chance of conflict if resource is locked
    weights = [0.7, 0.2, 0.1] # ok, conflict_detected, waiting_on_dependency
    if _resource_locked:
        weights = [0.1, 0.6, 0.3] # Increased chance of conflict or waiting

    outcome = random.choices(['ok', 'conflict_detected', 'waiting_on_dependency'], weights=weights, k=1)[0]
    
    status = "ok"
    message = f"Nexus check passed for {protocol_name} before {action}."

    if outcome == 'conflict_detected':
        status = "conflict_detected"
        message = f"Nexus detected a conflict: {protocol_name} cannot proceed while a critical resource is in use. (Simulated conflict)."
        _resource_locked = True # Simulate resource becoming locked due to conflict
    elif outcome == 'waiting_on_dependency':
        status = "waiting_on_dependency"
        message = f"Nexus is waiting on a dependency for {protocol_name} before {action}. Simulating delay and retry..."
        
        # Simulate a few retries
        for i in range(3):
            print(f"[NEXUS_MANAGER] Retry {i+1} for {protocol_name} before {action}...")
            await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulate a delay
            if random.random() > 0.5: # 50% chance to resolve dependency
                status = "ok"
                message = f"Nexus dependency resolved for {protocol_name} before {action}."
                break
        else:
            # If after retries, still waiting
            status = "waiting_on_dependency"
            message = f"Nexus dependency for {protocol_name} before {action} could not be resolved after retries. Still waiting."
    
    if status == "ok" and _resource_locked and random.random() > 0.8: # Small chance to unlock resource if ok
        _resource_locked = False
        print("[NEXUS_MANAGER] Simulated resource unlocked.")

    if status == "ok":
        _active_tasks[protocol_name] += 1 # Increment active tasks if check passes

    return NexusCheckResult(
        status=status,
        message=message
    )

def release_nexus_resource(protocol_name: str):
    """Simulates releasing a resource after a protocol completes its task."""
    global _active_tasks
    if _active_tasks[protocol_name] > 0:
        _active_tasks[protocol_name] -= 1
        print(f"[NEXUS_MANAGER] Resource released for {protocol_name}. Active tasks: {_active_tasks[protocol_name]}")
