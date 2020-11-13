from mikeio.spatial import min_horizontal_dist_meters, dist_in_meters, Grid2D
from mikeio.dfsu import Mesh
import numpy as np
import os


def test_dist_in_meters():

    np.random.seed = 42
    n = 100
    lon = np.random.uniform(low=-179, high=179, size=n)
    lat = np.random.uniform(low=-89, high=89, size=n)
    coords = np.vstack([lon, lat]).T
    poi = [0.0, 0.0]
    dist = dist_in_meters(coords, poi, is_geo=True)
    print(dist.max)
    assert dist.shape == (n,)
    assert dist.max() < 20040000


def test_min_horizontal_dist_meters():
    n = 11
    lon = np.linspace(0, 10, n)
    lat = np.linspace(50, 52, n)
    coords = np.vstack([lon, lat]).T

    lon = np.linspace(0, 10, 3)
    lat = np.linspace(52, 54, 3)
    targets = np.vstack([lon, lat]).T

    min_d = min_horizontal_dist_meters(coords, targets, is_geo=True)
    assert min_d.shape == (n,)
    assert min_d[0] == 222389.85328911748


def test_x_y():
    x0 = 2.0
    x1 = 8.0
    nx = 4
    dx = 2.0
    x = np.linspace(x0, x1, nx)
    y0 = 3.0
    y1 = 5
    ny = 3
    dy = 1.0
    y = np.linspace(y0, y1, ny)
    g = Grid2D(x, y)
    assert g.x0 == x0
    assert g.x1 == x1
    assert g.y0 == y0
    assert g.y1 == y1
    assert np.all(g.x == x)
    assert np.sum(g.y - y) == 0
    assert g.nx == nx
    assert g.ny == ny
    assert g.dx == dx
    assert g.dy == dy

    # BoundingBox(left, bottom, right, top)
    # Is this test good, or just a copy of the implementation?
    assert g.bbox == ((x0 - dx / 2), (y0 - dy / 2), (x1 + dx / 2), (y1 + dy / 2))


def test_xx_yy():
    nx = 4
    ny = 3
    x = np.linspace(1, 7, nx)
    y = np.linspace(3, 5, ny)
    g = Grid2D(x, y)
    assert g.n == nx * ny
    assert g.xx[0, 0] == 1.0
    assert g.yy[-1, -1] == 5.0
    assert np.all(g.xy[1] == [3.0, 3.0])


def test_create_in_bbox():
    bbox = [0, 0, 1, 5]
    shape = (2, 5)
    g = Grid2D(bbox=bbox, shape=shape)
    assert g.x0 == 0.25

    g = Grid2D(bbox)
    assert g.nx == 10
    assert g.ny == 50

    dx = 0.5
    g = Grid2D(bbox, dx=dx)
    assert g.dx == dx
    assert g.dy == dx
    assert g.n == 20

    dxdy = (0.5, 2.5)
    g = Grid2D(bbox, dx=dxdy)
    assert g.dx == dxdy[0]
    assert g.dy == dxdy[1]
    assert g.n == 4


def test_contains():
    bbox = [0, 0, 1, 5]
    g = Grid2D(bbox)
    xy1 = [0.5, 0.5]
    xy2 = [1.5, 0.5]
    assert g.contains(xy1)
    assert not g.contains(xy2)

    xy = np.vstack([xy1, xy2])
    inside = g.contains(xy)
    assert inside[0]
    assert not inside[1]


def test_to_mesh():
    outfilename = "temp.mesh"

    g = Grid2D([0, 0, 1, 5])
    g.to_mesh(outfilename)

    assert os.path.exists(outfilename)
    mesh = Mesh(outfilename)
    assert mesh.n_elements == g.n
    os.remove(outfilename)  # clean up


def test_xy_to_bbox():
    bbox = [0, 0, 1, 5]
    g = Grid2D(bbox)
    xy = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0, 5], [1, 5]], dtype=float)
    bbox2 = Grid2D.xy_to_bbox(xy)
    assert bbox[0] == bbox2[0]
    assert bbox[-1] == bbox2[-1]

    bbox2 = Grid2D.xy_to_bbox(xy, buffer=0.2)
    assert bbox2[0] == -0.2
    assert bbox2[3] == 5.2

