import numpy as np
import requests
from PIL import Image
from scipy import misc
from io import BytesIO


# Defaul Parameters
IMG_SIZE = 250
ZOOM_DEFAULT = 20
SCALE_DEFAULT = 1

def SaveMapFromLatLon(lat, lon, API_key, path, 
                        size = (IMG_SIZE, IMG_SIZE),
                        zoom = ZOOM_DEFAULT,
                        scale = SCALE_DEFAULT):
    """
    Function
    --------
    SaveMapFromLatLon

    Parameters
    ----------
    lat : float
        latitute
    lon : float
    path : string
        Path to image directory 
    filename : string
        Desired image filename
    size
    
    Returns
    -------
    None
    """
    
    h = size[0]
    w = size[1]
    
    url = 'https://maps.googleapis.com/maps/api/staticmap?center=' \
            + str(lat) + ',' + str(lon) + '&zoom=' + str(zoom) \
            + '&size=' + str(w) + 'x' + str(h+100) \
            + '&scale=' + str(scale) + '&maptype=satellite&key=' + API_key

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }            
    response = requests.get(url, headers=headers)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img_arr = np.asarray(img)
    
    if np.array_equal(img_arr[:10,:,:],img_arr[10:20,:,:]):
        print("Error! No Image at Zoom("+str(zoom)+") @ "+str(lat)+","+str(lon))
        pass
    else:
        filename = str(lat) + "," + str(lon) + ".jpg"
        cropped_image = img_arr[50:h+50, :, :]
        misc.imsave(path + filename, cropped_image)
    return None
