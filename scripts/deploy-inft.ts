import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying ENCLAVE Agent iNFT with:", deployer.address);

  const INFT = await ethers.getContractFactory("ENCLAVEAGENT");
  const inft = await INFT.deploy();
  await inft.waitForDeployment();

  const address = await inft.getAddress();
  console.log("ENCLAVEAGENT iNFT deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});