import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from blind_math import *
from blind_experiment import initial_directions,N_TRAIN,N_VAL,N_TEST,OBSERVERS

class TestBlind(unittest.TestCase):
    def test_triple_split_disjoint(self):
        seeds={key:np.arange(1,11,dtype=float) for key in ('material3_jet2','raw4_jet1','raw6_jet1')}
        p=initial_directions(seeds)
        for key in OBSERVERS:
            train=p[key]['train'];val=p[key]['val'];test=p[key]['test']
            self.assertEqual([len(train),len(val),len(test)],[N_TRAIN,N_VAL,N_TEST+1])
            self.assertTrue(np.min(np.linalg.norm(train[:,None,:]-test[None,:,:],axis=2))>1e-3)
            self.assertTrue(np.min(np.linalg.norm(train[:,None,:]-val[None,:,:],axis=2))>1e-3)
    def test_features(self):
        data=np.arange(4*17*3).reshape(4,17,3)
        self.assertTrue(np.all(feature_view(data,'instant')==data[:,-1,:]))
        self.assertEqual(feature_view(data,'recent_0.10').shape,(4,12))
        self.assertEqual(feature_view(data,'history_0.50').shape,(4,51))
    def test_independent_shuffle(self):
        ix=scrambled_indices(70,14)
        self.assertEqual(len({tuple(k) for k in ix}),70)
        self.assertTrue(all(sorted(k)==list(range(17)) for k in ix))
    def test_blind_linear_exact(self):
        rng=np.random.default_rng(7)
        A=rng.normal(size=(120,10));B=rng.normal(size=(10,3))
        fit=ridge_fit(A[:90],A[:90]@B,1e-10)
        self.assertLess(rmse(ridge_predict(fit,A[90:]),A[90:]@B),1e-8)
    def test_prediction_improves_with_informative_history(self):
        rng=np.random.default_rng(1)
        U=rng.normal(size=(200,2));future=U[:,1:2]
        current=U[:,0:1];history=np.stack([U[:,1],U[:,0]],axis=1)
        mcur=ridge_fit(current[:100],future[:100],1e-5)
        mhist=ridge_fit(history[:100],future[:100],1e-5)
        self.assertGreater(rmse(ridge_predict(mcur,current[100:]),future[100:]),.5)
        self.assertLess(rmse(ridge_predict(mhist,history[100:]),future[100:]),1e-5)
    def test_predictor_not_using_hidden_ode(self):
        import inspect,blind_math
        source=inspect.getsource(blind_math)
        self.assertNotIn('checkpoint_io',source)
        self.assertNotIn('solve_ivp',source)
        self.assertNotIn('source_state_11D',source)
        self.assertNotIn('P_full11D',source)
        self.assertNotIn('J_full11D',source)
    def test_noise_never_in_target(self):
        import inspect
        source=inspect.getsource(evaluate_blind)
        self.assertIn('xtr=trainX+noises[0]',source)
        self.assertNotIn('trainY+noises',source)
    def test_ridge_selection_on_validation_only(self):
        import inspect
        source=inspect.getsource(evaluate_blind)
        self.assertIn('score=rmse(ridge_predict(model,va),valY)',source)
        self.assertIn('pred=ridge_predict(model,te)',source)
    def test_noise_level_zero(self):
        rng=np.random.default_rng(9)
        X=rng.normal(size=(160,17,3));Y=rng.normal(size=(160,9))
        result,predict=evaluate_blind(X[:96],Y[:96],X[96:128],Y[96:128],X[128:],Y[128:],0.,seed=8)
        self.assertEqual(len(result['history_singular_values']),15)
        self.assertEqual(predict['instant'].shape,(32,9))
        self.assertTrue(all(np.isfinite(v).all() for v in predict.values()))
if __name__=='__main__':unittest.main()

class TestDelayLatent(unittest.TestCase):
    def test_latent_reconstructs_unseen_linear_futures(self):
        rng=np.random.default_rng(1823)
        A=rng.normal(size=(170,10))
        mats=rng.normal(size=(17,3,10))
        X=np.einsum('tmd,nd->ntm',mats,A)
        Y=A@rng.normal(size=(10,9))
        results,best=delay_latent_rank_scan(X[:96],Y[:96],X[96:128],Y[96:128],X[128:],Y[128:],0.)
        rank10=next(row for row in results if row['rank']==10)
        self.assertLess(rank10['test_rmse'],1e-10)
        self.assertLess(best['test_rmse'],1e-10)
        self.assertEqual(best['rank'],10) # Parsimonious numerical-tie selection
        self.assertFalse(best['physical_state_dimension_inferred'])
        self.assertLessEqual(best['validation_rmse'],best['validation_best_rmse']+best['validation_tie_tolerance'])

class TestLatentRankSelection(unittest.TestCase):
    def test_roundoff_tie_chooses_smallest_rank(self):
        data=[{'rank':10,'validation_rmse':2e-14},
              {'rank':15,'validation_rmse':1e-14},
              {'rank':20,'validation_rmse':8e-15}]
        best=choose_predictive_latent_rank(data,np.ones((32,9)))
        self.assertEqual(best['rank'],10)
        self.assertEqual(best['rank_selection_rule'],'lowest_rank_within_validation_numerical_tie')
    def test_meaningful_validation_gain_keeps_rank_20(self):
        data=[{'rank':10,'validation_rmse':0.024},
              {'rank':15,'validation_rmse':0.012},
              {'rank':20,'validation_rmse':0.009}]
        best=choose_predictive_latent_rank(data,np.ones((32,9)))
        self.assertEqual(best['rank'],20)
        self.assertFalse(best['physical_state_dimension_inferred'])
    def test_rank_scan_never_uses_test_for_selection(self):
        import inspect,blind_math
        body=inspect.getsource(blind_math.delay_latent_rank_scan)
        self.assertIn('choose_predictive_latent_rank(results,valY)',body)
        selection=inspect.getsource(blind_math.choose_predictive_latent_rank)
        self.assertNotIn('testY',selection)
