import matplotlib.pyplot as plt
import numpy


class Bregma:
    """
    Define a mouse's bregma location from image
    """
    def __init__(self, image=None, cmap='gray', from_image=True, column=None, row=None):
        """
        Create the Bregma object. The last location
        clicked on will be considered the bregma.

        :param image: 2D array containing image data
        :type: numpy.ndarray

        :param cmap: matplotlib colormap. default is 'gray'
        :type: str

        :from_image: flag used for from_coordinate construction
        :type: bool
        """
        if from_image:
            if image is None:
                raise TypeError('Parameter `image` expected but not found')
            fig, ax = plt.subplots()
            ax.matshow(image, cmap=cmap)
            y_clicks, x_clicks = [], []

            def onclick(event):
                y_clicks.append(int(event.ydata))
                x_clicks.append(int(event.xdata))

            fig.canvas.mpl_connect('button_press_event', onclick)
            if len(y_clicks) == 0:
                print('No Bregma Selected')
                del self
                return
            else:
                self.col, self.row = y_clicks[-1], x_clicks[-1]

        else:
            if column is None and row is None:
                raise TypeError('Parameters `column` and `row` expected bt not found')
            else:
                self.col, self.row = int(column), int(row)

        print(self)

    def __repr__(self):
        return f"Bregma Location:\nColumn {self.col}\nRow {self.row}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_coordinates(cls, column, row):
        """
        Manually create a bregma object

        :param column: column index of bregma
        :type: int or float
        :param row: row index of bregma
        :type: int or float

        :return: instance of Bregma
        """
        if type(column) not in (int, float):
            raise TypeError('Argument `column` must be a positive integer or float')
        if column < 0:
            raise ValueError('Argument `column` must be a positive integer or float')
        if type(row) not in (int, float):
            raise TypeError('Argument `row` must be a positive integer or float')
        if row < 0:
            raise ValueError('Argument `row` must be a positive integer or float')
        return cls(column=column, row=row, from_image=False)


class Seed:
    """
    Seed pixel
    """
    def __init__(self, name, y, x):
        """
        :param name: Name of seed pixel
        :type: str
        :param y: y position in mm
        :type: int or float
        :param x: x position in mm
        :type: int or float
        """
        if type(name) is str:
            self.name = name
        else:
            del self
            raise TypeError("Argument `name` should be a string")
        if type(y) in (int, float):
            self.y = y
        else:
            del self
            raise TypeError("Argument `y` must be a float or integer")
        if type(x) in (int, float):
            self.x = x
        else:
            del self
            raise TypeError("Argument `x` must be a float or integer")


class ScaledSeed:
    """
    Scaled seed pixel
    """
    def __init__(self, name, row, col, bregma):
        self.name = name
        self.row = row
        self.col = col
        self.signal = None
        self.bregma = bregma
        self.corr_map = None


def generate_scaled_seeds(seeds, bregma, ppmm, direction=None):
    """
    Generate Scaled Seed pixels

    :param seeds: list or tuple containing instances of Seed or tuples/lists containing arguments to instantiate Seeds.
    :type: list or tuple
    :param bregma: instance of Bregma
    :type: Bregma
    :param ppmm: pixels per millimeter
    :type: int or float
    :param direction: one of ('l', 'r', 'u', 'd', None)
    :type: str or None

    :return: list of ScaledSeeds
    :type: list
    """
    if type(seeds) not in (tuple, list):
        raise AttributeError('Argument `seed` must be a list or tuple')

    seed_list = []
    for seed in seeds:
        if type(seed) in (tuple, list):
            seed_list.append(Seed(*seed))  # unpacking the collection
        elif isinstance(seed, Seed):
            seed_list.append(seed)
        else:
            raise TypeError(f"Invalid seed {seed}. Seed must be a valid tuple/list or instance of Seed.")

    if not isinstance(bregma, Bregma):
        raise TypeError("Argument `bregma` must be an instance of Bregma.")

    if type(ppmm) not in (int, float):
        raise TypeError('Argument `ppmm` must be an integer or a float')

    directions = ('u', 'd', 'l', 'r', None)
    if direction not in directions:
        raise AttributeError(f'Keyword `direction` must be one of {directions}')
    else:
        print(f'Direction chosen: {direction}')

    scaled_seeds = []
    if direction in ('u', None):
        for seed in seed_list:
            scaled_seeds.append(
                ScaledSeed(seed.name + "-L", int(bregma.row - ppmm * seed.y), int(bregma.col - ppmm * seed.x), bregma))
            scaled_seeds.append(
                ScaledSeed(seed.name + "-R", int(bregma.row - ppmm * seed.y), int(bregma.col + ppmm * seed.x), bregma))
    elif direction is 'd':
        for seed in seed_list:
            scaled_seeds.append(
                ScaledSeed(seed.name + "-R", int(bregma.row - ppmm * seed.y), int(bregma.col + ppmm * seed.x), bregma))
            scaled_seeds.append(
                ScaledSeed(seed.name + "-L", int(bregma.row - ppmm * seed.y), int(bregma.col - ppmm * seed.x), bregma))
    elif direction is 'r':
        for seed in seed_list:
            scaled_seeds.append(
                ScaledSeed(seed.name + "-R", int(bregma.row - ppmm * seed.x), int(bregma.col + ppmm * seed.y), bregma))
            scaled_seeds.append(
                ScaledSeed(seed.name + "-L", int(bregma.row + ppmm * seed.x), int(bregma.col + ppmm * seed.y), bregma))
    else:  # direction is 'l'
        for seed in seed_list:
            scaled_seeds.append(
                ScaledSeed(seed.name + "-R", int(bregma.col + ppmm * seed.x), int(bregma.row - ppmm * seed.y), bregma))
            scaled_seeds.append(
                ScaledSeed(seed.name + "-L", int(bregma.col - ppmm * seed.x), int(bregma.row - ppmm * seed.y), bregma))
    return scaled_seeds


def _seed_pixel_box(
        row,
        col,
        radius,
        height,
        width
):
    top = row - radius
    bottom = row + radius
    left = col - radius
    right = col + radius

    if top < 0:
        top = 0
    if bottom > height:
        bottom = height
    if left < 0:
        left = 0
    if right > width:
        right = width

    return top, bottom+1, left, right+1


def generate_correlation_matrix(
        l_mouse_frames,
        r_mouse_frames,
        l_seeds,
        r_seeds,
        title,
        filename=None,
        radius=5,
        interpolation="nearest",
        cmap="viridis",
        figsize=(10, 11)
):
    """
    Generate correlation matrix and plot of correlation matrix for dual imaging experiment.
    Also generate visualisation of bregma location and seed pixel regions.

    :param l_mouse_frames: left mouse brain imaging frames
    :type: numpy.ndarray
    :param r_mouse_frames: right mouse brain imaging frames
    :type: numpy.ndarray
    :param l_seeds: collection of left mouse ScaledSeeds
    :type: list/tuple/numpy.ndarray
    :param r_seeds: collection of right mouse ScaledSeeds
    :type: list/tuple/numpy.ndarray
    :param title: chart title for correlation matrix
    :type: str
    :param filename: if files need saving, filenames to ascribe to plots and correlation matrix
    :type: str
    :param radius: default 5. number of pixels in either side of the seed pixel used to calculate the temporal mean
    :type: int
    :param interpolation: default `nearest`. one of `nearest, `linear`, `cubic`, interpolation type to use for correlation matrix chart
    :type: str
    :param cmap: default `viridis`. matplotlib colormap.
    :type: str
    :param figsize: default (10,11). size of correlation matrix plot in inches.
    :type: tuple
    """
    radius = int(radius)
    num_seeds = numpy.size(l_seeds)+numpy.size(r_seeds)
    seed_signals = numpy.zeros(
        (num_seeds, l_mouse_frames.shape[0])
    )  # initialise matrix used to calculate correlation coefficient
    labels, positions = [], []  # for labelling correlation coefficient matrix

    # to display bregma and seed pixel regions
    l_first_frame = l_mouse_frames[0]
    r_first_frame = r_mouse_frames[0]

    l_bregma, r_bregma = l_seeds[0].bregma, r_seeds[0].bregma
    l_first_frame[l_bregma.row, l_bregma.col] = 255
    r_first_frame[r_bregma.row, r_bregma.col] = 255

    height, width = l_first_frame.shape
    # for each seed, find the mean of the signal within specified radius of seed pixel
    for i, seed in enumerate(l_seeds):
        labels.append(seed.name+"-L")
        top, bottom, left, right = _seed_pixel_box(
            seed.row,
            seed.col,
            radius,
            height,
            width
        )
        seed.signal = numpy.mean(
            numpy.mean(l_mouse_frames[:, top:bottom, left:right], axis=(1, 2))
        )
        seed_signals[i] = seed.signal
        l_first_frame[top:bottom, left:right] = 255
        positions.append((seed.row, seed.col))

    for i, seed in enumerate(l_seeds, start=i+1):  # continue looping through seed_signals
        labels.append(seed.name+"-R")
        top, bottom, left, right = _seed_pixel_box(
            seed.row,
            seed.col,
            radius,
            height,
            width
        )
        seed.signal = numpy.mean(
            numpy.mean(r_mouse_frames[:, top:bottom, left:right], axis=(1, 2))
        )
        seed_signals[i] = seed.signal
        r_first_frame[top:bottom, left:right] = 255
        positions.append((seed.row, seed.col))

    correlation_matrix = numpy.corrcoef(seed_signals)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlation_matrix, interpolation=interpolation, vmin=0, vmax=1, cmap=cmap)
    fig.colorbar(cax, fraction=0.046, pad=0.04)
    ax.set_title(title + "\n", y=1.15)
    ax.set_xticks([i for i in range(num_seeds)])
    ax.set_yticks([i for i in range(num_seeds)])
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_yticklabels(labels)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.imshow(l_first_frame, cmap='gray')
    ax.set_title('Left brain seed pixel regions and bregma')
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    ax3.imshow(r_first_frame, cmap='gray')
    ax.set_title('Right brain seed pixel regions and bregma')

    if type(filename) is str:
        print("Saving correlation matrix")
        fig.savefig(filename + ".svg")
        numpy.save(filename + ".npy", correlation_matrix)
