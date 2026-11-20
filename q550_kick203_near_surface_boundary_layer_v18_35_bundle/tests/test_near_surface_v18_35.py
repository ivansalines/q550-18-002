"""v18.35 unit/regression tests, no original Q550 ODE solve needed."""
import sys,unittest
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from near_surface_math_v18_35 import (microgrid,diagnostic_distance,nearest_training,
    classify_start_and_exit,refine_first_exit,calibration_radius,weighted_exact_budget)
class Tests(unittest.TestCase):
    def test_grid_micro_and_endpoint(self):
        t=microgrid();self.assertEqual(t[0],0.);self.assertEqual(t[-1],.0125);self.assertTrue(np.all(np.diff(t)>0));self.assertGreater(len(t),150)
    def test_fixed_reference_drift(self):
        s=np.r_[np.zeros(10),1.];moving=s.copy();moving[0]=900.;perturb=moving.copy();perturb[1]=.01
        self.assertGreater(diagnostic_distance(perturb,s,np.ones(10)),899)
        self.assertAlmostEqual(diagnostic_distance(perturb,moving,np.ones(10)),.01)
    def test_crossing_exact_root(self):
        t=np.linspace(0,.01,11);d=5*t/.01
        status,t0,a,b=refine_first_exit(t,d,2.,lambda x:500*x)
        self.assertEqual(status,'CROSSED_AFTER_START');self.assertAlmostEqual(t0,.004)
    def test_outside_at_start_is_not_exit(self):
        s,t0,a,b=refine_first_exit([0,.1],[2,3],1,lambda t:2+t)
        self.assertEqual(s,'OUTSIDE_AT_START');self.assertIsNone(t0)
    def test_no_exit(self):
        s,t0,a,b=refine_first_exit([0,.1],[.1,.3],1,lambda t:.1+t)
        self.assertEqual(s,'NO_EXIT_OBSERVED');self.assertIsNone(t0)
    def test_calibration_radius(self):
        a=np.zeros((3,11));a[:,0]=[0,.5,1.];cal=calibration_radius(a,np.zeros(11),np.ones(10))
        self.assertAlmostEqual(cal['radius_max'],1.);self.assertEqual(cal['sample_count'],3)
    def test_nearest_local_train(self):
        a=np.zeros((3,11));a[:,0]=[1.,3.,5.];x=np.zeros(11);x[0]=4.
        self.assertAlmostEqual(nearest_training(x,a,np.ones(10)),1.)
    def test_identity_integrated_source(self):
        # C'=mu C + r; mu=-1, constant r=2; C=2*(1-e^-t)
        t=np.linspace(0,.1,41);z=2*(np.exp(t)-1);C=2*(1-np.exp(-t))
        self.assertTrue(np.allclose(weighted_exact_budget(0,t,-1,z),C,rtol=1e-13,atol=1e-14))
    def test_distances_include_phase_neither(self):
        y=np.zeros(11);z=y.copy();z[10]=999.
        self.assertEqual(diagnostic_distance(y,z,np.ones(10)),0.)
    def test_training_ball_initial_condition(self):
        x=np.array([2.,3.]);t=np.array([0.,.01]);state,*_=classify_start_and_exit(t,x,1.)
        self.assertEqual(state,'OUTSIDE_AT_START')
if __name__=='__main__':unittest.main()
