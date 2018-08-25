"""
create by gaowenfeng on 2018/8/25
"""
import hashlib
import json
from urllib.parse import urlparse

import requests

__author__ = "gaowenfeng"

from time import time
from app.settings import PROOF_DIFFICULTY

"""
区块的结构
{
    "index": 0, 索引
    "timestamp": "", 时间戳
    "transactions": [
        {
            "sender": "",
            "recipient": "",
            "amount": 5
        }
    ],
    "proof": "", # 工作量证明
    "previous_hash": "" # 上一个区块的hash
}
"""


class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # 创始区块 工作量证明随意，上一个区块hash值随意
        self.new_block(proof=100, previous_hash=1)

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def resolve_conflicts(self):
        neighbours = self.nodes

        max_len = len(self.chain)
        new_chain = None

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if len(chain) > max_len and self._valid_chain(chain):
                    max_len = length
                    new_chain = chain

        if not new_chain:
            return False

        self.chain = new_chain
        return True

    def new_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,  # 链的长度+1
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        # 返回上一个区块的索引
        return self.last_block['index']+1

    @staticmethod
    def hash(block):

        block_string = json.dumps(block, sort_keys=True).encode()

        # hexdigest 是hash过后的摘要信息
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]  # -1 数组里的最后一个元素

    def proof_of_work(self, last_proof):
        proof = 0
        # 工作量证明需要使用上一个区块的hash值，这里做一个简化版，拿上一个区块的工作量证明
        while self._valid_proof(last_proof, proof) is False:
            proof += 1
        print("proof:%s" % proof)
        return proof

    def _valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        print("guess_hash:%s" % guess_hash)
        return guess_hash[0:4] == PROOF_DIFFICULTY

    def _valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self._valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True








