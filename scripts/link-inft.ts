import { ethers } from "hardhat";

const PROXY_ADDRESS = '0x2ABa418de1A2756989D89aB97aF77f3D8229EddD';
const INFT_ADDRESS = '0xe64624675E915fD50748a538d9bD566073B60d52';
const AGENT_ID = ethers.keccak256(ethers.toUtf8Bytes('ENCLAVE_AGENT_AST_001'));

const ABI = [
  {
    inputs: [
      { internalType: 'bytes32', name: 'agentId', type: 'bytes32' },
      { internalType: 'address', name: 'inftContract', type: 'address' },
      { internalType: 'uint256', name: 'tokenId', type: 'uint256' },
    ],
    name: 'linkINFT',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
];

async function main() {
  const [deployer] = await ethers.getSigners();
  const contract = new ethers.Contract(PROXY_ADDRESS, ABI, deployer);

  console.log('Linking iNFT to agent...');
  const tx = await contract.linkINFT(AGENT_ID, INFT_ADDRESS, 1);
  const receipt = await tx.wait();

  console.log('✅ iNFT linked onchain!');
  console.log(`TX: ${receipt.hash}`);
}

main().catch(console.error);