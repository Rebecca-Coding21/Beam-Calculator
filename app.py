import os
from helpers import apology
import csv 
import sys
from zipfile import ZipFile
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from flask import Flask, redirect, render_template, flash, request
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWebKit import *

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods = ["GET", "POST"])
def index():

    list_of_fields = [2,3,4,5]
    index = 0
    
    return render_template("index.html", index = index, fields = list_of_fields)

@app.route("/calculated", methods=["GET", "POST"])
def calculation():
    
    list_of_fields = [2,3,4,5]

    if request.method == "POST":
        
        # Check for input errors
        index = 0

        if not request.form.get("fields"):
            return render_template("index.html", index = 1, fields = list_of_fields)
        elif not request.form.get("span"):
            return render_template("index.html", index = 2, fields = list_of_fields)
        elif not request.form.get("load"):
            return render_template("index.html", index = 3, fields = list_of_fields)

        #get variables from user-input
        n = int(request.form.get("fields")) # number of fields selected by the user (1-5)
        length = request.form.get("span") # span in meters
        l = float(length.replace(",", "."))
        load = request.form.get("load") # constant line-load in kN/m
        q = float(load.replace(",", "."))
        
        #get moment factors for calculation from csv-file
        momentfactorsData = []

        with open("momentfactors.csv") as momentfactorFile:
            momentfactorsData = csv.reader(momentfactorFile)
            momentfactors = list(momentfactorsData)
        
        #define factors for calculation
        m1_factor = float(momentfactors[n][1])
        m2_factor = float(momentfactors[n][2])
        m3_factor = float(momentfactors[n][3])
        mb_factor = float(momentfactors[n][4])
        mc_factor = float(momentfactors[n][5])
        A_factor = float(momentfactors[n][6])
        B_factor = float(momentfactors[n][7])
        C_factor = float(momentfactors[n][8])
        Vbl_factor = float(momentfactors[n][9])
        Vbr_factor = float(momentfactors[n][10])     
        Vcl_factor = float(momentfactors[n][11])  
        Vcr_factor = float(momentfactors[n][12])            
        M1 = 0.0
        M2 = 0.0
        M3 = 0.0
        Mb = 0.0
        Mc = 0.0
        A = 0.0
        B = 0.0
        C = 0.0
        Vbl = 0.0
        Vbr = 0.0
        Vcl = 0.0
        Vcr = 0.0

        if n == 1:
            Vbl = (q * l)/2     # Shear Force at both supports in kN
            M1 = float((q * l**2)/8 )  # Bending - Moment in middle of field in kNm
        else:
            M1 = round(m1_factor * q * l**2,2)
            M2 = round(m2_factor * q * l**2,2)
            M3 = round(m3_factor * q * l**2,2)
            Mb = round(mb_factor * q * l**2,2)
            Mc = round(mc_factor * q * l**2,2)
            A = round(A_factor * q * l,2)
            B = round(B_factor * q * l,2)
            C = round(C_factor * q * l,2)
            Vbl = round(Vbl_factor * q * l,2)
            Vbr = round(Vbr_factor * q * l,2)
            Vcl = round(Vcl_factor * q * l,2)
            Vcr = round(Vcr_factor * q * l,2)
        
        #list of shear forces
        shearForces = []
       # if n == 1:
            #shearForces = [A, -A, 0]
            #outlineImageLink = ".\static\images\schemeimage_einfeldträger.png"
        if n == 2:
            shearForces = [A, Vbl, -Vbl, -A, 0] # two values at one x-location!!! 
            outlineImageLink = ".\static\images\schemeimage_zweifeldträger.png"
            shearForces_minima = ['Vbl', 'A']
            shearForces_maxima = ['-Vbl']
        elif n == 3:
            shearForces = [A, Vbl, Vbr, Vbl, Vbr, -A, 0]
            outlineImageLink = ".\static\images\schemeimage_dreifeldträger.png"
            shearForces_minima = ['Vbl', 'Vbl', 'A']
            shearForces_maxima = ['Vbr', 'Vbr']
        elif n == 4:
            shearForces = [A, Vbl, Vbr, Vcl, Vcr, Vbl, Vbr, -A, 0]
            outlineImageLink = ".\static\images\schemeimage_vierfeldträger.png"
            shearForces_minima = ['Vbl', 'Vcl', 'Vbl', 'A']
            shearForces_maxima = ['Vbr', 'Vcl', 'Vbr']
        elif n == 5:
            shearForces = [A, Vbl, Vbr, Vcl, Vcr, Vcl, Vcr, Vbl, Vbr, -A, 0]
            outlineImageLink = ".\static\images\schemeimage_fünffeldträger.png"
            shearForces_minima = ['Vbl', 'Vcl', 'Vcl', 'Vbl', 'A']
            shearForces_maxima = ['Vbr', 'Vcl', 'Vcl', 'Vbr']
                
        # x-locations for shear forces (because of 2 values at the supports)
        x_locationV = []

        for i in range(n + 1):
            x_loc = i * l
            x_locationV.append(x_loc)

            if(x_loc != 0):
                x_locationV.append(x_loc)      

         #Plot graph V:
        ax = plt.gca()
        ax.invert_yaxis()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['left'].set_position(('data', 0))
        #PlotShearForces(x_locationV, shearForces)
        
        # Call the function to find minima and maxima
        minima_V, maxima_V = find_extrema(shearForces)
        
        # Plot these points
        for i, min_str in zip(minima_V, shearForces_minima):
            plt.annotate(min_str, (x_locationV[i], shearForces[i]), textcoords="offset points", xytext=(0,10), ha='center')

        for i, max_str in zip(maxima_V, shearForces_maxima):
            plt.annotate(max_str, (x_locationV[i], shearForces[i]), textcoords="offset points", xytext=(0,-15), ha='center')
        
        plt.plot(x_locationV, shearForces)
        plt.xticks(np.arange(0, max(x_locationV) + 1, l/2))
        plt.savefig(".\\static\\images\\results\\shearForces.png")
        plt.close()

        #find minima for moments
        if(n == 2):
            moments_minima = ['Mb']
            moments_maxima = ['M1', 'M1']
        elif(n == 3):
            moments_minima = ['Mb', 'Mb']
            moments_maxima = ['M1', 'M2', 'M1']
        elif(n == 4):
            moments_minima = ['Mb', 'Mc', 'Mb']
            moments_maxima = ['M1', 'M2', 'M2', 'M1']
        elif(n == 5):
            moments_minima = ['Mb', 'Mc', 'Mc', 'Mb']
            moments_maxima = ['M1', 'M2', 'M3', 'M2', 'M1']
            
        #Plot graph My:
        #PlotMoments(x, moments)

        x = np.arange(0, (n * l) + 1, 0.1)
        
        y = np.piecewise(x,[x <= l, (x > l) & (x <= 2 * l), (x > 2 * l) & (x <= 3 * l), (x > 3 * l) & (x <= 4 * l), (x > 4 * l) & (x <= 5 * l)], [lambda x: f1(x, mb_factor, m1_factor, q, l, n), lambda x: f2(x,mb_factor, m1_factor, m2_factor, mc_factor, q, l, n), lambda x: f3(x, mb_factor, m1_factor, m2_factor, m3_factor, mc_factor, q, l, n), lambda x: f4(x, mb_factor, m1_factor, m2_factor, mc_factor, q, l, n), lambda x: f5(x, mb_factor, m1_factor, q, l, n)])
        ax = plt.gca()
        ax.invert_yaxis()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['left'].set_position(('data', 0))

        plt.plot(x, y)
        
        # Set x-axis labels every l/2
        plt.xticks(np.arange(0, max(x), l/2))
      #  plt.xticks(range(1,10), x)

        
        # Call the function to find minima and maxima
        minima, maxima = find_extrema(y)

        # Plot these points
        for i, min_str in zip(minima, moments_minima):
            plt.annotate(min_str, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

        for i, max_str in zip(maxima, moments_maxima):
            plt.annotate(max_str, (x[i], y[i]), textcoords="offset points", xytext=(0,-15), ha='center')
            #plt.annotate(str(round(y[i], 2)), (x[i], y[i]), textcoords="offset points", xytext=(0,-15), ha='center')

        plt.savefig(".\\static\\images\\results\\moments.png")
        plt.close()    

        #create csv-file for results
        csv_results = [M1, M2, M3, Mb, Mc, A, B, C, Vbl, Vbr, Vcl, Vcr]   

        with open(".\\static\\results.csv", "w") as r:
            writer = csv.writer(r)
            writer.writerow('M1, M2, M3, Mb, Mc, A, B, C, Vbl, Vbr, Vcl, Vcr')
            writer.writerow(csv_results)
        
        #create zip-file for diagrams
        with ZipFile('.\\static\\images\\results.zip', 'w') as zip_object:
            zip_object.write('.\\static\\images\\results\\moments.png')
            zip_object.write('.\\static\\images\\results\\shearForces.png')
        
        return render_template("calculated.html", span = l, load = q, fields = n, Vbl = Vbl, Vbr = Vbr, Vcl = Vcl, Vcr = Vcr, M1 = M1, M2 = M2, M3 = M3, Mb = Mb, Mc = Mc, A = A, B = B, C = C, moments = ".\\static\\images\\results\\moments.png", shearForces = ".\\static\\images\\results\\shearForces.png", outlineImage = outlineImageLink)
        
        
    else:
        return render_template("index.html")

#def PlotMoments(x_location, moments):
 #   plt.plot(x_location, moments)
  #  return plt.savefig(".\\static\\images\\results\\moments.png")

#def PlotShearForces(x_locationV, shearForces):
 #   plt.plot(x_locationV, shearForces)
  #  return plt.savefig(".\\static\\images\\results\\shearForces.png")
    
def find_extrema(y_data):
    minima = [i for i in range(1, len(y_data)-1) if y_data[i-1] > y_data[i] < y_data[i+1]]
    maxima = [i for i in range(1, len(y_data)-1) if y_data[i-1] < y_data[i] > y_data[i+1]]
    return minima, maxima    

def f1(x, mb_factor, m1_factor, q, l, n):
    if n == 1:
        return q * (l**2) / 8
    else:
        return ((5/3) * mb_factor * q - (25/6) * m1_factor * q) * x**2 + (-(2/3) * mb_factor * q * l + (25/6) * m1_factor * q * l) * x

def f2(x, mb_factor, m1_factor, m2_factor, mc_factor, q, l, n):
    x = x - l
    if n == 2:
        return ((5/3) * mb_factor * q - (25/6) * m1_factor * q) * x**2 + (-(8/3) * mb_factor * q * l + (25/6) * m1_factor * q * l) * x + mb_factor * q * l**2
    elif n == 3:
        return (4 * mb_factor * q - 4 * m2_factor * q) * x**2 + (-4 * mb_factor * q * l + 4 * m2_factor * q * l) * x + mb_factor * q * l**2
    elif n == 4 or n == 5:
        return (2 * mb_factor * q + 2 * mc_factor * q - 4 * m2_factor * q) * x**2 + (-3 * mb_factor * q *l - mc_factor * q* l + 4 * m2_factor * q * l) * x + mb_factor * q * l**2

def f3(x, mb_factor, m1_factor, m2_factor, m3_factor, mc_factor, q, l, n):
    x = x - (2 * l)
    if n == 3:
        return ((5/3) * mb_factor * q - (25/6) * m1_factor * q) * x**2 + (-(8/3) * mb_factor * q * l + (25/6) * m1_factor * q * l) * x + mb_factor * q * l**2   
    elif n == 4: 
        return (2 * mc_factor * q + 2 * mb_factor * q- 4 * m2_factor * q) * x**2 + (-3 * mc_factor * q * l - mb_factor * q * l + 4 * m2_factor * q * l) * x + mc_factor * q * l**2
    elif n == 5:
        return (4 * mc_factor * q - 4 * m3_factor * q) * x**2 + (- 4 * mc_factor * q *l + 4 * m3_factor * q * l) * x + mc_factor * q * l**2

def f4(x, mb_factor, m1_factor, m2_factor, mc_factor, q, l, n):
    x = x - (3 * l)
    if n == 4:
        return ((5/3) * mb_factor * q - (25/6) * m1_factor * q) * x**2 + (-(8/3) * mb_factor * q * l + (25/6) * m1_factor * q * l) * x + mb_factor * q * l**2
    elif n == 5:
        return (2 * mb_factor * q + 2 * mc_factor * q - 4 * m2_factor * q) * x**2 + (-3 * mc_factor * q *l - mb_factor * q* l + 4 * m2_factor * q * l) * x + mc_factor * q * l**2
    
def f5(x, mb_factor, m1_factor, q, l, n):
    x = x - (4 * l)
    if n == 5:
        return ((5/3) * mb_factor * q - (25/6) * m1_factor * q) * x**2 + (-(8/3) * mb_factor * q * l + (25/6) * m1_factor * q * l) * x + mb_factor * q * l**2


