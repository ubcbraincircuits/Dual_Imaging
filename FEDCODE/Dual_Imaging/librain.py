import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
from os.path import join, getsize, isfile, isdir
from pathlib import Path
from dateutil.parser import parse 

class Data:


    def __init__(self, directory):
        self.directory = directory
        self.dates = os.listdir(self.directory)


    def experiment(self, date, exp_num, listfiles=False):
        """
        Returns the directory of the experiment if it exists and if not,
        an exception is raised.

        :param date: the date the experiment was conducted in any format
        :type: str
        :param exp_num: the experiment number
        :type: int 
        :param listfiles: if False, only the first value below is returned; otherwise, 
        both are returned
        :type: bool

        :return: full path to the directory of the experiment
        :type: str
        :return: all files in the experiment directory
        :type: list
        """
        if type(date) is str:
            d_format = parse(date)
            d = f"/{d_format.year}{d_format:%m}{d_format:%d}"
            date_path = Path(str(self.directory) + d) 
            if isdir(date_path) is False:
                raise Exception(f'Folder {d} does not exist')
            else:
                exp = f"/Experiment_{exp_num}"
                exp_folder = Path(str(date_path) + exp)
                if isdir(exp_folder) is True:
                    if listfiles is True:
                        files = [file for file in os.listdir(exp_folder)]
                        return str(exp_folder), files
                    else:
                        return str(exp_folder)
                else:
                    raise Exception(f'Folder Experiment {exp_num} does not exist in folder {d}')
                

    def file(self, exp_folder, fname, subfolder=None):
        """
        Returns fname if it exists in exp_folder. If fname is not in exp_folder, 
        an exception is raised.

        :param exp_folder: complete path to experiment folder, i.e. Experiment 1
        :type: str
        :param fname: one of 
        'timestamps', 
        'interpolated', 
        'h264', 
        'combined', 
        'processed',
        'mean_stim_frames', 
        'fixed_stim_frames', 
        'LM_mask', 
        'left blue', 
        'left green', 
        'right blue',
        'right green', 
        'left blue 0.01-3.0Hz', 
        'left green 0.01-3.0Hz', 
        'right blue 0.01-3.0Hz',
        'right green 0.01-3.0Hz'
        :type: str 
        :param subfolder: can be specified as 'Behaviour'
        :type: str

        :return: full path to fname 
        :type: str
        """
        fnames = [
            'timestamps', 
            'interpolated',
            'subset interpolated', 
            'h264', 
            'combined', 
            'processed',
            'mean_stim_frames', 
            'fixed_stim_frames', 
            'LM_mask', 
            'left blue', 
            'left green', 
            'right blue',
            'right green', 
            'left blue 0.01-3.0Hz', 
            'left green 0.01-3.0Hz', 
            'right blue 0.01-3.0Hz',
            'right green 0.01-3.0Hz'
            'left blue 0.01-12.0Hz', 
            'left green 0.01-12.0Hz', 
            'right blue 0.01-12.0Hz',
            'right green 0.01-12.0Hz'
            'left 0.01-12.0Hz'
            'right 0.01-12.0Hz'
            'left 0.01-3.0Hz'
            'right 0.01-3.0Hz'
            ]

        if fname not in fnames:
            raise ValueError(f'{fname} is not a valid filename. Check help(<directory>.file) for a list of filenames')

        if subfolder is 'Behaviour':   
            direc = os.path.join(str(exp_folder), subfolder)        
            for root, dirs, files in os.walk(direc): 
                for f in files:
                    if 'timestamps' in f and fname is 'timestamps':
                        return str(Path(os.path.join(root, f)))
                    elif 'interpolated' in f and not 'subset' in f and fname is 'interpolated':
                        return str(Path(os.path.join(root, f)))
                    elif 'interpolated' in f and fname is 'interpolated':
                        return str(Path(os.path.join(root, f)))
                    elif 'h264' in f and fname is 'h264':
                        return str(Path(os.path.join(root, f)))                     
            raise FileNotFoundError(f'File {fname} does not exist in subfolder {subfolder}') 
        
        elif subfolder is None:         
            for root, dirs, files in os.walk(str(exp_folder)):
                for f in files:
                    if 'combined' in f and 'raw' in f and 'upscaled' not in f:
                        if not 'gsr' in f:
                            if '0.01-3' in f:
                                if fname is 'combined':
                                    return Path(os.path.join(root, f))
                    elif 'processed' in f and fname is 'processed':
                        return str(Path(os.path.join(root, f)))
                    elif 'mean_stim_frames.raw' in f and fname is 'mean_stim_frames':
                        return str(Path(os.path.join(root, f)))
                    elif 'fixed_stim_frames' in f and fname is 'fixed-stim_frames':
                        return str(Path(os.path.join(root, f)))
                    elif 'LM_mask' in f and fname is 'LM_mask':
                        return str(Path(os.path.join(root, f)))

                    elif 'BLUE' in f:
                        if 'LEFT' in f:
                            if 'RAW' in f and fname is 'left blue':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-3.0' and fname is 'left blue 0.01-3.0Hz':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-12.0' and fname is 'left blue 0.01-12.0Hz':
                                return str(Path(os.path.join(root, f)))
                        if 'RIGHT' in f:
                            if 'RAW' in f and fname is 'right blue':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-3.0' and fname is 'right blue 0.01-3.0Hz':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-12.0' and fname is 'right blue 0.01-12.0Hz':
                                return str(Path(os.path.join(root, f)))   
                    elif 'GREEN' in f:
                        if 'LEFT' in f:
                            if 'RAW' in f and fname is 'left green':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-3.0' and fname is 'left green 0.01-3.0Hz':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-12.0' and fname is 'left green 0.01-12.0Hz':
                                return str(Path(os.path.join(root, f)))   
                        if 'RIGHT' in f:
                            if 'RAW' in f and fname is 'right green':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-3.0' and fname is 'right green 0.01-3.0Hz':
                                return str(Path(os.path.join(root, f)))
                            if '0.01-12.0' and fname is 'right green 0.01-12.0Hz':
                                return str(Path(os.path.join(root, f)))   
                    
                    elif 'LEFT_corrected' in f:
                        if '0.01-3.0' in f and fname is 'left 0.01-3.0Hz':
                            return str(Path(os.path.join(root, f)))
                        if '0.01-12.0' in f and fname is 'left 0.01-12.0Hz':
                            return str(Path(os.path.join(root, f)))
                    elif 'RIGHT_corrected' in f:
                        if '0.01-3.0' in f and fname is 'right 0.01-3.0Hz':
                            return str(Path(os.path.join(root, f)))
                        if '0.01-12.0' in f and fname is 'right 0.01-12.0Hz':
                            return str(Path(os.path.join(root, f)))


            raise FileNotFoundError(f'File {fname} does not exist')

        else:
            raise FileNotFoundError(f'Subfolder {subfolder} does not exist in folder {exp_folder}')


class Output:


    def __init__(self, directory):
        self.directory = directory


    def saveas(self, f_in, f_out, suffix, ftype, save=False, path="", dirname="Derivatives", fig=False):
        """
        Returns file name of a result with the same naming convention as the corresponding raw data. 
        The result can also be saved.

        :param f_in: complete path to raw file from which the result was derived
        :type: str 
        :param f_out: the result to be saved
        :type: any
        :param suffix: word or phrase to append to the raw file name (i.e. <raw file>_PROCESSED)
        :type: str
        :param ftype: desired file type
        :type: str
        :param path: complete path to the directory in which the file will be saved; if unspecified, the file
        will be saved in "Derivatives" folder created automatically within self.directory
        :type: str
        :param dirname: name of the directory in which the file will be saved
        :type: str
        :param fig: must be set to True if f_out is a figure; the file is saved in npy format otherwise
        :type: bool

        :return: file name of result
        :type: str
        """
        if path is "":
            direc = self.directory + f'/{dirname}/'
            if isdir(direc) is False:
                direc = os.mkdir(direc)
        else:
            if isdir(path) is False:
                raise FileNotFoundError(f'{path} does not exist')
            else:
                direc = path + f'/{dirname}/'
                if isdir(direc) is False:
                    direc = os.mkdir(direc)
        
        if isfile(f_in) is False:
            raise FileNotFoundError(f'{f_in} does not exist')

        # isolate file name
        if '/' in f_in: 
            fname = f_in.split('/')[-1].split('.')
        elif '\\' in f_in:
            fname = f_in.split('\\')[-1].split('.')
        rm_type = ""
        for i in range(len(fname)-1): 
            # Removes file type. In case there are periods in the file name, 
            # concatenate up to but not including the file type. 
            rm_type += fname[i]
        fname = rm_type + f'_{suffix}' + f'.{ftype}'
            
        path = Path(direc+fname)

        if save is True:
            if fig is True:
                f_out.savefig(path)
                print(f"Saved as {fname}")
                return fname
            else:
                np.save(path, f_out)
                print(f"Saved as {fname}")
                return fname
        else:
            return fname 




