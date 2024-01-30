import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gpxpy
import re
import json
from data import *
from itertools import chain

def histogr(path):
    df = pd.read_json(path)
    #print(df.head())
    #print(df["duration"].min())
    #print(df["distance"].min())

    fig, axes = plt.subplots(2, 2)
    df.hist("duration", ax=axes[0][0])
    df.hist("distance", ax=axes[0][1])
    #df.hist("finish", ax=axes[1][1])
    #df.boxplot("duration", ax=axes[1][0])
    #df.boxplot("distance", ax=axes[1][1])

    plt.show()

def distributionPlot(path):
    fig, axes = plt.subplots(1, 2)

    # group data by subgroups and sort via amount of patients in each subgroup
    data = pd.read_json(path)
    data = data[data["duration"] <= 172]
    start_pts = data.groupby("start").size().sort_values(ascending=True)
    finish_pts = data.groupby("finish").size().sort_values(ascending=True)
    print(data["start"].values)

    # create plot for start points
    distrPlot_start = start_pts.plot(kind='barh', ylabel='start points',
                                   xlabel='times it was the start point', ax=axes[0])

    distrPlot_start.bar_label(distrPlot_start.containers[0])
    distrPlot_start.spines['right'].set_visible(False)
    plt.subplots_adjust(left=0.2)

    # create plot for finish points
    distrPlot_finish = finish_pts.plot(kind='barh', ylabel='finish points',
                                     xlabel='times it was the finish point', ax=axes[1])

    distrPlot_finish.bar_label(distrPlot_finish.containers[0])
    distrPlot_finish.spines['right'].set_visible(False)
    plt.subplots_adjust(left=0.2)
    #plt.savefig('distr.png')

    drawNetworkStartEnd(path, "duration", data["start"].values, data["finish"].values)

    plt.show()

def tour_min(data, metric):
    # tourdata can consist of many solutions, therefore extract the one with min duration and min distance
    tourdata_min = {}

    for tour in data:
        if not bool(tourdata_min): # if tour is empty
            tourdata_min = tour
        elif tourdata_min.get(metric) > tour.get(metric):
            tourdata_min = tour

    tour = tourdata_min['tour']
    drawNetworkFromTour(tourdata_min["tour"], "distance")
    return tour

def drawNetwork(tourdata, metric):

    points = getWayPoints()

    # tourdata can consist of many solutions, therefore extract the one with min duration and min distance
    tourdata_min = {}

    improvement = True
    for tour in tourdata:
        if not bool(tourdata_min): # if tour is empty
            tourdata_min = tour
        elif tourdata_min.get(metric) > tour.get(metric):
            tourdata_min = tour

    tour = tourdata_min['tour']
    start = tour[0]
    finish = tour[-1]
    print(tourdata_min["tour"])
    print(tourdata_min["distance"])
    print(tourdata_min["duration"])


    fig, ax = plt.subplots()
    fig.suptitle(f'{metric}: From HWN{start:03d} (green) to HWN{finish:03d} (red)')

    lines, = ax.plot(
        [points[p]['lon'] for p in tour],
        [points[p]['lat'] for p in tour],
        '-',
        alpha=0.5
    )

    ax.scatter(
        x=[points[p]['lon'] for p in points.keys()],
        y=[points[p]['lat'] for p in points.keys()],
        c='black',
        s=10
    )

    # start point
    ax.scatter(
        x=points[start]['lon'],
        y=points[start]['lat'],
        c='lightgreen',
        s=100
    )

    # end point
    ax.scatter(
        x=points[finish]['lon'],
        y=points[finish]['lat'],
        c='tomato',
        s=100
    )

    plt.savefig('shortest_distance_tour.png')
    plt.show()

def drawNetworkFromTour(tour, metric):

    points = getWayPoints()
    pointids = list(points.keys())
    dist, dur = getDistAndDur(pointids)

    start = tour[0]
    finish = tour[-1]
    print(tour)
    print(total_distance(tour, dist))
    print(total_duration(tour, dur))


    fig, ax = plt.subplots()
    fig.suptitle(f'{metric}: From HWN{start:03d} (green) to HWN{finish:03d} (red)')

    lines, = ax.plot(
        [points[p]['lon'] for p in tour],
        [points[p]['lat'] for p in tour],
        '-',
        alpha=0.5
    )

    ax.scatter(
        x=[points[p]['lon'] for p in points.keys()],
        y=[points[p]['lat'] for p in points.keys()],
        c='black',
        s=10
    )

    # start point
    ax.scatter(
        x=points[start]['lon'],
        y=points[start]['lat'],
        c='lightgreen',
        s=100
    )

    # end point
    ax.scatter(
        x=points[finish]['lon'],
        y=points[finish]['lat'],
        c='tomato',
        s=100
    )

    plt.savefig('shortest_distance_tour.png')
    plt.show()

### draws all points and marks the start and finish points of the tours whose metric (duration/distance) is
### below a specific threshold
def drawNetworkStartEnd(tourJson, metric, start_pts, finish_pts):

    points = getWayPoints()

    pointids = list(points.keys())

    with open(tourJson) as f:
        tourdata = json.load(f)

    fig, ax = plt.subplots()
    #fig.suptitle(f'{metric}: From HWN{start:03d} (green) to HWN{finish:03d} (red)')

    ax.scatter(
        x=[points[p]['lon'] for p in points.keys()],
        y=[points[p]['lat'] for p in points.keys()],
        c='black',
        s=10
    )

    # start point
    ax.scatter(
        x=[points[start]['lon'] for start in start_pts],
        y=[points[start]['lat'] for start in start_pts],
        c='lightgreen',
        s=100
    )

    # end point
    ax.scatter(
        x=[points[finish]['lon'] for finish in finish_pts],
        y=[points[finish]['lat'] for finish in finish_pts],
        c='tomato',
        s=100
    )

    plt.savefig('shortest_distance_tour.png')
    plt.show()

def duplicateTours(data):

    df = pd.DataFrame(data)
    if (df["tour"].equals(df["tour"].drop_duplicates())):
        print("There are no duplicate tours.")
    else:
        print("Duplicates need to be removed!")

# helper function for analyzeEdges
# function to get all pairs of adjacent numbers in a list
def get_pairs(lst):
    return [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]

# counts which edges are present in tours
# in order to find out where the paths are nearly the same
def analyzeEdges(data, listLength):
    # get all pairs of adjacent numbers in each list
    all_pairs = list(chain.from_iterable([get_pairs(lst["tour"]) for lst in data]))

    # initialize a dictionary to store the count of each pair of numbers
    count_dict = {}

    # loop through each pair of numbers and update the count_dict
    for pair in all_pairs:
        pair2 = (pair[1], pair[0])
        if (pair in count_dict) | (pair2 in count_dict):
            if pair in count_dict:
                count_dict[pair] += 1
            else:
                count_dict[pair2] += 1
        else:
            count_dict[pair] = 1

    # sort the count_dict by the count of each pair of numbers
    sorted_counts = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    # print the most common pairs of adjacent numbers
    for i in range(listLength):
        pair = sorted_counts[i][0]
        count = sorted_counts[i][1]
        print(f"Pair: {pair}, Count: {count}")

def findCommonEdges(data):
    # create dict with keys being the commonEdges from 1 to 222
    commonEdges = {k: [] for k in range(223)}
    del commonEdges[0]

    for solution in data:
        for number in solution["tour"]:
            number_idx = solution["tour"].index(number)
            if number_idx == (len(solution["tour"]) - 1):
                break
            elif (solution["tour"][number_idx+1] in commonEdges[number]):
                continue
            else:
                commonEdges[number].append(solution["tour"][number_idx+1])
                commonEdges[solution["tour"][number_idx + 1]].append(number)

    for key, values in commonEdges.items():
        values.sort()
        print(key, " : ", values)

    return commonEdges

def loadCommonEdges():
    with open('2opt830_commonEdges.json') as f:
        commonEdges = json.load(f)
    return commonEdges




