import time
shopListRaw=[]
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
def readOrderStorage(file="order.txt"):
    global shopListRaw
    try:
        with open(file, 'r') as r:
            shopListRaw=eval(r.read())
    except:
        print("Couldn't read")
        shopListRaw=[]
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
def writeOrderStorage(content,file="order.txt"):
    try:
        with open(file,'w') as f:
            f.write(content)
    except:
        print("Couldn't write")
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
def listConvert():
    orderList=[]
    for item in shopListRaw:
        order=Order(
            id=item["id"],
            name=item["name"],
            price=item["price"],
            category=item["category"],
            timestamp=item["timestamp"],
            edittime=item["edittime"]
        )
        orderList.append(order)
    return orderList
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
def pickMenu(options):
        print("\nShoping list actions:")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        while True:
            try:
                choice = int(input(f"\nChoose (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return options[choice-1]
                else:
                    print(f"Enter a number between 1 and {len(options)}")
            except ValueError:
                print("Enter a valid number")
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
def pickNumber(text="Choose ID:",error="Enter a valid ID"):
    while True:
        try:
            choice = int(input(f"\n{text}"))
            if 1 <= choice :
                return choice
            else:
                print(error)
        except ValueError:
            print(error)
def pickNumberFloat(text="Enter number:",error="Enter a valid number"):
    while True:
        try:
            choice = float(input(f"\n{text}"))
            return choice
            
        except ValueError:
            print(error)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
class OrderController():
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def __init__(self,orderList):
        self._orderList = orderList
        self._typeAction = None
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listShow(self,listSh=None):
        showingList = listSh if listSh != None else self._orderList
        if len(showingList) > 10:
            print("No\tName\tPrice\tCategory\tCreation time\t\tLast edited")
            for order in showingList[:10]:
                print(f"{order._id}\t{order._name}\t{order._price}\t{order._category}\t\t\t{time.ctime(order._timestamp) if order._timestamp else 'none'}\t\t{time.ctime(order._edittime) if order._edittime else 'none'}")
            print(f"... and {len(showingList)-10} more items")
            if input("Show all items? (y/n): ").lower() == 'y':
                print("No\tName\tPrice\tCategory\tCreation time\t\tLast edited")
                for order in showingList:
                    print(f"{order._id}\t{order._name}\t{order._price}\t{order._category}\t\t\t{time.ctime(order._timestamp) if order._timestamp else 'none'}\t\t{time.ctime(order._edittime) if order._edittime else 'none'}")
        else:
            print("No\tName\tPrice\tCategory\tCreation time\t\tLast edited")
            for order in showingList:
                print(f"{order._id}\t{order._name}\t{order._price}\t{order._category}\t\t\t{time.ctime(order._timestamp) if order._timestamp else 'none'}\t\t{time.ctime(order._edittime) if order._edittime else 'none'}")
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listSearchByName(self):
        while True:
            foundList=[]
            searchName=input("Enter name of the item or (exit):")
            if searchName=="exit":
                break
            else:
                for i,item in enumerate(self._orderList):
                    if searchName.lower() in item._name.lower():
                        foundList.append(item)
                if len(foundList) == 0:
                    print("No match found") 
                else:
                    self.listShow(foundList)
                    return(foundList)
    def listSearchById(self):
        while True:
            foundList=[]
            searchID=pickNumber("Search by ID (or exit):")
            for i,item in enumerate(self._orderList):
                if searchID == item._id:
                    foundList.append(item)
                    self.listShow(foundList)
                    return(item._id)
            if len(foundList) == 0:
                print("No match found") 
                break
        
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listEdit(self,itemId,listSh=None):
        options=["Name","Price","Category"]
        picked=pickMenu(options)
        for i,item in enumerate(self._orderList):
            if itemId==item._id:
                editedList=[]
                if picked=="Name":
                    newName=input("Enter a new name:")
                    item._name=newName
                    editedList.append(item)
                elif picked=="Price":
                    newPrice=pickNumberFloat("Enter a new price:")
                    item._price=newPrice
                    editedList.append(item)
                elif picked=="Category":
                    newCategory=input("Enter a new category:")
                    item._category=newCategory
                    editedList.append(item)
                item._edittime=time.time()
                self.listWriteUpdate()
                return editedList
        else:
            print("No match found")
            self.listWriteUpdate()
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listAdd(self,listSh=None):
        newOrder=Order(
            id=max(item._id for item in self._orderList) + 1 if self._orderList else 1,
            name=input("Enter a new name:"),
            price=pickNumberFloat("Enter a new price:"),
            category=input("Enter a new category:"),
            timestamp=time.time(),
            edittime=None
        )
        self._orderList.append(newOrder)
        self.listWriteUpdate()
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listConvertBack(self,listSh=None):
        workingList = listSh if listSh != None else self._orderList
        convertedList=[]
        for order in workingList:
            newId = order._id
            newName = order._name
            newTime = order._timestamp
            newPrice = order._price
            newCategory = order._category
            newEdittime = order._edittime
            newItem = {
                "id": newId,
                "name": newName,
                "price": newPrice,
                "category": newCategory,
                "timestamp":newTime,
                "edittime":newEdittime
            }
            convertedList.append(newItem)
        return convertedList
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listWriteUpdate(self,file="order.txt"):
        newList=self.listConvertBack()
        try:
            with open(file,'w') as f:
                f.write(str(newList))
        except:
            print("Couldn't write")
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def shiftId(self):
        for i, item in enumerate(self._orderList, start=1):
            item._id = i
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def listDelete(self,itemid):
        deletedItem=None
        for i, item in enumerate(self._orderList):
            if item._id == itemid:
                deletedItem = self._orderList.pop(i)
                print(f"Deleted: {deletedItem._id} (ID: {itemid})")
                self.shiftId()
                break
        if not deletedItem:
            print(f"Item with ID {itemid} not found")
        self.listWriteUpdate()
        return deletedItem

   

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Order():
    def __init__(self,id,name,price,category,timestamp=None,edittime=None):
        self._id = id
        self._name = name
        self._price = price 
        self._category = category
        self._timestamp = timestamp
        self._edittime = edittime
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
def main():
    while True:
        readOrderStorage()
        orderList=listConvert()
        controls=OrderController(orderList)
        options=["Show list","Search","Add", "Delete","Edit","Exit"]
        selected=pickMenu(options)
        if selected=="Show list":
            controls.listShow()
        elif selected=="Add":
            controls.listAdd()
        elif selected=="Delete":
            print("Delete Item:")
            controls.listDelete(pickNumber())
        elif selected=="Search":
            foundItems=controls.listSearchByName()
            searchOptions=["Edit","Delete"]
            if input("Choose action? (y/n): ").lower() == 'y':
                searchSelected=pickMenu(searchOptions)

                if searchSelected=="Edit":
                    itemId=pickNumber()
                    controls.listEdit(itemId)
                elif searchSelected=="Delete":
                    itemId=pickNumber()
                    controls.listDelete(itemId)
        elif selected=="Edit":
            foundID=controls.listSearchById()
            controls.listEdit(foundID)



        elif selected=="Exit":
            controls.listWriteUpdate()
            break

        input("\nPress Enter to continue...")
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    main()









