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
        self.filename = filename#.lower()
        self.category = category
        self.weight = weight

        # OPTIONAL:
        self.set = set
        #self.includes = [x.lower() for x in includes]   # Filename of another item or of a category
        #self.excludes = [x.lower() for x in excludes]   # Filename of another item or of a category

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


#### A bunch of Data Models
def percentileSelection(chance):
    if random.randint(0, 100) <= chance:
        return True

    return False

def weightedSelection(nekoItems):
    return random.choices(nekoItems, (o.weight for o in nekoItems), k = 1)[0]

def budgetedSelection(nekoItems):
    #if all(item.weight <= 0 for item in nekoItems):
        # return None  # or any other appropriate response
    selected = random.choices(nekoItems, weights=[o.weight for o in nekoItems], k = 1)[0]
    selected.weight -= 1 if selected.weight > 0 else 0
    return selected

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
        return data
    # Current category has "set" among its attributes, and NekoObject has some sets loaded in its data.
    firstMatchingItem = next((item for item in currentItems if any(NekoObject.sets) and item.set in NekoObject.sets), None)
    if firstMatchingItem:
        currentItems = [firstMatchingItem]

    chosenItem = weightedSelection(currentItems)
    NekoObject.addItem(chosenItem)
    return data #filterFromExcludes(data, chosenItem)

def buildNeko(id, dataSet):
    """
    @params: id to assign to the Neko object, class to assign to the Neko, working dataset

    @returns: one NekoObject that is ready to be serialized into builder's list and OpenSea API.
    """
    thisNeko = NekoObject(id)
    availableItems = dataSet

    # 1_Background
    availableItems = addnekoItem(thisNeko, availableItems, "Background")

    # 2_Tails
    availableItems = addnekoItem(thisNeko, availableItems, "Tail")

    # 3_Body
    availableItems = addnekoItem(thisNeko, availableItems, "Body")

    # 4_Tops
    availableItems = addnekoItem(thisNeko, availableItems, "Top")

    # 5_Mouths
    availableItems = addnekoItem(thisNeko, availableItems, "Mouth")
    
    # 6_Eyes
    availableItems = addnekoItem(thisNeko, availableItems, "Eyes")

    # 7_Hairs
    availableItems = addnekoItem(thisNeko, availableItems, "Hair")

    # 8_Hats
    availableItems = addnekoItem(thisNeko, availableItems, "Hat")

    # 9_Extra
    availableItems = addnekoItem(thisNeko, availableItems, "Extra")

    return thisNeko

def calculateBudgets(nekoItems, nekoCount):
    budgetedItems = []
    
    # Group items by category
    itemsByCategory = defaultdict(list)
    for item in nekoItems:
        itemsByCategory[item.category].append(item)

    # For each category, calculate total weight and then individual item budgets
    for category, items in itemsByCategory.items():
        categoryWeight = sum(item.weight for item in items)
        
        # Calculate raw budgets and track the rounding error
        rawBudgets = [(item, (item.weight / categoryWeight) * nekoCount) for item in items]
        
        # Calculate the initial rounded budgets and the total of these rounded budgets
        roundedBudgets = [(item, round(budget)) for item, budget in rawBudgets]
        roundedTotal = sum(budget for item, budget in roundedBudgets)
        
        # Determine the adjustment needed to match the exact total (nekoCount)
        adjustment = nekoCount - roundedTotal
        
        # Apply adjustments based on the difference, prioritizing items with the largest fractional part of their budget
        if adjustment != 0:
            # Sort items by the fractional part of their budget, in descending order
            fractionalParts = sorted(rawBudgets, key=lambda x: x[1] - int(x[1]), reverse=True)
            
            for i in range(abs(adjustment)):
                item, _ = fractionalParts[i]
                # Adjust the budget up or down depending on whether we have a shortfall or surplus
                for j in range(len(roundedBudgets)):
                    if roundedBudgets[j][0] == item:
                        adj_budget = roundedBudgets[j][1] + (1 if adjustment > 0 else -1)
                        roundedBudgets[j] = (item, adj_budget)
                        break

        # Create copies of the items with adjusted budgets
        for item, adjustedBudget in roundedBudgets:
            item.weight = adjustedBudget
            budgetedItems.append(item)
    
    # This is basically just nekoItems, but with the weight field now representing how many of each entry are left.
    # budgetedSelection works similarly to weighted selection, but decrements the chosen item's weight by 1 when chosen
    # when weight = 0, it is always skipped
    # the result at the end should be that every item now has 0 weight (all 2000 budget total has been expended)
    return budgetedItems

#### The Big One
def buildNekos(start_num = 0, total = 3000, output_dir = "Output/Nekos/"):
    ### SCRIPT EXECUTION
    allNekoItems = nekoItemListFromJSON()
    budgetedNekos = []#calculateBudgets(allNekoItems, total)

    # Group budgetedNekos by category
    budgetedItemsByCategory = defaultdict(list)
    for item in budgetedNekos:
        budgetedItemsByCategory[item.category].append(item)
    
    # Print total weight of each category
    for category, items in budgetedItemsByCategory.items():
        totalWeight = sum(item.weight for item in items)
        print(f"Total budgeted weight for category '{category}': {totalWeight}")
        # Sanity check to ensure total weight equals total nekos to be generated
        if totalWeight != total:
            print(f"Warning: Total budgeted weight for category '{category}' does not equal {total}.")
        else:
            print(f"Sanity Check Passed for category '{category}'.")
    the_nekos = []

    # Create Nekos
    current = 0
    for i in range(0, total):
        the_nekos.append(buildNeko(i, allNekoItems))
        current += 1

    # Shuffle the entire batch a few times
    random.shuffle(the_nekos)

    # Reassign the ID's
    for i in range(len(the_nekos)):
        the_nekos[i].id = i + 1 + start_num

    # Export JSONS
    script_dir = os.path.dirname(__file__)
    for i in range(len(the_nekos)):
        metadataPath = output_dir + "NekoMetadata/" + str(i + 1 + start_num) + ".json"
        absMetadataPath = os.path.join(script_dir, metadataPath)
        #print(the_nekos[i].toJSON())
        os.makedirs(os.path.dirname(absMetadataPath), exist_ok=True)
        with open(absMetadataPath, 'w') as f:
            f.write(the_nekos[i].toOpenSeaJSON())

        builderPath = output_dir + "NekoBuilderData/" + str(i + 1 + start_num) + ".json"
        absBuilderPath = os.path.join(script_dir, builderPath)
        os.makedirs(os.path.dirname(absBuilderPath), exist_ok=True)
        with open(absBuilderPath, 'w') as f:
            f.write(the_nekos[i].getBuilderList())


# Colored Skulls / 5 blue : 10 Red
buildNekos(start_num = 0, total = 3000, output_dir = "Output/Neko1/")