"""Synthetic independent analytic integration and gauge checks, no Q550 ODE."""
import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from defect_budget_math_v18_34 import integrate_budget,segment_budget,first_crossing,unoriented_angle
class Tests(unittest.TestCase):
    def test_exact_constant_mu_source(self):
        t=np.linspace(0,1,81);mu=-np.ones_like(t);r=2*np.ones_like(t)
        C=3*np.exp(-t)+2*(1-np.exp(-t));D=mu*C+r
        b=integrate_budget(t,C,D,mu)
        self.assertLess(np.max(abs(b['pred_simp']-C)),2e-6)
        self.assertLess(np.max(abs(b['pred_trap']-C)),1e-4)
    def test_zero_source(self):
        t=np.linspace(0,1,81);mu=.25+0*t;C=2*np.exp(.25*t)
        b=integrate_budget(t,C,.25*C,mu)
        self.assertLess(max(abs(b['signed_simpson'])),1e-14)
    def test_sign_gauge_invariance(self):
        t=np.linspace(0,1,81);mu=-np.ones_like(t);C=np.cos(t);D=-np.sin(t)
        a=integrate_budget(t,C,D,mu);b=integrate_budget(t,-3*C,-3*D,mu)
        self.assertLess(max(abs(b['signed_simpson']+3*a['signed_simpson'])),1e-11)
    def test_piece_partition(self):
        t=np.linspace(0,1,81);C=1+t+t*t;D=1+2*t;mu=-np.ones_like(t);b=integrate_budget(t,C,D,mu)
        parts=[segment_budget(b,a,bb,1)['signed_to_T'] for a,bb in ((0,.1),(.1,.25),(.25,.5),(.5,1))]
        self.assertAlmostEqual(sum(parts),b['signed_simpson'][-1],places=11)
    def test_positive_negative_cancellation(self):
        t=np.linspace(0,1,81);C=np.sin(8*t);D=8*np.cos(8*t);mu=np.zeros_like(t)
        b=integrate_budget(t,C,D,mu)
        self.assertGreater(b['abs_contribution'][-1],abs(b['signed_simpson'][-1]))
    def test_crossing(self):
        self.assertEqual(first_crossing([0,.1,.2],[0,.5,2],1),.2)
        self.assertIsNone(first_crossing([0,.1],[0,.5],1))
    def test_normal_sign_gauge(self):
        g=np.array([1.,2.,3.]);h=np.array([2.,1.,3.])
        self.assertAlmostEqual(unoriented_angle(g,h),unoriented_angle(-3*g,h))
        self.assertAlmostEqual(unoriented_angle(g,h),unoriented_angle(g,-4*h))
    def test_metric_changes_angle(self):
        g=np.array([1.,2.,3.]);h=np.array([2.,1.,3.]);self.assertNotAlmostEqual(unoriented_angle(g,h),unoriented_angle(g,h,[.5,1.,2.]))
    def test_reject_bad_grid(self):
        with self.assertRaises(ValueError):integrate_budget([0,1,1,2,3],[1]*5,[1]*5,[1]*5)
    def test_time_varying_cofactor(self):
        t=np.linspace(0,1,81);mu=np.sin(t);M=1-np.cos(t);C=3*np.exp(M);D=mu*C
        b=integrate_budget(t,C,D,mu)
        self.assertLess(np.max(abs(b['signed_direct'])),1e-4)
    def test_inside_radius_flags(self):
        t=np.linspace(0,1,81);d=np.arange(81)/80*7
        self.assertLess(first_crossing(t,d,1),first_crossing(t,d,3))
if __name__=='__main__':unittest.main()
