"""
Summary:
This model provides functionality to pre-process the iemocap dataset
"""
import os
import pandas as pd

def returnrealfiles(filenameslist):
    """
    Takes a list of filenames and returns a tidied up list of filesnames,
    excluding the files that start with a . and only keeping the files that end with txt or wav

    Parameters
    ------------
    filenameslist : list of strings with full paths to files

    Returns
    ------------
    realfiles : list of strings with full paths to files
    """

    realfiles = []
    for i in range(len(filenameslist)):
        str_filename = str(filenameslist[i]).split("/")[-1]
        if (str_filename[0] != '.') & ((str_filename[-3:] == 'txt') | (str_filename[-3:] == 'wav')):
            realfiles.append(filenameslist[i])
    return realfiles;

def find_matching_label_file(wav_filename, labfiles, label_files_path):
    """
    Looks up which of the labfiles matched with the wav_filename

    Parameters
    ------------
    wav_filename : string
        The wav file name with full path
    labfiles: list
        The names of the label txt files (without path)
    label_files_path : string
        Path to txt files with labels

    Returns
    ------------
    lab_fullpath : string
        The name of the label txt file with full path
    """

    # the wav files have longer names than the label files, so first remove the end:
    wav_namepieces = wav_filename.split("/")[-1].split("_")
    matchinglabfile = wav_namepieces[0] + '_' + wav_namepieces[1] + '.txt'
    # check whether the matching label file truly exists:
    matchinglabfile2 = [item for index, item in enumerate(labfiles) if matchinglabfile == item]
    if len(matchinglabfile2) == 0:
        print("Error no matching label file found")
    elif len(matchinglabfile2) > 1:
        print("Error two or more matching label files found")
    matchinglabfile3 = ''.join(matchinglabfile2)
    # create full path for labelfile:
    lab_fullpath =  os.path.join(label_files_path, matchinglabfile3)
    return lab_fullpath;

def readlabtxt(lab_fullpath):
    """
    Loads txt with the Emotion labels, takes the summary labels per time frame,
     and stores it in a pandase data.frame

    Parameters
    ------------
    lab_fullpath : string
        The name of the label txt file with path

    Returns
    ------------
    labels : pandas data.frame
        pandas data.frame with all summary labels per time frame
    """    
    # get all labels for all utterances in this improvisation
    labels = pd.read_table(lab_fullpath,header=0).iloc[0::8,:] # the summary is stored in every 8th row
    # the format of the data needs to be tidied up a bit
    # turn rownames into column
    labels.index.name = 'newhead'
    labels.reset_index(inplace=True)
    # rename the columns that are now created
    labels = labels.rename(columns={'level_0': '[START_TIME - END_TIME]', 'level_1': 'TURN_NAME', 'level_2': 'EMOTION'})
    # split valence, activation, and dominance:
    labels[['V','A','D']] = labels['% [START_TIME - END_TIME] TURN_NAME EMOTION [V, A, D]'].str.split('\s',expand=True)
    labels[['START_TIME','END_TIME']] = labels['[START_TIME - END_TIME]'].str.split(' - ',expand=True)
    labels = labels.drop(['% [START_TIME - END_TIME] TURN_NAME EMOTION [V, A, D]','[START_TIME - END_TIME]'], axis=1)
    # remove unwanted characters
    for colnam in ['V','A','D', 'START_TIME','END_TIME']:
        labels[colnam] = labels[colnam].map(lambda x: x.lstrip('[,').rstrip('],'))
    return labels;
