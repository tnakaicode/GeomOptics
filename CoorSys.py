import numpy as np
import matplotlib.pyplot as plt

from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Trsf
from OCCUtils.Construct import vec_to_dir, dir_to_vec


def string_to_float(string):
    try:
        return float(string)
    except ValueError:
        if '-' in string[1:]:
            return float('E-'.join(string.rsplit('-', 1)))
        else:
            return float('E+'.join(string.rsplit('+', 1)))


def float_to_string(number):
    if number == 0 or abs(np.log10(abs(number))) < 100:
        return ' {: 0.10E}'.format(number)
    else:
        return ' {: 0.10E}'.format(number).replace('E', '')


def pnt_to_xyz(p):
    return p.X(), p.Y(), p.Z()


class Coord(object):
    """
    defne the coordinate axis
    used by position and two direction

    [name].cor
    file fomat
    line1: name
    line2: unit[mm]
    line3: gp_Pnt().X() gp_Pnt().Y() gp_Pnt().Z()
    line4: gp_Dir().X() gp_Dir().Y() gp_Dir().Z()
    line5: gp_Dir().X() gp_Dir().Y() gp_Dir().Z()
    """

    def __init__(self, name="surf", pxyz=[0, 0, 0], rxyz=[0, 0, 0]):
        self.name = name
        self.pxyz = pxyz
        self.rxyz = rxyz
        self.axis = gp_Ax3(gp_Pnt(*pxyz), gp_Dir(0, 0, 1))
        self.rotate(rxyz)

    def rotate(self, rxyz=[0, 0, 0]):
        for i, deg in enumerate(rxyz):
            if i == 0:
                axs = self.axis.Axis()
                axs.SetDirection(self.axis.XDirection())
            elif i == 1:
                axs = self.axis.Axis()
                axs.SetDirection(self.axis.YDirection())
            elif i == 2:
                axs = self.axis.Axis()
                axs.SetDirection(self.axis.Direction())
            else:
                axs = self.axis.Axis()
            self.axis.Rotate(axs, np.deg2rad(deg))

    def write_file(self, name=None, filename="pln.cor"):
        if name == None:
            name = self.name
        pnt = self.axis.Location()
        v_x = self.axis.XDirection()
        v_y = self.axis.YDirection()

        fp = open(filename, "w")
        fp.write(' {:s}\n'.format(name))
        fp.write(' {:s}\n'.format("mm"))
        fp.write(''.join([float_to_string(v) for v in pnt_to_xyz(pnt)]) + '\n')
        fp.write(''.join([float_to_string(v) for v in pnt_to_xyz(v_x)]) + '\n')
        fp.write(''.join([float_to_string(v) for v in pnt_to_xyz(v_y)]) + '\n')
        fp.close()

    def read_file(self, axs=gp_Ax3(), name=None, filename="pln.cor"):
        if name == None:
            name = self.name
        dat = np.loadtxt(filename, skiprows=2)
        pnt = gp_Pnt(*dat[0])
        d_x = gp_Dir(*dat[1])
        d_y = gp_Dir(*dat[2])
        d_z = d_x.Crossed(d_y)
        trf = gp_Trsf()
        trf.SetTransformation(axs, gp_Ax3())
        self.axis = gp_Ax3(pnt, d_z, d_x)
        self.axis.Transform(trf)


if __name__ == "__main__":
    obj = Coord()
    obj.write_file(filename="pln1.cor")
    obj.read_file()
