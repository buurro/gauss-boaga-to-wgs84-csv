import pyproj
import argparse
import csv

from pyproj.crs import CRS
from pyproj.transformer import Transformer

parser = argparse.ArgumentParser()
parser.add_argument("filename", metavar="filename", type=str, help="CSV Filename")
parser.add_argument(
    "-x", help="X column header. Defaults to 'X'", type=str, default="X"
)
parser.add_argument(
    "-y", help="Y column header. Defaults to 'Y'", type=str, default="Y"
)
parser.add_argument(
    "-d", "--delimiter", help="CSV Delimiter. Defaults to ';'", type=str, default=";"
)
args = parser.parse_args()

wgs84 = CRS("EPSG:4326")
gauss_boaga = CRS.from_proj4(
    "+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +towgs84=-104.1,-49.1,-9.9,0.971,-2.917,0.714,-11.68 +units=m +no_defs"
)
transformer = Transformer.from_crs(gauss_boaga, wgs84)

with open(args.filename, "r") as data:
    rows = [line for line in csv.DictReader(data, delimiter=args.delimiter)]


for r in rows:
    if r[args.x] and r[args.y]:
        x = float(r[args.x].replace(",", "."))
        y = float(r[args.y].replace(",", "."))
        r[args.x], r[args.y] = transformer.transform(x, y)


keys = rows[0].keys()
with open("out.csv", "w", newline="") as output_file:
    dict_writer = csv.DictWriter(output_file, keys, delimiter=args.delimiter)
    dict_writer.writeheader()
    dict_writer.writerows(rows)
