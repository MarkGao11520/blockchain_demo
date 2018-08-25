"""
create by gaowenfeng on 2018/8/25
"""
from flask import request
from flask.json import jsonify

from . import web
from app.blockchain import block_chain, node_identifier

__author__ = "gaowenfeng"


@web.route('/index', methods=['GET'])
def index():
    return "index"


@web.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if values is None or not all(k in values for k in required):
        return "Missing values", 400

    index = block_chain.new_transaction(values['sender'],
                                        values['recipient'],
                                        values['amount'])

    response = {'message': f'Transaction will be add to Block {index}'}
    return jsonify(response), 201


@web.route('/mine', methods=['GET'])
def mine():
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = block_chain.proof_of_work(last_proof)

    block_chain.new_transaction(sender='0', recipient=node_identifier, amount=1)
    block = block_chain.new_block(proof, None)

    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 201


@web.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain)
    }

    return jsonify(response), 200


@web.route('/node/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get("nodes")

    if nodes is None:
        return "Error: please supply a valid list of nodes", 400

    for node in nodes:
        block_chain.register_node(node)

    response = {
        'message': 'New Nodes have been added',
        'total_nodes': list(block_chain.nodes)
    }

    return jsonify(response), 201


@web.route('/node/resolve', methods=['GET'])
def consensus():
    replaced = block_chain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': block_chain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': block_chain.chain
        }

    return jsonify(response)
