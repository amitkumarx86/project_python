
# coding: utf-8

# <h1>Question 1</h1>

# In[41]:

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth,KMeans
import os
from skimage import io
import matplotlib.pyplot as plt

def imagePreprocessing(img):
    
    
    image = np.array(img)
    # reshape
    flat_image = np.reshape(image, [-1,3])
    return flat_image

def meanShift(flat_image):
    # Estimate Bandwidth
    bandwidth = estimate_bandwidth(flat_image, quantile = 0.2, n_samples=500)
    ms = MeanShift(bandwidth, bin_seeding=True)
    ms.fit(flat_image)
    labels = ms.labels_
    return ms.labels_, ms.cluster_centers_


    
def kmeans(flat_image, n_clusters=3):
    km = KMeans(n_clusters)
    km.fit(flat_image)
#     print (km.labels_)
    return km.labels_, km.cluster_centers_

def postProcessImage(labels, kmcenters,w, h):
    shape = []
    shape.append(w)
    shape.append(h)
    
    return np.reshape(labels,shape)

def plotImage(imgList):
    for i in range(len(imgList)):
        plt.subplot(1,len(imgList),i+1),
        plt.imshow(imgList[i])
        plt.axis('off')
    plt.show()
    
def callMainFunction(imgNamedict):
    for file, g_truth in imgNamedict.items():
        img = io.imread(file)
        w, h, r = img.shape    
        # print (shape)
        preProcessImage = imagePreprocessing(img)    

        # kmean 
        kmlabels, kmcenters = kmeans(preProcessImage,5)
        kmShiftedImage = postProcessImage(kmlabels, kmcenters,w, h)

        # mean shift
        mslabels, mscenters = meanShift(preProcessImage)
        meansShiftedImage = postProcessImage(mslabels, mscenters,w, h)

        imagelist = []
        imagelist.append(img)
        imagelist.append(kmShiftedImage)
        imagelist.append(meansShiftedImage)
        imagelist.append(io.imread(g_truth))
        
        # call plot image function, input is list of images
        plotImage(imagelist)

if __name__=="__main__":
    
    imgNamedict = dict()
    
    imgNamedict['a.jpg'] = 'a_truth.jpg'
    imgNamedict['b.jpg'] = 'b_truth.jpg'
    imgNamedict['c.jpg'] = 'c_truth.jpg'
    imgNamedict['d.jpg'] = 'd_truth.jpg'
    imgNamedict['e.jpg'] = 'e_truth.jpg'
    
    callMainFunction(imgNamedict)
    


# In[ ]:



