"""Synthetic mathematical regression tests; no original-server Q550 run here."""
import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from manifold_math_v18_32 import features,features_flow,features_material_gradient,cofactor,score_residual,scaled_fit,ensemble_score,project_to_level,surface_test
C=np.zeros(10);S=np.ones(10);T=0.
class ModelTests(unittest.TestCase):
    def test_dictionaries_contain_no_phase_only(self):
        y=np.zeros(11);y[10]=1.2
        for degree in (1,2):
            for phase in (False,True):self.assertLess(np.linalg.norm(features(y,C,S,T,degree,phase)),1e-15)
    def test_feature_lengths(self):
        y=np.arange(11.)
        self.assertEqual(len(features(y,C,S,T,1,False)),10)
        self.assertEqual(len(features(y,C,S,T,2,False)),65)
        self.assertEqual(len(features(y,C,S,T,2,True)),85)
    def test_exact_phase_covariant_first_integral(self):
        omega=.7;y=np.zeros(11);y[0]=1.;y[1]=2.;y[10]=.3
        f=np.zeros(11);f[0]=-omega*y[1];f[1]=omega*y[0];f[10]=omega
        q=np.zeros(30);q[20]=1.;q[11]=1. # cos theta*x1 and sin theta*x2
        self.assertAlmostEqual(score_residual(y,f,q,C,S,T,0.,0.,1,True),0.,places=13)
    def test_nonzero_cofactor_exact_tangency(self):
        rng=np.random.default_rng(14);lam=-.3;mod=.2
        y=rng.normal(size=11);f=np.zeros(11);f[10]=.6;f[0]=cofactor(y,T,lam,mod)*y[0]
        q=np.zeros(10);q[0]=1.
        self.assertLess(abs(score_residual(y,f,q,C,S,T,lam,mod,1,False)),1e-13)
    def test_changing_phase_requires_recomputing_field(self):
        y=np.zeros(11);y[0]=1.25;f=np.zeros(11);f[0]=.1*y[0];f[10]=.8
        q=np.zeros(10);q[0]=1.
        self.assertGreater(abs(score_residual(y,f,q,C,S,T,-.3,.2,1,False)),1e-3)
    def test_feature_gradient_matches_centered_difference(self):
        rng=np.random.default_rng(15);y=rng.normal(size=11);q=rng.normal(size=85)
        g=features_material_gradient(y,C,S,T,2,True).T@q
        for k in range(10):
            e=np.zeros(11);e[k]=1e-5
            n=(features(y+e,C,S,T,2,True)@q-features(y-e,C,S,T,2,True)@q)/(2e-5)
            self.assertAlmostEqual(n,g[k],places=8)
    def test_feature_flow_matches_finite_difference(self):
        rng=np.random.default_rng(151);y=rng.normal(size=11);f=rng.normal(size=11)
        for deg in (1,2):
            for phase in (False,True):
                exact=features_flow(y,f,C,S,T,deg,phase)
                fd=(features(y+f*1e-6,C,S,T,deg,phase)-features(y-f*1e-6,C,S,T,deg,phase))/(2e-6)
                self.assertLess(np.linalg.norm(fd-exact),1e-8)
    def test_project_to_surface(self):
        y=np.zeros(11);y[0]=.5;y[2]=.1;q=np.zeros(10);q[0]=1.
        z,length,ok=project_to_level(y,q,C,S,T,1,False)
        self.assertTrue(ok);self.assertLess(abs(z[0]),1e-11);self.assertAlmostEqual(z[2],y[2]);self.assertAlmostEqual(length,.5)
    def test_projected_surface_tangency(self):
        lam=.4;q=np.zeros(10);q[0]=1.
        states=np.zeros((6,11));states[:,0]=np.linspace(-.2,.2,6)
        def f(t,y):
            ret=np.zeros(11);ret[0]=lam*y[0];ret[10]=.5;return ret
        vals,proj,fail=surface_test(states,f,q,C,S,T,lam,0.,1,False)
        self.assertEqual(fail,0);self.assertEqual(len(proj),6)
        self.assertLess(max(v['surface_residual'] for v in vals),1e-12)
    def test_fit_finds_exact_invariant_plane(self):
        rng=np.random.default_rng(16);states=rng.normal(size=(150,11));fields=np.zeros_like(states)
        fields[:,0]=.3*states[:,0];fields[:,1:10]=rng.normal(size=(150,9));fields[:,10]=1.
        q,_=scaled_fit(states,fields,C,S,T,.3,0.,1,False,anchors=np.zeros((1,11)))
        e=ensemble_score(states,fields,q,C,S,T,.3,0.,1,False)
        self.assertLess(e['relative_residual'],1e-10)
    def test_wrong_cofactor_detected(self):
        y=np.zeros(11);y[0]=.4;f=np.zeros(11);f[0]=.15*y[0]
        q=np.zeros(10);q[0]=1.
        self.assertAlmostEqual(score_residual(y,f,q,C,S,T,.15,0.,1,False),0.,places=14)
        self.assertGreater(abs(score_residual(y,f,q,C,S,T,-.15,0.,1,False)),.1)
if __name__=='__main__':unittest.main()
