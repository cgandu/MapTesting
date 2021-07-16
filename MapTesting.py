

import folium
import pandas

data = pandas.read_csv("Parques.txt")
lon = list(data["LONG"])
lat = list(data["LAT"])
noms = list(data["AREA PROTEGIDA"])
visit = list(data["VISITANTES ANUALES"])
mapa = folium.Map(location = [-34.96, -65.11], zoom_start=6)

def color_pop_up(a):
    
    try:

        if a >= 50000:
            return "red"
        elif 20000 <= a < 50000:
            return "orange"
        elif a < 20000:
            return "green"
        else:
            return "gray"
    except:
        print("sin datos")
        return "gray"

fg = folium.FeatureGroup(name = "Mapa de Parques Nacionales en Argentina")

for lt, ln, nom, vis in zip(lat, lon, noms, visit):
    mapa.add_child(folium.Marker
                   (location = [lt, ln],
                   popup = folium.Popup(str(nom) + "** Visitantes anuales: " + str(vis) + " **", parse_html = True, max_width = "80%"),
                   tooltip = str(nom),
                   fill = True,
                   icon = folium.Icon(color = color_pop_up(vis)),
                   fill_opacity = 0.7))


fg.add_child(folium.GeoJson(data = (open("world.json", "r", encoding = "utf-8-sig").read()),
                            style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000
                                                      else "orange" if 10000000<= x["properties"]["POP2005"] < 20000000
                                                      else "red",
                                                      "weight": 0}))
mapa.add_child(fg)
mapa.save("mapaParques.html")