#EDITS:
#I. 09-08-2015. Disable time calculation and allow larger matrices.
#Additionally, perform queries exclusively on those schools within a given range
#of distance. 


#------------------------------------------------------------------------------
#Rodrigo Azuero Melo rodazuero@gmail.com
#08-10-2015
#------------------------------------------------------------------------------
#SUMMARY: In this file we will generate a csv file with the distance in car
#to travel from one school to each other school in the sample. The file needs to
#stop 10 seconds every 100 queries as it is the established limit.
#------------------------------------------------------------------------------
#PREVIOUS STEPS: Before running the following .py file it is necessary to have
#google key for the google matrix.distance API. The description of the steps are
#found in https://developers.google.com/maps/documentation/distancematrix/intro
#Once you follow those steps, you will get a key. Such key can only be used in
#a predetermined IP address. You need to store the key in the line where
#the command gmaps=Client is.
#------------------------------------------------------------------------------
#INPUTS: It is necessary to have a CSV file stored in Windows with the coordinates
#of the schools. There should be five columns. The first column includes
#only the number of the school (AMIE). The second column
#includes the Latitude. The third column includes the longitude. The
#fourth and fifth columns should include UTM coordinates. 
#The first row of the CSV file should include the names of the variables
#(Number,LAT,LON,xutm,yutm) with no quotes. Example:
#[Number, LAT, LON,xUTM,yUTM]
#[1, -4.0010175704956, -79.2003021240234,1234,5678]
#------------------------------------------------------------------------------
#OUTPUT: a CSV file containing a  matrix with distances.
#File called "distances.csv". N*N matrix with N*(N+1)/2 entries as is symmetric.
#------------------------------------------------------------------------------

#-----------------------------------------------------------------
#0. Block of package loading
#0.0. time package used to break python when 100 queries reached
import time
#0.1 csv package used to open and store csv files
import csv
#0.2 re package used to substring strings
import re
#0.3 os package used to change directory
import os
#0.4 Client package from google maps used to query distances
from googlemaps import Client
#0.5 Import numpy
import numpy as np 
#-----------------------------------------------------------------

#-----------------------------------------------------------------
#1. Change directory
os.chdir('/Users/rodrigoazuero/Documents/DATAIDB2015/Clusters/FinalFiles/Python/Cluster8')
#-----------------------------------------------------------------

#-----------------------------------------------------------------
#2. Store the API key in the following variables
gmaps=Client('AIzaSyDxbFepKJ3Jr1PrAXV2RVvtn2QDaF3jnRQ')
gmaps=Client(key='AIzaSyDxbFepKJ3Jr1PrAXV2RVvtn2QDaF3jnRQ')
#gmaps = Client('AIzaSyB0-AyNgrMrX4TV8BFEDPUyidA5Ss4vzSU')
#gmaps = Client(key='AIzaSyB0-AyNgrMrX4TV8BFEDPUyidA5Ss4vzSU')
#-----------------------------------------------------------------

#-----------------------------------------------------------------
#3. Matrix definitions for distances. We need to replace
#the values with the corresponding rank for the matrices.
drivedistance= np.empty((10000,10000), dtype=np.object)
walkdistance= np.empty((10000,10000), dtype=np.object)

#3.1 Define the threshold variable. I will compute the google maps query exclusively
#for those schools within the value of threshold
threshold=10

#-----------------------------------------------------------------

#-----------------------------------------------------------------
#4. Defining the iterators
#4.0 Iterator for number of queries
countdistance=0
#4.1 Columns
i=0
#4.2 Rows
j=0
#-----------------------------------------------------------------





#-----------------------------------------------------------------
#5. Calculating distance in a loop
#5.0 Open the 'MockDatA.csv' file.
with open('Cluster8INPUT.csv') as csvfile:
    reader=csv.reader(csvfile)
    #5.1 Iterating rows in the file. Start reading from row zero
    for row in reader:
        #5.2 We will skip the first row as it contains names of variables
        amie=row[0]
        walkdistance[i][0]=amie
        walkdistance[0][i]=amie
        i=i+1
        j=0
        if i>1:
            #5.3 Extract the coordinates from the rows. The coordinates are stored
            #as strings and we need to change it to floats.
            xcoord=float(row[1])
            ycord=float(row[2])
            xUTM1=float(row[3])
            yUTM1=float(row[4])
            print(amie)
            #5.4. Generate compound coordinate as (x,y).
            coordORIG=xcoord, ycord
            with open('Cluster8INPUT.csv') as csvfile2:
                reader2=csv.reader(csvfile2)
                #5.5 Iterating rows for the second time. Procedure repeated.
                for row2 in reader2:
                    j=j+1
                    if i<j:
                        xcoord2=float(row2[1])
                        ycoord2=float(row2[2])
                        xUTM2=float(row2[3])
                        yUTM2=float(row2[4])
                        #5.5.1 Getting the distance
                        d1=(xUTM2-xUTM1)**2
                        d2=(yUTM2-yUTM1)**2
                        d3=d1+d2
                        distance=d3**0.5
                        distance=distance/1000
                        print(distance)
                        #5.5.2. Now if the distance is below a given threshold, I will allow the computation
                        if distance<threshold:
                            coordCOMP=xcoord2, ycoord2
                            #5.6. Increase counter of distance by 1.
                            countdistance=countdistance+1
                            module10=countdistance%100
                            if module10==0:
                                #5.7. Every 100 queries we sleep for 10 seconds.
                                time.sleep(10)
                            #5.8 Walking distance.
                            algoprueba=gmaps.distance_matrix(coordORIG,coordCOMP,mode='walking')
                            #5.9 Driving distance stored in a set of dictionaries and lists.
                            #We need to extract it in seven steps.
                            algo2=algoprueba['rows']
                            algo3=algo2[0]
                            algo4=algo3['elements']
                            algo5=algo4[0]
                            status=algo5['status']
                            #5.10 If status ok, compute distance.
                            if status=='OK':
                                algo6=algo5['distance']
                                algo7=algo6['value']
                            else:
                                algo7='NA'
                                #5.10 Just to verify, it is being computed nice.
                                print(algo7)
                            #5.11 Store  distance
                            walkdistance[i-1][j-1]=algo7
                            print countdistance
                        else:
                            walkdistance[i-1][j-1]='FAR'

#-----------------------------------------------------------------
#6.Store the tables as csv
#6.0 Store the driving distance table
with open('walkdistance.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(walkdistance)

#-----------------------------------------------------------------
#7. Verify the file ran smoothly
print "Success!"
#-----------------------------------------------------------------
