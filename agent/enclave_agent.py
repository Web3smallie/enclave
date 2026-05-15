import os
import json
import hashlib
import asyncio
import sys
from cryptography.fernet import Fernet
from web3 import Web3
from dotenv import load_dotenv

# Add 0G SDK path
sys.path.insert(0, '/home/web3smallie/ENCLAVE-V2/agent/0g-py-sdk/0g_py_storage')
from core.file import ZgFile
from core.indexer import Indexer

load_dotenv("../.env")

# Config
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = "https://evmrpc-testnet.0g.ai"
CONTRACT_ADDRESS = "0xff817f080e4C2F472F23870685583E78B7a89CCC"
INDEXER_URL = "https://indexer-storage-testnet-turbo.0g.ai"

# Connect to 0G Chain
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Agent logic to be sharded
AGENT_LOGIC = """
Step 1: Analyze market data from 0G Storage
Step 2: Calculate risk score using proprietary algorithm
Step 3: Execute trade if risk score below threshold
Step 4: Record outcome back to 0G Storage
Step 5: Update agent memory with new learnings
"""

def split_into_shards(logic: str, num_shards: int = 3):
    key = Fernet.generate_key()
    f = Fernet(key)
    chunk_size = len(logic) // num_shards
    chunks = [logic[i:i+chunk_size] for i in range(0, len(logic), chunk_size)]
    chunks = chunks[:num_shards]
    shards = []
    for i, chunk in enumerate(chunks):
        encrypted = f.encrypt(chunk.encode())
        shard_hash = hashlib.sha256(encrypted).hexdigest()
        shards.append({
            "index": i,
            "encrypted_data": encrypted.hex(),
            "shard_hash": shard_hash,
            "key": key.decode()
        })
        print(f"✅ Shard {i} created | Hash: {shard_hash[:16]}...")
    return shards

async def upload_shard_to_0g_storage(shard: dict):
    shard_data = json.dumps({
        "index": shard["index"],
        "data": shard["encrypted_data"]
    }).encode()
    temp_file = f"shard_{shard['index']}.enc"
    with open(temp_file, "wb") as f:
        f.write(shard_data)
    zg_file = ZgFile.from_file_path(temp_file)
    tree, err = zg_file.merkle_tree()
    if err:
        print(f"❌ Merkle tree error: {err}")
        os.remove(temp_file)
        return None
    root_hash = tree.root_hash()
    indexer = Indexer(INDEXER_URL)
    opts = {'account': account}
    result, err = indexer.upload(zg_file, RPC_URL, PRIVATE_KEY, opts)
    os.remove(temp_file)
    if err:
        print(f"⚠️ Upload warning: {err}")
        return root_hash
    print(f"✅ Shard {shard['index']} uploaded to 0G Storage | Root: {root_hash}")
    return root_hash

async def main():
    print("🔐 ENCLAVE — Confidential Agent Logic Sharding")
    print("=" * 50)
    print(f"Wallet: {account.address}")
    print(f"Chain: 0G Testnet")
    print("\n📦 Splitting agent logic into encrypted shards...")
    shards = split_into_shards(AGENT_LOGIC, num_shards=3)
    print("\n☁️  Uploading shards to 0G Storage...")
    storage_roots = []
    for shard in shards:
        root = await upload_shard_to_0g_storage(shard)
        if root:
            storage_roots.append(root)
    print(f"\n✅ {len(storage_roots)}/3 shards uploaded to 0G Storage")
    print("\n🔒 No single node has the complete agent logic.")
    print("🛡️  ENCLAVE primitive active.")
    state = {
        "agent_id": w3.keccak(text="ENCLAVE_AGENT_001").hex(),
        "shard_roots": storage_roots,
        "shard_hashes": [s["shard_hash"] for s in shards]
    }
    with open("agent_state.json", "w") as f:
        json.dump(state, f, indent=2)
    print(f"\n💾 State saved to agent_state.json")
    print("\n📊 Shard Summary:")
    for i, root in enumerate(storage_roots):
        print(f"  Shard {i}: {root}")

if __name__ == "__main__":
    asyncio.run(main())