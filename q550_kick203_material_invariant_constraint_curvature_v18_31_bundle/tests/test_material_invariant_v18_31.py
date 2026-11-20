"""Synthetic certificates of the dictionary and curvature identities only."""
import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from invariant_math_v18_31 import feature,feature_derivative,gradient_hessian,select_modes,derivative_score,tangent_normal_curvature
from original_material_invariants_v18_31 import select_original_checkpoint,numpy_json_default
class MathTests(unittest.TestCase):
 def setUp(self):
    self.c=np.zeros(10);self.s=np.ones(10)
 def test_linear_derivative(self):
    y=np.arange(11,dtype=float)/10;f=np.ones(11)
    self.assertTrue(np.allclose(feature_derivative(y,f,self.c,self.s,1),np.ones(10)))
 def test_quadratic_derivative(self):
    y=np.arange(11,dtype=float)/10;v=np.arange(11,dtype=float)/7
    h=1e-6
    for degree in (1,2):
        num=(feature(y+h*v,self.c,self.s,degree)-feature(y-h*v,self.c,self.s,degree))/(2*h)
        self.assertTrue(np.allclose(num,feature_derivative(y,v,self.c,self.s,degree),atol=3e-10))
 def test_hessian_derivative(self):
    rng=np.random.default_rng(3);y=rng.normal(size=11);q=rng.normal(size=65)
    g,H=gradient_hessian(y,self.c,self.s,q,2)
    h=1e-6
    num=np.array([(feature(y+h*np.eye(11)[i],self.c,self.s,2)@q-feature(y-h*np.eye(11)[i],self.c,self.s,2)@q)/(2*h) for i in range(10)])
    self.assertTrue(np.allclose(g,num,atol=3e-9))
    self.assertTrue(np.allclose(H,H.T,atol=1e-12))
 def test_known_linear_first_integral(self):
    rng=np.random.default_rng(7);states=rng.normal(size=(400,11));fields=rng.normal(size=(400,11));fields[:,1]=-fields[:,0]
    A=np.array([feature_derivative(y,f,self.c,self.s,1) for y,f in zip(states,fields)])
    sv,modes=select_modes(A,1e-9,3)
    self.assertGreaterEqual(len(modes),1)
    self.assertLess(derivative_score(A,modes[0]['coeff']),1e-12)
 def test_curved_first_integral_constraint(self):
    # C=x2-x1*x1 and tangent vector u=(1,2*x1); its required w normal isn't zero.
    y=np.zeros(11);y[0]=.4
    q=np.zeros(65);q[1]=1;q[10]=-1  # x0^2 first quadratic pair
    G,H=gradient_hessian(y,self.c,self.s,q,2)
    u=np.array([1.,.8]+[0.]*8)
    self.assertAlmostEqual(G@u,0.,places=12)
    self.assertAlmostEqual(u@H@u,-2.,places=12)
    u2,w,geom=tangent_normal_curvature(y,np.r_[u,0.],self.c,self.s,q,2)
    self.assertLess(geom['first_constraint_defect'],1e-12)
    self.assertLess(geom['second_constraint_defect'],1e-12)
 def test_reject_generic_vector_field(self):
    rng=np.random.default_rng(9)
    y=rng.normal(size=(500,11));f=rng.normal(size=(500,11))
    for deg in (1,2):
        A=np.array([feature_derivative(a,b,self.c,self.s,deg) for a,b in zip(y,f)])
        _,modes=select_modes(A,1e-9)
        self.assertEqual(len(modes),0)
 def test_finite_anchored_derivative(self):
    rng=np.random.default_rng(21);y=rng.normal(size=11);f=rng.normal(size=11);c=rng.normal(size=10);s=np.exp(rng.normal(size=10));q=rng.normal(size=65)
    for deg in (1,2):
        h=1e-6
        numeric=(feature(y+h*f,c,s,deg)-feature(y-h*f,c,s,deg))/(2*h)
        self.assertTrue(np.allclose(numeric,feature_derivative(y,f,c,s,deg),atol=1e-8))
 def test_tight_checkpoint_selection(self):
    d={'standard':{'slope':.14,'source_state_11D':np.ones(11)},
       'tight':{'slope':.1343837,'source_state_11D':np.arange(11,dtype=float)}}
    self.assertIs(select_original_checkpoint(d),d['tight'])
    with self.assertRaisesRegex(RuntimeError,'tiers missing'):
        select_original_checkpoint({'slope':.134})
    with self.assertRaisesRegex(RuntimeError,'missing slope'):
        select_original_checkpoint({'tight':{'source_state_11D':np.zeros(11)}})
 def test_numpy_bool_and_scalar_json_serialization(self):
    import json
    doc={'passes':np.bool_(False),'index':np.int64(3),'ratio':np.float64(.25),
         'array':np.array([1.,2.]),'nested':[{'pass':np.bool_(True)}]}
    text=json.dumps(doc,default=numpy_json_default,allow_nan=False)
    decoded=json.loads(text)
    self.assertIs(decoded['passes'],False)
    self.assertIs(decoded['nested'][0]['pass'],True)
    self.assertEqual(decoded['index'],3)
    self.assertEqual(decoded['array'],[1.,2.])
    with self.assertRaises(TypeError): json.dumps({'bad':object()},default=numpy_json_default)
 def test_partial_recovery_missing_files_fails_closed(self):
    import importlib.util
    spec=importlib.util.spec_from_file_location('recovery_test',str(Path(__file__).resolve().parents[1]/'scripts/finalize_partial_v18_31_2.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        saved=(module.CSV,module.COEFF,module.GEOM,module.PROOF)
        module.CSV=Path(temp)/'missing.csv';module.COEFF=Path(temp)/'missing_coeffs.json';module.GEOM=Path(temp)/'missing_geom.json'
        try:
            with self.assertRaisesRegex(RuntimeError,'Cannot recover'): module._load_partial()
        finally:module.CSV,module.COEFF,module.GEOM,module.PROOF=saved
 def test_constant_is_excluded(self):
    self.assertEqual(len(feature(np.zeros(11),self.c,self.s,1)),10)
    self.assertEqual(len(feature(np.zeros(11),self.c,self.s,2)),65)
 def test_hessian_second_order_geometric_jet(self):
    y=np.zeros(11);y[0]=.25;q=np.zeros(65);q[1]=1;q[10]=-1
    u,w,diag=tangent_normal_curvature(y,np.r_[[1.,.5],np.zeros(9)],self.c,self.s,q,2)
    G,H=gradient_hessian(y,self.c,self.s,q,2)
    self.assertAlmostEqual(float(G@w+u@H@u),0,places=12)
if __name__=='__main__':unittest.main()
