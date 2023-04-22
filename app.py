import os
from helpers import apology
import csv 
import sys
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

    list_of_fields = [1,2,3,4,5]
    
    return render_template("index.html", fields = list_of_fields)

@app.route("/calculated", methods=["GET", "POST"])
def calculation():

    list_of_fields = [1,2,3,4,5]

    # Post = Calculate Button is pressed

    if request.method == "POST":
        # Check for input errors

        if not request.form.get("span"):
            return apology("Please enter a value for span!")
        elif not request.form.get("fields"):
            return apology("Please select a number of spans!")
        elif not request.form.get("load"):
            return apology("Please enter a load value!")

        n = int(request.form.get("fields")) # number of fields selected by the user (1-5)
        length = request.form.get("span") # span in meters
        l = float(length.replace(",", "."))
        load = request.form.get("load") # constant line-load in kN/m
        q = float(load.replace(",", "."))
        
        momentfactorsData = []

        with open("momentfactors.csv") as momentfactorFile:
            momentfactorsData = csv.reader(momentfactorFile)
            momentfactors = list(momentfactorsData)
        
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
        M1 = 0
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
            M1 = (q * l**2)/8   # Bending - Moment in middle of field in kNm
            outlineImageLink = ".\static\images\schemeimage_einfeldträger.png"
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

        # list of moments
        moments = []
        #if n == 1:
           # moments = [0.0, M1, 0.0]
        #elif n == 2:
           # moments = [0.0, M1, Mb, M1, 0.0]
           # outlineImageLink = ".\static\images\schemeimage_zweifeldträger.png"
        #elif n == 3:
           # moments = [0.0, M1, Mb, M2, Mb, M1, 0.0]
          #  outlineImageLink = ".\static\images\schemeimage_dreifeldträger.png"
        #elif n == 4:
           # moments = [0.0, M1, Mb, M2, Mc, M2, Mb, M1, 0.0]
           # outlineImageLink = ".\static\images\schemeimage_vierfeldträger.png"
        #elif n == 5:
           # moments = [0.0, M1, Mb, M2, Mc, M3, Mc, M2, Mb, M1, 0.0]
           # outlineImageLink = ".\static\images\schemeimage_fünffeldträger.png"
        
        #list of shear forces
        shearForces = []
        if n == 1:
            shearForces = [A, -A]
            outlineImageLink = ".\static\images\schemeimage_einfeldträger.png"
        elif n == 2:
            shearForces = [A, Vbl, -Vbl, -A] # two values at one x-location!!! 
            outlineImageLink = ".\static\images\schemeimage_zweifeldträger.png"
        elif n == 3:
            shearForces = [A, Vbl, Vbr, Vbl, Vbr, -A]
            outlineImageLink = ".\static\images\schemeimage_dreifeldträger.png"
        elif n == 4:
            shearForces = [A, Vbl, Vbr, Vcl, Vcr, Vbl, Vbr, -A]
            outlineImageLink = ".\static\images\schemeimage_vierfeldträger.png"
        elif n == 5:
            shearForces = [A, Vbl, Vbr, Vcl, Vcr, Vcl, Vcr, Vbl, Vbr, -A]
            outlineImageLink = ".\static\images\schemeimage_fünffeldträger.png"
                        
        #List for x-locations
        x_location = []

        for i in range(n * 2 + 1):
            x = i/2 * l
            x_location.append(x)

        for x in x_location: 
            M = A * x - (q * x**2)/2
            moments.append(M)

        x_locationV = []

        for i in range(n + 1):
            x = i * l
            x_locationV.append(x)
            if i != 0 and i != n:
                x_locationV.append(x)
        
        #print(x_locationV)
        
        csv_results = [M1, M2, M3, Mb, Mc, A, B, C, Vbl, Vbr, Vcl, Vcr]

        #Plot graph My:
        PlotMoments(x_location, moments)
        plt.close()

        #Plot graph V:
        PlotShearForces(x_locationV, shearForces)
        plt.close()

        with open(".\\static\\results.csv", "w") as r:
            writer = csv.writer(r)
            writer.writerow('M1, M2, M3, Mb, Mc, A, B, C, Vbl, Vbr, Vcl, Vcr')
            writer.writerow(csv_results)
        
        #web = QWebView()
        #web.load(QUrl("http://127.0.0.1:5000/calculated"))
        #printer = QPrinter()
        #printer.setPageSize(QPrinter.A4)
        #printer.setOutputFormat(QPrinter.PdfFormat)
        #printer.setOutputFileName("results.pdf")

        #outlineImageLink = ".\static\images\schemeimage_zweifeldträger.png"
        
        return render_template("calculated.html", span = l, load = q, fields = n, Vbl = Vbl, Vbr = Vbr, Vcl = Vcl, Vcr = Vcr, M1 = M1, M2 = M2, M3 = M3, Mb = Mb, Mc = Mc, A = A, B = B, C = C, moments = ".\static\images\moments.png", shearForces = ".\static\images\shearForces.png", outlineImage = outlineImageLink)
        
        
    else:
        return render_template("index.html")

def PlotMoments(x_location, moments):
    plt.plot(x_location, moments)
    return plt.savefig(".\static\images\moments.png")

def PlotShearForces(x_locationV, shearForces):
    plt.plot(x_locationV, shearForces)
    return plt.savefig(".\static\images\shearForces.png")
    





