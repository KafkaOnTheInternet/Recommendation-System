import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask import Flask, redirect, url_for, request

excel_file = "/home/arjun/Desktop/flask_proj/movies1.xlsx"
df = pd.read_excel(excel_file, sheet_name="movies")
flag = 0

name = df["movie_title"]
genre = df["genres"]
actor1 = df["actor_1_name"]
actor2 = df["actor_2_name"]

print("Welcome to the data set viewer")
print("Please input the movie you'd like")

movie = input()
def checker(movie):
    max, index = 0, 0
    for i in range(len(name)):
        if fuzz.partial_ratio(movie, name[i]) > max:
            max = fuzz.partial_ratio(movie, name[i])
            index = i
        else:
            continue
    if max == 100:
        print("Movie found! Here is it's index and genre")
        print(name[index] + "\t" + genre[index])
    elif max < 40:
        print("We couldn't find your movie, maybe it isnt in the data set")
    else:
        print("Is this the movie you were looking for?")
        print(name[index] + "\t" + genre[index] + "\t" + actor1[index] + "\t" + actor2[index])
    print("We thought you'd be interested in these movies too")
    max, newIndex, i = 0, 0, 0
    for i in range(len(actor1)):
        if i == index:
            continue
        elif ((fuzz.token_set_ratio(actor1[i], actor1[index]) + fuzz.token_set_ratio(actor2[i], actor2[index]))/2) > max:
            max = (fuzz.token_set_ratio(actor1[i], actor1[index]) + fuzz.token_set_ratio(actor2[i], actor2[index]))/2
            newIndex = i

    if max < 70:
        print("We couldn't match any of the lead actors")
    else:
        print(max)
        print("On the basis of of the lead actors, we thought you might like")
        print(name[newIndex] + "\t" + genre[newIndex] + "\t" + actor1[newIndex] + actor2[newIndex])
        #Because of genres
    max, newerIndex, i = 0, 0, 0
    for i in range(len(actor1)):
        if i == index:
            continue
        elif fuzz.token_set_ratio(genre[i], genre[index]) > max:
            newerIndex = i
            max = fuzz.token_set_ratio(genre[i], genre[index])

    if max < 50:
        print("We couldn't match any movie based on genre")
    else:
        print("On the basis of of the lead actors, we thought you might like")
        print(name[newerIndex] + "\t" + genre[newerIndex])
    return index, newIndex, newerIndex

index, newIndex, newerIndex = checker(movie)
