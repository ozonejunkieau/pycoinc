# pycoinc
**List Mode Software Coincidence Processing for NumPy and Python**

This code forms a basic library for the analysis of list mode detector data. 

The basic data structure used by this code is a NumPy array of specified type. Valid types are specified within the code, but generally include time, energy and shape data.

Each array represents a single channel of data. Times are assumed to sorted.

![alt tag](https://raw.githubusercontent.com/ozonejunkieau/pycoinc/master/Documentation/coincplot.png)

**pyCoinc.getCoincIndices(startTimes, stopTimes, stopTimeShift, resolvingWindow, debug=False)**

This function returns coincidence incidences given a set of resolving parameters. It does not modify data that is parsed to it, merely returning element numbers that form coincidence events.
* startTimes is a list of coincidence starting times, typically generated via channelName['time']
* stopTimes is a list of coincidence stop times, in the same format as above.
* stopTimeShift is a float value that shifts the stopTimes array.
* resolvingWindow is another float value that specifies how wide the coincidence window is.
* debug is a boolean indicator that controls the printing of debug information.

*Return format is startIndices, stopIndices*

**def getCoincCount(startTimes, stopTimes, stopTimeShift, resolvingWindow, debug=False)**

This function returns only the number of coincident events for a given parameter set. It does this through a call to getCoincIndices, so it is no faster. It is used to simpleify the calling used for range functions. Parameters are as per above.

*Return format is a count of coincident events.*

**def coincidenceTiming(startChannel, stopChannel, startIndices, stopIndices)**

This function returns an array of time differences between coincident events. Used for generating a histogram of time differences.

*Return format is a single float array of time differences.*

**def coincidenceEnergies(startChannel, stopChannel, startIndices, stopIndices)**

This function returns coincident energy information. Used for generating coincident enery spectra.

*Return format is two float arrays of energy, startEnergy, stopEnergy.*


**def getCoincCountRange(startTimes, stopTimes, startTimeShift, stopTimeShift, resolvingWindow, NumSteps = 15)**

This is a helper function for determining coincidence settings. Given two arrays of start and stop times as above and:
* startTimeShift is the initial timeShift used on the stop channel.
* stopTimeShift is the final timeShift used on the stop channel.
* NumSteps is the number of steps between startTime to stopTime that are evaluated.
By plotting offsets vs. counts, it is possible to deduce the channel offset required to optimise coincidence events.

*Return format is two arrays: offsets, counts.*


**def coincidencePlots(startChannel, stopChannel, startIndices, stopIndices, plotRatio=4, bins=100)**

This function generates a plot of the coincidence data given two channels and coincident indices. 
* plotRatio is the ratio of plot sizes. The plot sizes are N:1, defaulting to 4.
* bins is the number of bins used in the histograms and the hexbin routine for the intensity plots.

*Return type is a a pyplot figure.
