import sys,unittest,inspect
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from nonlinear_server_v18_24 import generate
from robust_math_v18_24 import evaluate,ANCHORS
from blind_math import HISTORY,HORIZONS
class TestNewNonlinearGrid(unittest.TestCase):
 def test_all_anchor_windows_distinct_and_exact(self):
  for anchor in ANCHORS:
   grid=np.r_[anchor+HISTORY,anchor+HORIZONS]
   self.assertEqual(len(grid),len(np.unique(grid)))
   self.assertAlmostEqual(grid[len(HISTORY)-1],anchor)
   self.assertAlmostEqual(grid[-1],anchor+1.0)
 def test_generator_linear_tracer_phase_and_times(self):
  def f(t,y):
   return np.r_[np.ones(10),2*np.pi]
  for anchor in ANCHORS:
   y0=np.arange(11,dtype=float)
   y=generate(f,anchor,y0,np.ones(10),1e-5)
   times=np.r_[anchor+HISTORY,anchor+HORIZONS]
   expected=y0+np.r_[np.ones(10)*1e-5,0.] + np.outer(times-anchor,np.r_[np.ones(10),2*np.pi])
   self.assertLess(np.max(abs(y-expected)),1e-11)
 def test_shifted_test_not_used_for_fit(self):
  src=inspect.getsource(evaluate)
  self.assertIn('reference=anchored[4.0]',src)
  self.assertIn("Xtr,Ytr=reference['train'];Xva,Yva=reference['val']",src)
  self.assertIn('for anchor in ANCHORS:',src)
if __name__=='__main__':unittest.main()
