
"""
Author      : Tom Fu
Date        : 2020 April 8
Description : distanceToPrimerPair.py for DNA Printing Project
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
dfDict = dict(zip(df['Productlength'], df['pairInfo']))

# make list of productLength
productLengthList = list(df['Productlength'])
distRatioList10K = [productLength/10000 for productLength in productLengthList]


def rawDistToPrimerPair(distUnadjusted):
    """
    Para: distUnadjusted - a float, representing the adjusted distance, which is the productLength the input 
                         distance is the closest to.
    Output: the matched primer pair info as a string, will be printed out in a human-readable form
    """
    # 1. find the productlength that's closest to the input
        ## source: https://stackoverflow.com/questions/40271548/how-to-find-the-smallest-closest-number-in-a-list-in-python
    distAdjusted = min(distRatioList10K, key=lambda x: (abs(x - distUnadjusted), x))
    primerPairInfo = dfDict[int(round(distAdjusted*10000))]
    return primerPairInfo



