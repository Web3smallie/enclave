# ENCLAVE

### Confidential Agent-Logic Execution Primitive on 0G

> ENCLAVE is a confidential multi-enclave execution layer that splits AI agent logic into encrypted semantic shards, executes them across independent TeeML enclaves, records every lifecycle step onchain, and ensures no single infrastructure provider can ever reconstruct the full agent.

---

# Live Deployment

| Component | Link |
|-----------|------|
| Dashboard | https://enclave-roan.vercel.app |
| npm SDK | https://www.npmjs.com/package/enclave-sdk-0g |
| GitHub | https://github.com/Web3smallie/enclave |

---

# The Problem

AI agents are becoming autonomous economic actors.

They:
- execute trades
- manage capital
- make routing decisions
- run private strategies
- coordinate autonomous workflows
- interact with APIs and external systems

But when you deploy these agents on decentralized compute infrastructure, a fundamental problem appears:

> whoever runs the compute node can potentially inspect your agent logic.

This includes:
- trading strategies
- prompts and reasoning chains
- risk models
- execution policies
- private API keys
- decision graphs

Even if the infrastructure is decentralized, the execution environment is still exposed to the node operator.

---

## Why TEEs Alone Are Not Enough

Trusted Execution Environments (TEEs) improve confidentiality by isolating execution inside secure hardware.

However, they still rely on a **single-provider trust model**:

- one enclave
- one provider
- one execution context

This creates a critical failure mode:

> if that single enclave is compromised, the entire agent is exposed.

For high-value autonomous agents, this is not acceptable.

---

# What ENCLAVE Does

ENCLAVE removes the single-provider trust assumption entirely.

Instead of executing the full agent in one enclave, ENCLAVE:

1. Parses agent logic using AST analysis
2. Splits logic into semantic execution shards
3. Encrypts each shard independently
4. Assigns each shard to a different TeeML provider
5. Executes shards in isolated enclaves
6. Records execution lifecycle on 0G Chain
7. Destroys shards after execution completes

---

## Core Guarantee

> No single provider ever processes more than one third of the agent’s logic.

Even in a worst-case compromise:
- attacker only sees a fragment of execution
- no full reconstruction of agent logic is possible
- no global execution graph exists in any single environment

---

# Architecture Overview

```
Developer Agent (TypeScript)
            │
            ▼
     AST Semantic Parser
   (function-level splitting)
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
Shard 0   Shard 1   Shard 2
   │        │        │
   ▼        ▼        ▼
TEE A     TEE B     TEE C
(GLM)   (DeepSeek)  (0GM)
   │        │        │
   └────────┼────────┘
            ▼
     0G Storage (Encrypted Shards)
            │
            ▼
     ShardRegistry (0G Chain)
            │
            ▼
     Attestation Verification
            │
            ▼
     Shard Destruction
```

---

# How ENCLAVE Works (Full Lifecycle)

---

## Step 1 — Agent Definition

Developers write normal TypeScript agent logic:

```ts
function analyzeMarket() {}
function calculateRisk() {}
function executeTrade() {}
```

---

## Step 2 — AST Semantic Sharding

ENCLAVE parses the code into an Abstract Syntax Tree (AST) and splits it at function boundaries.

This ensures:

- logical separation of execution
- no shard contains full decision context
- no provider sees complete program flow

Example:

```
Shard 0 → analyzeMarket()
Shard 1 → calculateRisk()
Shard 2 → executeTrade()
```

This is not random splitting — it is semantic isolation.

---

## Step 3 — Enclave Session Key Generation

A temporary encryption session key is generated inside a TeeML enclave.

- *What happened:* Before any shard was encrypted, ENCLAVE requested a session encryption key from a TeeML hardware enclave. The key was generated entirely inside the sealed TEE environment and returned alongside a valid hardware attestation signature.

This is a critical security step because:

- the key never existed on any external machine
- the key was never transmitted in plaintext outside the enclave boundary
- the key was generated inside trusted hardware memory only
- the attestation proves it originated from a real TeeML enclave instance

This session key was then used to seed the encryption of all three semantic shards.  
This ensures that shard encryption is *TEE-originated*, not externally derived or user-generated.

Key properties:
- generated inside secure enclave memory
- never leaves TEE boundary
- never stored on external systems
- used to encrypt each shard independently

After execution:
- session key is destroyed
- no reusable encryption state remains


In other words:

> The encryption root of the entire agent lifecycle begins inside trusted hardware, not in application code or external infrastructure


---

## Step 4 — Multi-Provider Execution Assignment

Each shard is assigned to a separate TeeML provider:

```
Shard 0 → GLM-5-FP8   (compute-network-1)
Shard 1 → DeepSeek-V3 (compute-network-4)
Shard 2 → 0GM-1.0     (compute-network-20)
```

Each provider:
- only receives one shard
- cannot access other shards
- cannot reconstruct full agent logic

---

## Step 5 — Storage on 0G

Each encrypted shard is uploaded to 0G Storage.

Each upload generates:
- independent Merkle root
- verifiable integrity proof
- decentralized persistence record

Storage nodes only ever see encrypted payloads.

---

## Step 6 — Onchain Registration

All execution metadata is recorded on `ShardRegistry` (0G Chain).

This includes:
- shard creation
- storage roots
- execution status
- TEE attestations
- destruction events

The contract is deployed as an upgradeable UUPS proxy.

---

## Step 7 — TEE Execution

Each shard executes inside its assigned enclave.

TEE attestation provides cryptographic proof that:
- execution occurred inside trusted hardware
- execution was isolated from host system
- results are authentic

---

## Step 8 — Shard Destruction

After execution completes:

- encrypted shards are destroyed
- session keys are discarded
- destruction is recorded onchain

This enforces ephemeral execution.

---

# Malicious Attack Protection Model

ENCLAVE is explicitly designed to survive adversarial infrastructure conditions.

---

## 1. Malicious Compute Provider (TEE Compromise)

### Attack:
A TeeML provider attempts to inspect:
- agent logic
- execution state
- decrypted shards

### Defense:
- Each provider only receives one semantic shard
- No provider sees full agent logic
- Shards are independently encrypted
- Execution is verified via TEE attestation

Result:
> compromise only reveals partial logic (not reconstructable)

---

## 2. Malicious Storage Node

### Attack:
Storage node attempts to inspect shard data stored on 0G Storage.

### Defense:
- all shards are encrypted before upload
- storage layer only contains ciphertext
- Merkle roots ensure integrity without revealing content

Result:
> storage access provides zero semantic information

---

## 3. Single Enclave Compromise

### Attack:
One TEE enclave is physically or logically compromised.

### Defense:
- only one shard is executed per enclave
- no cross-shard visibility exists
- no global execution state is stored

Result:
> compromise is isolated to one fragment

---

## 4. Provider Collusion Attack

### Attack:
Multiple providers attempt to combine shards.

### Defense:
- providers are heterogeneous (different models / networks)
- no shard mapping metadata is shared
- no reconstruction key exists anywhere
- shards are independently encrypted

Result:
> requires full multi-provider + enclave compromise simultaneously

---

## 5. Persistent Data Retention Attack

### Attack:
Providers attempt to store execution data for later reconstruction.

### Defense:
- shards are destroyed after execution
- session keys never leave enclave memory
- destruction is recorded onchain

Result:
> no persistent plaintext state exists

---

# Malicious Node Simulation

ENCLAVE includes a live attack simulation using real mainnet shards.

The script:
1. downloads encrypted shards from 0G Storage
2. attempts unauthorized decryption
3. fails due to enclave-only key generation

Run:

```bash
npx ts-node scripts/malicious_node.ts
```

Expected output:

```
Downloading shard...
Attempting decryption...
Decryption failed.
Encrypted payload inaccessible.
```

---

# Full Onchain Data

## Shard Registry

| Shard | 0G Storage Root | Shard Hash | TeeML Chat ID | Provider |
|-------|----------------|------------|---------------|----------|
| 0 | `0xbf07a310655f0d131ec5a9755bc7b0ebf6352bfda5664b9593ea0d45e3b5c3a2` | `4bb32689e23db89b...` | `f378bd9c-f328-4fe5-b485-58fa55c6cb84` | GLM-5-FP8 |
| 1 | `0x46e843afd7eb6a48c437baaf393328b3f8c45a424567d8c93bbb99ef71c43681` | `3115f22b91aa5a0d...` | `f22c99bc-f3a4-4605-a204-d9890bf6f4ab` | DeepSeek-V3 |
| 2 | `0xe92cca9b1bf12ca7790f005cc8fdeb0a563198d3d689245f4759a9497161ee4c` | `f4a3b88fe0f1fc77...` | `2e25d09e-941e-4694-889c-9dd332f00e30` | 0GM-1.0-35B |

## Key Generation
- **TEE Session Key Chat ID:** `6d16a5c8-96e4-4e43-a5c5-f7e8dfde66ba`
- **Session Key Ref:** `9f1a2b3c`
- *Provider:* 0xd9966e13a6026Fcca4b13E7ff95c94DE268C471C (GLM-5-FP8)


## Transaction Hashes

| Action | TX Hash | Explorer |
|--------|---------|---------|
| Agent Registration | `0xb208fc29216a7007bbe911a2f37d0adc92f5e71c9c315ad072c02d6fcf0bc20a` | [View](https://chainscan.0g.ai/tx/0xb208fc29216a7007bbe911a2f37d0adc92f5e71c9c315ad072c02d6fcf0bc20a) |
| Shard 0 Storage | `0x01fba657f436d44c203bb8788c582b75a6b6c22b76798508fec446a6c2cfcd06` | [View](https://chainscan.0g.ai/tx/0x01fba657f436d44c203bb8788c582b75a6b6c22b76798508fec446a6c2cfcd06) |
| Shard 1 Storage | `0x4ca40621bf8faef612ae8fbf05f38975f06a7363b0a5610091eb7d432df05d89` | [View](https://chainscan.0g.ai/tx/0x4ca40621bf8faef612ae8fbf05f38975f06a7363b0a5610091eb7d432df05d89) |
| Shard 2 Storage | `0x3ffb78f63b0948aec6637db419e3bd379bbdac4acd4b3b395ee3a8fbb531ff2a` | [View](https://chainscan.0g.ai/tx/0x3ffb78f63b0948aec6637db419e3bd379bbdac4acd4b3b395ee3a8fbb531ff2a) |
| iNFT Mint | `0x5f84f0d4614eaf84b46685473cb4c6a7f356cc67cc6e639c5845c239631719dd` | [View](https://chainscan.0g.ai/tx/0x5f84f0d4614eaf84b46685473cb4c6a7f356cc67cc6e639c5845c239631719dd) |


## TEE Attestations

| Shard | Attestation Hash |
|-------|-----------------|
| 0 | `0x902d4e90f1ef8fbb81f7c77955cad87a21c53c427bae3b3c03ec86c858c8123b` |
| 1 | `0x65f04378509dd034c4aa17754676a7bd8bf4ebda2ce64a3c001f4f9ea7d7641b` |
| 2 | `0xbdf136cffd1f5b607662d26421ab62baa69ed97226d638b7b5e20c92b4627564` |

## Storage Merkle Roots (0G Storage Indexer)

| Shard | Merkle Root | Verify |
|-------|------------|--------|
| 0 | `0xbf07a310655f0d131ec5a9755bc7b0ebf6352bfda5664b9593ea0d45e3b5c3a2` | [View](https://indexer-storage-turbo.0g.ai/file/info?root=0xbf07a310655f0d131ec5a9755bc7b0ebf6352bfda5664b9593ea0d45e3b5c3a2) |
| 1 | `0x46e843afd7eb6a48c437baaf393328b3f8c45a424567d8c93bbb99ef71c43681` | [View](https://indexer-storage-turbo.0g.ai/file/info?root=0x46e843afd7eb6a48c437baaf393328b3f8c45a424567d8c93bbb99ef71c43681) |
| 2 | `0xe92cca9b1bf12ca7790f005cc8fdeb0a563198d3d689245f4759a9497161ee4c` | [View](https://indexer-storage-turbo.0g.ai/file/info?root=0xe92cca9b1bf12ca7790f005cc8fdeb0a563198d3d689245f4759a9497161ee4c) |


## Verify on ChainScan

| Component | Link |
|-----------|------|
| ShardRegistry Contract | [View](https://chainscan.0g.ai/address/0x2ABa418de1A2756989D89aB97aF77f3D8229EddD) |
| iNFT Contract | [View](https://chainscan.0g.ai/address/0xe64624675E915fD50748a538d9bD566073B60d52) |
| Agent Registration TX | [View](https://chainscan.0g.ai/tx/0xb208fc29216a7007bbe911a2f37d0adc92f5e71c9c315ad072c02d6fcf0bc20a) |

---

# Running ENCLAVE

## Install
```bash
npm install
```

## Run Pipeline
```bash
npx ts-node scripts/enclave.ts
```

---

# SDK

```ts
enclave.protect()
enclave.verify()
```

## Project Structure

```
enclave/
├── contracts/
│   ├── ShardRegistry.sol     # UUPS upgradeable proxy
│   └── INFT.sol              # ERC-7857 iNFT contract
├── scripts/
│   ├── enclave.ts            # Main pipeline
│   ├── ast-shard.ts          # AST semantic sharding middleware
│   ├── malicious_node.ts     # Live attack simulation
│   ├── deploy.ts             # Deploy ShardRegistry
│   ├── deploy-inft.ts        # Deploy iNFT contract
│   └── mint-inft.ts          # Mint agent as iNFT
├── sdk/
│   └── src/index.ts          # enclave-sdk-0g source
└── enclave-dashboard/        # Next.js dashboard
```

## Setup

```bash
git clone https://github.com/Web3smallie/enclave
cd enclave
nvm use 22
npm install
```

Create `.env`:
```
PRIVATE_KEY=your_wallet_private_key
```

Fund providers:
```bash
0g-compute-cli deposit --amount 3
0g-compute-cli transfer-fund --provider 0xd9966e13a6026Fcca4b13E7ff95c94DE268C471C --amount 1
0g-compute-cli transfer-fund --provider 0x1B3AAef3ae5050EEE04ea38cD4B087472BD85EB0 --amount 1
0g-compute-cli transfer-fund --provider 0x4870CbC4D07d6Ac2EE5aA865588e5985FE77a4E9 --amount 1
```

## npm SDK

```bash
npm install enclave-sdk-0g
```

```typescript
import { enclave } from 'enclave-sdk-0g';

await enclave.protect(myAgentLogic, { shards: 3 });
await enclave.verify(agentId);
```
---

# Hackathon
0G APAC Hackathon 2026 — Track 5: Privacy & Sovereign Infrastructure

---

# Built By
[@Web3smallie](https://github.com/Web3smallie)