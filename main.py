import discord
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def get_cars():
    urls = ["https://www.autoscout24.de/lst/volkswagen/golf-(alle)/ve_mk-6","https://www.autoscout24.de/lst/volkswagen/golf-(alle)/ve_mk-7"]
    params = {
        "sort": "standard",
        "desc": "false",
        "ustate": "U",
        "size": "20",
        "cy": "D",
        "fregfrom": "2008",
        "kmto": "200000",
        "atype": "C",
        "fpos": "Stuttgart",
        "radius": "100",
        "unfall": "Unfallfrei",
        "priceto": "20000"
    }
    cars = []
    cars= []
    for url in urls:
        r = requests.get(url, params=params)
        soup = BeautifulSoup(r.text, "html.parser")
    
        items = soup.find_all("article", {"class": "cldt-summary-full-item listing-impressions-tracking list-page-item false ListItem_newDesignArticle__wr7pi"})
        for item in items:
            price = f"€{item['data-price']}"
            title = item.find("h2").text.strip()
            location = item.find("span", {"class": "SellerInfo_address__txoNV"})
            if location != None:
                location = item.find("span", {"class": "SellerInfo_address__txoNV"}).text.strip()
                #Split location
                location = location.split(" ")
                location = location[-1]
            else:
                location = item.find("span", {"class": "SellerInfo_private__JCxcm"}).text.strip()
                location = location.split(" ")
                location = location[-1]

            link = "https://www.autoscout24.com" +item.find("a", {"class": "ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l"})['href']

            if "Finanzierung" not in title and "Leasing" not in title and "Mietkauf" not in title:
                car = [title,price, location, link]
                cars.append(car)
    return cars

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    cars = get_cars()
    if len(cars) > 0:
        channel_id = 563586646423896088
        channel = client.get_channel(channel_id)
        for car in cars:
            embed = discord.Embed(
                title="Neues Auto gefunden!",
                description=f"""
                Title: {car[0]}
                Price: {car[1]}
                Location: {car[2]}
                Link: {car[3]}
                """)
            await channel.send(embed=embed)

client.run(TOEKN)
