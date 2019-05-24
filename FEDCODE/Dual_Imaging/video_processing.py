import numpy


def extract_channel(filename, channel, width, height):
    """ Extract channel from .RAW file containing image data
    
    Args: 
        :filename (str): name of .RAW file containing image data
        :channel (one of ['red', 'blue', 'green']): name of channel to extract
        :width (int): width of data
        :height (int): height of data
        
    Returns:
        :numpy.ndarray: channel extracted from .RAW file
    """
    with open(filename, "rb") as file:
        raw_frames = numpy.fromfile(file, dtype=numpy.uint8)
        time_dim_float = raw_frames.shape[0] / (width*height*3)
        time_dim = int(time_dim_float)
        if time_dim != time_dim_float:
            raise Exception('Invalid input file, width or height')
        raw_frames = numpy.reshape(raw_frames, (time_dim, height, width, 3))
        print(f"Dimensions of {channel} channel: {numpy.shape(raw_frames)[0:-1]}")
        channels = {'red': 0, 'green': 1, 'blue': 2}
    return raw_frames[..., channels[channel]]
