import json

with open(r"c:\Users\rozao\Pop\work\Practice-4\sample-data.json","r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20}  {'Speed':<8}{'MTU':>6}  ")
print(f"{'-'*50} {'-'*20}  {'-'*6}  {'-'*6}")

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    print(f"{dn:<50} {descr:<20}  {speed:<8}{mtu:>6} ")