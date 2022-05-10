import json
import requests
api_key = 'k_03xy1plm'
url1 = 'https://imdb-api.com'
req = requests.get(url1)

print('Connection Status:')
if req.status_code == 200:
    print("OK")
elif req.status_code in (301, 302, 304):
    print("Redirection")
elif req.status_code in (401, 403, 404, 405):
    print("Client Error")
elif req.status_code in (501, 503, 504, 502):
    print("Server Error")
else:
    print("Unknown Error")

print('Type of Content:')
print(req.headers['Content-Type'])

print('------------------------------')

movie_name = input("Input Movie Name: ")
#ამ ლინკით ვპპოულობ მომხმარებლის მიერ შეყვანილი დასახელების მსგავს ფილმებს და ვპრინტავ ჩამონათვალს
url_movie_search = f'https://imdb-api.com/en/API/Search/{api_key}/{movie_name}'
reqMS = requests.get(url_movie_search)
req_jsonMS = reqMS.text
req_dictMS = json.loads(req_jsonMS)
req_dict_readableMS = json.dumps(req_dictMS, indent=5)

with open('json_data.json', 'w') as file:
    file.write(req_dict_readableMS)

for each in req_dictMS['results']:
    print(f"ID: {each['id']}")
    print(f"Title: {each['title']}")
    print(f"Description: {each['description']}")
    print(f"Image Link: {each['image']}")
    print('-----------------')


movie_id = input('Input Movie ID: ')

#ამ ლინკით ვპპოულობ მომხმარებლის მიერ შეყვანილი აიდის მიხედვით ფილმის რეიტინგს (ამ აიდის მომხმარებელი ნახულობს მანამდე მიღებული ტექსტიდან)
url_movie_ID = f'https://imdb-api.com/en/API/Ratings/{api_key}/{movie_id}'
req = requests.get(url_movie_ID)
req_jsonID = req.text
req_dictID = json.loads(req_jsonID)

title = req_dictID['title']
print(f"{title} Ratings:")
print(f"IMDb: {req_dictID['imDb']}")
print(f"Metacritic: {req_dictID['metacritic']}")
print('-----------------')


#არჩეული ფილმის პოსტერის შენახვა
response = input("Do You Want to Save This Movies Poster? Y or N ")

while response != "Y" and response != "N":
        print("Input was Invalid")
        response = input("Do You Want to Save This Movies Poster? Y or N ")


for each in req_dictMS['results']:
    if each['id'] == movie_id:
        image_url = f"{each['image']}"
        break
    else:
        pass

req = requests.get(image_url)

if response == "Y":
    file = open(f"{title}.jpg", 'wb')
    file.write(req.content)
    print("Image was Successfully Saved")
elif response == "N":
    print("Okay")




#ცხრილი
#მოცემული ცხრილის საშუალებით ინახება მომხმარებლის მიერ მოძებნილი ფილმები და მათი რეიტინგები,ასევე ფილმის აიდი
import sqlite3
connect = sqlite3.connect('search_history_db.sqlite')
cursor = connect.cursor()

#ცხრილის შექმნა
# cursor.execute('CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT, IMDb_ID VARCHAR(30), Title VARCHAR(30), IMDb_Rate INTEGER, Metacritic_Rate INTEGER);')

#ინფორმაციის შეტანა
cursor.execute('INSERT INTO history (IMDb_ID, Title, IMDb_Rate, Metacritic_Rate) VALUES(?,?,?,?)', (movie_id, req_dictID['title'], req_dictID['imDb'], req_dictID['metacritic']))
connect.commit()
connect.close()
