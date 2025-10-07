import math
import unittest

import queues as q

class TestQueues(unittest.TestCase):

    def test_calc_bk_mmc(self):
        k = 3
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, (10, 20, 10), 50, 2))
        self.assertAlmostEqual(0.9, q.calc_bk_mmc(1, (10, 20, 10), 50, 2))

        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, 30, 50, 2))
        self.assertAlmostEqual(0.7, q.calc_bk_mmc(1, 30, 50, 2))

        self.assertTrue(math.isnan(q.calc_bk_mmc(1, 30, 0, 2)))

    def test_calc_wqk_mmc(self):
        k = 3
        self.assertAlmostEqual(0.0533333333333333, q.calc_wqk_mmc(1, (10, 20, 10), 50, 2))

        self.assertTrue(math.isnan(q.calc_wqk_mmc(-k, 30, 50, 2)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(0, 30, 50, 2)))

    def test_calc_lqk_mmc(self):
        k = 2
        lamda = (15, 25)
        wqk = q.calc_wqk_mmc(k, lamda, 5, 3)

        self.assertTrue(math.isnan(q.calc_lqk_mmc(0, lamda, wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(k, (15,), wqk)))

        self.assertAlmostEqual(lamda[k - 1] * wqk, q.calc_lqk_mmc(k, lamda, wqk))

    def test_use_littles_law(self):
        lamda = 2
        mu = 4
        c = 3

        expected = {'lq': 1.0, 'l': 2.0, 'wq': 0.5, 'w': 0.75, 'r': 1.5, 'ro': 0.5}

        actual = q.use_littles_law(lamda, mu, c, lq=1.0)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], places=5)


if __name__ == '__main__':
    unittest.main(verbosity=2)