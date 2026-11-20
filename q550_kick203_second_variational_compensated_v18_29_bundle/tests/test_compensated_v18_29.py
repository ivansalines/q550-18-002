"""Mathematical tests: Jacobian-integral identity, compensated even/odd, and gauge."""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from scipy.integrate import solve_ivp
from compensated_math_v18_29 import *

class TestCompensated(unittest.TestCase):
 def setUp(self):
  self.y=np.zeros(11);self.y[0]=4200.;self.y[1]=.01;self.y[10]=.5
  def f(t,y):
   v=np.zeros(11);v[0]=.02*y[0]+1.5*y[1]**2+0.3*y[1]**3
   v[1]=.13*y[1]-.4*y[1]**2;v[10]=1.;return v
  def J(y):
   v=np.zeros((11,11));v[0,0]=.02;v[0,1]=3*y[1]+.9*y[1]**2
   v[1,1]=.13-.8*y[1];return v
  self.f=f;self.J=J
 def test_exact_line_quadrature_polynomial(self):
  d=np.zeros(11);d[0]=.3;d[1]=.4
  exact=self.f(0.,self.y+d)-self.f(0.,self.y)
  got=line_increment(self.J,self.y,d,3)
  self.assertLess(np.max(abs(exact-got)),1e-11)
 def test_direct_jac_second(self):
  u=np.zeros(11);u[1]=2.
  expected=np.zeros(11);expected[0]=(3.+1.8*self.y[1])*4.;expected[1]=-.8*4.
  for h in [.002,.01,.05]:
   self.assertLess(np.max(abs(direct_second_from_jac(self.J,self.y,u,h)-expected)),1e-9)
 def test_compensated_integrates_true_futures(self):
  u0=np.zeros(10);u0[1]=1.;eps=1e-5
  state=np.r_[self.y,eps*u0,-eps*u0]
  q=solve_ivp(compensated_rhs(self.f,self.J,eps,3),(0.,.8),state,rtol=1e-12,atol=1e-14)
  yp=solve_ivp(self.f,(0.,.8),self.y+np.r_[eps*u0,0.],rtol=1e-12,atol=1e-14)
  ym=solve_ivp(self.f,(0.,.8),self.y-np.r_[eps*u0,0.],rtol=1e-12,atol=1e-14)
  yb=solve_ivp(self.f,(0.,.8),self.y,rtol=1e-12,atol=1e-14)
  self.assertLess(np.max(abs(q.y[:11,-1]-yb.y[:,-1])),1e-8)
  self.assertLess(np.max(abs(q.y[11:21,-1]-(yp.y[:10,-1]-yb.y[:10,-1]))),3e-9)
  self.assertLess(np.max(abs(q.y[21:31,-1]-(ym.y[:10,-1]-yb.y[:10,-1]))),3e-9)
 def test_small_eps_second_variation_finite_pair(self):
  u0=np.zeros(10);u0[1]=1.;H=np.eye(10)[:2]
  for eps in [1e-5,1e-6]:
   base=np.r_[self.y,eps*u0,-eps*u0]
   pair=solve_ivp(compensated_rhs(self.f,self.J,eps,3),(0.,.5),base,rtol=1e-12,atol=2e-14)
   v0=np.r_[self.y,u0,np.zeros(10)]
   v=solve_ivp(jacobian_variational_rhs(self.f,self.J,.01),(0.,.5),v0,rtol=1e-12,atol=2e-14)
   z=pair.y[:,-1].reshape(1,-1)
   measured,_=even_odd_from_deltas(z,eps,H)
   predicted=.5*eps*(v.y[21:31,-1]@H.T)
   self.assertLess(np.linalg.norm(measured.ravel()-predicted)/max(np.linalg.norm(predicted),1e-20),.002)
 def test_perturbed_phase_exact(self):
  u=np.zeros(10);u[1]=1.;eps=1e-6
  q=solve_ivp(compensated_rhs(self.f,self.J,eps,3),(0.,.5),np.r_[self.y,eps*u,-eps*u])
  self.assertEqual(len(q.y),31)
 def test_prevent_big_state_even_cancellation(self):
  y=4200.;eps=1e-7; a=1e-7;b=3.2e-14
  conventional=((y+a+b)+(y-a+b)-2*y)/(2*eps)
  compensated=((a+b)+(-a+b))/(2*eps)
  self.assertLess(abs(compensated-b/eps),1e-14)
  self.assertGreater(abs(conventional-compensated),1e-8)
 def test_identical_clock_jacobian_integral(self):
  d=np.zeros(11);d[1]=.5
  self.assertEqual(line_increment(self.J,self.y,d)[10],0.)
 def test_even_odd_normalization(self):
  z=np.zeros((2,31));eps=1e-4
  z[:,11]=eps+.5*eps**2*2;z[:,21]=-eps+.5*eps**2*2
  H=np.zeros((1,10));H[0,0]=1
  e,o=even_odd_from_deltas(z,eps,H)
  self.assertLess(abs(e[0,0]-eps),1e-12)
  self.assertAlmostEqual(o[0,0],1.,places=10)
 def test_gauge_invariant_observable(self):
  z=np.zeros((1,31));z[0,11:13]=[.02,.03];z[0,21:23]=[-.01,-.03]
  H=np.eye(10)[:2];e,o=even_odd_from_deltas(z,.01,H)
  Q=np.array([[0.,-1.],[1.,0.]])
  e2,o2=even_odd_from_deltas(z,.01,Q@H)
  self.assertLess(np.max(abs(e2-e@Q.T)),1e-14)
  self.assertLess(np.max(abs(o2-o@Q.T)),1e-14)
if __name__=='__main__':unittest.main()
