import * as dotenv from "dotenv";
dotenv.config();
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "@openzeppelin/hardhat-upgrades";

const PRIVATE_KEY = process.env.PRIVATE_KEY || "";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.22",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    zerogravity: {
      url: "https://evmrpc.0g.ai",
      accounts: [PRIVATE_KEY],
      chainId: 16661,
    },
    zerogravity_testnet: {
      url: "https://evmrpc-testnet.0g.ai",
      accounts: [PRIVATE_KEY],
      chainId: 16602,
    },
  },
};

export default config;