// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ENCLAVEAGENT is ERC721, Ownable {
    
    struct AgentMetadata {
        bytes32 metadataHash;
        string encryptedURI;
        uint256 mintedAt;
        bool active;
    }

    mapping(uint256 => AgentMetadata) public agents;
    uint256 private _nextTokenId = 1;

    event AgentMinted(uint256 indexed tokenId, bytes32 metadataHash, address owner);
    event AgentUpdated(uint256 indexed tokenId, bytes32 newHash);

    constructor() ERC721("ENCLAVE Agent", "EAGENT") Ownable(msg.sender) {}

    function mint(
        address to,
        string calldata encryptedURI,
        bytes32 metadataHash
    ) external onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        
        agents[tokenId] = AgentMetadata({
            metadataHash: metadataHash,
            encryptedURI: encryptedURI,
            mintedAt: block.timestamp,
            active: true
        });

        emit AgentMinted(tokenId, metadataHash, to);
        return tokenId;
    }

    function updateMetadata(
        uint256 tokenId,
        bytes32 newHash,
        string calldata newURI
    ) external onlyOwner {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        agents[tokenId].metadataHash = newHash;
        agents[tokenId].encryptedURI = newURI;
        emit AgentUpdated(tokenId, newHash);
    }

    function getAgent(uint256 tokenId) external view returns (AgentMetadata memory) {
        return agents[tokenId];
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return agents[tokenId].encryptedURI;
    }
}