# Extension for 3D Slicer to Analyze Line Intensity Profile of Medical Images

# Abstract

This repository consists of Line intensity profile extension build for slicer software as a requirement to fulfill Medical Image Processing module (University of Moratuwa).  The line intensity profile provides the plot of intensity levels of pixels in the drawn line, which can be used to compare anatomical structures and noise levels of multiple images. The following slicer extension is capable of plotting line intensity profiles of a drawn line in 2 given 3D images and visualize the results. 

A sample of the Line Intensity Profile extension in 3D Slicer:

![                                                    A sample of the Line Intensity Profile extension in 3D Slicer](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/trailer_image.png)

                                                    

Line intensity profiles of two 3D MRI Brain images was plotted in axial, sagittal and coronal planes. The results are as follows:

**Axial:**

![sample1_axial.PNG](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/sample1_axial.png)

**Sagittal:** 

![sagittal.PNG](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/sagittal.png)

**Coronal:**

![coronal.PNG](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/coronal.png)

# **Getting Started**

## **Requirements**

1. **Python**
2. **3D Slicer Software**
    
    3D Slicer is a free, open source and multi-platform software package widely used for medical, biomedical, and related imaging research. Slicer is created for the purpose of subject specific image analysis and visualization. The software can be downloaded from [slicer.org](https://www.slicer.org/). 
    

## Instructions

1. **Load Sample Data** 
    
    The **Sample data** module can be found using **Module finder** in 3D Slicer.  (Own data can also be loaded for testing)
    
    Module Finder → Sample data → Select any two built-in data
    
    ![Module finder.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/Module_finder.png)
    
    Any sample images provided by slicer can be selected for line intensity analysis.
    
    ![Sample_Data.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/Sample_Data.png)
    
2. **Load Line Intensity Profile Extension**
    
    The Line Intensity Profile can be loaded as follows:
    
    Modules → Examples → Line Intensity Profile
    
     
    
    ![Examples_LIP.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/Examples_LIP.png)
    

The User interface of the Line Intensity Profile widget as follows:

    ![widget.PNG](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/widget.png)

3. **Reload and Test**
    
    Click **“Reload and Test”** button in the widget to load and test the functionality of line intensity profile. Here, the functionality is correct, if two samples volumes are loaded and a ruler is placed on a given predefined position. The outcome should be as given below:
    
    ![reload_and_test.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/reload_and_test.png)
    
4. **Select the correct volume nodes and then the ruler can be selected from the toolbar**
    
    
    ![ruler.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/ruler.png)
    
5. **Acquire Line Intensity Profiles**
    
    Place the ruler on any one of the loaded image and draw a line across the Region of Interest as shown before to acquire Line Intensity Profiles.  (Example given below)
    
    ![Ruler_placement.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/Ruler_placement.png)
    
     
    
    The Corresponding Line Intensity Profile:
    
    ![LIP.png](Extension%20for%203D%20Slicer%20to%20Analyze%20Line%20Intensity/LIP.png)
    
    Hope you enjoyed it. Happy exploring!
    
    # Acknowledgment
    
    I would like to express my gratitude towards Dr. Nuwan Dayananda, Dr. Ranga Rodrigo and Mr. Achintha Iroshan, for introducing us to 3D Slicer software and enabling us to develop line intensity profile extension using slicer. 
    
    # Reference
    
    [Developing and contributing extensions for 3D Slicer](https://docs.google.com/presentation/d/1JXIfs0rAM7DwZAho57Jqz14MRn2BIMrjB17Uj_7Yztc/htmlpresent)
    
    by: Andrey Fedorov, Jean-Christophe Fillion-Robin and Steve Pieper.
    
    Brigham and Women’s Hospital/Harvard Medical School, Kitware Inc., Isomics Inc.
