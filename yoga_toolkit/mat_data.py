""" every point in yoga mat"""
class mat_point:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f"heatPoint(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

""" yoga_mat data"""
class mat_data:
    def __init__(self, points = [], center = mat_point(0,0,0,0)):
        self.center = center
        self.point_count = len(points)
        self.points = points

    def __str__(self):
        foot_points_str = ", ".join(str(point) for point in self.points)
        return (f"heatmap(foot_count={self.point_count}\n"
                f"foot_points_str=[{foot_points_str}]")

