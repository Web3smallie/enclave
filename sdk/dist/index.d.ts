export interface ProtectOptions {
    shards?: number;
    network?: 'mainnet' | 'testnet';
}
export interface VerifyResult {
    agentId: string;
    totalShards: number;
    executedShards: number;
    active: boolean;
    shards: {
        index: number;
        shardHash: string;
        storageRoot: string;
        executedBy: string;
        executedAt: number;
        executed: boolean;
        destroyed: boolean;
    }[];
}
export declare const enclave: {
    /**
     * Protect agent logic by splitting it into encrypted shards
     * and registering them on 0G Chain
     */
    protect: (logic: string, options?: ProtectOptions) => Promise<{
        agentId: string;
        shards: number;
    }>;
    /**
     * Verify an agent's execution proof on 0G Chain
     */
    verify: (agentId: string) => Promise<VerifyResult>;
};
export default enclave;
