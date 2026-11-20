"""Algebraic safety and no-evidence-inflation tests for v18.26."""
import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from amplitude_math_v18_26 import (AMPLITUDES,NOISE_MODES,RANKS,effective_sigma,
                                   sensor_noise,predict_with_alignment)
from transport_math_v18_25 import latent_encode
from robust_math_v18_24 import fit_latent_models,predict_latent

class TestVanishingAmplitude(unittest.TestCase):
    def test_five_distinct_amplitudes(self):
        self.assertEqual(len(AMPLITUDES),5)
        self.assertTrue(all(a>b for a,b in zip(AMPLITUDES,AMPLITUDES[1:])))
    def test_constant_absolute_noise(self):
        self.assertAlmostEqual(1e-5*effective_sigma(1e-5,'fixed_absolute'),
                               1e-7*effective_sigma(1e-7,'fixed_absolute'))
    def test_constant_normalized_noise(self):
        self.assertEqual(effective_sigma(1e-5,'fixed_normalized'),
                         effective_sigma(1e-7,'fixed_normalized'))
    def test_noise_increases_100_fold_relative(self):
        self.assertAlmostEqual(effective_sigma(1e-7,'fixed_absolute')/
                               effective_sigma(1e-5,'fixed_absolute'),100)
    def test_zero_noise(self):
        self.assertEqual(effective_sigma(1e-7,'none'),0.)
    def test_noise_rng_reproducible(self):
        x=np.ones((10,17,3))
        self.assertTrue(np.array_equal(sensor_noise(x,.01,423),sensor_noise(x,.01,423)))
        self.assertFalse(np.array_equal(sensor_noise(x,.01,424),sensor_noise(x,.01,423)))
    def test_predictor_has_no_oracle_import(self):
        source=(Path(__file__).resolve().parents[1]/'scripts/amplitude_math_v18_26.py').read_text()
        self.assertNotIn('from checkpoint_io_',source)
        self.assertNotIn('from q550_',source)
        self.assertNotIn('support_rhs_float',source)
    def test_rank_20_allowed_when_useful(self):
        rng=np.random.default_rng(91)
        X=rng.normal(size=(96,20));V=rng.normal(size=(32,20))
        # Target deliberately requires all columns, rank10 must generally degrade.
        B=rng.normal(size=(20,5));Y=X@B;W=V@B
        models,rows,selection=fit_latent_models(X,Y,V,W,ranks=(10,20))
        e={r['rank']:r['validation_rmse'] for r in rows}
        self.assertLess(e[20],e[10])
        self.assertEqual(selection['rank'],20)
    def test_paired_observation_has_reproducible_alignment(self):
        rng=np.random.default_rng(98);X=rng.normal(size=(96,10));V=rng.normal(size=(32,10));B=rng.normal(size=(10,3))
        models,_,_=fit_latent_models(X,X@B,V,V@B,ranks=(10,))
        m=models[10];cal=X[:32];test=V[:5]
        pred,info=predict_with_alignment(m,'orthogonal',cal,cal,test)
        self.assertTrue(np.all(np.isfinite(pred)))
        self.assertLess(np.max(abs(pred-predict_latent(m,test))),1e-9)
        self.assertFalse(info is None)
    def test_covariance_and_phase_not_in_noise_model(self):
        self.assertEqual(NOISE_MODES,('none','fixed_normalized','fixed_absolute'))
        self.assertEqual(RANKS,(10,20))

if __name__=='__main__':unittest.main()
