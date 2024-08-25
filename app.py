from flask import Flask, render_template, request
import os
from time import time
from blockchain import BlockChain, Block, Miner, Node
from conversion import getGasPrices

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

# Create dictionary of the nodes
allNodes = {}

@app.route("/", methods= ["GET", "POST"])
def home():
    global blockData, currentBlock, chain, failedBlocks, allNodes
     
    # Get node parameter from url i.e get request and save it in nodeId
    nodeId = request.args.get("node")



    if(nodeId == None or nodeId == ""):
        # Open newnode.html page to create the new node of blockchain. 
        return render_template('newnode.html', allNodes = allNodes )
    
    # Check if nodeId does not exits in allNodes, and then create new node
    if(allNodes = nodeId == None or nodeId == ""):
        node = Node(nodeId)
        miner1 = Miner('Miner 1')
        miner2 = Miner('Miner 2')
        miner3 = Miner('Miner 3')

        node.blockchain.addMiner(miner1)
        node.blockchain.addMiner(miner2)
        node.blockchain.addMiner(miner3)
        
        allNodes[nodeId] = node
    
    currentNode = allNodes[nodeId]
     
    allPrices = getGasPrices()
    
    chain = currentNode.blockchain
    currentBlock = currentNode.currentBlock
    failedBlocks = currentNode.failedBlocks
        
    if request.method == "GET":
        return render_template('index.html', allPrices = allPrices, nodeId = nodeId)
    else:
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        landId = request.form.get("landId")
        lattitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        area = request.form.get("area")
        amount = request.form.get("amount")
        mode = request.form.get("mode")
        print(mode)

        gasPrices, gweiPrices, etherPrices, dollarPrices = allPrices

        gasPriceGwei = gweiPrices[mode]
        gasPriceEther = etherPrices[mode]
        transactionFeeEther = etherPrices[mode] * 21000
        transactionFeeDollar = dollarPrices[mode] * 21000

        transaction = { 
                "sender": sender, 
                "receiver": receiver, 
                "amount": amount,
                "landId": landId,  
                "latitude": lattitude,
                "longitude": longitude,
                "area": area,
                "gasPriceGwei" : gasPriceGwei,
                "gasPriceEther" : gasPriceEther, 
                "transactionFeeEther" : transactionFeeEther,
                "transactionfeeDollar" : transactionFeeDollar          
            }  
        chain.addToMiningPool(transaction)
        
    # Pass the nodeId to index.html
    return render_template('index.html', blockChain = chain, allPrices = allPrices, nodeId = nodeId)

@app.route("/blockchain", methods= ["GET", "POST"])
def show():
    global chain, currentBlock, failedBlocks, allNodes

    nodeId =request.args.get("node")
    if(nodeId == None or nodeId == ""):
            return render_template('badRequest.html')
        
    if(nodeId not in allNodes):
            return render_template('notExits.html')
            
    currentNode = allNodes[nodeId]
    chain =currentNode.blockchain
    currentBlock = currentNode.currentBlock


    currentBlockLength  = 0
    if currentNode.currentBlock:
            currentBlockLength = len(currentNode.currentBlock.transactions)
    
    return render_template('blockchain.html', blockChain = chain.chain, currentBlockLength = currentBlockLength, failedBlocks= failedBlocks, nodeId = nodeId)
    

@app.route("/miningPool", methods= ["GET", "POST"])
def miningPool():
    global chain, allNodes
    nodeId =request.args.get("node")
    if(nodeId == None or nodeId == ""):
            return render_template('badRequest.html')
        
    if(nodeId not in allNodes):
            return render_template('notExits.html')
            
    currentNode = allNodes[nodeId]
    chain =currentNode.blockchain
    
    if request.method == "POST":
        minerAddress = request.form.get("miner")
        chain.minePendingTransactions(minerAddress)

    return render_template('miningPool.html', pendingTransactions = chain.pendingTransactions, miners = chain.miners, nodeId = nodeId)
    
if __name__ == '__main__':
    app.run(debug = True, port=4001)