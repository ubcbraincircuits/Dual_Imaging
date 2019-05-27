import numpy


def extract_channel(filename, channel, width, height):
    """
    Extract channel from .RAW file containing image data

    :param filename: name of .RAW file containing image data
    :type: str
    :param channel: name of channel to extract
    :type: str, one of: ['red', 'blue', 'green']
    :param width: width of data
    :type: int
    :param height: height of data
    :type: int
    :return: channel extracted from .RAW file
    :type: numpy.ndarray
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


def clean_raw_timestamps(filename):
    """
    Perform cleaning routine on .RAW timestamps

    :param filename: name of .RAW file containing timestamps
    :type:str
    :return: cleaned timestamp array
    :type: numpy.ndarray
    """
    with open(filename, 'rb') as file:
        raw_timestamps = numpy.fromfile(file, dtype=numpy.float32)
    raw_timestamps[0] = 1
    return raw_timestamps[numpy.where(raw_timestamps > 0)]


def get_locations_of_dropped_frames(timestamps, fps):
    """
    Return delta(timestamps) and indices of timestamps of dropped
    frames

    :param timestamps: 1-D numpy array containing timestamps
    :type: numpy.ndarray
    :param fps: frame rate of footage
    :type: int, one of: [30,90]
    :return differences between timestamps; dt
    :type: numpy.ndarray
    :return indices of timestamps where frames were dropped
    :type: numpy.ndarray
    """
    differences = numpy.diff(timestamps, 1)
    thresholds = {30: 50_000, 90: 12_500}
    threshold = thresholds[fps]
    print("Mean filtered frame difference: ", numpy.mean(
        differences[numpy.where(differences <= threshold)]
    ))
    # 50,000 for 30fps
    # 12,500 for 90fps
    return differences, numpy.where(differences > threshold)[0]


def generate_frames(frames, differences, locations, true_frame_rate):
    for location in locations:
        number_of_dropped_frames = int(
            numpy.round(differences[location] / (1.e6/true_frame_rate))
        ) - 1
        first_frame, last_frame = frames[location:location+2]
        yield first_frame, last_frame, number_of_dropped_frames, location


class DroppedFrames:
    """
    Used to fill in dropped frames by interpolating between closest
    available data pairs
    """
    
    def __init__(self, first_frame, last_frame, num_dropped_frames, location):
        self.height, self.width = first_frame.shape
        self.num_dropped_frames = num_dropped_frames
        # the frames need to be added
        self.location = location
        # Must eventually make it to use all channels.
        self.first_frame = first_frame
        self.last_frame = last_frame
        self.interpolated_frames = False

    def interpolate(self):
        diff_per_frame = (self.last_frame-self.first_frame) / (self.num_dropped_frames+1)

        interpolated_frames = numpy.empty(
            (self.number_of_dropped_frames, self.height, self.width),
            dtype=numpy.uint8
        )
        for frame_index in range(self.num_dropped_frames):
            interpolated_frames[frame_index] = (frame_index+1)*diff_per_frame+self.first_frame
        del self.first_frame
        del self.last_frame
        self.interpolated_frames = interpolated_frames


def insert_interpolated_frames(frames, list_of_generated_frames):
    """
    Insert interpolated frames into input array as a substitute for
    dropped frames

    :param frames: array of frames from RAW channel with dropped frames
    :type: numpy.ndarray
    :param list_of_generated_frames: list of DroppedFrames objects
    :type: list
    :return: array of frames with dropped frames filled
    :type: numpy.ndarray
    """
    shifting_index = 0
    for generated_frames in list_of_generated_frames:
        interpolated_frames = generated_frames.interpolate()
        frames = numpy.insert(
            frames,
            interpolated_frames.location + shifting_index + 1,
            interpolated_frames.interpolated_frames,
            0
        )
        shifting_index += generated_frames.number_of_dropped_frames
    return frames

