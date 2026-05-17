# enclave-sdk-0g

Confidential agent-logic execution primitive on 0G Labs.

## Install

```bash
npm install enclave-sdk-0g
```

## Usage

```typescript
import { enclave } from 'enclave-sdk-0g';

// Protect agent logic across 3 TEE enclaves on 0G
const result = await enclave.protect(myAgentLogic, { shards: 3 });

// Verify execution proof on 0G Chain
const proof = await enclave.verify(result.agentId);
```

## What it does

ENCLAVE splits your TypeScript agent logic into encrypted semantic shards using an AST parser, executes each shard in a separate TeeML hardware enclave on 0G Compute, uploads to 0G Storage, and records every step on 0G Chain.

## Links

- GitHub: https://github.com/Web3smallie/enclave
- Dashboard: https://enclave-roan.vercel.app