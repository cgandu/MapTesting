

import folium
import pandas

data = pandas.read_csv("Parques.txt")
lon = list(data["LONG"])
lat = list(data["LAT"])
noms = list(data["AREA PROTEGIDA"])
reg = list(data["REGION"])
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

fPar = folium.FeatureGroup(name = "Parques Nacionales")

for lt, ln, nom, vis in zip(lat, lon, noms, visit):
    fPar.add_child(folium.Marker
                   (location = [lt, ln],
                   popup = folium.Popup(str(nom) + "** Visitantes anuales: " + str(vis) + " **", parse_html = True, max_width = "80%"),
                   tooltip = str(nom),
                   fill = True,
                   icon = folium.Icon(color = color_pop_up(vis)),
                   fill_opacity = 0.7))


fPob = folium.FeatureGroup(name = "Paises por poblacion")

fPob.add_child(folium.GeoJson(data = (open("world.json", "r", encoding = "utf-8-sig").read()),
                            style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000
                                                      else "orange" if 10000000<= x["properties"]["POP2005"] < 20000000
                                                      else "red",
                                                      "weight": 0}))

fReg = folium.FeatureGroup(name="Region")
mapa.add_child(fPar)
mapa.add_child(fPob)

mapa.add_child(folium.LayerControl())



mapa.save("mapaParques.html")