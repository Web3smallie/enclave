import { ethers, upgrades } from "hardhat";

const PROXY_ADDRESS = '0x2ABa418de1A2756989D89aB97aF77f3D8229EddD';

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log('Upgrading ShardRegistry with:', deployer.address);

  const ShardRegistry = await ethers.getContractFactory('ShardRegistry');
  const upgraded = await upgrades.upgradeProxy(PROXY_ADDRESS, ShardRegistry);
  await upgraded.waitForDeployment();

  console.log('✅ ShardRegistry upgraded at:', PROXY_ADDRESS);
}

main().catch(console.error);