#!/usr/bin/env python3.8.2
import json
import random
from random import choice, choices, randint
from collections import defaultdict
import os

#### Defining Data Objects
class NekoObject:
    def __init__(self, id):
        self.id = id
        self.imageLayers = []
        self.attributes = []
        self.sets = []

    def buildTrait(self, traitType, traitValue):
        return {
            "trait_type": traitType,
            "value": traitValue
        }

    def addItem(self, nekoItem):
        # self.nekoItems.append(nekoItem)
        self.imageLayers.append(nekoItem.category + "/" + nekoItem.filename)
        
        # Put the Trait
        if not nekoItem.category == "Tail":
            nameTrait = self.buildTrait(nekoItem.category, nekoItem.name)
            self.attributes.append(nameTrait)

        # Add sets (identifier for pairings of items that have to go together)
        if nekoItem.set:
            self.sets.append(nekoItem.set)

        # Handle Includes
        #self.imageLayers = self.imageLayers + nekoItem.includes
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def toOpenSeaJSON(self):
        tokenName = "Neko " + str(self.id)
        tokenUrl = "https://api.nekomaker.io/metadata/" + str(self.id) + ".json"
        imgURL = "https://api.nekomaker.io/nekos/" + str(self.id) + ".png"

        jsonDict = {
            "name": tokenName,
            "external_url": tokenUrl,
            "image": imgURL,
            "description": "burenyuu :3",
            "attributes": self.attributes
        }
        return json.dumps(jsonDict, indent=4)

    def getBuilderList(self):
        return json.dumps(self.imageLayers)

class nekoItem:
    def __init__(self, name, filename, category, weight = 0.75,
            set = None, includes = [], excludes = []):

        # MANDATORY:
        self.name = name
        self.filename = filename
        self.category = category
        self.weight = weight

        # OPTIONAL:
        self.set = set
        #self.includes = [x for x in includes]   # Filename of another item or of a category
        self.excludes = [x for x in excludes]   # Filename of another item or of a category

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


#### A bunch of Data Models
def percentileSelection(chance):
    if random.randint(0, 100) <= chance:
        return True
    return False

def weightedSelection(nekoItems):
    return random.choices(nekoItems, (o.weight for o in nekoItems), k = 1)[0]

def selectWhereCategoryMatches(collection, category):
    return [x for x in collection if x.category == category]

def selectWhereClassMatches(collection, className):
    return [x for x in collection if x.classes.__contains__(className)]

def doesContainClass(collection, className):
    return any((item.classes.__contains__(className)) for item in collection)

def doesContainCategory(collection, category):
    return any((category == item.category) for item in collection)

def doesCategoryHaveSet(collection, category):
    return any((category == item.category and item.set) for item in collection)

def filterFromName(data, filteredFiles):
    return [x for x in data if x.filename not in filteredFiles]

def filterFromExcludes(data, currentItem):
    if not currentItem.excludes:
        return data
    return [x for x in data if x.filename not in currentItem.excludes]

#### Parsing Utils
def printObjects(obj_list):
    for i in range(0, len(obj_list)):
        print(obj_list[i].toJSON())

def nekoItemListFromJSON():
    nekoItems = []
    with open("./NekoMakerData.json") as json_file:
        data = json.load(json_file)
        for item in data:
            parsednekoItem = nekoItem(**item)
            nekoItems.append(parsednekoItem)
        
    return nekoItems

#### Neko Building
def addnekoItem(NekoObject, data, categoryName):
    """
    @params: NekoObject the Neko we're working with, data the current dataset, category name of the item to add.
    
    @returns: a new working dataset filtered by the excludes of the item added.
    """
    currentItems = selectWhereCategoryMatches(data, categoryName)
    if not currentItems:
        return None
    
    # Current category has "set" among its attributes, and NekoObject has some sets loaded in its data.
    firstMatchingItem = next((item for item in currentItems if any(NekoObject.sets) and item.set in NekoObject.sets), None)
    if firstMatchingItem:
        NekoObject.addItem(firstMatchingItem)
        if "Crying" in firstMatchingItem.name or "Star" in firstMatchingItem.name:
            print("Burenyu")
        return filterFromExcludes(data, firstMatchingItem)
    
    # Not in a set, just choose an item normally
    chosenItem = weightedSelection(currentItems)
    if chosenItem is None:
        return None
    
    if "Crying" in chosenItem.name or "Star" in chosenItem.name:
        print("Burenyu")
    
    NekoObject.addItem(chosenItem)
    return filterFromExcludes(data, chosenItem)

def buildNeko(id, dataSet, activeLayers):
    """
    @params: id to assign to the Neko object, class to assign to the Neko, working dataset

    @returns: one NekoObject that is ready to be serialized into builder's list and OpenSea API.
    """
    thisNeko = NekoObject(id)
    availableItems = dataSet

    for layer in activeLayers:
        availableItems = addnekoItem(thisNeko, availableItems, layer)
        if availableItems is None:
            return None

    return thisNeko

#### The Big One
def buildNekos(start_num = 0, total_count = 3000, output_dir = "Output/Nekos/"):
    ### SCRIPT EXECUTION
    allNekoItems = nekoItemListFromJSON()
        
    # Create the Nekos
    the_nekos = []
    current = 0

    layers = [
        "Background",
        "Tail",
        "Body",
        "Hair",
        "Mouth",
        "Top",
        "Eyes",
        "Hat",
        "Extra"
    ]
    for i in range(0, int(total_count * 0.75)):
        this_neko = buildNeko(i, allNekoItems, layers)
        if this_neko is None: 
            break   # Some error occured or something, halt NekoGen.
        the_nekos.append(this_neko)
        current += 1

    layers = [
        "Background",
        "Tail",
        "Body",
        "Hair",
        "Mouth",
        "Top",
        "Eyes",
        "Hat"
    ]
    for i in range(current, total_count):
        this_neko = buildNeko(i, allNekoItems, layers)
        if this_neko is None: 
            break   # Some error occured or something, halt NekoGen.
        the_nekos.append(this_neko)
        current += 1

    # Shuffle the batch and reassign the ID's.
    random.shuffle(the_nekos)
    for i in range(len(the_nekos)):
        the_nekos[i].id = i + 1 + start_num

    # Export JSONS
    script_dir = os.path.dirname(__file__)
    for i in range(len(the_nekos)):
        metadataPath = output_dir + "NekoMetadata/" + str(i + 1 + start_num) + ".json"
        absMetadataPath = os.path.join(script_dir, metadataPath)
        os.makedirs(os.path.dirname(absMetadataPath), exist_ok=True)
        with open(absMetadataPath, 'w') as f:
            f.write(the_nekos[i].toOpenSeaJSON())

        builderPath = output_dir + "NekoBuilderData/" + str(i + 1 + start_num) + ".json"
        absBuilderPath = os.path.join(script_dir, builderPath)
        os.makedirs(os.path.dirname(absBuilderPath), exist_ok=True)
        with open(absBuilderPath, 'w') as f:
            f.write(the_nekos[i].getBuilderList())

# Neko
buildNekos(start_num = 0, total_count = 3000, output_dir = "Output/TNDTNDTND!!!!!/")