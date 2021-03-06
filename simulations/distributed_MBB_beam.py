from __future__ import print_function, division
from fenics import *

from elasticity.boundary_conditions import BoundaryConditions
from elasticity.utils import scale_mesh
from run_simulation import run_simulation


class DistributedMBBBoundaryConditions(BoundaryConditions):
    def get_fixed(self):
        width, height, tol = self.width, self.height, self.tol

        class BottomBoundary(SubDomain):
            """ Constrain the bottom to not move. """
            def inside(self, x, on_boundary):
                return ((near(x[0], 0.1, 2e1) or
                    near(x[0], width - 0.1, 2e1)) and near(x[1], 0, tol))
        return [BottomBoundary()]

    def get_forces(self):
        width, height, tol = self.width, self.height, self.tol

        class PointLoad(SubDomain):
            """ Add a point load to the top center. """
            def inside(self, x, on_boundary):
                return (near(x[0], width / 2.0, width / 4) and
                    near(x[1], height, tol))
        return [PointLoad()], [Constant((0.0, -2e-1))]

if __name__ == "__main__":
    width, height, tol = 600, 100, 5e-2
    bc = DistributedMBBBoundaryConditions(width, height, tol)
    mesh = Mesh("meshes/bridge-distributed-load.xml")
    scale_mesh(mesh, width, height)
    run_simulation(mesh, bc, "MBB/bridge-distributed-load-")
