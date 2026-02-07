import time
shopList=[
    {"id": 1,"name":"Milk" ,"price": 3.99, "category": "Dairy","timestamp":None,"edittime":None},
    {"id": 2,"name":"Bread", "price": 2.50, "category": "Bakery","timestamp":None,"edittime":None},
    {"id": 3,"name":"Cheese", "price": 2.99, "category": "Dairy","timestamp":None,"edittime":None},
    {"id": 4,"name":"Ham", "price": 8.99, "category": "Meat","timestamp":None,"edittime":None},
    {"id": 5,"name":"Eggs", "price": 4.99, "category": "Dairy","timestamp":None,"edittime":None},
    {"id": 6,"name":"Apple", "price": 1.99, "category": "Fruit","timestamp":None,"edittime":None},
    {"id": 7,"name":"Banana", "price": 0.99, "category": "Fruit","timestamp":None,"edittime":None},
    {"id": 8,"name":"Coffee", "price": 6.49, "category": "Beverage","timestamp":None,"edittime":None},
    {"id": 9,"name":"Tea", "price": 3.49, "category": "Beverage","timestamp":None,"edittime":None},
    {"id": 10,"name":"Sugar", "price": 2.29, "category": "Baking","timestamp":None,"edittime":None},
    {"id": 11,"name":"Salt", "price": 1.49, "category": "Spices","timestamp":None,"edittime":None},
    {"id": 12,"name":"Butter", "price": 4.79, "category": "Dairy","timestamp":None,"edittime":None},
    {"id": 13,"name":"Rice", "price": 5.99, "category": "Grains","timestamp":None,"edittime":None},
    {"id": 14,"name":"Pasta", "price": 2.99, "category": "Grains","timestamp":None,"edittime":None},
    {"id": 15,"name":"Tomato", "price": 2.49, "category": "Vegetable","timestamp":None,"edittime":None}
]
#/////////////////////////
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

#/////////////////////////
def pickNumber():
    while True:
        try:
            choice = int(input(f"\nChoose ID: "))
            if 1 <= choice :
                return choice
            else:
                print(f"Enter a valid ID")
        except ValueError:
            print("Enter a valid ID")


#/////////////////////////
def listShow(list):
    if len(list) > 10:
        print("No\tName\tPrice\tCategory\tCreation time\t\tLast edited")
        for product in list[:10]:
            print(f"{product['id']}\t{product['name']}\t{product['price']}\t{product['category']}\t\t{time.ctime(product['timestamp']) if product['timestamp'] else 'none'}\t\t{time.ctime(product['edittime']) if product['edittime'] else 'none'}")
        print(f"... and {len(list)-10} more items")
        if input("Show all items? (y/n): ").lower() == 'y':
            print("No\tName\tPrice\tCategory\tCreation time\t\tLast edited")
            for product in list:
                print(f"{product['id']}\t{product['name']}\t{product['price']}\t{product['category']}\t\t{time.ctime(product['timestamp']) if product['timestamp'] else 'none'}\t\t{time.ctime(product['edittime']) if product['edittime'] else 'none'}")
    else:
        print("No\tName\tPrice\tCategory\tCreation time\t\tLast edited")
        for product in list:
            print(f"{product['id']}\t{product['name']}\t{product['price']}\t{product['category']}\t\t{time.ctime(product['timestamp']) if product['timestamp'] else 'none'}\t\t{time.ctime(product['edittime']) if product['edittime'] else 'none'}")
#/////////////////////////
def listSearchByName(list):
    while True:
        foundList=[]
        searchName=input("Enter name of the item or (exit):")
        if searchName=="exit":
            break
        else:
            for i,item in enumerate(list):
                if searchName.lower() in item["name"].lower():
                    foundList.append(item)
            if len(foundList) == 0:
                print("No match found") 
            else:
                listShow(foundList)
                return(foundList)

#/////////////////////////
def listEdit(list,itemId):
    options=["Name","Price","Category"]
    for i,item in enumerate(list):
        picked=pickMenu(options)
        if itemId==item["id"]:
            editedList=[]
            if picked=="Name":
                newName=input("Enter new name:")
                item["name"]=newName
                editedList.append(item)
            elif picked=="Price":
                newPrice=input("Enter new price:")
                item["price"]=newPrice
                editedList.append(item)
            elif picked=="Category":
                newCategory=input("Enter new category:")
                item["category"]=newCategory
                editedList.append(item)
            item["edittime"]=time.time()
            print(editedList)
            return editedList
    else:
        print("No match found")

#/////////////////////////
def listAdd(list):
    newId = max(item["id"] for item in list) + 1 if list else 1
    newName = input("Enter name:")
    newTime=time.time()
    newPrice = input("Enter price:")
    newCategory = input("Enter category:")
    newItem = {
        "id": newId,
        "name": newName,
        "price": newPrice,
        "category": newCategory,
        "timestamp":newTime,
    }
    shopList.append(newItem)

#/////////////////////////
def shiftId(list):
    for i, item in enumerate(list, start=1):
        item["id"] = i

#/////////////////////////
def listDelete(list,id):
    deletedItem=None
    for i, item in enumerate(list):
        if item["id"] == id:
            deletedItem = list.pop(i)
            print(f"Deleted: {deletedItem['name']} (ID: {id})")
            shiftId(list)
            break
    if not deletedItem:
        print(f"Item with ID {id} not found")
    return deletedItem
print(len(shopList))
#/////////////////////////
def main():
    while True:
        options=["Show list","Search","Add", "Delete","Edit","Exit"]
        selected=pickMenu(options)
        if selected=="Show list":
            listShow(shopList)
        elif selected=="Add":
            listAdd(shopList)
        elif selected=="Delete":
            deleteID=int(input("Enter id to delete item:"))
            listDelete(shopList,deleteID)
        elif selected=="Search":
            searchOptions=["Edit","Delete"]
            
            foundItems=listSearchByName(shopList)

            if input("Choose action? (y/n): ").lower() == 'y':
                searchSelected=pickMenu(searchOptions)

                if searchSelected=="Edit":
                    itemId=pickNumber()
                    listEdit(shopList,itemId)
                elif searchSelected=="Delete":
                    itemId=pickNumber()
                    listDelete(shopList,itemId)
        elif selected=="Edit":
            itemId=pickNumber()
            listEdit(shopList,itemId)



        elif selected=="Exit":
            break

        input("\nPress Enter to continue...")
main()
