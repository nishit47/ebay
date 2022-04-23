import re
price="23.456 to 199.98"
totalPr=0
prices= re.findall(r"[-+]?\d*\.\d+|\d+", price)
for pr in prices:
    totalPr+=float(pr)
AvPr=totalPr/2
price=AvPr




    except:
        totalPr=0
        prices= re.findall(r"[-+]?\d*\.\d+|\d+", price)
        for pr in prices:
            totalPr+=float(pr)
        AvPr=totalPr/2
        price=AvPr

    