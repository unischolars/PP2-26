import json 
with open("sample-data.json") as f: #open file so that it will be closed
    d=json.load(f) #read file and if it sees that it is json then convert it into python structure
print("Interface Status")
print("================================================================================")
print("DN                                                 Description           Speed    MTU  ")
print("-------------------------------------------------- --------------------  ------  ------")
for i in d.get("imdata", []): #looks for and itterate through an imdata list
    intf = i.get("l1PhysIf", {}) #looks for first physicle layer
    dn = intf.get("dn", "") 
    desc = intf.get("descr", "")
    speed = intf.get("speed", "")
    mtu = intf.get("mtu", "")
    print(f"{dn:<50} {desc:<20} {speed:<6} {mtu:<6}") #print it so that it will fit patern 
