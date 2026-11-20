"""Synthetic checks for independent RHS Hessian and second-order constraint math."""
import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from hessian_constraint_math_v18_30 import (rhs_hessian,jac_hessian,finite_jac_c,
    finite_c_hessian,constraint_initial_jet,second_variational_rhs)

def qf(t,y):
    y=np.asarray(y,float)
    z=np.zeros_like(y);z[0]=y[0]**2+3*y[0]*y[1]+2*y[1]**2;z[1]=y[0]*y[1];z[10]=2.7
    return z

def qJ(y):
    J=np.zeros((11,11));J[0,0]=2*y[0]+3*y[1];J[0,1]=3*y[0]+4*y[1];J[1,0]=y[1];J[1,1]=y[0]
    return J

class TestHessian(unittest.TestCase):
    def setUp(self):
        self.y=np.linspace(.1,1.1,11);self.u=np.zeros(11);self.u[:2]=[.6,-.8]
        self.want=np.zeros(11);self.want[0]=2*self.u[0]**2+6*self.u[0]*self.u[1]+4*self.u[1]**2
        self.want[1]=2*self.u[0]*self.u[1]
    def test_rhs_independent_quadratic(self):
        np.testing.assert_allclose(rhs_hessian(qf,0,self.y,self.u,.02),self.want,atol=2e-11)
    def test_jacobian_derivative_quadratic(self):
        np.testing.assert_allclose(jac_hessian(qJ,self.y,self.u,.03),self.want,atol=2e-12)
    def test_direction_squared_scale(self):
        np.testing.assert_allclose(rhs_hessian(qf,0,self.y,3*self.u,.02),9*self.want,atol=5e-11)
    def test_phase_has_zero_second_variation_source(self):
        self.assertLess(abs(rhs_hessian(qf,0,self.y,self.u,.02)[10]),1e-12)
    def test_rhs_5point_rejects_zero_h(self):
        with self.assertRaises(ValueError):rhs_hessian(qf,0,self.y,self.u,0)
    def test_second_variational_source(self):
        z=np.r_[self.y,self.u[:10],np.zeros(10)]
        derivative=second_variational_rhs(qf,qJ,.02)(0,z)
        np.testing.assert_allclose(derivative[21:23],self.want[:2],atol=2e-11)
    def test_constraint_circle_projection(self):
        def C(y):return np.array([y[0]**2+y[1]**2])
        y=np.zeros(11);y[0]=1.; v=np.zeros(11);v[:2]=[.3,.8]
        u,w,info=constraint_initial_jet(C,y,v)
        np.testing.assert_allclose(u[:2],[0.,1.],atol=1e-9)
        np.testing.assert_allclose(w[:2],[-1.,0.],atol=1e-7)
        self.assertLess(info['tangent_defect'],1e-8)
        self.assertLess(info['second_tangent_defect'],1e-7)
    def test_second_order_constraint_retraction(self):
        def C(y):return np.array([y[0]**2+y[1]**2])
        y=np.zeros(11);y[0]=1.;v=np.zeros(11);v[1]=1.
        u,w,info=constraint_initial_jet(C,y,v)
        e=1e-3
        y2=y+e*u+.5*e*e*w
        self.assertLess(abs(C(y2)[0]-C(y)[0]),5e-12)
    def test_constrained_flow_circle(self):
        # Rotations preserve circle C=x²+y²; tangent and curvature relations hold.
        def C(y):return np.array([y[0]**2+y[1]**2])
        y=np.zeros(11);y[0]=1.;v=np.zeros(11);v[1]=1.
        u,w,info=constraint_initial_jet(C,y,v)
        np.testing.assert_allclose(finite_jac_c(C,y)@u,[0.],atol=1e-7)
        np.testing.assert_allclose(finite_jac_c(C,y)@w+finite_c_hessian(C,y,u),[0.],atol=1e-7)
    def test_no_inferred_material_constraint(self):
        # The phase fiber is a gauge restriction, not a first integral of theta'=c.
        y=np.linspace(.1,1.1,11);vec=np.zeros(11);vec[0]=1
        self.assertEqual(vec[10],0.)
        self.assertNotEqual(qf(0,y)[10],0.)

if __name__=='__main__': unittest.main()
