"""
create by gaowenfeng on 2018/8/25
"""
from uuid import uuid4

from app.blockchain.blockchain import Blockchain

__author__ = "gaowenfeng"

block_chain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')
