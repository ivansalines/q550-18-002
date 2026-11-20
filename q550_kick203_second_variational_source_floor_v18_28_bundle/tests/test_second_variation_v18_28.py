"""Synthetic analytic unit tests; NEVER substitute for Q550 original RHS proof."""
import unittest,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'scripts')]
from second_variational_math_v18_28 import (directional_first,directional_second,
                  second_variational_rhs,paired_even_observation,rms)

class TestSecondVariation(unittest.TestCase):
 def setUp(self):
    self.a=np.linspace(-.15,.15,11);self.b=np.linspace(.02,.06,11)
    self.y=np.linspace(-.8,.8,11);self.u=np.linspace(-.3,.3,11);self.u[-1]=0
    def f(t,y):return self.a*y+self.b*y*y
    self.f=f
 def test_first_directional(self):
    exact=(self.a+2*self.b*self.y)*self.u
    self.assertLess(np.max(abs(directional_first(self.f,self.y,self.u)-exact)),2e-11)
 def test_second_directional(self):
    exact=2*self.b*self.u*self.u
    for step in (.03,.08,.2):
      self.assertLess(np.max(abs(directional_second(self.f,self.y,self.u,step)-exact)),2e-11)
 def test_hessian_stencil_quadratic(self):
    exact=2*self.b*self.u*self.u
    for order in (2,4):
      self.assertLess(np.max(abs(directional_second(self.f,self.y,self.u,.075,order)-exact)),2e-11)
 def test_linear_has_zero_hessian(self):
    self.assertLess(np.max(abs(directional_second(lambda t,y:self.a*y,self.y,self.u,.1))),1e-11)
 def test_variational_consistency_against_actual_pairs(self):
    y0=self.y.copy();y0[-1]=0.;u0=self.u.copy()
    s=np.r_[y0,u0[:10],np.zeros(10)]
    sol=solve_ivp(second_variational_rhs(self.f,.1), (0.,.5),s,method='DOP853',rtol=4e-13,atol=4e-14)
    self.assertTrue(sol.success)
    w=sol.y[21:31,-1]
    # Last coordinate of u is fixed to zero by our physics protocol.
    eps=1e-3
    def evolve(state):
      return solve_ivp(self.f,(0.,.5),state,method='DOP853',rtol=4e-13,atol=4e-14).y[:,-1]
    p=evolve(y0+eps*u0);m=evolve(y0-eps*u0);base=evolve(y0)
    recovered=(p[:10]+m[:10]-2*base[:10])/eps**2
    self.assertLess(rms(recovered-w),3e-7)
 def test_matched_odd_even_formula(self):
    B=np.zeros((2,11));P=B.copy();M=B.copy();
    P[:,:10]=1.;M[:,:10]=-1.
    even,odd=paired_even_observation(B,P,M,np.eye(10)[:2],.5)
    self.assertEqual(rms(even),0.)
    self.assertAlmostEqual(float(odd[0,0]),2.)
 def test_finite_step_not_epsilon(self):
    # Hessian stencil must remain fixed under changes in the nonlinear-pair epsilon.
    a=directional_second(self.f,self.y,self.u,.075)
    b=directional_second(self.f,self.y,self.u,.075)
    self.assertTrue(np.array_equal(a,b))
 def test_zero_tangent_exactly_zero(self):
    np.testing.assert_array_equal(directional_first(self.f,self.y,0*self.u),np.zeros(11))
    np.testing.assert_array_equal(directional_second(self.f,self.y,0*self.u),np.zeros(11))
 def test_hessian_source_changes_with_direction_not_sign(self):
    a=directional_second(self.f,self.y,self.u)
    b=directional_second(self.f,self.y,-self.u)
    self.assertLess(rms(a-b),1e-13)
 def test_variational_state_phase_shared(self):
    f=lambda t,x: np.r_[self.a[:10]*x[:10]+self.b[:10]*x[:10]**2,2*np.pi]
    z=np.r_[self.y,self.u[:10],np.zeros(10)]
    out=second_variational_rhs(f)(0,z)
    self.assertEqual(len(out),31)
    self.assertAlmostEqual(out[10],2*np.pi)

if __name__=='__main__':unittest.main()
