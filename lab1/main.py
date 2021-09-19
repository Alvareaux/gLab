# External
import numpy as np
from matplotlib import pyplot as plt

# Internal
from lab1.module.builder import Builder

# ---------------------------------------------------------------------------------------------------------------------

pi = np.pi


class Figure:
    builder = None

    # ------------------------------------
    # Surface and global params
    surf_width = 800
    surf_height = 800

    d = 25

    d_width = int(surf_width / 2)
    d_height = int(surf_height / 2)

    bg_color = (255, 255, 255)  # White
    st_color = (0, 0, 0)  # Black
    st_width = 2

    center = (d_width, d_height)

    # ------------------------------------
    # Local params
    #  Perimeter
    class Perimeter:
        class UpperArc:
            angle_start = 1 / 1 * pi
            angle_end = 3 / 2 * pi
            delta_radius = 30

        class Arc:
            pass

    #  Circle
    class Circle:
        radius = 40

    #  Big arc
    class BigArc:
        radius = 70  # r2 > r1
        delta_radius = 30
        angle_start = 1 / 8 * pi
        angle_end = 3 / 4 * pi

    # ------------------------------------

    def __init__(self):
        figure = self.build_figure()
        self.show_figure(figure)

    def build_figure(self):
        self.builder = Builder(self.surf_width, self.surf_height, self.bg_color, self.st_color, self.st_width)

        self.__perimeter()

        self.__centre_circle()
        self.__big_arc()

        return self.builder.get_image()

    def show_figure(self, data):
        # Basic fig
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.grid()

        # X and Y axis tick
        plt.xticks(np.arange(-self.d_width, self.d_width, self.d), rotation=90)
        plt.yticks(np.arange(-self.d_height, self.d_height, self.d))

        # Image display and axis transformation from (0, width/height) to (-d_width/d_height, d_width/-d_height)
        ax.imshow(data, interpolation='nearest', extent=(-self.d_width, self.d_width, self.d_height, -self.d_height))
        fig.show()

    # -----------------------------------------------------------------------------------------------------------------
    # Circle

    # -----------------------------------------------------------------------------------------------------------------
    # Circle
    def __centre_circle(self):
        circle = self.builder.build_circle(r=self.Circle.radius,
                                           xy=self.center, stroke=self.st_color, stroke_width=self.st_width)

    # -----------------------------------------------------------------------------------------------------------------
    # Big arc
    def __big_arc(self):
        self.__inside_arc()
        self.__outside_arc()
        self.__left_line()
        self.__right_line()

    def __inside_arc(self):
        self.builder.build_arc(r=self.BigArc.radius,
                               a1=self.BigArc.angle_start, a2=self.BigArc.angle_end,
                               xy=self.center)

    def __outside_arc(self):
        self.builder.build_arc(r=self.BigArc.radius + self.BigArc.delta_radius,
                               a1=self.BigArc.angle_start, a2=self.BigArc.angle_end,
                               xy=self.center)

    def __left_line(self):
        line_left_upper_x = self.BigArc.radius * np.cos(self.BigArc.angle_start) + self.d_width
        line_left_upper_y = self.BigArc.radius * np.sin(self.BigArc.angle_start) + self.d_height

        line_left_lower_x = (self.BigArc.radius + self.BigArc.delta_radius) * \
                            np.cos(self.BigArc.angle_start) + self.d_width
        line_left_lower_y = (self.BigArc.radius + self.BigArc.delta_radius) * \
                            np.sin(self.BigArc.angle_start) + self.d_height

        self.builder.build_line(points=[
            (line_left_upper_x, line_left_upper_y),
            (line_left_lower_x, line_left_lower_y)
        ])

    def __right_line(self):
        line_right_upper_x = self.BigArc.radius * np.cos(self.BigArc.angle_end) + self.d_width
        line_right_upper_y = self.BigArc.radius * np.sin(self.BigArc.angle_end) + self.d_height

        line_right_lower_x = (self.BigArc.radius + self.BigArc.delta_radius) * \
                             np.cos(self.BigArc.angle_end) + self.d_width
        line_right_lower_y = (self.BigArc.radius + self.BigArc.delta_radius) * \
                             np.sin(self.BigArc.angle_end) + self.d_height

        self.builder.build_line(points=[
            (line_right_upper_x, line_right_upper_y),
            (line_right_lower_x, line_right_lower_y)
        ])

    # -----------------------------------------------------------------------------------------------------------------
    # Perimeter
    #  Upper arc

    def __perimeter(self):
        self.__upper_arc()
        lower_endpoint = self.__arc_line_lower()
        upper_endpoint = self.__arc_line_upper()

    def __upper_arc(self):
        self.builder.build_arc(r=self.Circle.radius + self.Perimeter.UpperArc.delta_radius,
                               a1=self.Perimeter.UpperArc.angle_start, a2=self.Perimeter.UpperArc.angle_end,
                               xy=self.center)

    def __arc_line_lower(self):
        x = self.d_width - (self.Circle.radius + self.Perimeter.UpperArc.delta_radius)
        self.builder.build_line(points=[
            (x, self.d_height),
            (x, self.d_height + self.Circle.radius)
        ])

        return x, self.d_height + self.Circle.radius

    def __arc_line_upper(self):
        y = self.d_height - (self.Circle.radius + self.Perimeter.UpperArc.delta_radius)
        line_u = self.builder.build_line(points=[
            (self.d_width, y),
            (self.d_width + self.Circle.radius / 2, y)
        ])

        return self.d_width + self.Circle.radius / 2, y

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    fig = Figure()
