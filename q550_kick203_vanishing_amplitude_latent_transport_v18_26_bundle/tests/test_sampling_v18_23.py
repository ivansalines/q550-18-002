import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from blind_math import HISTORY,HORIZONS
from nonlinear_server_v18_23 import generate
class TestNonlinearSampling(unittest.TestCase):
    def test_exact_past_future_grid_and_phase(self):
        def f(t,y):
            z=np.zeros(11);z[0]=y[1];z[1]=-y[0];z[10]=2*np.pi
            return z
        center=np.zeros(11);center[10]=10.
        a=4+HISTORY;b=4+HORIZONS
        sol=generate(f,center,np.eye(10)[0],1e-5,a,b)
        self.assertEqual(sol.shape,(20,11))
        self.assertLess(abs(sol[16,0]-1e-5),1e-13)
        self.assertLess(abs(sol[0,0]-1e-5*np.cos(.5)),1e-10)
        self.assertLess(abs(sol[-1,0]-1e-5*np.cos(1.)),1e-10)
        self.assertAlmostEqual(sol[0,10],10.-np.pi,places=9)
        self.assertAlmostEqual(sol[-1,10],10.+2*np.pi,places=9)
if __name__=='__main__':unittest.main()
