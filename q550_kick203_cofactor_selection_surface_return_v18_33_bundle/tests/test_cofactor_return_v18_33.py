"""Independent numerical-regression checks, not original Q550 results."""
import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from cofactor_return_math_v18_33 import *
from manifold_math_v18_32 import features,score_residual,project_to_level
class CofactorTests(unittest.TestCase):
    def test_singular_trap_no_longer_selected(self):
        a=[dict(id='fake',phase=False,feature_count=10,train_relative_residual=1.,objective=1e-15),
           dict(id='real',phase=False,feature_count=10,train_relative_residual=.001,objective=1e-8)]
        self.assertEqual(training_rank(a)[0]['id'],'real')
    def test_rank_never_consults_holdout(self):
        a=[dict(id='a',phase=False,feature_count=10,train_relative_residual=.2,holdout=0.),
           dict(id='b',phase=False,feature_count=10,train_relative_residual=.1,holdout=99.)]
        self.assertEqual(training_rank(a)[0]['id'],'b')
    def test_tie_by_dimension_and_name(self):
        a=[dict(id='a',phase=True,feature_count=65,train_relative_residual=.1),
           dict(id='b',phase=True,feature_count=10,train_relative_residual=.1)]
        self.assertEqual(training_rank(a)[0]['id'],'b')
    def test_duplicate_candidates_fail(self):
        a=[dict(id='x',feature_count=10,train_relative_residual=.1)]*2
        with self.assertRaises(ValueError):training_rank(a)
    def test_nonfinite_training_score_fails(self):
        with self.assertRaises(ValueError):training_rank([dict(id='x',feature_count=10,train_relative_residual=np.nan)])
    def test_gauge_sign_same_normal(self):
        a=np.array([1.,3.,-4.]);self.assertAlmostEqual(gauge_agnostic_normal_angle(a,-a),0.)
    def test_orthogonal_normal_different(self):
        self.assertAlmostEqual(gauge_agnostic_normal_angle(np.array([1.,0.]),np.array([0.,1.])),90.)
    def test_constraint_cofactor_correct(self):
        q=np.zeros(10);q[0]=1.;y=np.zeros(11);y[0]=.4;f=np.zeros(11);f[0]=-.5*y[0]
        self.assertAlmostEqual(score_residual(y,f,q,np.zeros(10),np.ones(10),0.,-.5,0.,1,False),0.)
    def test_clock_return_not_material(self):
        result=phase_clock_return(2*np.pi)
        self.assertTrue(result['phase_cycle_only']);self.assertFalse(result['material_recurrence_certified'])
    def test_wrong_phase_cycle_rejected(self):
        self.assertFalse(phase_clock_return(2*np.pi+.2)['phase_cycle_only'])
    def test_surface_failure_when_no_certified_return(self):
        self.assertFalse(surface_accept(.0001,0.,0.,0.,0.,0.,0.))
    def test_overlap_is_independent_numeric_gate(self):
        self.assertFalse(surface_accept(0.,0.,0.,0.,0.,15.,0.))
        self.assertFalse(surface_accept(0.,0.,0.,0.,0.,0.,.1))
        self.assertTrue(surface_accept(0.,0.,0.,0.,0.,1.,.001))
    def test_surface_math_no_phase_only_terms(self):
        y=np.zeros(11);y[10]=.8
        self.assertTrue(np.all(features(y,np.zeros(10),np.ones(10),0.,2,True)==0))
    def test_projection_normalized_metric(self):
        y=np.zeros(11);y[0]=.2;q=np.zeros(10);q[0]=1.
        z,_,ok=project_to_level(y,q,np.zeros(10),np.ones(10),0.,1,False)
        self.assertTrue(ok);self.assertLess(abs(z[0]),1e-10)
    def test_original_short_flow_cofactor_and_clock(self):
        from original_cofactor_surface_return_v18_33 import stream_return
        y=np.zeros(11);y[0]=.2
        q=np.zeros(10);q[0]=1.
        def field(t,y):
            out=np.zeros(11);out[0]=-.5*y[0];out[10]=2*np.pi;return out
        opts=dict(degree=1,phase=False,lam=-.5,mod=0.)
        rows=stream_return(field,y,opts,q,np.zeros(10),np.ones(10),0.,3.5)
        self.assertEqual(len(rows),3)
        self.assertLess(max(x['abs_transport_residual'] for x in rows),1e-10)
        self.assertTrue(rows[-1]['phase_cycle_only'])
        self.assertFalse(rows[-1]['material_recurrence_certified'])
        self.assertGreater(rows[-1]['material_displacement_scaled'],.01)
    def test_analytic_cofactor_transport(self):
        from scipy.integrate import solve_ivp
        lam=-.5;y0=.33
        sol=solve_ivp(lambda t,y:[lam*y[0]],(0,1),[y0],t_eval=[0,1],rtol=1e-13,atol=1e-14)
        self.assertAlmostEqual(sol.y[0,-1],y0*np.exp(lam),places=11)
if __name__=='__main__':unittest.main()
