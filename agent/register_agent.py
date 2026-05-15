import os
import sys
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv("../.env")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = "https://evmrpc-testnet.0g.ai"
CONTRACT_ADDRESS = "0xff817f080e4C2F472F23870685583E78B7a89CCC"

# The 3 shard roots from our upload
SHARD_ROOTS = [
    "0x48c17b36b89353e67162043f7e35eca13b6e7c2d2940858facdc50002ef58fca",
    "0xa8a8342f3a09f187225117d7b56be35bc163412b8bb2693feea141fa38958808",
    "0x437269000733ca61a35edbc50b5215bcb2c518bb39ec8bc43c96d4b752d99d52"
]

SHARD_HASHES = [
    "0xf3bb65f884a553060000000000000000000000000000000000000000000000000",
    "0xd2adbdf0ff2d5ef20000000000000000000000000000000000000000000000000",
    "0x9e85314b6ec7d9000000000000000000000000000000000000000000000000000"
]

ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "agentId", "type": "bytes32"},
            {"internalType": "uint256", "name": "totalShards", "type": "uint256"},
            {"internalType": "bytes32[]", "name": "shardHashes", "type": "bytes32[]"},
            {"internalType": "bytes32[]", "name": "storageRoots", "type": "bytes32[]"}
        ],
        "name": "registerAgent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "agentId", "type": "bytes32"},
            {"internalType": "uint256", "name": "shardIndex", "type": "uint256"},
            {"internalType": "bytes32", "name": "outputHash", "type": "bytes32"}
        ],
        "name": "recordExecution",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "agentId", "type": "bytes32"},
            {"internalType": "uint256", "name": "shardIndex", "type": "uint256"}
        ],
        "name": "recordDestruction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "agentId", "type": "bytes32"},
            {"internalType": "uint256", "name": "shardIndex", "type": "uint256"}
        ],
        "name": "getShard",
        "outputs": [
            {"internalType": "bytes32", "name": "shardHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "storageRoot", "type": "bytes32"},
            {"internalType": "address", "name": "executedBy", "type": "address"},
            {"internalType": "uint256", "name": "executedAt", "type": "uint256"},
            {"internalType": "bool", "name": "executed", "type": "bool"},
            {"internalType": "bool", "name": "destroyed", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def register_agent():
    print("🔐 ENCLAVE — Registering Agent on 0G Chain")
    print("=" * 50)

    # Generate agent ID
    agent_id = w3.keccak(text="ENCLAVE_AGENT_001")
    print(f"Agent ID: {agent_id.hex()}")

    # Convert roots to bytes32
    shard_hashes = [bytes.fromhex(h[2:].ljust(64, '0')) for h in SHARD_HASHES]
    storage_roots = [bytes.fromhex(r[2:]) for r in SHARD_ROOTS]

    # Build transaction
    tx = contract.functions.registerAgent(
        agent_id,
        3,
        shard_hashes,
        storage_roots
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': w3.eth.gas_price,
    })

    # Sign and send
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"✅ Agent registered on 0G Chain!")
    print(f"TX Hash: {tx_hash.hex()}")
    print(f"Block: {receipt['blockNumber']}")
    print(f"Agent ID: {agent_id.hex()}")
    
    # Save agent ID for other scripts
    with open("agent_state.json", "w") as f:
        json.dump({
            "agent_id": agent_id.hex(),
            "shard_roots": SHARD_ROOTS,
            "tx_hash": tx_hash.hex()
        }, f, indent=2)
    
    print("\n💾 Agent state saved to agent_state.json")

if __name__ == "__main__":
    register_agent()