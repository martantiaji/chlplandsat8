import ee
import geemap
import streamlit as st


def app():
    st.title("Chlorophyll-a")
    "#streamlit geemap klorofil-a"

    st.markdown("""
    
    Aplikasi Web ini dibuat dengan menggunakan Streamlit untuk menampilkan nilai 
    estimasi besar klorofil-a pada Danau Matano dan Danau Towuti menggunakan 
    algoritma Jaelani 2015 berdasarkan jurnal [Pemetaan Distribusi Spasial Konsentrasi Klorofil-A dengan Landsat 8 di Danau Matano dan Danau Towuti, Sulawesi Selatan](http://lipi.go.id/publikasi/pemetaan-distribusi-spasial-konsentrasi-klorofil-a-dengan-landsat-8-di-danau-matano-dan-danau-towuti-sulawesi-selatan/2062)
    
    """)
    
    
def clhT2():
    
    st.header("Landsat 8 Surface Reflectance Tier 2")
    
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
    
    startdate=ee.Date.fromYMD(startYear,1,1)
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
    def clh_collection (ynz):
        image = col.filter(ee.Filter.calendarRange(ynz, ynz, 'year')).map(maskL8sr).mean()
        ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
        clh_a = image.expression(
            'exp(-0.9889*((RrsB4)/(RrsB5))+0.3619)',
            {'RrsB4': image.select('B4'),
             'RrsB5': image.select('B5')}).updateMask(ndwi)
        
        return clh_a.set('year', ynz).set('month', 1)\
    .set('date', ee.Date.fromYMD(ynz,1,1))\
    .set('system:time_start',ee.Date.fromYMD(ynz,1,1))
    
    def clh():
        return ee.ImageCollection.fromImages(year_list.flatten().map(fung_chl))
    print(clh_collection, 'Clorophil-a')
    
    parameter = {'min':0, 'max':1, 'palette':['blue','green']}
    #range(i=2016, i<=2020, i++)
    tahun= range (2016, 2021)
    for i in tahun:
        def clh (clh_collection):
            chl = clh_collection.filter(ee.Filter.eq('year', i)).first().clip(studyarea)
            Map.addLayer(clh,parameter,"Clorophyl-a"+i)
Map
