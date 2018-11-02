import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask import Flask, redirect, url_for, request, render_template

excel_file = "/home/arjun/Desktop/flask_proj/movies1.xlsx"
df = pd.read_excel(excel_file, sheet_name="movies")
flag = 0

name = df["movie_title"]
genre = df["genres"]
actor1 = df["actor_1_name"]
actor2 = df["actor_2_name"]

def checker(movie):
    max, index = 0, 0
    for i in range(len(name)):
        if fuzz.partial_ratio(movie, name[i]) > max:
            max = fuzz.partial_ratio(movie, name[i])
            index = i
        else:
            continue
    max, newIndex, i = 0, 0, 0
    for i in range(len(actor1)):
        if i == index:
            continue
        elif ((fuzz.token_set_ratio(actor1[i], actor1[index]) + fuzz.token_set_ratio(actor2[i], actor2[index]))/2) > max:
            max = (fuzz.token_set_ratio(actor1[i], actor1[index]) + fuzz.token_set_ratio(actor2[i], actor2[index]))/2
            newIndex = i

        #Because of genres
    max, newerIndex, i = 0, 0, 0
    for i in range(len(actor1)):
        if i == index:
            continue
        elif fuzz.token_set_ratio(genre[i], genre[index]) > max:
            newerIndex = i
            max = fuzz.token_set_ratio(genre[i], genre[index])

    return index, newIndex, newerIndex

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "GET":
        result = request.args.get("nm")
        index, newIndex, newerIndex = checker(result)
        movFinal, genFinal, act1Final = str(name[index]), str(genre[index]), str(actor1[index])
        rec1Final, rec1gen, rec1act1 = str(name[newIndex]), str(genre[newIndex]),  str(actor1[newIndex])
        rec2Final, rec2gen, rec2act1 = str(name[newerIndex]) , str(genre[newerIndex]) , str(actor1[newerIndex])
        resultDict = {
            "movie":movFinal, 
            "rec1":rec1Final, 
            "rec2":rec2Final, 
            "movieGen": genFinal,
            "movieAct1": act1Final,
            "rec1gen": rec1gen,
            "rec2gen": rec2gen,
            "rec1act1": rec1act1,
            "rec2act1": rec2act1,
            "index":index, 
            "newIndex":newIndex, 
            "newerIndex": newerIndex
            }
        return render_template("result.html", result = resultDict)

if __name__ == "__main__":
    app.run(debug = True)