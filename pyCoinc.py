#!/usr/bin/python
# Filename: pyCoinc.py

import numpy as np
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt


timeListdType = [('time', float)]
energyListdType = [('energy', float), ('time', float)]
shapeListdType = [('shape', float), ('energy', float), ('time', float)]


def getCoincIndices(startTimes, stopTimes, stopTimeShift, resolvingWindow, debug=False):
    #This function returns coincidence incidences given a set of resolving parameters.

    stopTimes = stopTimes + stopTimeShift
    startTimesCount = np.size(startTimes)
    stopTimesCount = np.size(stopTimes)

    startIndices = np.arange(startTimesCount)
    stopIndices = np.arange(stopTimesCount)


    #Get the indices required to sort A into B (locations for A to be a start signal)
    sortedIndices = np.searchsorted(stopTimes,startTimes)
    if debug: print "Sorted Indices", sortedIndices

    #determine the maximum number of events to include, ignore events that sit at the end of the array with no following stop signal
    comparisonSize = np.size(sortedIndices)
    #validSortedIndices represents the sort indices that are all a valid size
    validSortedIndices = sortedIndices[sortedIndices<comparisonSize]

    #generate a selector for the first N events, to ensure an equal size comparison. This drops useless events off of the end.
    comparableIndices = np.arange(np.size(validSortedIndices))

    #generate time difference between all nearest values
    allTimeDiffs =  stopTimes[validSortedIndices] - startTimes[comparableIndices] 

    if debug: print "All Time Differences", allTimeDiffs

    #Set "Acceptable" coincidence resolving time
    timeThresh = resolvingWindow

    #generate a list of locations that meet the coincidence requirements
    inRangeTimeDiffs = np.where(allTimeDiffs<=timeThresh)[0]
    if debug: print "Found ", np.size(inRangeTimeDiffs), " coincidences based on a ", timeThresh, " unit threshold."
    #This represents all time differences within the window
    if debug: print "Time differences (valid): ", allTimeDiffs[inRangeTimeDiffs]
    #This represents the respective location of all coincidences
    if debug: print "Valid Coincidence Indices: ", inRangeTimeDiffs

    #in order to identify events that share an event, we look for the originating indices
    if debug: print "Event Indices used for Stop Times: ", validSortedIndices[inRangeTimeDiffs]

    uniqueStopInds, uniqueStopIndIndices = np.unique(validSortedIndices[inRangeTimeDiffs],return_index = True,return_counts=False)

    #These are the unique start indices
    coincStartInds =  inRangeTimeDiffs[uniqueStopIndIndices]
    coincStartTimes = startTimes[coincStartInds]
    if debug: print "Unique Indices used for Start Times: ", coincStartInds

    #These are the unique stop indices
    coincStopInds =  uniqueStopInds
    coincStopTimes = stopTimes[uniqueStopInds]
    if debug: print "Unique Indices used for Stop Times: ", coincStopInds

    if debug: print "Start Times", coincStartTimes
    if debug: print "Stop Times", coincStopTimes

        
    return coincStartInds, coincStopInds

def getCoincCount(startTimes, stopTimes, stopTimeShift, resolvingWindow, debug=False):
    #This function gets the number of coincidence events given certain parameters

    startIndices, stopIndices = getCoincIndices(startTimes,stopTimes,stopTimeShift,resolvingWindow,debug)
    
    return np.size(startIndices)

def coincidenceTiming(startChannel, stopChannel, startIndices, stopIndices):
    tDiff = stopChannel['time'][stopIndices] - startChannel['time'][startIndices]
    return tDiff

def coincidenceEnergies(startChannel, stopChannel, startIndices, stopIndices):
    #returns an array of coincident event energies
    return startChannel['energy'][startIndices], stopChannel['energy'][stopIndices]

def getCoincCountRange(startTimes, stopTimes, startTimeShift, stopTimeShift, resolvingWindow, NumSteps = 15):
    #checks a range of values for coincidence counts
    offsets = np.linspace(startTimeShift,stopTimeShift,num=NumSteps)

    coincCounts = np.zeros(np.size(offsets))

    for n, offset in enumerate(offsets):
        coincCounts[n]  = getCoincCount(startTimes,stopTimes,offset,resolvingWindow,debug=False)
    return offsets, coincCounts

def coincidencePlots(startChannel, stopChannel, startIndices, stopIndices, plotRatio=4, bins=100):
    if 'energy' not in startChannel.dtype.fields:
        return "ERROR"
    
    #get energies of coincidence events
    coincEnStartChannel, coincEnStopChannel = coincidenceEnergies(startChannel,stopChannel,startIndices, stopIndices)

    #set up limits of graphs
    startMin = np.min(startChannel['energy'][startIndices])
    startMax = np.max(startChannel['energy'][startIndices])
    stopMin = np.min(stopChannel['energy'][stopIndices])
    stopMax = np.max(stopChannel['energy'][stopIndices])

    fig = plt.figure(figsize=(15,15))  #create figure object
    
    g = gs.GridSpec(2,2,width_ratios=[1,plotRatio],height_ratios=[plotRatio,1]) #create grid for plots

    plt.subplot(g[0,0])             # top left, stop energy histogram
    plt.hist(coincEnStopChannel,bins,orientation="horizontal",range=[stopMin,stopMax]);
    plt.ylim([stopMin,stopMax])


    plt.subplot(g[0,1])             # top right, 2d historgram
    hpl = plt.hexbin(startChannel['energy'][startIndices],stopChannel['energy'][stopIndices],cmap=plt.cm.nipy_spectral,mincnt=1,gridsize=bins)
    plt.title('Coincidence Matrix')
    plt.xlabel('Start Energy')
    plt.ylabel('Stop Energy')


    plt.subplot(g[1,0])             # bottom left, timing histogram
    coincTiming = coincidenceTiming(startChannel,stopChannel,startIndices,stopIndices)
    plt.hist(coincTiming,512,log=True);
    plt.xlabel('deltaTime')


    plt.subplot(g[1,1])             # bottom right, start enery histogram
    plt.hist(coincEnStartChannel,bins,range=[startMin,startMax]);
    plt.xlim([startMin,startMax])

    plt.tight_layout()
    
    return fig
