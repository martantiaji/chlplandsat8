import streamlit as st
import ee
import numpy as np
import geemap
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pygal
import ipygee as ui
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

def L8_T1():
    
    st.header("Landsat 8 Surface Reflectance Tier 1")
    
    row1_col1, row1_col2 = st.columns([3, 1])
    width = 950
    height = 600
    
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

    m = geemap.Map()

    start_year = 2013
    end_year = 2020
    study_area = ee.Geometry.Polygon([
        [121.731876,-2.330221], [121.069735, -2.317823], [121.214026,-2.994612], [121.785511,-2.992766]
    ])

    collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filterBounds(study_area)

    yearlist = range(start_year, end_year)


    def mask_clouds(image):
        # Bits 3 and 5 are cloud shadow and cloud, respectively.
        cloud_shadow_bit_mask = (1 << 3)
        clouds_bit_mask = (1 << 5)
        # Get the pixel QA band.
        qa = image.select('pixel_qa')
        # Both flags should be set to zero, indicating clear conditions.
        mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) \
            .And(qa.bitwiseAnd(clouds_bit_mask).eq(0))
        return image \
            .divide(10000) \
            .divide(3.141593) \
            .updateMask(mask)


    def calculate_clorophil_a(year) :
        image = collection \
            .filter(ee.Filter.calendarRange(year, year, 'year')) \
            .map(mask_clouds) \
            .median()
        ndwi = image \
            .normalizedDifference(['B3', 'B5']) \
            .rename('NDWI')
        clorophil_a = image \
            .expression('10**(-0.9889*((RrsB4)/(RrsB5))+0.3619)', {
                'RrsB4': image.select('B4'),
                'RrsB5': image.select('B5')
            }) \
            .updateMask(ndwi)
        return clorophil_a \
            .set('year', year) \
            .set('month', 1) \
            .set('date', ee.Date.fromYMD(year,1,1)) \
            .set('system:time_start',ee.Date.fromYMD(year, 1, 1))

    clorophil_a_collection = ee.ImageCollection.fromImages([
        calculate_clorophil_a(year)
        for year in yearlist
    ])
    print(clorophil_a_collection.getInfo())

    parameter = {'min':0, 'max':1, 'palette':['blue','green']}
    m.addLayer(clorophil_a_collection,parameter,"Clorophyll-a")
    m.add_colorbar(
        parameter,
        label="Clorophyll-a (mg/m3)",
        orientation="horizontal",
        layer_name="Clorophyll-a",
        transparent_bg=True,
    )
    m.centerObject(study_area, 10)
    m.to_streamlit(width=width, height=height)

    st.markdown("![Timelapse Chlorophyll-a Tier 1](https://media.giphy.com/media/Lq2dG9Q3H6zLBIAQed/giphy.gif)")
    #out_gif= "https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/videoThumbnails/95777a5052393f9d132687dc74b5ac7a-dd3291f7f99d0e209c6839234dc430bd:getPixels"
    #st.image(out_gif, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


def L8_T2() :
    
    st.header("Landsat 8 Surface Reflectance Tier 2")
    
    row1_col1, row1_col2 = st.columns([3, 1])
    width = 950
    height = 600

    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

    m = geemap.Map()

    start_year = 2016
    end_year = 2020
    yearlist = range(start_year, end_year)

    study_area = ee.Geometry.Polygon([
        [121.731876,-2.330221], [121.069735, -2.317823], [121.214026,-2.994612], [121.785511,-2.992766]
    ])

    collection = ee.ImageCollection('LANDSAT/LC08/C01/T2_SR') \
                .filterBounds(study_area)

    def mask_clouds(image):
        # Bits 3 and 5 are cloud shadow and cloud, respectively.
        cloud_shadow_bit_mask = (1 << 20)
        clouds_bit_mask = (1 << 25)
        # Get the pixel QA band.
        qa = image.select('pixel_qa')
        # Both flags should be set to zero, indicating clear conditions.
        mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) \
            .And(qa.bitwiseAnd(clouds_bit_mask).eq(0))
        return image\
            .divide(10000)\
            .divide(3.141593)\
            .updateMask(mask)

    def calculate_clorophil_a(year) :
        image = collection \
            .filter(ee.Filter.calendarRange(year, year, 'year')) \
            .map(mask_clouds) \
            .median() 
        #diubah menjadi median semua mean nya (rentang waktu)
        ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
        clorophil_a = image.expression(
            '10**(-0.9889*((RrsB4)/(RrsB5))+0.3619)', {
                'RrsB4': image.select('B4'),
                'RrsB5': image.select('B5')
            }).updateMask(ndwi)
        return clorophil_a \
            .set('year', year) \
            .set('month', 1) \
            .set('date', ee.Date.fromYMD(year,1,1)) \
            .set('system:time_start',ee.Date.fromYMD(year, 1, 1))

    clorophil_a_collection = ee.ImageCollection.fromImages([
        calculate_clorophil_a(year)
        for year in yearlist
    ])
    print(clorophil_a_collection.getInfo())

    parameter = {'min':0, 'max':1, 'palette':['blue','green']}
    m.addLayer(clorophil_a_collection,parameter,"Clorophyll-a")
    m.add_colorbar(
        parameter,
        label="Clorophyll-a (mg/m3)",
        orientation="horizontal",
        layer_name="Clorophyll-a",
        transparent_bg=True,
    )
    m.centerObject(study_area, 10)
    m.to_streamlit(width=width, height=height)
    
    st.markdown("![Timelapse Chlorophyll-a Tier 2](https://media.giphy.com/media/IdjzI6SLP8kDW46XgZ/giphy.gif)")
    
    #out_gif= "https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/videoThumbnails/deef43df5ac8457bf353c66994fd1826-17679fe21c10ddc2c6f8da0d998f339d:getPixels"
    #st.image(out_gif, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")          
    
def app():
    st.title("Chlorophyll-a")

    st.markdown("""

    Aplikasi Web ini dibuat dengan menggunakan Streamlit untuk menampilkan nilai 
    estimasi besar klorofil-a pada Danau Matano dan Danau Towuti menggunakan 
    algoritma Jaelani 2015 berdasarkan jurnal [Pemetaan Distribusi Spasial Konsentrasi Klorofil-A dengan Landsat 8 di Danau Matano dan Danau Towuti, Sulawesi Selatan](http://lipi.go.id/publikasi/pemetaan-distribusi-spasial-konsentrasi-klorofil-a-dengan-landsat-8-di-danau-matano-dan-danau-towuti-sulawesi-selatan/2062)

    """)
    
    apps = ["Landsat 8 Surface Reflectance Tier 1", "Landsat 8 Surface Reflectance Tier 2"]
    
    selected_app = st.selectbox("Select an app", apps)
    
    if selected_app == "Landsat 8 Surface Reflectance Tier 1":
        L8_T1()
    elif selected_app == "Landsat 8 Surface Reflectance Tier 2":
        L8_T2()