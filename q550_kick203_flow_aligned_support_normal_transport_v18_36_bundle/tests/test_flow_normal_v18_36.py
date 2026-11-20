"""Synthetic and provenance safety checks for v18.36."""
import unittest,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from flow_normal_math_v18_36 import scaled_jacobian,transport_rhs,unit,tangent_to,normal_angle,first_exit,source_budget
class TestMath(unittest.TestCase):
    def test_scaled_jac(self):
        A=np.diag([2.,3.]+[0.]*8);s=np.array([2.,5.]+[1.]*8)
        self.assertAlmostEqual(scaled_jacobian(A,s)[0,0],2.)
    def test_dual_pairing(self):
        rng=np.random.default_rng(33);B=rng.normal(size=(10,10));m=rng.normal(size=10);u=rng.normal(size=10)
        dm,du=transport_rhs(B,m,u);self.assertAlmostEqual(float(dm@u+m@du),0.,places=11)
    def test_tangent(self):
        n=unit(np.arange(1.,11.));t=tangent_to(n,np.roll(n,1));self.assertLess(abs(n@t),1e-14)
    def test_orthogonal_normal_gauge(self):
        n=np.arange(1.,11.);self.assertLess(normal_angle(n,-3*n),1e-5)
    def test_nontrivial_candidate_mismatch(self):
        m=np.zeros(10);m[0]=1;n=np.zeros(10);n[1]=1
        self.assertAlmostEqual(normal_angle(m,n),90.,places=9)
    def test_initial_outside(self):
        self.assertEqual(first_exit([0.,.1],[2.,3.],1.,lambda t:2.)[0],'OUTSIDE_AT_START')
    def test_later_exit(self):
        status,t=first_exit(np.linspace(0.,1.,9),np.linspace(0.,2.,9),1.,lambda t:2*t)
        self.assertEqual(status,'CROSSED_AFTER_START');self.assertAlmostEqual(t,.5)
    def test_no_exit(self):
        self.assertEqual(first_exit([0.,1.],[0.,.2],1.,lambda t:.2*t)[0],'NO_EXIT_OBSERVED')
    def test_budget(self):
        t=np.array([0.,.2,.3]);z=np.ones(3)
        np.testing.assert_allclose(source_budget(0.,-1.,t,z),np.exp(-t))
    def test_exact_invariant_synthetic_normal(self):
        # An invariant coordinate surface maintains its normal direction.
        B=np.diag([-.3,.2]+[0.]*8)
        m=np.zeros(10);m[0]=1.
        u=np.zeros(10);u[1]=1.
        from scipy.integrate import solve_ivp
        def rhs(t,x):
            dm,du=transport_rhs(B,x[:10],x[10:]);return np.r_[dm,du]
        sol=solve_ivp(rhs,(0.,1.),np.r_[m,u],rtol=1e-11,atol=1e-13)
        self.assertTrue(sol.success)
        self.assertLess(normal_angle(sol.y[:10,-1],m),1e-5)
        self.assertLess(abs(sol.y[:10,-1]@sol.y[10:,-1]),1e-10)
    def test_projection_inside_training_support(self):
        from original_flow_normal_v18_36 import projected_independent_seed
        ref=np.zeros(11);center=np.zeros(10);scale=np.ones(10)
        q=np.r_[1.,np.zeros(9)]
        for branch in (0,1):
            z,record=projected_independent_seed(ref,q,center,scale,0.,dict(degree=1,phase=False),.8,np.random.default_rng(36),branch)
            self.assertLess(abs(z[0]),1e-9)
            self.assertLess(np.linalg.norm(z[:10]),.64)
            self.assertLess(abs(z[10]),.2)
            self.assertTrue(record[-1]['in_support'])
    def test_scale_invariance(self):
        n=np.arange(1.,11.);m=np.roll(n,1)
        self.assertAlmostEqual(normal_angle(n,m),normal_angle(n*3,m*-2))
if __name__=='__main__':unittest.main()
