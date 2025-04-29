from typing import Dict, Any, Optional, List
from solana.rpc.async_api import AsyncClient
from solana.rpc.websocket import connect
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solders.system_program import transfer, TransferParams
from solders.sysvar import SYSVAR_RENT_PUBKEY
import asyncio
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class SolanaManager:
    """Manager for Solana connections and interactions."""
    
    def __init__(self):
        self.clients: Dict[str, AsyncClient] = {}
        self.ws_clients: Dict[str, Any] = {}
        self.programs: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
        
    async def initialize(self, config: Dict[str, Any]):
        """Initialize Solana connections."""
        self.config = config
        
        # Initialize RPC clients
        self.clients["mainnet"] = AsyncClient(config["SOLANA_RPC_URL"])
        self.clients["devnet"] = AsyncClient(config["SOLANA_DEVNET_RPC_URL"])
        
        # Initialize WebSocket clients
        self.ws_clients["mainnet"] = await connect(config["SOLANA_WS_URL"])
        self.ws_clients["devnet"] = await connect(config["SOLANA_DEVNET_WS_URL"])
        
        # Load programs
        await self._load_programs()
        
    async def _load_programs(self):
        """Load program IDs and interfaces."""
        try:
            # Load mainnet program
            self.programs["mainnet"] = {
                "program_id": PublicKey(self.config["PROGRAM_ID_MAINNET"]),
                "spl_token": PublicKey(self.config["SPL_TOKEN_MAINNET"])
            }
            
            # Load devnet program
            self.programs["devnet"] = {
                "program_id": PublicKey(self.config["PROGRAM_ID_DEVNET"]),
                "spl_token": PublicKey(self.config["SPL_TOKEN_DEVNET"])
            }
        except Exception as e:
            logger.error(f"Failed to load programs: {e}")
            
    async def get_balance(self, network: str, address: str) -> int:
        """Get SOL balance for an address."""
        client = self.clients.get(network)
        if not client:
            raise ValueError(f"No client for network {network}")
            
        try:
            response = await client.get_balance(PublicKey(address))
            return response.value
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            raise
            
    async def get_token_balance(self,
                              network: str,
                              token_address: str,
                              wallet_address: str) -> int:
        """Get SPL token balance."""
        client = self.clients.get(network)
        if not client:
            raise ValueError(f"No client for network {network}")
            
        try:
            response = await client.get_token_account_balance(
                PublicKey(token_address)
            )
            return response.value.amount
        except Exception as e:
            logger.error(f"Error getting token balance: {e}")
            raise
            
    async def send_transaction(self,
                             network: str,
                             from_keypair: Keypair,
                             to_address: str,
                             amount: int) -> str:
        """Send a SOL transaction."""
        client = self.clients.get(network)
        if not client:
            raise ValueError(f"No client for network {network}")
            
        try:
            # Create transfer instruction
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=from_keypair.public_key,
                    to_pubkey=PublicKey(to_address),
                    lamports=amount
                )
            )
            
            # Create and sign transaction
            transaction = Transaction().add(transfer_ix)
            response = await client.send_transaction(
                transaction,
                from_keypair
            )
            
            return response.value
        except Exception as e:
            logger.error(f"Error sending transaction: {e}")
            raise
            
    async def get_slot(self, network: str) -> int:
        """Get current slot number."""
        client = self.clients.get(network)
        if not client:
            raise ValueError(f"No client for network {network}")
            
        try:
            response = await client.get_slot()
            return response.value
        except Exception as e:
            logger.error(f"Error getting slot: {e}")
            raise
            
    async def get_block(self, network: str, slot: int) -> Dict[str, Any]:
        """Get block information."""
        client = self.clients.get(network)
        if not client:
            raise ValueError(f"No client for network {network}")
            
        try:
            response = await client.get_block(slot)
            return response.value
        except Exception as e:
            logger.error(f"Error getting block: {e}")
            raise
            
    async def subscribe_to_account(self,
                                 network: str,
                                 address: str,
                                 callback: callable):
        """Subscribe to account changes."""
        ws_client = self.ws_clients.get(network)
        if not ws_client:
            raise ValueError(f"No WebSocket client for network {network}")
            
        try:
            await ws_client.account_subscribe(
                PublicKey(address),
                callback
            )
        except Exception as e:
            logger.error(f"Error subscribing to account: {e}")
            raise
            
    async def estimate_fee(self,
                         network: str,
                         transaction: Transaction) -> int:
        """Estimate transaction fee."""
        client = self.clients.get(network)
        if not client:
            raise ValueError(f"No client for network {network}")
            
        try:
            response = await client.get_fee_for_message(
                transaction.compile_message()
            )
            return response.value
        except Exception as e:
            logger.error(f"Error estimating fee: {e}")
            raise 