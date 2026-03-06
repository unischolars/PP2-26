import re 
import json 
with open(r"c:\Users\rozao\Pop\work\Practice-5\raw.txt","r", encoding="utf-8") as f:
    txt = f.read()
#price like 308,00
price_pattern=re.compile(r"\b\d[\d ]*,\d{2}\b")
price=price_pattern.findall(txt)

#name like 1. then goes string
name_pattern=re.compile(r"\d+\.\s*\n(.+)")
name=name_pattern.findall(txt)
#total "ИТОГО /n " then like  18 009,00 
total_pattern=re.compile(r"ИТОГО:\s*\n?\s*([\d\s]+,\d{2})")
total=total_pattern.search(txt).group(1)
#time search for two groups like 18.04.2019 and 11:13:58 separated by space 
datetime_pat=re.compile(r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})")
datetime=datetime_pat.search(txt)
date=datetime.group(1)
time=datetime.group(2)
#payment look for either Банковская карта or Наличные
payment=re.search(r"(Банковская карта|Наличные)",txt)
payment_mehtod=payment.group(1)
#results
result={"name":name,"price":price,"total":total,"date":date,"time":time,"payment":payment_mehtod}
print(json.dumps(result, indent=4, ensure_ascii=False))