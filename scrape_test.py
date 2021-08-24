import requests
page = requests.get(
    "https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?&rows=1000&areaId=601&parent_areaid=6")

print(page.content)
