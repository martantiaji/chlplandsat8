import streamlit as st
from streamlit_option_menu import option_menu
from apps import (home,geemap_script)
#import your app modules here


st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": geemap_script.app, "title": "Chlorophyll-a", "icon": "map"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        Aplikasi web ini dikelola ole Martanti Aji dengan dosen pembimbing Dr. Lalu Muhamad Jaelani S.T., M.Sc., PhD. 
        Url aplikasi web ini yaitu <https://streamlit.geemap.org>
        
        Anda dapat mengakses referensi kode : [GitHub Aji](https://github.com/martantiaji/chlplandsat8.git)

    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
