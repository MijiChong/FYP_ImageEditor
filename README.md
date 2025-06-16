# FYP_ImageEditor

#Purpose#

This is for Year 3 Final Year Project purpose. All editors and models are workable on each type of images. The calculation models is for image quality evaluation and table result comparison.

#Reminder# 

Please activate virtual environment before use the code:

--> quality\Scripts\activate

#The datasets are all getting from ChartQA: https://github.com/vis-nlp/ChartQA.git

================================================================

# Image Editors

Color_bgr.py --> Remove Image Background

Color.py --> Edit Image Color Depth

colorCal.py --> Calculate Image Color Depth

gaussianB.py --> Image Gaussian Blur Editor

ImpNoise.py --> Image Impulse Noise Editor

blur.py --> Compare and Visualize Types of Blur

overlay.py --> Image Overlay

ratioRsz.py --> Resize Image Pixels based on Ratio

resize.py --> Resize Image Pixels

=================================================================

# Image and Results Calculators

percent.py --> Calculate RMSE & Percentage Difference of RMSE (using Mean)

psnr.py --> Calculate PSNR & SSIM

qualityTest.py --> Calculate Image Quality 

=================================================================

# Image Order 

For dataset-Blur & Noise --> order.csv

For dataset - Pixel & Color --> newOrder.csv

================================================================

# Files Rename

R.py --> Add 'R' behind original file name

noR.py --> Remove 'R' behind original file name 
