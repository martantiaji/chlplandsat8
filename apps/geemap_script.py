import ee
import geemap
import streamlit as st
import numpy as np


def app():
    st.title("Chlorophyll-a")
    "#streamlit geemap klorofil-a"

    st.markdown("""
    
    Aplikasi Web ini dibuat dengan menggunakan Streamlit untuk menampilkan nilai 
    estimasi besar klorofil-a pada Danau Matano dan Danau Towuti menggunakan 
    algoritma Jaelani 2015 berdasarkan jurnal [Pemetaan Distribusi Spasial Konsentrasi Klorofil-A dengan Landsat 8 di Danau Matano dan Danau Towuti, Sulawesi Selatan](http://lipi.go.id/publikasi/pemetaan-distribusi-spasial-konsentrasi-klorofil-a-dengan-landsat-8-di-danau-matano-dan-danau-towuti-sulawesi-selatan/2062)
    
    """)
    
    
def clhT1():
    
    st.header("Landsat 8 Surface Reflectance Tier 2")
    
    Map = geemap.Map()
    
    polygon = ee.Geometry.Polygon([
        [121.731876,-2.330221], [121.069735, -2.317823], [121.214026,-2.994612], [121.785511,-2.992766]
    ])
    
    studyarea= polygon
    
    #Make a time
    startYear = 2013
    endYear = 2020
    startdate=ee.Date.fromYMD(startYear,1,1)
    enddate=ee.Date.fromYMD(endYear+1,12,31)
    yearlist = range(startYear, endYear)
    print(yearlist)
    #Read the Data
    for col in yearlist:
        col= ee.ImageCollection("LANDSAT/LC08/C01/T2_SR")\
            .filterBounds(studyarea).filter(ee.Filter.eq('year', yearlist)).first()
    #cloud masking area
    def maskL8sr(col):
        # Bits 3 and 5 are cloud shadow and cloud, respectively.
        cloudShadowBitMask = (1 << 3)
        cloudsBitMask = (1 << 5)
        # Get the pixel QA band.
        qa = col.select('pixel_qa')
        # Both flags should be set to zero, indicating clear conditions.
        mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)\
        .And(qa.bitwiseAnd(cloudsBitMask).eq(0))
        
        return col.divide(10000).divide(3.141593).updateMask(mask)
        
    #Make a calculate for Clorophil-a
    def chla (ynz) :
        image = col.filter(ee.Filter.calendarRange(ynz, ynz, 'year')).map(maskL8sr).mean()
        ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
        clh_a = image.expression(
            'exp(-0.9889*((RrsB4)/(RrsB5))+0.3619)',
            {'RrsB4': image.select('B4'),
             'RrsB5': image.select('B5')}).updateMask(ndwi)
        return clh_a.set('year', ynz).set('month', 1).set('date', ee.Date.fromYMD(ynz,1,1)).set('system:time_start',ee.Date.fromYMD(ynz,1,1)).map()
    
    parameter = {'min':0, 'max':1, 'palette':['blue','green']}
    
    clhcollection = ee.ImageCollection.fromImages([chla]).flatten()
    
    Map.addLayer(clhcollection, parameter, 'Clorophyll-a')
    Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
    Map.to_streamlit(width=width, height=height)
