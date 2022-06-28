#import requests
#import cv2
import numpy as np
from numpy import genfromtxt
import multiprocess as mp

# Function for reading .csv file
def read_file(filepath):
    data = genfromtxt(filepath, delimiter=',', filling_values = '0', skip_header = 1, dtype=str)
    return data


def white_row(row):
    import requests
    import cv2
    import numpy as np
    import multiprocess as mp

    # url picture conversion to jpg
    def jpg_creator(url, image_name = 'last_photo.jpg'):
        with open(image_name, 'wb') as f:
            f.write(requests.get(url, headers={"User-Agent": "XY"}).content)
        return

    # function for searching if the white background is present
    def find_white_background(imgpath='last_photo.jpg', threshold=0.3):
        # reads picture
        imgArr = cv2.imread(imgpath)
        background = np.array([255, 255, 255])
        # how much of the picture is white (255,255,255) (RGB)
        percent = (imgArr == background).sum() / imgArr.size
        # Very likely a white background
        if percent >= threshold:
            return "yes"
        # Likely a white background (should check)
        elif (percent < threshold) & (percent > 0.05):
            return str(round(percent,2))
        # Unlikely a white background
        else:
            return "no"

    sku = row[0]
    # How many links + 1
    n_links = np.size(row)
    iter = np.arange(1, n_links) # automatically -1 for sku
    name = str(mp.current_process()._identity) # custom name for each core (prevents crashing)
    for index in iter:
        jpg_creator(row[index],name)
        is_white = find_white_background(name)
        if is_white == "yes":
            return row
        elif is_white == "no":
            print("SKU: {}.\tUnlikely white bacground. White < 5 %".format(sku))
            return #prideti ieskojima naujo white background foto
        else:
            print("SKU: {}.\tWhite % = {}. Did not swap.".format(sku,is_white))
            return row
    #return #cia turi returninti eilute atnaujinta

#programos aktyvacijos salyga
if __name__ == '__main__':
    df = read_file('links2.csv')
    ncores = mp.cpu_count() # number of cores in pc
    pool = mp.Pool(processes=ncores)

    m1 = pool.map(white_row, df)#kiekvienas branduolys gaus po porcija
    print(m1)
    pool.close()
    pool.join()



# Test failai
#url_baltas = 'https://lexorahome.com/wp-content/uploads/2022/02/LD342248SAWQ000_2-scaled.jpg'
#url_pilkas = 'https://lexorahome.com/wp-content/uploads/2022/02/LD342248SAWQ000_1-scaled.jpg'
#url_mazaibalto = 'https://lexorahome.com/wp-content/uploads/2022/02/LD342284DBWQ000_2-scaled.jpg'

#url_kilimai = 'https://suryas1.blob.core.windows.net/productimages/Throws/AAR-1000/512x512/aar1000-5060.jpg'

# LIKO PADARYTI:
# - Padaryti, kad funkcija white_row() visada grazintu galutine sku ir linku eilute
# - Sujungti white_row() grazinamas eilutes i bendra masyva, padaryti .csv faila
# - Sutvarkyti skaityma nuo direktorijos kad veiktu su .py failu, ne sln
# - Sukurti .exe faila

# PAPILDOMAI:
# - Klausimas del apatines (5%) ribos keitimo (rankiniu budu ivesti)