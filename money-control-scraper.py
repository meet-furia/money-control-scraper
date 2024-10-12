import os
import csv
from datetime import datetime
import pyuser_agent
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_stock_data(url):
    ua = pyuser_agent.UA()
    headers = {
        "User-Agent": ua.random
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(r.text, 'html.parser')

        if "indian-indices" in url:
            # Nifty-specific scraping logic
            index_name_div = soup.find("div", class_="inid_name")
            index_name = index_name_div.text.strip() if index_name_div else "Stock name not found"
            
            price_div = soup.find("div", class_="inprice1")
            price_span = price_div.find("span", id="sp_val").text.strip() if price_div else "Live price not found"

            low_div = soup.find("div", id="sp_low")
            low_price = low_div.text.strip() if low_div else "Today's Low not found"

            high_div = soup.find("div", id="sp_high")
            high_price = high_div.text.strip() if high_div else "Today's High not found"

            return index_name, price_span, low_price, high_price

        else:
            # Stock-specific scraping logic
            stock_name_div = soup.find("div", class_="inid_name")
            stock_name = stock_name_div.find("h1").text.strip() if stock_name_div else "Stock name not found"

            price_div = soup.find(class_="inprice1 nsecp")
            low_div = soup.find(id="sp_low")
            high_div = soup.find(id="sp_high")

            price = price_div.text.strip() if price_div else "Live Price not found"
            low_price = low_div.text.strip() if low_div else "Today's Low not found"
            high_price = high_div.text.strip() if high_div else "Today's High not found"

            return stock_name, price, low_price, high_price
    except Exception as e:
        return f"Error fetching data from {url}: {e}"

# List of URLs to scrape
urls = [
    "https://www.moneycontrol.com/india/stockpricequote/infrastructure-general/abbindia/ABB",
    "https://www.moneycontrol.com/india/stockpricequote/cement-major/acc/ACC06",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/ausmallfinancebank/ASF02",
    "https://www.moneycontrol.com/india/stockpricequote/chemicals/aartiindustries/AI45",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/abbottindia/AI51",
    "https://www.moneycontrol.com/india/stockpricequote/trading/adanienterprises/AE13",
    "https://www.moneycontrol.com/india/stockpricequote/infrastructuregeneral/adaniportsspecialeconomiczone/MPS",
    "https://www.moneycontrol.com/india/stockpricequote/finance-investments/adityabirlacapital/ABC9",
    "https://www.moneycontrol.com/india/stockpricequote/retail/adityabirlafashionretail/PFR",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/alkemlaboratories/AL05",
    "https://www.moneycontrol.com/india/stockpricequote/cement-major/ambujacements/AC18",
    "https://www.moneycontrol.com/india/stockpricequote/hospitalsmedical-services/apollohospitalsenterprises/AHE",
    "https://www.moneycontrol.com/india/stockpricequote/tyres/apollotyres/AT14",
    "https://www.moneycontrol.com/india/stockpricequote/auto-lcvshcvs/ashokleyland/AL",
    "https://www.moneycontrol.com/india/stockpricequote/paintsvarnishes/asianpaints/AP31",
    "https://www.moneycontrol.com/india/stockpricequote/plastics/astrallimited/APT02",
    "https://www.moneycontrol.com/india/stockpricequote/chemicals/atul/A06",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/aurobindopharma/AP",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/axisbank/AB16",



    "https://www.moneycontrol.com/india/stockpricequote/auto-23-wheelers/bajajauto/BA10",
    "https://www.moneycontrol.com/india/stockpricequote/finance-nbfc/bajajfinance/BAF",
    "https://www.moneycontrol.com/india/stockpricequote/finance-investments/bajajfinserv/BF04",
    "https://www.moneycontrol.com/india/stockpricequote/tyres/balkrishnaindustries/BI03",
    "https://www.moneycontrol.com/india/stockpricequote/sugar/balrampurchinimills/BCM",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/bandhanbank/BB09",
    "https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/bankbaroda/BOB",
    "https://www.moneycontrol.com/india/stockpricequote/leather-products/bataindia/BI01",
    "https://www.moneycontrol.com/india/stockpricequote/paintsvarnishes/bergerpaintsindia/BPI02",
    "https://www.moneycontrol.com/india/stockpricequote/aerospacedefence/bharatelectronics/BE03",
    "https://www.moneycontrol.com/india/stockpricequote/castingsforgings/bharatforge/BF03",
    "https://www.moneycontrol.com/india/stockpricequote/infrastructure-general/bharatheavyelectricals/BHE",
    "https://www.moneycontrol.com/india/stockpricequote/refineries/bharatpetroleumcorporation/BPC",
    "https://www.moneycontrol.com/india/stockpricequote/telecommunications-service/bhartiairtel/BA08",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/biocon/BL03",
    "https://www.moneycontrol.com/india/stockpricequote/computers-software-mediumsmall/birlasoft/KPI02",
    "https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/bosch/B05",
    "https://www.moneycontrol.com/india/stockpricequote/food-processing/britanniaindustries/BI",


   
    "https://www.moneycontrol.com/india/stockpricequote/finance-housing/canfinhomes/CFH",
    "https://moneycontrol.com/india/stockpricequote/banks-public-sector/canarabank/CB06",
    "https://www.moneycontrol.com/india/stockpricequote/fertilisers/chambalfertiliserschemicals/CFC",
    "https://www.moneycontrol.com/india/stockpricequote/finance-nbfc/cholamandalaminvestmentfinancecompany/CDB",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/cipla/C",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/cityunionbank/CUB",
    "https://www.moneycontrol.com/india/stockpricequote/miningminerals/coalindia/CI11",
    "https://www.moneycontrol.com/india/stockpricequote/computers-software/coforgelimited/NII02",
    "https://www.moneycontrol.com/india/stockpricequote/personal-care/colgatepalmoliveindia/CPI",
    "https://www.moneycontrol.com/india/stockpricequote/transportlogistics/containercorporationindia/CCI",
    "https://www.moneycontrol.com/india/stockpricequote/fertilisers/coromandelinternational/CI45",
    "https://www.moneycontrol.com/india/stockpricequote/electricals/cromptongreavesconsumerelectrical/CGC01",
    "https://www.moneycontrol.com/india/stockpricequote/engines/cumminsindia/CI02",

   
    "https://www.moneycontrol.com/india/stockpricequote/constructioncontracting-real-estate/dlf/D04",
    "https://www.moneycontrol.com/india/stockpricequote/personal-care/daburindia/DI",
    "https://www.moneycontrol.com/india/stockpricequote/cement-major/dalmiabharat/OCL",
    "https://www.moneycontrol.com/india/stockpricequote/chemicals/deepaknitrite/DN",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/divislaboratories/DL03",
    "https://www.moneycontrol.com/india/stockpricequote/electricals/dixontechnologies/DT07",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/drlalpathlabs/DLP01",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/drreddyslaboratories/DRL",


    "https://www.moneycontrol.com/india/stockpricequote/auto-lcvshcvs/eichermotors/EM",
    "https://www.moneycontrol.com/india/stockpricequote/automobile-tractors/escortskubota/E",
    "https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/exideindustries/EI",


    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/federalbank/FB",


    "https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/gailindia/GAI",
    "https://www.moneycontrol.com/india/stockpricequote/transport-infrastructure/gmrairportsinfrastructure/GI27",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/glenmarkpharma/GP08",
    "https://www.moneycontrol.com/india/stockpricequote/personal-care/godrejconsumerproducts/GCP",
    "https://www.moneycontrol.com/india/stockpricequote/constructioncontracting-real-estate/godrejproperties/GP11",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/granulesindia/GI25",
    "https://www.moneycontrol.com/india/stockpricequote/diversified/grasimindustries/GI01",
    "https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/gujaratgas/GGC",
    "https://www.moneycontrol.com/india/stockpricequote/fertilizers/gujaratnarmadavalleyfertchem/GNV",



    "https://www.moneycontrol.com/india/stockpricequote/computers-software/hcltechnologies/HCL02",
    "https://www.moneycontrol.com/india/stockpricequote/finance-investments/hdfcassetmanagementcompany/HAM02",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/hdfcbank/HDF01",
    "https://www.moneycontrol.com/india/stockpricequote/lifehealth-insurance/hdfclifeinsurancecompany/HSL01",
    "https://www.moneycontrol.com/india/stockpricequote/electric-equipment/havellsindia/HI01",
    "https://www.moneycontrol.com/india/stockpricequote/auto-23-wheelers/heromotocorp/HHM",
    "https://www.moneycontrol.com/india/stockpricequote/ironsteel/hindalcoindustries/HI",
    "https://www.moneycontrol.com/india/stockpricequote/aerospacedefence/hindustanaeronautics/HAL",
    "https://www.moneycontrol.com/india/stockpricequote/metals-non-ferrous/hindustancopper/HC07",
    "https://www.moneycontrol.com/india/stockpricequote/refineries/hindustanpetroleumcorporation/HPC",
    "https://www.moneycontrol.com/india/stockpricequote/personal-care/hindustanunilever/HU",



    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/icicibank/ICI02",
    "https://www.moneycontrol.com/india/stockpricequote/multiline-insurancebrokers/icicilombardgeneralinsurancecompany/ILG",
    "https://www.moneycontrol.com/india/stockpricequote/finance-general/iciciprudentiallifeinsurancecompany/IPL01",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/idfcfirstbank/IDF01",
    "https://www.moneycontrol.com/india/stockpricequote/finance-housing/idfc/IDF",
    "https://www.moneycontrol.com/india/stockpricequote/diversified/itc/ITC",
    "https://www.moneycontrol.com/india/stockpricequote/retailing/indiamartintermesh/II12",
    "https://www.moneycontrol.com/india/stockpricequote/diversified/indianenergyexchange/IEE",
    "https://www.moneycontrol.com/india/stockpricequote/hotels/indianhotelscompany/IHC",
    "https://www.moneycontrol.com/india/stockpricequote/refineries/indianoilcorporation/IOC",
    "https://www.moneycontrol.com/india/stockpricequote/miscellaneous/irctc-indianrailwaycateringtourismcorp/IRC",
    "https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/indraprasthagas/IG04",
    "https://www.moneycontrol.com/india/stockpricequote/telecommunications-equipment/industowers/BI14",
    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/indusindbank/IIB",
    "https://www.moneycontrol.com/india/stockpricequote/miscellaneous/infoedgeindia/IEI01",
    "https://www.moneycontrol.com/india/stockpricequote/computers-software/infosys/IT",
    "https://www.moneycontrol.com/india/stockpricequote/transportlogistics/interglobeaviation/IA04",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/ipcalaboratories/IL",



    "https://www.moneycontrol.com/india/stockpricequote/cement-major/jkcement/JKC03",
    "https://www.moneycontrol.com/india/stockpricequote/steel-large/jswsteel/JSW01",
    "https://www.moneycontrol.com/india/stockpricequote/steel-sponge-iron/jindalsteelpower/JSP",
    "https://www.moneycontrol.com/india/stockpricequote/miscellaneous/jubilantfoodworks/JF04",



    "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/kotakmahindrabank/KMB",



    "https://www.moneycontrol.com/india/stockpricequote/finance-investments/ltfinance/LFH",
    "https://www.moneycontrol.com/india/stockpricequote/engineering/lttechnologyservices/LTS",
    "https://www.moneycontrol.com/india/stockpricequote/finance-housing/lichousingfinance/LIC",
    "https://www.moneycontrol.com/india/stockpricequote/computers-software/ltimindtree/LI12",
    "https://www.moneycontrol.com/india/stockpricequote/infrastructure-general/larsentoubro/LT",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/lauruslabs/LL05",
    "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/lupin/L",



    "https://www.moneycontrol.com/india/stockpricequote/tyres/mrf/MRF",
    "https://www.moneycontrol.com/india/stockpricequote/refineries/mahanagargas/MG02",
    "https://www.moneycontrol.com/india/stockpricequote/finance-nbfc/mahindramahindrafinancialservices/MMF04",
    "https://www.moneycontrol.com/india/stockpricequote/auto-carsjeeps/mahindramahindra/MM",
    "https://www.moneycontrol.com/india/stockpricequote/finance-leasinghire-purchase/manappuramfinance/MGF01",
    "https://www.moneycontrol.com/india/stockpricequote/personal-care/marico/M13",
    "https://www.moneycontrol.com/india/stockpricequote/auto-carsjeeps/marutisuzukiindia/MS24",
    "https://www.moneycontrol.com/india/stockpricequote/finance-investments/maxfinancialservices/MI",
    "https://www.moneycontrol.com/india/stockpricequote/hospitalsmedical-services/metropolishealthcare/MH06",
    "https://www.moneycontrol.com/india/stockpricequote/computers-software/mphasis/MB02",
    "https://www.moneycontrol.com/india/stockpricequote/miscellaneous/multicommodityexchangeindia/MCE",
    "https://www.moneycontrol.com/india/stockpricequote/finance-investments/muthootfinance/MF10",



    "https://www.moneycontrol.com/india/stockpricequote/miningminerals/nmdc/NMD02",
    "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/ntpc/NTP",
    "https://www.moneycontrol.com/india/stockpricequote/aluminium/nationalaluminiumcompany/NAC",
    "https://www.moneycontrol.com/india/stockpricequote/chemicals/navinfluorineinternational/NFI",
    "https://www.moneycontrol.com/india/stockpricequote/food-processing/nestleindia/NI",
    "https://www.moneycontrol.com/indian-indices/nifty-50-9.html",
    "https://www.moneycontrol.com/indian-indices/nifty-bank-23.html",
    "https://www.moneycontrol.com/indian-indices/nifty-fin-service-47.html",
    "https://www.moneycontrol.com/indian-indices/NIFTY-MID-SELECT-128.html",
    "https://www.moneycontrol.com/indian-indices/nifty-next-50-6.html",


"https://www.moneycontrol.com/india/stockpricequote/constructioncontracting-real-estate/oberoirealty/OR",
"https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG",
"https://www.moneycontrol.com/india/stockpricequote/computers-software/oraclefinancialservicessoftware/OFS01",



"https://www.moneycontrol.com/india/stockpricequote/pesticidesagro-chemicals/piindustries/PII",
"https://www.moneycontrol.com/india/stockpricequote/mediaentertainment/pvrinox/PVR",
"https://www.moneycontrol.com/india/stockpricequote/textiles-readymade-apparels/pageindustries/PI35",
"https://www.moneycontrol.com/india/stockpricequote/computers-software/persistentsystems/PS15",
"https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/petronetlng/PLN",
"https://www.moneycontrol.com/india/stockpricequote/chemicals/pidiliteindustries/PI11",
"https://www.moneycontrol.com/india/stockpricequote/finance-nbfc/piramalenterprises/PH05",
"https://www.moneycontrol.com/india/stockpricequote/cables-powerothers/polycabindia/PI44",
"https://www.moneycontrol.com/india/stockpricequote/finance-term-lending-institutions/powerfinancecorporation/PFC02",
"https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/powergridcorporationindia/PGC",
"https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/punjabnationalbank/PNB05",



"https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/rblbank/RB03",
"https://www.moneycontrol.com/india/stockpricequote/finance-term-lending-institutions/rec/REC02",
"https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI",



"https://www.moneycontrol.com/india/stockpricequote/finance-term-lending/sbicardspaymentservices/SCP02",
"https://www.moneycontrol.com/india/stockpricequote/lifehealth-insurance/sbilifeinsurancecompany/SLI03",
"https://www.moneycontrol.com/india/stockpricequote/diversified/srf/SRF",
"https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries-auto-truckmotorcycle-parts/samvardhanamothersoninternational/MSS01",
"https://www.moneycontrol.com/india/stockpricequote/cement-major/shreecements/SC12",
"https://www.moneycontrol.com/india/stockpricequote/finance-leasinghire-purchase/shriramfinance/STF",
"https://www.moneycontrol.com/india/stockpricequote/infrastructure-general/siemens/S",
"https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/statebankindia/SBI",
"https://www.moneycontrol.com/india/stockpricequote/steel-large/steelauthorityindia/SAI",
"https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/sunpharmaceuticalindustries/SPI",
"https://www.moneycontrol.com/india/stockpricequote/mediaentertainment/suntvnetwork/STN01",
"https://www.moneycontrol.com/india/stockpricequote/miscellaneous/syngeneinternational/SI10",



"https://www.moneycontrol.com/india/stockpricequote/auto-23-wheelers/tvsmotorcompany/TVS",
"https://www.moneycontrol.com/india/stockpricequote/chemicals/tatachemicals/TC",
"https://www.moneycontrol.com/india/stockpricequote/telecommunications-service/tatacommunications/TC17",
"https://www.moneycontrol.com/india/stockpricequote/computers-software/tataconsultancyservices/TCS",
"https://www.moneycontrol.com/india/stockpricequote/plantations-teacoffee/tataconsumerproducts/TT",
"https://www.moneycontrol.com/india/stockpricequote/auto-lcvshcvs/tatamotors/TM03",
"https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/thetatapowercompany/TPC",
"https://www.moneycontrol.com/india/stockpricequote/ironsteel/tatasteel/TIS",
"https://www.moneycontrol.com/india/stockpricequote/computers-software/techmahindra/TM4",
"https://www.moneycontrol.com/india/stockpricequote/cement-major/theramcocements/MC",
"https://www.moneycontrol.com/india/stockpricequote/miscellaneous/titancompany/TI01",
"https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/torrentpharmaceuticals/TP06",
"https://www.moneycontrol.com/india/stockpricequote/retail/trent/T04",



"https://www.moneycontrol.com/india/stockpricequote/chemicals/upl/UP04",
"https://www.moneycontrol.com/india/stockpricequote/cement-major/ultratechcement/UTC01",
"https://www.moneycontrol.com/india/stockpricequote/breweriesdistilleries/unitedbreweries/UB02",



"https://www.moneycontrol.com/india/stockpricequote/miningminerals/vedanta/SG",
"https://www.moneycontrol.com/india/stockpricequote/telecommunication-service-provider/vodafoneidea/IC8",
"https://www.moneycontrol.com/india/stockpricequote/diversified/voltas/V",



"https://www.moneycontrol.com/india/stockpricequote/computers-software/wipro/W",



"https://www.moneycontrol.com/india/stockpricequote/zyduslife/zyduslifesciences/CHC"
# Add more URLs as needed
]

# Get the current date and time
current_date_time = datetime.now().strftime("%d %B %Y - %I-%M %p")

# Specify the directory where the CSV file will be saved
save_directory = r"C:\Users\Meet\Programming\Back-End\Python\Money Control Data"

# Ensure the directory exists
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Create a new file name with the current timestamp
new_file_path = os.path.join(save_directory, f"stock_data_{current_date_time}.csv")

# Write the stock data to a new CSV file
try:
    with open(new_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stock Name", "Live Price", "Day's Low", "Day's High"])

        # Use ThreadPoolExecutor for concurrent fetching
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Map each URL to a future but preserve the order of URLs
            futures = [executor.submit(fetch_stock_data, url) for url in urls]

            # Iterate over futures in the order of submission (urls order)
            for future in futures:
                try:
                    result = future.result()
                    if isinstance(result, tuple):
                        writer.writerow(result)
                        print(f"Fetched data: {result}")
                    else:
                        print(result)  # Print the error message
                except Exception as e:
                    print(f"Error processing: {e}")

    print(f"Stock data saved to {new_file_path}")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")