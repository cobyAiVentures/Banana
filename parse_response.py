import csv, json

data = [
    {"firstName":"Tina","middleName":"Michelle","lastName":"Willis","firmName":"Tina Willis Law Injury Accident Lawyer","primaryLocation":{"city":"Orlando","region":"FL","phone":"(407) 803-2139","cell":None},"email":"tina@tinawillislaw.com"},
    {"firstName":"Julie","middleName":"Ann Hauge","lastName":"Rice","firmName":"Julie A. Rice Attorney at Law","primaryLocation":{"city":"Oldsmar","region":"FL","phone":"(770) 865-8654","cell":None},"email":"juliericelaw@icloud.com"},
    {"firstName":"Isaiah","middleName":"Kaneen","lastName":"Floyd","firmName":"Rolfes Henry, LPA CO","primaryLocation":{"city":"Bradenton","region":"FL","phone":"(941) 684-0100","cell":None},"email":"ifloyd@rolfeshenry.com"},
    {"firstName":"Willie","middleName":"James","lastName":"Walker","firmName":"The Walker Law Offices","primaryLocation":{"city":"Jacksonville","region":"FL","phone":"(904) 358-7104","cell":None},"email":"wjwesq@aol.com"},
    {"firstName":"John","middleName":"S.","lastName":"Myers","firmName":"John S Myers PC","primaryLocation":{"city":"Saint Marys","region":"GA","phone":"(912) 882-2332","cell":None},"email":"jsmpc@tds.net"},
    {"firstName":"James","middleName":"Wrixam","lastName":"McIlvaine","firmName":"McIlvaine Law Group","primaryLocation":{"city":"Brunswick","region":"GA","phone":"(912) 275-8014","cell":None},"email":"wrix@mcilvainelaw.net"},
    {"firstName":"Nathan","middleName":"Taylor","lastName":"Williams","firmName":"The Williams Litigation Group, P.C.","primaryLocation":{"city":"Brunswick","region":"GA","phone":"(912) 208-3721","cell":None},"email":"nathan@williamslg.com"},
    {"firstName":"Michael","middleName":"Chas","lastName":"Whitehead","firmName":"Mayfield Law","primaryLocation":{"city":"Brunswick","region":"GA","phone":"(912) 457-8557","cell":None},"email":"chas@mayfieldinjury.com"},
    {"firstName":"Michael","middleName":"Sheppard","lastName":"Bennett","firmName":"Bennett Law Firm","primaryLocation":{"city":"Valdosta","region":"GA","phone":"(229) 242-6726","cell":None},"email":"mbennettjr@bennettlawfirmllp.com"},
    {"firstName":"Carl","middleName":"Grover","lastName":"Fulp","firmName":"Carl G Fulp III PC","primaryLocation":{"city":"Valdosta","region":"GA","phone":"(229) 242-1434","cell":None},"email":"carl@fulplaw.com"},
    {"firstName":"J.","middleName":"Converse","lastName":"Bright","firmName":"Coleman Talley LLP","primaryLocation":{"city":"Valdosta","region":"GA","phone":"(229) 671-8243","cell":None},"email":"converse.bright@colemantalley.com"},
    {"firstName":"Christopher","middleName":"Kenneth","lastName":"Rodd","firmName":"The Rodd Firm LLC","primaryLocation":{"city":"Thomasville","region":"GA","phone":"(229) 421-7777","cell":None},"email":"chris@roddfirm.com"},
    {"firstName":"Zachary","middleName":"Hamilton","lastName":"Thomas","firmName":"Zachary H Thomas Law PC","primaryLocation":{"city":"Savannah","region":"GA","phone":"(912) 525-1196","cell":None},"email":"zach@zhtlawpc.com"},
    {"firstName":"Paul","middleName":"Graham","lastName":"Phillips","firmName":"Paul G Phillips LLC","primaryLocation":{"city":"Albany","region":"GA","phone":"(229) 461-6195","cell":None},"email":"phillips@pgp.law"},
    {"firstName":"Shawn","middleName":"Travis","lastName":"Pinkston","firmName":"Pinkston Law Firm, LLC","primaryLocation":{"city":"Mount Pleasant","region":"SC","phone":"(843) 814-5472","cell":None},"email":""},
    {"firstName":"Michael","middleName":"Earl","lastName":"Mayo","firmName":"The Mayo Firm","primaryLocation":{"city":"Macon","region":"GA","phone":"(478) 238-9887","cell":None},"email":"mayo@mayofirm.law"},
    {"firstName":"David","middleName":"Thomas","lastName":"Dorer","firmName":"Dozier Law Firm LLC","primaryLocation":{"city":"Macon","region":"GA","phone":"(478) 742-8441","cell":None},"email":"dorerlawteam@dozierlaw.com"},
    {"firstName":"Edward","middleName":"Larry","lastName":"Long","firmName":"Law Office of Edward L Long Jr.","primaryLocation":{"city":"Macon","region":"GA","phone":"(478) 238-6413","cell":None},"email":"ed@edlongatty.com"},
    {"firstName":"Jarome","middleName":"Emile","lastName":"Gautreaux","firmName":"Gautreaux Law, LLC","primaryLocation":{"city":"Macon","region":"GA","phone":"(478) 238-9758","cell":None},"email":"jarome@gautreauxlawfirm.com"},
    {"firstName":"Donald","middleName":"J.","lastName":"Jordan","firmName":"Adams Jordan & Herrington PC","primaryLocation":{"city":"Milledgeville","region":"GA","phone":"(478) 453-3997","cell":None},"email":"jjordan@adamsjordan.com"},
]

fields = ["First Name","Middle Name","Last Name","Firm Name","Firm Location","Office Phone","Cell Phone","Email"]

with open("medical_malpractice_georgia.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for a in data:
        loc = a["primaryLocation"]
        w.writerow({
            "First Name":    a["firstName"],
            "Middle Name":   a["middleName"],
            "Last Name":     a["lastName"],
            "Firm Name":     a["firmName"],
            "Firm Location": f"{loc['city']}, {loc['region']}",
            "Office Phone":  loc["phone"] or "",
            "Cell Phone":    loc["cell"] or "",
            "Email":         a["email"],
        })

print("Done — 20 records written to medical_malpractice_georgia.csv")
