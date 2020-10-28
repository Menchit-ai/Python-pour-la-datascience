import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("requests")

install("pandas")
install("plotly")
install("plotly.express")
install("folium")
install("geopandas")

install("pycountry")
install("pycountry_convert")
install("numpy")
install("datetime")

install("dash")
install("dash_core_components")
install("dash_html_components")
install("Input")
install("Output")