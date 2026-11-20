import sys,unittest,inspect
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from robust_math_v18_24 import *
from blind_math import ridge_fit,ridge_predict
class TestEndpoint(unittest.TestCase):
 def setUp(self):self.a=np.random.default_rng(91).normal(size=(43,17,3))
 def test_endpoint_bit_for_bit(self):
  for seed in (1,20,300):self.assertTrue(np.array_equal(self.a[:,-1],permute_past_only(self.a,seed)[:,-1]))
 def test_scramble_keeps_past_multiset(self):
  p=permute_past_only(self.a,91)
  self.assertTrue(np.array_equal(np.sort(p[:,:-1],axis=1),np.sort(self.a[:,:-1],axis=1)))
 def test_scramble_destroys_timing(self):
  p=permute_past_only(self.a,91)
  self.assertGreater(np.mean(np.abs(p[:,:-1]-self.a[:,:-1])),0.5)
 def test_all_modes_preserve_endpoint(self):
  for kind in MODELS:
   m=features(self.a,kind,seed=17)
   self.assertTrue(np.array_equal(m[:,-3:],self.a[:,-1]))
 def test_global_reverse_invariance_to_ridge(self):
  u=self.a;v=np.random.default_rng(6).normal(size=(43,9))
  p=ridge_fit(features(u[:30],'chronological'),v[:30],1e-2)
  q=ridge_fit(features(u[:30],'past_reversed_global'),v[:30],1e-2)
  t1=ridge_predict(p,features(u[30:],'chronological'))
  t2=ridge_predict(q,features(u[30:],'past_reversed_global'))
  self.assertLess(np.max(np.abs(t1-t2)),1e-11)
 def test_shared_permutation_is_global_only(self):
  p=permute_past_only(self.a,3,False)
  self.assertTrue(np.array_equal(p[:,-1],self.a[:,-1]))
 def test_rank_selection_uses_only_val(self):
  body=inspect.getsource(evaluate)
  self.assertIn('fit_latent_models(features(TR',body)
  self.assertNotIn('test_truth[anchor],ranks',body)
 def test_blind_math_has_no_model_operator(self):
  import robust_math_v18_24
  source=inspect.getsource(robust_math_v18_24)
  for phrase in ('checkpoint_io','solve_ivp','P_full11D','source_state_11D'):
   self.assertNotIn(phrase,source)
 def test_anchors(self):self.assertEqual(ANCHORS,(3.5,4.,4.5))
 def test_noise_not_applied_to_future(self):
  import robust_math_v18_24
  src=inspect.getsource(robust_math_v18_24.evaluate)
  self.assertIn("Xtr,Ytr=reference['train']",src)
  self.assertIn("truth=test_truth[anchor]",src)
 def test_latent_rank10_vs20(self):
  rng=np.random.default_rng(1)
  a=rng.normal(size=(130,20));b=rng.normal(size=(20,7))
  model,scan,win=fit_latent_models(a[:70],a[:70]@b,a[70:95],a[70:95]@b)
  self.assertTrue(10 in model and 20 in model)
  self.assertEqual(win['rank'],20)
  self.assertLess(rmse(predict_latent(model[20],a[95:]),a[95:]@b),1e-10)
if __name__=='__main__':unittest.main()
