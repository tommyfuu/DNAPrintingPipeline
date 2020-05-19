
"""
Author      : Tom Fu
Date        : 2020 April 8
Description : distanceToPrimerPairLinear.py for DNA Printing Project
"""
import sys
import pandas as pd

# load dataset
df = pd.read_csv('./OrderedPrimersOfficialCombinations-Sheet1-1.csv')

# combine columns
df['primer1Info'] = df['ID1'].str.cat(df['Primer1sequence'])
df['primer2Info'] = df['ID2'].str.cat(df['Primer2sequence'])
df['pairInfo'] = df['primer1Info'].str.cat(df['primer2Info'])

# make df dict
dfDict = dict(zip(df['order'], df['pairInfo']))

def rawDistToPrimerPair(yindex):
    """
    Para: yindex - an int, representing the distance we want to travel to
    Output: the matched primer pair info as a string, will be printed out in a human-readable form
    """
    primerPairInfo = dfDict[yindex+1] 
    return primerPairInfo


