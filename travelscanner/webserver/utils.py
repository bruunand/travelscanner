from flask import make_response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def make_response_from_figure(fig):
    # Get figure canvas and then write to a byte array in PNG format
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)

    # Make response from bytes
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response
