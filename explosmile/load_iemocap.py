"""
Summary:
This model provides functionality to pre-process the iemocap dataset
"""
import os

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
