import numpy as np
from scipy.spatial.transform import Rotation as R

class Vec3D():
    # x=0., y=0.,z=0.
    # 3 coordinates, rotation, projection
    def __init__(self, x=None, y=None, z=None, coord=None):
        if coord is None and all(isinstance(comp, (int, float)) for comp in (x, y, z)): 
            self.coord = np.array([x, y, z])    
        elif all(comp is None for comp in (x, y, z)) and \
             all(isinstance(val, (int, float)) for val in coord) and\
             len(coord) == 3:
            self.coord = np.array(coord)
        else:
            raise ValueError('Coordinates of the vector must be provided wheather as xyz-components or as a list.')
        

    @property
    def x(self):
        return self.coord[0]        

    @property
    def y(self):
        return self.coord[1]        

    @property
    def z(self):
        return self.coord[2]

    def __str__(self, prec=2):
        return f"vector x, y, z = ({self.x:.{prec}f}, {self.y:.{prec}f}, {self.z:.{prec}f})"

    def rot_euler(self, ax_seq=None, angles=None, in_degrees=True):
        if not (isinstance(ax_seq, str) and 3 >= len(ax_seq) >= 1):
            raise(ValueError('ax_seq should be string of "xyzXYZ" of length 1 to 3'))
        if not all(isinstance(val, (int, float)) for val in angles):
            raise(ValueError('Values of the rotation angles should be provided.'))
        if not isinstance(in_degrees, bool):
            raise(ValueError('Unit values of the rotation angles should be provided as boolean (deg = True, rad = False).'))
        if len(ax_seq) != len(angles):
            raise(ValueError('Lengthes of axis sequence and angles list must be the same.'))
        rot = R.from_euler(ax_seq, angles, degrees=in_degrees)
        
        return Vec3D(coord=rot.apply(self.coord))

    @property
    def proj_yz(self):
        return self.y, self.z

            
class RectYZ():
    # yl=0., zl=0., yu=0.1, zu=0.1
    # rectangle for transmission integrantion
    def __init__(self, yl=None, zl=None, yu=None, zu=None):
        if not all(isinstance(val, (int, float)) for val in (yl, zl, yu, zu)): 
            raise ValueError('Coordinates of rectangle corners should be float.')
        if yl >= yu or zl >= zu:
            raise ValueError('Wrong order of the coordinats: lower one must be less then upper one.')
        self.yl = yl
        self.zl = zl
        self.yu = yu
        self.zu = zu
        
    def __str__(self):
        info = f"lower y, z = ({self.yl},{self.zl}), upper y, z = ({self.yu},{self.zu})"
        return info
    

if __name__ == '__main__':
    test_rect = RectYZ(0., 0., 1., 1.)
    print(test_rect)
    
    test_vec = Vec3D(0.3, 0., 0.)
    print(test_vec)
    
    rot_vec = test_vec.rot_euler('xyz', [90., 45., 45.])
    print(rot_vec)
    print(f' which yz-projection is {rot_vec.proj_yz}')
    
