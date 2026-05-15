import { ethers, upgrades } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying ENCLAVE ShardRegistry with:", deployer.address);

  const ShardRegistry = await ethers.getContractFactory("ShardRegistry");
  
  const registry = await upgrades.deployProxy(ShardRegistry, [deployer.address], {
    initializer: "initialize",
    kind: "uups",
  });

  await registry.waitForDeployment();
  
  const address = await registry.getAddress();
  console.log("ShardRegistry deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});