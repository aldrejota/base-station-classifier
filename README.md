# Detecting Base Transceiver Stations on Satellite Images using Deep Convolutional Neural Networks

The goal of this study is to verify locations of base transceiver stations (BTS) in a particular region by utilizing a deep neural network with which to classify geo-referenced image tiles for presence or non-presence of BTS.

This codebase (in Python 3.6) allows the reader to replicate the results of this study.

For bug reports, please email *Aldre Jota* at aldrejota[at]gmail.com.

## Neural Network Model

Download trained model [here](http://www.lipsum.com/).
![Training and Validation Accuracy Plot](https://github.com/aldrejota/base-station-classifier/blob/master/notebooks/figures/accuracy.png)

The architecture of the neural network is similar to the **base layers of VGG16\* (Simonyan & Zisserman, 2014) topped with a single 256-node fully-connected layer regularized with 50% dropout**.

Optimized using stochastic gradient descent with 0.0001 learning rate and 0.9 momentum.

\*Simonyan & Zisserman, 2014, Very Deep Convolutional Networks for Large-Scale Image Recognition [[Arxiv]](https://arxiv.org/abs/1409.1556)

## Instructions for Generating Training Data

1. Generate an API key for [Google Static Maps API](https://developers.google.com/maps/documentation/static-maps/) (free). 
2. Select areas of interest in OpenStreetMap (OSM) and create a file listing the area boundary IDs delimited by new line. Note: keep the boundaries small for faster searches; no continent-level boundaries.
3. Install required Python packages:
	```
	pip install -r requirements.txt
	```
4. Run the scripts **scrape_bts.py** and **scrape_non-bts.py** with inputs from (1) and (2) .
	* The scripts locate coordinates in OSM with tags for BTS (communication towers, mobile communications) and Non-BTS (highways, residential lands, bridges, parking spaces, natural water, etc). 
	* Then, the scripts download image tiles from Google Static Maps specified by the latitude and longitude coordinates to the **data/bts_images/*[area]*** directory.
4. **Important**: Manually filter images for inconsistencies and mistags.

## Instructions for Building Classifier

1. Check out the application examples from the [Keras](https://keras.io/applications/) website.
2. Download the **keras_model.json** from this repository to recreate the architecture.
```
json_model = open('keras_model.json', 'r').read()
BTS_model = model_from_json(json_model)
```
