import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

class GPSVis(object):
    # Class for visualisation of the GPS data
    # Creates a visualisation on the image downloaded from Open Street Maps

    def __init__(self, data_path, map_path, points):
        # data_path = file containing containing GPS records
        # map_path = location of the map image
        # points = Upper-Left and lower-right GPS points of the map (lat1, lon1, lat2, lon2).
        self.data_path = data_path
        self.points = points
        self.map_path = map_path

        self.result_image = Image
        self.x_ticks = []
        self.y_ticks = []

    def plot_map(self, output='save', save_as='visualisation.png'):
        # Plotting out GPS coords for visualisation
        # output = saves the plotted map
        # save_as = saves the map as a PNG file
        self.get_ticks()
        fig, axis1 = plt.subplots(figsize=(10,10))
        axis1.imshow(self.result_image)
        axis1.set_xlabel('Longitude')
        axis1.set_ylabel('Latitude')
        axis1.set_xticklabels(self.x_ticks)
        axis1.set_yticklabels(self.y_ticks)
        axis1.grid()
        if output == 'save':
            plt.savefig(save_as)
        else:
            plt.show()

    def create_image(self, color, width=2):
        # Creates an image that contains the Map and the GPS record
        # color = color the GPS line is
        # width = width of the GPS line
        data = pd.read_csv(self.data_path, header=0)
        # sep will separate the latitude from the longitude
        data.info()
        self.result_image = Image.open(self.map_path, 'r')
        img_points = []
        gps_data = tuple(zip(data['latitude'].values, data['longitude'].values))

        for d in gps_data:
            x1, y1 = self.scale_to_img(d, (self.result_image.size[0], self.result_image.size[1]))
            img_points.append((x1, y1))
        draw = ImageDraw.Draw(self.result_image)
        draw.line(img_points, fill=color, width=width)

    def scale_to_img(self, lat_lon, h_w):
        # Makes lat/long into image pixels
        # lat_lon will draw the lat1, lon1
        # h_w: size of the map image from open street maps height and width in pixels
        # This is a tuple, it will contain the x and y coords ready to be plotted on the map image.
        old = (self.points[2], self.points[0])
        new = (0, h_w[1])
        y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        old = (self.points[1], self.points[3])
        new = (0, h_w[0])
        x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        return int(x), h_w[1] - int(y)

    def get_ticks(self):
        # Creates custom ticks from the GPS Coords for matplotlib to output.
        self.x_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[1], self.points[3], num=7))
        y_ticks = map(
            lambda x: round(x,4),
            np.linspace(self.points[2], self.points[0], num=8))
        self.y_ticks = sorted(y_ticks, reverse=True)
        # Ticks have to be reversed as of the orientation of the image in matplotlib.
        # the image (0, 0) coord is in the upper left corner // coord system has (0,0) in the bottom left corner

