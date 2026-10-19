from components.resistor import Resistor
from components.voltageSource import VoltageSource
from components.ground import Ground
from components.wire import Wire
from util.current import Current
from util.node import Node
from util.voltage import Voltage
from util.enums import NodeDirection as nd
from components.element import Element
from util.loop import Loop

volSource0 = VoltageSource(Voltage(20))
res0 = Resistor(330)
wire0 = Wire()
wire1 = Wire()

node0 = Node()
node1 = Node()
node2 = Node()
node3 = Node()

ground = Ground()

elementVolSource =  Element(volSource0)
elementRes = Element(res0)
elementWire0 = Element(wire0)
elementWire1 = Element(wire1)
elementGround = Element(ground)

elementVolSource.connectTerminalPolarity(node0, nd.TOP, False)
elementVolSource.connectTerminalPolarity(node1, nd.BOTTOM, True)
elementRes.connectTerminalPolarity(node1, nd.RIGHT, True)
elementRes.connectTerminalPolarity(node2, nd.LEFT, False)
elementWire0.connectTerminalPolarity(node2, nd.BOTTOM, True)
elementWire0.connectTerminalPolarity(node3, nd.TOP, False)
elementWire1.connectTerminalPolarity(node3, nd.LEFT, True)
elementWire1.connectTerminalPolarity(node0, nd.RIGHT, False)
elementGround.connectTerminal(node0, nd.BOTTOM)

node4 = Node()
node5 = Node()

res1 = Resistor(550)
res2 = Resistor(660)
wire2 = Wire()

elementRes1 = Element(res1)
elementRes2 = Element(res2)
elementWire2 = Element(wire2)

elementRes1.connectTerminalPolarity(node2, nd.RIGHT, True)
elementRes1.connectTerminalPolarity(node4, nd.LEFT, False)
elementRes2.connectTerminalPolarity(node4, nd.BOTTOM, True)
elementRes2.connectTerminalPolarity(node5, nd.TOP, False)
elementWire2.connectTerminalPolarity(node5, nd.LEFT, True)
elementWire2.connectTerminalPolarity(node3, nd.RIGHT, False)

'''
node0.printNodeScheme()

node1.printNodeScheme()

node2.printNodeScheme()

node3.printNodeScheme()

node4.printNodeScheme()
node5.printNodeScheme()
'''

node6 = Node()
node7 = Node()

res3 = Resistor(100)
volSource1 = VoltageSource(Voltage(10))
wire3 = Wire()

elementRes3 = Element(res3)
elementVolSource1 = Element(volSource1)
elementWire3 = Element(wire3)

elementRes3.connectTerminalPolarity(node2, nd.TOP, False)
elementRes3.connectTerminalPolarity(node6, nd.BOTTOM, True)
elementVolSource1.connectTerminalPolarity(node6, nd.RIGHT, True)
elementVolSource1.connectTerminalPolarity(node7, nd.LEFT, False)
elementWire3.connectTerminalPolarity(node7, nd.BOTTOM, True)
elementWire3.connectTerminalPolarity(node4, nd.TOP, False)


successfullLoops = {}
verifyingLoops = {}

listSearched = []

def checkClosedLoop(thisNode: Node, startingNodeID: int | None = None, previousDirection: nd | None = None):
        # Checks if the current node equals the analysed node's ID (if so, it has come full circle and a loop was found)
        if startingNodeID == thisNode.id and previousDirection:
            print(f"Reached same node, closed loop identified at node ${startingNodeID}")
            verifyingLoops[startingNodeID].add(thisNode) # closes the loop
            successfullLoops[thisNode.id] = verifyingLoops[thisNode.id]

        else:
            elementTerminalRight = thisNode.elements[0]
            elementTerminalTop = thisNode.elements[1]
            elementTerminalLeft = thisNode.elements[2]
            elementTerminalBottom = thisNode.elements[3]

            if elementTerminalTop:
                if (previousDirection != nd.BOTTOM):
                    # If there's a top element in the node, starts a new analysis with the node's ID
                    if (type(elementTerminalTop.connectedElement.terminals) is not Ground and len(elementTerminalTop.connectedElement.terminals) > 1):

                        oppositeTerminal = elementTerminalTop.connectedElement.getOppositeTerminal(elementTerminalTop)
                        if oppositeTerminal:
                            nextNode = Node.getNodeList()[oppositeTerminal.connectedNodeID]
                            nextNodeID = nextNode.id

                            if previousDirection is not None:
                                    if previousDirection == nd.TOP:
                                        print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, going top, next node ID is ${nextNodeID}')
                                        verifyingLoops[startingNodeID].add(thisNode)
                                        checkClosedLoop(nextNode, startingNodeID, nd.TOP)
                                    else:
                                        if thisNode.id not in listSearched:
                                            print(f"Starting new loop analysis at node ${thisNode.id}")
                                            print(f'Comparing node ${thisNode.id}, current is {thisNode.id}, came from ${previousDirection}, going top, next node ID is ${nextNodeID}')
                                            newLoop = Loop()
                                            newLoop.add(thisNode)
                                            verifyingLoops[thisNode.id] = newLoop
                                            listSearched.append(thisNode.id)
                                            checkClosedLoop(nextNode, thisNode.id, nd.TOP)

                                    
                            elif startingNodeID is not None:
                                print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, previous direction was ${previousDirection},  going top, next node ID is ${nextNodeID}')
                                verifyingLoops[startingNodeID].add(thisNode)
                                checkClosedLoop(nextNode, startingNodeID, nd.TOP)

                            
                            elif not elementTerminalRight:
                                print(f"right corner element (node ${thisNode.id}), can't start analysis here...")


                            else:
                                if thisNode.id not in listSearched:
                                    # Starts a new analysis with the current node's ID
                                    print(f"Starting new loop analysis at node ${thisNode.id}")
                                    newLoop = Loop()
                                    newLoop.add(thisNode)
                                    verifyingLoops[thisNode.id] = newLoop
                                    listSearched.append(thisNode.id)
                                    checkClosedLoop(nextNode, thisNode.id, nd.TOP)
                            
                           
                     
            if elementTerminalRight:
                if (previousDirection != nd.LEFT):
                        if (type(elementTerminalRight.connectedElement.terminals) is not Ground and len(elementTerminalRight.connectedElement.terminals) > 1):
                            #print(f'Currently on node ${thisNode.id}, going to element ${elementTerminalRight.getConnectedElementDescription()}')
                    
                            oppositeTerminal = elementTerminalRight.connectedElement.getOppositeTerminal(elementTerminalRight)
                            if oppositeTerminal:
                                nextNode = Node.getNodeList()[oppositeTerminal.connectedNodeID]
                                nextNodeID = nextNode.id
                                #print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, going right, and next node ID is ${nextNodeID}')
                                #There's still elements to that direction, keeps checking all of them
                                if startingNodeID is not None:
                                    print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, came from ${previousDirection}, going right, next node ID is ${nextNodeID}')
                                    verifyingLoops[startingNodeID].add(thisNode)
                                    checkClosedLoop(nextNode, startingNodeID, nd.RIGHT)
                                else:
                                
                                            print(f"Searching for the next node with a top element... current is ${thisNode.id}, going right, next is ${nextNodeID}")
                                            #print(f"Starting new loop analysis at node ${thisNode.id}")
                                            #print(f'Comparing node ${thisNode.id}, current is {thisNode.id}, going right, next node ID is ${nextNodeID}')
                                            checkClosedLoop(nextNode)

            if elementTerminalBottom:
                if (previousDirection != nd.TOP):
                            if (type(elementTerminalBottom.connectedElement.terminals) is not Ground and len(elementTerminalBottom.connectedElement.terminals) > 1):
                                #print(f'Currently on node ${thisNode.id}, going to element ${elementTerminalBottom.getConnectedElementDescription()}')
                                oppositeTerminal = elementTerminalBottom.connectedElement.getOppositeTerminal(elementTerminalBottom)
                                if oppositeTerminal:
                                    nextNode = Node.getNodeList()[oppositeTerminal.connectedNodeID]
                                    nextNodeID = nextNode.id
                                    #print(f'Comparing node ${startingNodeID}, current is {thisNode.id }, going bottom, next node ID is ${nextNodeID}')

                                    if not elementTerminalRight and previousDirection is not None:
                                        if startingNodeID is not None:
                                            print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, came from ${previousDirection}, going bottom, next node ID is ${nextNodeID}')
                                            verifyingLoops[startingNodeID].add(thisNode)
                                            checkClosedLoop(nextNode, startingNodeID, nd.BOTTOM)
                                        
                                        else: 
                                            print(f"Searching for next thisNode... current is ${thisNode.id}, going bottom, next is ${nextNodeID}")
                                            checkClosedLoop(nextNode)
                                    else:
                                        '''
                                        print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, came from ${previousDirection}, going right, next node ID is ${nextNodeID}')
                                        verifyingLoops[startingNodeID].add(thisNode)
                                        checkClosedLoop(nextNode, startingNodeID, nd.BOTTOM)
                                        '''
                                        print("error here")

            if elementTerminalLeft:
                if (previousDirection != nd.RIGHT):

                            if (type(elementTerminalLeft.connectedElement.terminals) is not Ground and len(elementTerminalLeft.connectedElement.terminals) > 1):
            
                                oppositeTerminal = elementTerminalLeft.connectedElement.getOppositeTerminal(elementTerminalLeft)

                                if oppositeTerminal:
                                    nextNode = Node.getNodeList()[oppositeTerminal.connectedNodeID]
                                    nextNodeID = nextNode.id
                                    #There's still elements to that direction, keeps checking all of them

                                    if not elementTerminalBottom and previousDirection:                                
                                        if startingNodeID is not None:
                                            if thisNode not in listSearched:
                                                print(f'Comparing node ${startingNodeID}, current is {thisNode.id}, came from ${previousDirection}, going left, next node ID is ${nextNodeID}')
                                                verifyingLoops[startingNodeID].add(thisNode)
                                                checkClosedLoop(nextNode, startingNodeID, nd.LEFT)
                                            else:
                                                print(f"Stopping analysis on node {startingNodeID}, it has already been analysed")
                                                listSearched.remove(startingNodeID)
                                        else:
                                            #print(f'Comparing node ${thisNode.id}, current is {thisNode.id}, going left, next node ID is ${nextNodeID}')
                                            print(f"Searching for next thisNode... current is ${thisNode.id}, going left, next is ${nextNodeID}")
                                            checkClosedLoop(nextNode)


def isRightmostCornerElement(node: Node):
    return node.elements[0] is None and node.elements[3] is None


checkClosedLoop(node0)

a = []
for i in verifyingLoops:
    temp = []
    list = verifyingLoops[i].nodepath
    for j in list:
        temp.append(j.id)
    a.append(temp)

print(a)
print(listSearched)