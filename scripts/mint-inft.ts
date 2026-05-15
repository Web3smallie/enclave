import { ethers } from "hardhat";
import * as fs from "fs";
import * as dotenv from "dotenv";
dotenv.config();

const INFT_ADDRESS = '0xe64624675E915fD50748a538d9bD566073B60d52';

const INFT_ABI = [
  {
    inputs: [
      { internalType: 'address', name: 'to', type: 'address' },
      { internalType: 'string', name: 'encryptedURI', type: 'string' },
      { internalType: 'bytes32', name: 'metadataHash', type: 'bytes32' },
    ],
    name: 'mint',
    outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
    stateMutability: 'nonpayable',
    type: 'function',
  },
  {
    inputs: [{ internalType: 'uint256', name: 'tokenId', type: 'uint256' }],
    name: 'getAgent',
    outputs: [
      {
        components: [
          { internalType: 'bytes32', name: 'metadataHash', type: 'bytes32' },
          { internalType: 'string', name: 'encryptedURI', type: 'string' },
          { internalType: 'uint256', name: 'mintedAt', type: 'uint256' },
          { internalType: 'bool', name: 'active', type: 'bool' },
        ],
        internalType: 'struct ENCLAVEAGENT.AgentMetadata',
        name: '',
        type: 'tuple',
      },
    ],
    stateMutability: 'view',
    type: 'function',
  },
];

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log('🔐 Minting ENCLAVE Agent as iNFT...');
  console.log(`Wallet: ${deployer.address}`);

  // Load agent state from latest run
  const state = JSON.parse(fs.readFileSync('agent_state.json', 'utf8'));

  // Build metadata
  const metadata = {
    name: 'ENCLAVE Agent #1',
    description: 'Confidential agent-logic execution primitive on 0G. Logic sharded across 3 TEE enclaves. No single provider ever saw the complete logic.',
    architecture: 'AST_SHARDING + TEE_KEY_GEN + MULTI_NODE_EXECUTION',
    contract: state.contractAddress,
    providers: state.providers,
    storageRoots: state.storageRoots,
    registerTx: state.registerTxHash,
    network: '0G Mainnet',
    standard: 'ERC-7857 iNFT',
    timestamp: state.timestamp,
  };

  const metadataStr = JSON.stringify(metadata);
  const metadataHash = ethers.keccak256(ethers.toUtf8Bytes(metadataStr));
  const encryptedURI = `0g://enclave/${metadataHash}`;

  console.log(`\nMetadata hash: ${metadataHash}`);
  console.log(`Encrypted URI: ${encryptedURI}`);

  const contract = new ethers.Contract(INFT_ADDRESS, INFT_ABI, deployer);

  const tx = await contract.mint(deployer.address, encryptedURI, metadataHash);
  const receipt = await tx.wait();

  console.log(`\n✅ ENCLAVE Agent minted as iNFT!`);
  console.log(`TX: ${receipt.hash}`);
  console.log(`Token ID: 1`);
  console.log(`Contract: ${INFT_ADDRESS}`);
  console.log(`\n🔗 View on ChainScan: https://chainscan.0g.ai/token/${INFT_ADDRESS}`);
}

main().catch(console.error);