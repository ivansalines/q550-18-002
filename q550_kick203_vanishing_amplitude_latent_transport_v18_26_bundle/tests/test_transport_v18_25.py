"""Analytical invariants, observability and anti-leakage for v18.25."""
import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from transport_math_v18_25 import (past_shift,center_map_fit,center_map_predict,
    fit_latent_transport,latent_encode,latent_target,rank_models,
    choose_lag,CAL_N,CAL_TR,RANKS,TRANSPORTS,ANCHORS)
from blind_math import HISTORY,HORIZONS,rmse

class Transport(unittest.TestCase):
    def test_past_endpoint_exact(self):
        a=np.random.default_rng(12).normal(size=(7,17,3))
        for lag in (-.125,-.05,0.,.05,.125):
            changed=past_shift(a,lag)
            self.assertTrue(np.array_equal(changed[:,-1],a[:,-1]))
    def test_zero_lag_exact(self):
        a=np.random.default_rng(12).normal(size=(7,17,3))
        self.assertTrue(np.allclose(past_shift(a,0),a,atol=1e-14))
    def test_invalid_shape(self):
        with self.assertRaises(ValueError):past_shift(np.zeros((7,16,3)),.01)
    def test_orthogonal_map_recovers_rotation(self):
        rng=np.random.default_rng(122);z=rng.normal(size=(45,10))
        Q,_=np.linalg.qr(rng.normal(size=(10,10)))
        target=z@Q+0.7
        learned=center_map_fit(z,target,'orthogonal')
        self.assertLess(rmse(center_map_predict(learned,z[35:]),target[35:]),1e-12)
    def test_affine_recovers_shear(self):
        rng=np.random.default_rng(12);z=rng.normal(size=(75,10))
        M=np.eye(10)+rng.normal(size=(10,10))*.15
        goal=z@M+.42
        mdl=center_map_fit(z[:50],goal[:50],'affine_ridge',1e-10)
        self.assertLess(rmse(center_map_predict(mdl,z[50:]),goal[50:]),1e-8)
    def test_wrong_pair_not_equivalent(self):
        rng=np.random.default_rng(213);z=rng.normal(size=(32,10))
        Q,_=np.linalg.qr(rng.normal(size=(10,10)))
        y=z@Q
        correct=center_map_fit(z,y,'orthogonal')
        wrong=center_map_fit(z,y[rng.permutation(32)],'orthogonal')
        self.assertLess(rmse(center_map_predict(correct,z),y),1e-12)
        self.assertGreater(rmse(center_map_predict(wrong,z),y),.1)
    def test_lag_and_calibration_do_not_consume_future(self):
        rng=np.random.default_rng(32)
        a=rng.normal(size=(CAL_N,17,3))
        b=a.copy()
        val,score=choose_lag(a,b)
        self.assertAlmostEqual(val,0.,places=12)
    def test_latent_gauge_equivariance(self):
        rng=np.random.default_rng(338)
        zshift=rng.normal(size=(50,10))
        zref=rng.normal(size=(50,10))
        future_model=rng.normal(size=(11,7))
        p=center_map_fit(zshift[:32],zref[:32],'orthogonal')
        predict=lambda Z,M: np.c_[np.ones(len(Z)),center_map_predict(M,Z)]@future_model
        y0=predict(zshift[32:],p)
        Q,_=np.linalg.qr(rng.normal(size=(10,10)))
        p_rot=center_map_fit(zshift[:32]@Q,zref[:32]@Q,'orthogonal')
        rotated_beta=np.vstack((future_model[0],Q.T@future_model[1:]))
        y1=np.c_[np.ones(18),center_map_predict(p_rot,zshift[32:]@Q)]@rotated_beta
        self.assertLess(np.max(abs(y0-y1)),1e-11)
    def test_rank20_not_forced_to_10(self):
        self.assertEqual(RANKS,(10,20))
        self.assertIn('affine_ridge',TRANSPORTS)
        self.assertIn('broken_pair_orthogonal',TRANSPORTS)
    def test_temporal_sections(self):
        self.assertEqual(ANCHORS,(3.5,4.0,4.5))
        self.assertEqual(len(HISTORY),17)
        self.assertEqual(len(HORIZONS),3)
    def test_test_labels_not_in_alignment_functions(self):
        import inspect
        import transport_math_v18_25 as t
        src=inspect.getsource(t.choose_lag)+inspect.getsource(t.fit_latent_transport)
        self.assertNotIn('test_truth',src)
        self.assertNotIn('test_future',src)
    def test_equal_present_under_shift_even_with_noise(self):
        rng=np.random.default_rng(99)
        a=rng.normal(size=(30,17,6))
        a+=rng.normal(size=a.shape)*.001
        self.assertTrue(np.array_equal(past_shift(a,.11)[:,-1],a[:,-1]))
    def test_rank_predictor_independent_of_shifted_labels(self):
        rng=np.random.default_rng(12)
        X=rng.normal(size=(96,17,3))
        Xv=rng.normal(size=(32,17,3))
        b=rng.normal(size=(51,9))
        Y=X.reshape(96,-1)@b
        Yv=Xv.reshape(32,-1)@b
        models,scan,selected=rank_models(X,Y,Xv,Yv)
        self.assertIn(20,models)
        self.assertTrue(all('test_rmse' not in s for s in scan))

if __name__=='__main__':unittest.main()
