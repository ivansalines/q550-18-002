"""Independent mathematical invariance and leakage checks for v18.27."""
import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'reference')]
from singular_subspace_v18_27 import principal_metrics,svd_frame,authentic_data,get,matched_original,matched_frozen
from robust_math_v18_24 import fit_latent_models,predict_latent
from amplitude_math_v18_26 import effective_sigma,sensor_noise,AMPLITUDES
from blind_math import rmse
from nonlinear_floor_v18_27 import summarize_pair
class TestSubspace(unittest.TestCase):
    def test_subspace_gauge(self):
        rng=np.random.default_rng(3);V=np.linalg.qr(rng.normal(size=(34,20)))[0]
        Q=np.linalg.qr(rng.normal(size=(20,20)))[0]
        self.assertLess(principal_metrics(V,V@Q,20)['max_principal_angle_deg'],1e-5)
        self.assertLess(principal_metrics(V,V@Q,20)['projector_distance_frob'],1e-5)
    def test_shifted_subspace(self):
        V=np.eye(30)[:,:10];W=np.eye(30)[:,10:20]
        self.assertGreater(principal_metrics(V,W,10)['max_principal_angle_deg'],89.9)
    def test_training_only_svd(self):
        rng=np.random.default_rng(14);X=rng.normal(size=(96,17,3))
        m,s,sp,V=svd_frame(X)
        self.assertEqual(V.shape,(51,51))
        self.assertTrue(np.allclose(V.T@V,np.eye(51),atol=1e-12))
        self.assertTrue(np.all(np.diff(sp)<=1e-12))
    def test_rotation_prediction_gauge(self):
        rng=np.random.default_rng(5);X=rng.normal(size=(96,40));Y=rng.normal(size=(96,9));V=rng.normal(size=(32,40));W=rng.normal(size=(32,9))
        mdl=fit_latent_models(X,Y,V,W,ranks=(10,20))[0][20]
        Q=np.linalg.qr(rng.normal(size=(20,20)))[0]
        m,s,P,B=mdl
        rev=(m,s,P@Q,np.r_[B[:1],Q.T@B[1:]])
        self.assertLess(np.max(abs(predict_latent(mdl,V)-predict_latent(rev,V))),1e-12)
    def test_sensor_sigma_scaling(self):
        self.assertAlmostEqual(effective_sigma(1e-7,'fixed_absolute'),1e-2)
        self.assertAlmostEqual(effective_sigma(1e-7,'fixed_normalized'),1e-4)
    def test_even_odd_synthetic(self):
        baseline=np.zeros((20,11));p=baseline.copy();m=baseline.copy();eps=1e-5
        response=np.arange(20.)[:,None]*np.ones((20,10))
        p[:,:10]=eps*response+eps**2*0.2
        m[:,:10]=-eps*response+eps**2*0.2
        odd,even=summarize_pair((p,m,baseline),np.eye(3,10),eps)
        self.assertLess(np.max(abs(odd-response[:,:3])),1e-10)
        self.assertLess(np.max(abs(even-eps*.2)),1e-10)
    def test_amplitudes_strictly_descend(self):
        self.assertTrue(all(AMPLITUDES[i]>AMPLITUDES[i+1] for i in range(4)))
    def test_parent_original_verified(self):
        db,pr,r,f,e=authentic_data()
        self.assertEqual(pr['parent_integrations'],1596)
        self.assertEqual(len(db.files),210)
        self.assertEqual(len(e),45)
    def test_parent_samples_not_same_splits(self):
        db,*_=authentic_data();x,y=get(db,1e-5,'material3',4,'train');v,w=get(db,1e-5,'material3',4,'val')
        self.assertEqual(x.shape,(96,17,3));self.assertEqual(v.shape,(32,17,3))
        self.assertFalse(np.array_equal(x[:32],v))
    def test_parent_cross_references(self):
        _,_,r,f,_=authentic_data()
        self.assertTrue(matched_original(r,'material3',1e-5,'none',3.5,'none',20)>0)
        self.assertTrue(matched_frozen(f,'material3',1e-7,'none',4.5,20)>0)

if __name__=='__main__':unittest.main()
