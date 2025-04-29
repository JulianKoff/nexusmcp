"""
Web3 integration manager for handling blockchain interactions.
"""
from typing import Dict, Any, Optional, List
from web3 import Web3
from web3.types import TxReceipt, BlockData, LogReceipt, Wei

class Web3Manager:
    """Manages Web3 instances and interactions with different blockchain networks."""

    def __init__(self):
        self.web3_instances: Dict[int, Web3] = {}
        self.contracts: Dict[int, Dict[str, Any]] = {}

    async def initialize(self, config: Dict[int, Dict[str, Any]]) -> None:
        """Initialize Web3 instances for each chain."""
        for chain_id, chain_config in config.items():
            w3 = Web3(Web3.HTTPProvider(chain_config["rpc_url"]))
            if chain_config.get("is_poa"):
                from web3.middleware import geth_poa_middleware
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            self.web3_instances[chain_id] = w3
            self.contracts[chain_id] = {}
            for contract_name, contract_config in chain_config.get("contracts", {}).items():
                self.contracts[chain_id][contract_name] = w3.eth.contract(
                    address=contract_config["address"],
                    abi=contract_config["abi"]
                )

    async def cleanup(self) -> None:
        """Cleanup resources."""
        for w3 in self.web3_instances.values():
            if hasattr(w3.provider, "close"):
                await w3.provider.close()

    async def get_balance(self, chain_id: int, address: str) -> Wei:
        """Get native token balance."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        return await self.web3_instances[chain_id].eth.get_balance(address)

    async def get_token_balance(self, chain_id: int, token_address: str, address: str) -> int:
        """Get ERC20 token balance."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        contract = self.web3_instances[chain_id].eth.contract(
            address=token_address,
            abi=[{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]
        )
        return await contract.functions.balanceOf(address).call()

    async def get_transaction_receipt(self, chain_id: int, tx_hash: str) -> Optional[TxReceipt]:
        """Get transaction receipt."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        return await self.web3_instances[chain_id].eth.get_transaction_receipt(tx_hash)

    async def estimate_gas(self, chain_id: int, transaction: Dict[str, Any]) -> int:
        """Estimate gas for a transaction."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        return await self.web3_instances[chain_id].eth.estimate_gas(transaction)

    async def get_block_number(self, chain_id: int) -> int:
        """Get current block number."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        return await self.web3_instances[chain_id].eth.block_number

    async def get_block(self, chain_id: int, block_identifier: int) -> BlockData:
        """Get block data."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        return await self.web3_instances[chain_id].eth.get_block(block_identifier)

    async def get_logs(self, chain_id: int, filter_params: Dict[str, Any]) -> List[LogReceipt]:
        """Get event logs."""
        if chain_id not in self.web3_instances:
            raise ValueError(f"Chain ID {chain_id} not supported")
        return await self.web3_instances[chain_id].eth.get_logs(filter_params)

    def get_contract(self, chain_id: int, contract_name: str) -> Any:
        """Get deployed contract instance."""
        if chain_id not in self.contracts:
            raise ValueError(f"Chain ID {chain_id} not supported")
        if contract_name not in self.contracts[chain_id]:
            raise ValueError(f"Contract {contract_name} not found for chain {chain_id}")
        return self.contracts[chain_id][contract_name] 