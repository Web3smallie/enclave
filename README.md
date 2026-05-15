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
| 0 | `0xd8a8e687586fccbbba7062643d9499a6a0f40a28e5ecf643cbc1b1f168cd1ff6` | `6a6eb59bfbf0f8ce0b9ef6a166a7e833b9d2036690035d38c58fcab3225c9a4e` | `9c6200f0-c80b-4837-a008-1a178a3f4530` | GLM-5-FP8 |
| 1 | `0xc443fe8ec3c1d80e670afc8b0b674e705ef3ef7c57967829a58dd0df7c03c7b5` | `d4df3e50d4e39cddee5a6ee685be36f2616ea1e656b38c8ab221e5765e2c5640` | `d58c512f-0e57-467c-a225-e8a071c280df` | DeepSeek-V3 |
| 2 | `0x07879916b034a0e7582c209fd97e6c7c64d43f9d212277550a03c6835d1b44ff` | `78f2a52828b42eeb0908554aa745464d1c29f393c649ca9c72590af90fd9b33b` | `b45d229b-ccf3-48df-9725-04a703e5708d` | 0GM-1.0-35B |

## Key Generation
- **TEE Session Key Chat ID:** `6d16a5c8-96e4-4e43-a5c5-f7e8dfde66ba`
- **Session Key Ref:** `9f1a2b3c`
- *Provider:* 0xd9966e13a6026Fcca4b13E7ff95c94DE268C471C (GLM-5-FP8)

## Transaction Hashes

| Action | TX Hash |
|--------|---------|
| Agent Registration | `0x49fb94c84da4f3ff846550d04ff69d60cb035ef044dec64694d10ec4f4fae18f` |
| iNFT Mint | `0x5f84f0d4614eaf84b46685473cb4c6a7f356cc67cc6e639c5845c239631719dd` |
| Shard 0 Storage TX | `0xf77b85f9b28db84d173addf7d2d7a311c99dd41ad6ce56423e6e138d315702ed` |
| Shard 1 Storage TX | `0xf3891009b30c00f3caacab376a09fd0ae0496518d75b65c8cad5f053e3ecfc2e` |
| Shard 2 Storage TX | `0x25764d6b87ff98a95627a247b7773ff2b685e3c461064632d4d9030a586df583` |

## Verify on ChainScan

- Contract: https://chainscan.0g.ai/address/0x2ABa418de1A2756989D89aB97aF77f3D8229EddD
- iNFT: https://chainscan.0g.ai/address/0xe64624675E915fD50748a538d9bD566073B60d52
- Registration TX: https://chainscan.0g.ai/tx/0x49fb94c84da4f3ff846550d04ff69d60cb035ef044dec64694d10ec4f4fae18f

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

---

# Hackathon
0G APAC Hackathon 2026 — Track 5: Privacy & Sovereign Infrastructure

---

# Built By
[@Web3smallie](https://github.com/Web3smallie)