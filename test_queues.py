from unittest import TestCase
from unittest import main


import math

import queues as q

class Test_queues(TestCase):
    lamda = 0.0
    mu = 0.0
    c = 1.0

    def setUp(self):
        self.lamda = 20.0
        self.mu = 25.0
        self.c = 1.0

    # def tearDown(self):
    #     result = self.defaultTestResult()  # These two methods have no side effects
    #     print("printing captured result")
    #     print(result)
    #
    #     self._feedErrorsToResult(result, self._outcome.errors)
    #
    #     error = self.list2reason(result.errors)
    #     failure = self.list2reason(result.failures)
    #     ok = not error and not failure
    #
    #     # Demo:   report short info immediately (not important)
    #     if not ok:
    #         typ, text = ('ERROR', error) if error else ('FAIL', failure)
    #         msg = [x for x in text.split('\n')[1:] if not x.startswith(' ')][0]
    #         print("\n%s: %s\n     %s" % (typ, self.id(), msg))


    def test_is_valid(self):
        lamda = self.lamda
        mu = self.mu
        c = self.c

        # valid single valued lamda
        self.assertEqual(True, q.is_valid(lamda, mu))
        self.assertEqual(True, q.is_valid(lamda, mu, c))
        self.assertEqual(True, q.is_valid(lamda, mu, 2))
        self.assertEqual(True, q.is_valid(25, 20, 1))

        # test with non-positive arguments
        self.assertEqual(False, q.is_valid(0, mu, c))
        self.assertEqual(False, q.is_valid(lamda, 0, c))
        self.assertEqual(False, q.is_valid(lamda, mu, 0))
        self.assertEqual(False, q.is_valid(0, mu, 1))
        self.assertEqual(False, q.is_valid(0, 0, 1))
        self.assertEqual(False, q.is_valid(lamda, 0, 0))
        self.assertEqual(False, q.is_valid(0, mu, 0))
        self.assertEqual(False, q.is_valid(0, 0, 0))

        self.assertEqual(False, q.is_valid(-lamda, mu, c))
        self.assertEqual(False, q.is_valid(lamda, -mu, c))
        self.assertEqual(False, q.is_valid(lamda, mu, -c))
        self.assertEqual(False, q.is_valid(-lamda, -mu, c))
        self.assertEqual(False, q.is_valid(-lamda, mu, -c))
        self.assertEqual(False, q.is_valid(lamda, -mu, -c))
        self.assertEqual(False, q.is_valid(-lamda, -mu, -c))

        # test with non-numeric arguments
        self.assertEqual(False, q.is_valid("twenty", mu, c))
        self.assertEqual(False, q.is_valid(lamda, "25", c))
        self.assertEqual(False, q.is_valid(lamda, mu, "one"))
        self.assertEqual(False, q.is_valid("twenty", "25", c))
        self.assertEqual(False, q.is_valid("twenty", mu, "one"))
        self.assertEqual(False, q.is_valid(lamda, "25", "one"))
        self.assertEqual(False, q.is_valid("twenty", "25", "one"))

        # test valid with multi-valued lamda (or at least lamda a tuple)
        self.assertEqual(True, q.is_valid((5, 10, 5), mu))
        self.assertEqual(True, q.is_valid((5, 10, 5), mu, c))
        self.assertEqual(True, q.is_valid((20,), mu, 1))
        self.assertEqual(True, q.is_valid((20,), mu, 2))

        # test invalid with multi-valued lamda
        self.assertEqual(False, q.is_valid((-5, 10, 5), mu, c))
        self.assertEqual(False, q.is_valid((5, -10, 5), mu, c))
        self.assertEqual(False, q.is_valid((5, 10, -5), mu, c))
        self.assertEqual(False, q.is_valid((-5, -10, 5), mu, c))
        self.assertEqual(False, q.is_valid((-5, 10, -5), mu, c))
        self.assertEqual(False, q.is_valid((5, -10, -5), mu, c))
        self.assertEqual(False, q.is_valid((-5, -10, -5), mu, c))

        self.assertEqual(False, q.is_valid((-5, 10, 5), -mu, c))
        self.assertEqual(False, q.is_valid((5, -10, 5), -mu, c))
        self.assertEqual(False, q.is_valid((5, 10, -5), -mu, c))
        self.assertEqual(False, q.is_valid((-5, -10, 5), -mu, c))
        self.assertEqual(False, q.is_valid((-5, 10, -5), -mu, c))
        self.assertEqual(False, q.is_valid((5, -10, -5), -mu, c))
        self.assertEqual(False, q.is_valid((-5, -10, -5), -mu, c))

        self.assertEqual(False, q.is_valid((-5, 10, 5), mu, -c))
        self.assertEqual(False, q.is_valid((5, -10, 5), mu, -c))
        self.assertEqual(False, q.is_valid((5, 10, -5), mu, -c))
        self.assertEqual(False, q.is_valid((-5, -10, 5), mu, -c))
        self.assertEqual(False, q.is_valid((-5, 10, -5), mu, -c))
        self.assertEqual(False, q.is_valid((5, -10, -5), mu, -c))
        self.assertEqual(False, q.is_valid((-5, -10, -5), mu, -c))


        self.assertEqual(False, q.is_valid((-5, 10, 5), -mu, -c))
        self.assertEqual(False, q.is_valid((5, -10, 5), -mu, -c))
        self.assertEqual(False, q.is_valid((5, 10, -5), -mu, -c))
        self.assertEqual(False, q.is_valid((-5, -10, 5), -mu, -c))
        self.assertEqual(False, q.is_valid((-5, 10, -5), -mu, -c))
        self.assertEqual(False, q.is_valid((5, -10, -5), -mu, -c))
        self.assertEqual(False, q.is_valid((-5, -10, -5), -mu, -c))


    def test_is_feasible(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test with valid queues, single-valued lamda
        self.assertEqual(True, q.is_feasible(20, 25))
        self.assertEqual(True, q.is_feasible(20, 25, 1))
        self.assertEqual(True, q.is_feasible(20, 25, 2))
        self.assertEqual(False, q.is_feasible(25, 25))
        self.assertEqual(False, q.is_feasible(25, 25, 1))
        self.assertEqual(True, q.is_feasible(25, 25, 2))
        self.assertEqual(False, q.is_feasible(40, 25, 1))
        self.assertEqual(True, q.is_feasible(40, 25, 2))
        self.assertEqual(False, q.is_feasible(50, 25, 2))
        self.assertEqual(True, q.is_feasible(50, 25, 3))

        # test for valid queues, multi-valued lamda
        self.assertEqual(True, q.is_feasible((5, 10, 5), 25))
        self.assertEqual(True, q.is_feasible((5, 10, 5), 25, 1))
        self.assertEqual(True, q.is_feasible((5, 10, 5), 25, 2))
        self.assertEqual(False, q.is_feasible((5, 10, 10), 25))
        self.assertEqual(False, q.is_feasible((5, 10, 10), 25, 1))
        self.assertEqual(True, q.is_feasible((5, 10, 10), 25, 2))
        self.assertEqual(False, q.is_feasible((10, 20, 10), 25, 1))
        self.assertEqual(True, q.is_feasible((10, 20, 10), 25, 2))
        self.assertEqual(False, q.is_feasible((10, 20, 20), 25, 2))
        self.assertEqual(True, q.is_feasible((10, 20, 20), 25, 3))

        # test for invalid queues
        # test for non-positive arguments

        self.assertEqual(False, q.is_valid(0, mu, c))
        self.assertEqual(False, q.is_valid(lamda, 0, c))
        self.assertEqual(False, q.is_valid(lamda, mu, 0))
        self.assertEqual(False, q.is_valid(0, mu, 1))
        self.assertEqual(False, q.is_valid(0, 0, 1))
        self.assertEqual(False, q.is_valid(lamda, 0, 0))
        self.assertEqual(False, q.is_valid(0, mu, 0))
        self.assertEqual(False, q.is_valid(0, 0, 0))

        self.assertEqual(False, q.is_valid(-lamda, mu, c))
        self.assertEqual(False, q.is_valid(lamda, -mu, c))
        self.assertEqual(False, q.is_valid(lamda, mu, -c))
        self.assertEqual(False, q.is_valid(-lamda, -mu, c))
        self.assertEqual(False, q.is_valid(-lamda, mu, -c))
        self.assertEqual(False, q.is_valid(lamda, -mu, -c))
        self.assertEqual(False, q.is_valid(-lamda, -mu, -c))

        # test with non-numeric arguments
        self.assertEqual(False, q.is_feasible("twenty", mu, c))
        self.assertEqual(False, q.is_feasible(lamda, "25", c))
        self.assertEqual(False, q.is_feasible(lamda, mu, "one"))
        self.assertEqual(False, q.is_feasible("twenty", "25", c))
        self.assertEqual(False, q.is_feasible("twenty", mu, "one"))
        self.assertEqual(False, q.is_feasible(lamda, "25", "one"))
        self.assertEqual(False, q.is_feasible("twenty", "25", "one"))

        # test valid with multi-valued lamda (or at least lamda a tuple)
        self.assertEqual(True, q.is_feasible((5, 10, 5), mu))
        self.assertEqual(True, q.is_feasible((5, 10, 5), mu, c))
        self.assertEqual(True, q.is_feasible((20,), mu, 1))
        self.assertEqual(True, q.is_feasible((20,), mu, 2))

        # test invalid with multi-valued lamda
        self.assertEqual(False, q.is_feasible((-5, 10, 5), mu, c))
        self.assertEqual(False, q.is_feasible((5, -10, 5), mu, c))
        self.assertEqual(False, q.is_feasible((5, 10, -5), mu, c))
        self.assertEqual(False, q.is_feasible((-5, -10, 5), mu, c))
        self.assertEqual(False, q.is_feasible((-5, 10, -5), mu, c))
        self.assertEqual(False, q.is_feasible((5, -10, -5), mu, c))
        self.assertEqual(False, q.is_feasible((-5, -10, -5), mu, c))
        self.assertEqual(False, q.is_feasible((5, 10, 5), -mu, c))
        self.assertEqual(False, q.is_feasible((5, 10, 5), mu, -c))
        self.assertEqual(False, q.is_feasible((5, 10, 5), -mu, -c))
        self.assertEqual(False, q.is_feasible((-5, 10, 5), -mu, -c))

    # def test_calc_lq_mm1(self):
    #
    #     self.assertAlmostEqual(3.2, q.calc_lq_mm1(20,25))
    #     self.assertAlmostEqual(math.inf, q.calc_lq_mm1(25,25))
    #     self.assertTrue(math.isnan(q.calc_lq_mm1(0,25)))
    #     self.assertTrue(math.isnan(q.calc_lq_mm1(20,0)))
    #     self.assertTrue(math.isnan(q.calc_lq_mm1(0,0)))


    def test_calc_p0(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test for valid queues, single valued lamda
        self.assertAlmostEqual(0.2, q.calc_p0(20, 25, 1))
        self.assertAlmostEqual(0.4, q.calc_p0(15, 25))
        self.assertAlmostEqual(0.0345423, q.calc_p0(65, 25, 3))


        # test for invalid queues
        self.assertTrue(math.isnan(q.calc_p0(0, 25, 1)))
        self.assertTrue(math.isnan(q.calc_p0(20, 0, 1)))
        self.assertTrue(math.isnan(q.calc_p0(20, 25, 0)))
        self.assertTrue(math.isnan(q.calc_p0(0, 0, 1)))
        self.assertTrue(math.isnan(q.calc_p0(0, 25, 0)))
        self.assertTrue(math.isnan(q.calc_p0(20, 0, 0)))
        self.assertTrue(math.isnan(q.calc_p0(0, 0, 0)))

        self.assertTrue(math.isnan(q.calc_p0(-lamda, mu, c)))
        self.assertTrue(math.isnan(q.calc_p0(lamda, -mu, c)))
        self.assertTrue(math.isnan(q.calc_p0(lamda, mu, -c)))
        self.assertTrue(math.isnan(q.calc_p0(-lamda, -mu, c)))
        self.assertTrue(math.isnan(q.calc_p0(-lamda, mu, -c)))
        self.assertTrue(math.isnan(q.calc_p0(lamda, -mu, -c)))
        self.assertTrue(math.isnan(q.calc_p0(-lamda, -mu, -c)))

        # test for infeasible queues
        self.assertTrue(math.isinf(q.calc_p0(lamda, lamda, c)))
        self.assertTrue(math.isinf(q.calc_p0(mu, mu, c)))
        self.assertTrue(math.isinf(q.calc_p0(2 * lamda, mu, c)))
        self.assertTrue(math.isinf(q.calc_p0((5, 10, 5), lamda, c)))

        # test for valid queues, multi-valued lamda
        self.assertAlmostEqual(0.2, q.calc_p0((5, 10, 5), 25, 1))
        self.assertAlmostEqual(0.4, q.calc_p0((2, 3, 10), 25))
        self.assertAlmostEqual(0.0345423, q.calc_p0((15, 20, 30), 25, 3))



    def test_calc_lq_mmc(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test valid results
        self.assertAlmostEqual(3.2, q.calc_lq_mmc(20, 25))
        self.assertAlmostEqual(3.2, q.calc_lq_mmc(20, 25, 1))
        self.assertAlmostEqual(2.8444, q.calc_lq_mmc(40, 25, 2), 4)
        self.assertAlmostEqual(0.8889, q.calc_lq_mmc(50, 25, 3), 4)
        self.assertAlmostEqual(1.0002, q.calc_lq_mmc(70, 25, 4), 4)
        self.assertAlmostEqual(46.8439, q.calc_lq_mmc(98, 25, 4), 4)

        # test invalid results

        self.assertTrue(math.isnan(q.calc_lq_mmc(0, 25, 1)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(20, 0, 1)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(20, 25, 0)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(0, 0, 1)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(0, 25, 0)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(20, 0, 0)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(0, 0, 0)))

        self.assertTrue(math.isnan(q.calc_lq_mmc(-lamda, mu, c)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(lamda, -mu, c)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(lamda, mu, -c)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(-lamda, -mu, c)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(-lamda, mu, -c)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(lamda, -mu, -c)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(-lamda, -mu, -c)))

        # test infeasible queues
        self.assertTrue(math.isinf(q.calc_lq_mmc(lamda, lamda, c)))
        self.assertTrue(math.isinf(q.calc_lq_mmc(mu, mu, c)))
        self.assertTrue(math.isinf(q.calc_lq_mmc(2 * lamda, mu, c)))
        self.assertTrue(math.isinf(q.calc_lq_mmc((5, 10, 5), lamda, c)))

        # test valid results with multiple classes
        self.assertAlmostEqual(3.2, q.calc_lq_mmc((5, 10, 5), 25, 1))
        self.assertAlmostEqual(2.8444, q.calc_lq_mmc((10, 15, 15), 25, 2), 4)
        self.assertAlmostEqual(0.8889, q.calc_lq_mmc((10, 20, 20), 25, 3), 4)
        self.assertAlmostEqual(1.0002, q.calc_lq_mmc((20, 20, 30), 25, 4), 4)
        self.assertAlmostEqual(46.8439, q.calc_lq_mmc((40, 58), 25, 4), 4)




    def test_calc_bk_mmc(self):
        k = 2
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, (5, 10, 5), 25, 1))
        self.assertAlmostEqual(0.8, q.calc_bk_mmc(1, (5, 10, 5), 25, 1))
        self.assertAlmostEqual(0.4, q.calc_bk_mmc(2, (5, 10, 5), 25, 1))
        self.assertAlmostEqual(0.2, q.calc_bk_mmc(3, (5, 10, 5), 25, 1))

        # test with non tuple lamda
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, 20, 25, 1))
        self.assertAlmostEqual(0.2, q.calc_bk_mmc(1, 20, 25, 1))
        self.assertTrue(math.isnan(q.calc_bk_mmc(2, 20, 25, 1)))

        # test with single value tuple lamda
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, (20,), 25, 1))
        self.assertAlmostEqual(0.2, q.calc_bk_mmc(1, (20,), 25, 1))
        self.assertTrue(math.isnan(q.calc_bk_mmc(2, (20,), 25, 1)))

        self.assertTrue(math.isnan(q.calc_bk_mmc(-k, 20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(k, (20, -4), 25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(k, (-20, 4), 25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(1, -20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(1, 20, -25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(1, 20, 25, -1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(1, 20, -25, 1)))


    def test_calc_wqk_mmc(self):
        k = 2
        self.assertAlmostEqual(0.04, q.calc_wqk_mmc(1, (5, 10, 5), 25, 1))
        self.assertAlmostEqual(0.1, q.calc_wqk_mmc(2, (5, 10, 5), 25, 1))
        self.assertAlmostEqual(0.4, q.calc_wqk_mmc(3, (5, 10, 5), 25, 1))

        self.assertAlmostEqual(0.16, q.calc_wqk_mmc(1, (20,), 25, 1))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(2, (20,), 25, 1)))

        self.assertAlmostEqual(0.16, q.calc_wqk_mmc(1, 20, 25, 1))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(2, 20, 25, 1)))

        self.assertTrue(math.isnan(q.calc_wqk_mmc(-k, 20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(0, 20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(k, (20, -4), 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(k, (-20, 4), 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(1, -20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(1, 20, -25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(1, 20, 25, -1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(1, 20, -25, 1)))

    def test_calc_lqk_mmc(self):
        k = 3
        lamda = (10,15,20)
        wqk = q.calc_wqk_mmc(k, lamda, self.mu, 2)

        # validity checks
        self.assertTrue(math.isnan(q.calc_lqk_mmc(0, lamda, wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(-k, lamda, wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(k, (10,15), wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(2, (10,), wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(k, 0, wqk)))

        # test with non-numeric arguments
        parms = [["one", 20, 25],
                 [1, "twenty", 25],
                 [1, 20, "twenty-five"],
                 ["one", "twenty", 25],
                 ["one", 20, "twenty-five"],
                 [1, "twenty", "twenty-five"],
                 ["one", "twenty", "twenty-five"]
        ]

        for k, lamda, wqk in parms:
            with self.subTest(k=k, lamda=lamda, wkq=wqk):
                self.assertTrue(math.isnan(q.calc_lqk_mmc(k, lamda, wqk)))

        # test with valid arguments
        parms = [[1, (5, 10, 15), 35],
                 [2, (5, 10, 15), 35],
                 [3, (5, 10, 15), 35],
                 [1, (5, 10, 15), 100],
                 [2, (5, 10, 15), 100],
                 [3, (5, 10, 15), 100]
        ]

        for k, lamda, wqk in parms:
            with self.subTest(k=k, lamda=lamda, wkq=wqk):
                self.assertAlmostEqual(lamda[k-1] * wqk, q.calc_lqk_mmc(k, lamda, wqk))


    def test_use_littles_law(self):
        lamda = 1
        mu = 2
        c = 3

        # using default values test default values for lamda, mu, and c (see setUp)

        # test all variations with a single server
        expected = { 'lq' : 3.2,
                     'l' : 4.0,
                     'wq' : 0.16,
                     'w' : 0.2,
                     'r' : 0.8,
                     'ro' : 0.8
                     }

        # test invalid call, no lq specified
        self.assertEqual(None,q.use_littles_law(self.lamda, self.mu, self.c))

        # test invalid queue
        self.assertTrue(math.isnan(q.use_littles_law(0, 25, 1, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(20, 0, 1, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(20, 25, 0, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(0, 0, 1, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(0, 25, 0, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(20, 0, 0, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(0, 0, 0, lq=math.nan)))

        self.assertTrue(math.isnan(q.use_littles_law(-lamda, mu, c, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(lamda, -mu, c, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(lamda, mu, -c, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(-lamda, -mu, c, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(-lamda, mu, -c, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(lamda, -mu, -c, lq=math.nan)))
        self.assertTrue(math.isnan(q.use_littles_law(-lamda, -mu, -c, lq=math.nan)))


        # test infeasible queue
        self.infLamda = 50
        self.infMu = 10
        self.infC = 1
        self.assertTrue(math.isinf(q.use_littles_law(self.infLamda, self.infMu, self.infC, lq=math.inf)))
        self.assertTrue(math.isinf(q.use_littles_law(self.infMu, self.infMu, 1, lq=math.inf)))
        self.assertTrue(math.isinf(q.use_littles_law(self.infLamda, self.infLamda, self.infC, lq=math.inf)))
        self.assertTrue(math.isinf(q.use_littles_law(2 * self.lamda, self.infMu, self.infC, lq=math.inf)))
        self.assertTrue(math.isinf(q.use_littles_law((5, 10, 15), 5, self.infC, lq=math.inf)))

        actual = q.use_littles_law(self.lamda, self.mu, self.c, lq=3.2)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], 5)

        actual = q.use_littles_law(self.lamda, self.mu, self.c, l=4.0)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], 5)

        actual = q.use_littles_law(self.lamda, self.mu, self.c, wq=0.16)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], 5)

        actual = q.use_littles_law(self.lamda, self.mu, self.c, w=0.2)


        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], 5)

        # now test with multiple classes of service
        self.lamda = (5, 20, 30)
        self.c = 3

        expected = { 'lq' : 1.49094,
                     'l' : 3.690940,
                     'wq' : 0.027108,
                     'w' : 0.067108,
                     'r' : 2.2,
                     'ro' : 0.733333
                     }
        expected_qk = {'wqk': [0.007745126563863838, 0.011617689845795755, 0.04066191446028516],
                       'lqk': [0.03872563281931919, 0.2323537969159151, 1.2198574338085548]}

        actual = q.use_littles_law(self.lamda, self.mu, self.c, lq=1.49094)

        #print(actual)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], round(actual[k],6), places=6)

        for k in expected_qk.keys():
            with self.subTest(metric=k):
                qkmetric = actual[k]
                rndact = [round(x, 6) for x in qkmetric]
                rndexp = [round(x, 6) for x in expected_qk[k]]
                self.assertListEqual(rndexp, rndact)

        # now test with a single class of service
        self.lamda = 55
        self.c = 3

        expected = { 'lq' : 1.49094,
                     'l' : 3.69094,
                     'wq' : 0.02711,
                     'w' : 0.06711,
                     'r' : 2.2,
                     'ro' : 0.73333
                     }
        expected_qk = {'wqk': [0.0077451, 0.0116177, 0.0406619],
                       'lqk': [0.0387256, 0.2323538, 1.2198574]}

        actual = q.use_littles_law(self.lamda, self.mu, self.c, lq=1.49094)

        #print(actual)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], places=5)

        for k in expected_qk.keys():
            with self.subTest(metric=k):
                self.assertFalse(k in actual)

        # now test with a single class of service as a tuple
        self.lamda = (55,)
        self.c = 3

        expected = { 'lq' : 1.49094,
                     'l' : 3.69094,
                     'wq' : 0.02711,
                     'w' : 0.06711,
                     'r' : 2.2,
                     'ro' : 0.73333
                     }
        expected_qk = {'wqk': [0.0077451, 0.0116177, 0.0406619],
                       'lqk': [0.0387256, 0.2323538, 1.2198574]
                       }

        actual = q.use_littles_law(self.lamda, self.mu, self.c, lq=1.49094)

        #print(actual)

        for k in expected.keys():
            with self.subTest(metric=k):
                self.assertAlmostEqual(expected[k], actual[k], 5)

        # for k in expected_qk.keys():
        #     with self.subTest(metric=k):
        #         self.assertFalse(k in actual)

        # verify that no qk statistics were produced
        self.assertFalse('lqk' in actual)
        self.assertFalse('wqk' in actual)


# suite = unittest.TestSuite([Test_queues()])

if __name__ == '__main__':
    rslt = main(verbosity=2, exit=False)

    print('done')






