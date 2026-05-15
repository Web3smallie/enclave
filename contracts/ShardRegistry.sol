// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract ShardRegistry is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    
    struct Shard {
        bytes32 shardHash;        // hash of encrypted shard
        bytes32 storageRoot;      // 0G Storage root hash
        address executedBy;       // node that executed it
        uint256 executedAt;       // block timestamp
        bool executed;            // has it been run
        bool destroyed;           // local copy destroyed
    }

    struct AgentFlow {
        bytes32 agentId;
        uint256 totalShards;
        uint256 executedShards;
        bool active;
        mapping(uint256 => Shard) shards;
    }

    mapping(bytes32 => AgentFlow) private agents;
    
    event AgentRegistered(bytes32 indexed agentId, uint256 totalShards);
    event ShardExecuted(bytes32 indexed agentId, uint256 shardIndex, address executor);
    event ShardDestroyed(bytes32 indexed agentId, uint256 shardIndex);
    event FlowComplete(bytes32 indexed agentId);

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address owner) public initializer {
    __Ownable_init(owner);
    }

    function registerAgent(
        bytes32 agentId,
        uint256 totalShards,
        bytes32[] calldata shardHashes,
        bytes32[] calldata storageRoots
    ) external {
        require(!agents[agentId].active, "Agent already registered");
        require(shardHashes.length == totalShards, "Hash count mismatch");
        require(storageRoots.length == totalShards, "Root count mismatch");

        AgentFlow storage flow = agents[agentId];
        flow.agentId = agentId;
        flow.totalShards = totalShards;
        flow.executedShards = 0;
        flow.active = true;

        for (uint256 i = 0; i < totalShards; i++) {
            flow.shards[i] = Shard({
                shardHash: shardHashes[i],
                storageRoot: storageRoots[i],
                executedBy: address(0),
                executedAt: 0,
                executed: false,
                destroyed: false
            });
        }

        emit AgentRegistered(agentId, totalShards);
    }

    function recordExecution(
        bytes32 agentId,
        uint256 shardIndex,
        bytes32 outputHash
    ) external {
        AgentFlow storage flow = agents[agentId];
        require(flow.active, "Agent not active");
        
        Shard storage shard = flow.shards[shardIndex];
        require(!shard.executed, "Shard already executed");
        require(outputHash != bytes32(0), "Invalid output hash");

        shard.executedBy = msg.sender;
        shard.executedAt = block.timestamp;
        shard.executed = true;
        flow.executedShards++;

        emit ShardExecuted(agentId, shardIndex, msg.sender);

        if (flow.executedShards == flow.totalShards) {
            emit FlowComplete(agentId);
        }
    }

    function recordDestruction(
        bytes32 agentId,
        uint256 shardIndex
    ) external {
        AgentFlow storage flow = agents[agentId];
        Shard storage shard = flow.shards[shardIndex];
        require(shard.executed, "Not yet executed");
        require(!shard.destroyed, "Already destroyed");

        shard.destroyed = true;
        emit ShardDestroyed(agentId, shardIndex);
    }

    function getShard(
        bytes32 agentId,
        uint256 shardIndex
    ) external view returns (
        bytes32 shardHash,
        bytes32 storageRoot,
        address executedBy,
        uint256 executedAt,
        bool executed,
        bool destroyed
    ) {
        Shard storage shard = agents[agentId].shards[shardIndex];
        return (
            shard.shardHash,
            shard.storageRoot,
            shard.executedBy,
            shard.executedAt,
            shard.executed,
            shard.destroyed
        );
    }

    function getAgentStatus(bytes32 agentId) external view returns (
        uint256 totalShards,
        uint256 executedShards,
        bool active
    ) {
        AgentFlow storage flow = agents[agentId];
        return (flow.totalShards, flow.executedShards, flow.active);
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}