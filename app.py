import os

from flask import Flask, redirect, render_template, flash, request

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

        #if not request.form.get("span"):
           # return apology()
        #elif not request.form.get("fields"):
           # return apology()
        #elif not request.form.get("load"):
            #return apology()

        n = request.form.get("fields")      # number of fields selected by the user (1-5)
        l = float(request.form.get("span")) # pan in meters
        q = float(request.form.get("load")) # constant line-load in kN/m

        #if amountOfFields == 1:
        shearForce = (q * l)/2              # Shear Force at both supports in kN
        bendingMomentField = (q * l**2)/8   # Bending - Moment in middle of field in kNm
        #else:
            #shearForce

        return render_template("calculated.html", span = l, load = q, fields = n, shearForce = shearForce, bendingMomentField = bendingMomentField)

    else:
        return render_template("index.html")

