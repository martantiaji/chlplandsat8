import ee
import geemap
import streamlit as st
from streamlit_folium import folium_static
import geopandas as gpd


def app():
    st.title("Chlorophyll-a")
    "#streamlit geemap klorofil-a"

    st.markdown("""
    
    Aplikasi Web ini dibuat dengan menggunakan Streamlit untuk menampilkan nilai 
    estimasi besar klorofil-a pada Danau Matano dan Danau Towuti menggunakan 
    algoritma Jaelani 2015 berdasarkan jurnal [Pemetaan Distribusi Spasial Konsentrasi Klorofil-A dengan Landsat 8 di Danau Matano dan Danau Towuti, Sulawesi Selatan](http://lipi.go.id/publikasi/pemetaan-distribusi-spasial-konsentrasi-klorofil-a-dengan-landsat-8-di-danau-matano-dan-danau-towuti-sulawesi-selatan/2062)
    
    """)
    
Map = geemap.Map()

polygon = ee.Geometry.Polygon([
  [[121.731876,-2.330221], [121.069735, -2.317823], [121.214026,-2.994612], [121.785511,-2.992766]]
])

studyarea= polygon

#Read the Data
col= ee.ImageCollection("LANDSAT/LC08/C01/T2_SR") \
            .filterBounds(studyarea)

Map.addLayer(col,{},"Natural Color")
print(col)

#Make a time
startYear = 2016
endYear = 2020

startdate=ee.Date.fromYMD(startYear,01,01)
enddate=ee.Date.fromYMD(endYear+1,12,31)
year_list = ee.List.sequence(startYear, endYear)

#cloud masking area
def maskL8sr(col):
  # Bits 3 and 5 are cloud shadow and cloud, respectively.
  cloudShadowBitMask = (1 << 3)
  cloudsBitMask = (1 << 5)
  # Get the pixel QA band.
  qa = col.select('pixel_qa')
  # Both flags should be set to zero, indicating clear conditions.
  mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0) \
                 .And(qa.bitwiseAnd(cloudsBitMask).eq(0))
  return col.divide(10000).divide(3.141593).updateMask(mask)


#Make a calculate for Clorophil-a

def func_xod (ynz):
  image = col.filter(ee.Filter.calendarRange(ynz, ynz, 'year')) \
              .map(maskL8sr) \
              .mean()

            ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
            clh_a = image.expression(
              'exp(-0.9889*((RrsB4)/(RrsB5))+0.3619)',
              {'RrsB4': image.select('B4'),
              'RrsB5': image.select('B5')}).updateMask(ndwi)

              return clh_a.set('year', ynz) \
              .set('month', 1) \
              .set('date', ee.Date.fromYMD(ynz,1,1)) \
              .set('system:time_start',ee.Date.fromYMD(ynz,1,1))

clh_collection =  ee.ImageCollection.fromImages(year_list.map(func_xod
).flatten())

).flatten())

print(clh_collection, 'Clorophil-a')

#year = 2016
parameter = {'min':0, 'max':1, 'palette':['blue','green']}
for i in range(i=2016, i<=2020, 1):
  clh = clh_collection.filter(ee.Filter.eq('year', i)).first()
  clipped = clh.clip(studyarea)
  Map.addLayer(clipped,parameter,'Clorophyl-a '+i)

#--------------------------------------------#
#              MEMBUAT LEGENDA               #
#--------------------------------------------#
parameter = {'min':0, 'max':10, 'palette':['blue','green']}
#Membuat palet
def makeColorBarParams(palette):
  return {
    'bbox': [0, 0, 1, 0.1],
    'dimensions': '200x20',
    format: 'png',
    'min': 0,
    'max': 1,
    'palette': palette,
  }

#Membuat colorbar
colorBar = ui.Thumbnail({
  'image': ee.Image.pixelLonLat().select(0),
  'params': makeColorBarParams(parameter.palette),
  'style': '{stretch': 'vertical', 'margin': '0px 8px', 'maxHeight': '24px'},
})

#Membuat panel
legendLabels = ui.Panel({
  'widgets': [
    ui.Label(parameter.min, {'margin': '4px 5px', 'textAlign': 'left'}),
    ui.Label(parameter.max, {'margin': '4px 170px', 'textAlign': 'right'})
  ],
  'layout': ui.Panel.Layout.flow('horizontal')
})

legendTitle = ui.Label({
  'value': 'Chlorophyll-a (mg/m3)',
  'style': '{fontWeight': 'bold'}
})

#Menampilkan legenda
legendPanel = ui.Panel([legendTitle, colorBar, legendLabels])
Map.add(legendPanel)

#--------------------------------------------#
#               MEMBUAT CHART                #
#--------------------------------------------#

klo_chart = ui.Chart.image.series({
  'imageCollection': clh_collection,
  'region': boundary,
  'reducer': ee.Reducer.mean(),
  'scale' : 10000,
  'xProperty': 'system:time_start'}) \
  .setOptions({
    'title': 'Nilai Klorofil-a',
    'vAxis': '{title': 'Klorofil-a (mg/m3)'},
})
print(klo_chart)
Map
