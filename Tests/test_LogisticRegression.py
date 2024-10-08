# Copyright 2004-2008 by Michiel de Hoon.  All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

# See the Biopython Tutorial for an explanation of the biological
# background of these tests.

"""Tests for LogisticRegression module."""

import copy
import unittest
import warnings

try:
    import numpy as np
    from numpy import linalg  # missing in PyPy's micronumpy
except ImportError:
    from Bio import MissingExternalDependencyError

    raise MissingExternalDependencyError(
        "Install NumPy if you want to use Bio.LogisticRegression."
    ) from None

from Bio import BiopythonDeprecationWarning

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=BiopythonDeprecationWarning)
    from Bio import LogisticRegression


xs = [
    [-53, -200.78],
    [117, -267.14],
    [57, -163.47],
    [16, -190.30],
    [11, -220.94],
    [85, -193.94],
    [16, -182.71],
    [15, -180.41],
    [-26, -181.73],
    [58, -259.87],
    [126, -414.53],
    [191, -249.57],
    [113, -265.28],
    [145, -312.99],
    [154, -213.83],
    [147, -380.85],
    [93, -291.13],
]

ys = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]


def show_progress(iteration, loglikelihood):
    """No action callback function, used when training the model."""


class TestLogisticRegression(unittest.TestCase):
    def test_xs_and_ys_input_parameter_lengths(self):
        modified_xs = copy.copy(xs)
        modified_xs.pop()
        self.assertRaises(ValueError, LogisticRegression.train, modified_xs, ys)

    def test_ys_input_class_assignments(self):
        modified_ys = copy.copy(ys)
        modified_ys.pop()
        modified_ys.append(2)
        self.assertRaises(ValueError, LogisticRegression.train, xs, modified_ys)

    def test_dimensionality_of_input_xs(self):
        modified_xs = copy.copy(xs)
        modified_xs[0] = []
        self.assertRaises(ValueError, LogisticRegression.train, modified_xs, ys)

    def test_calculate_model(self):
        model = LogisticRegression.train(xs, ys)
        beta = model.beta
        self.assertAlmostEqual(beta[0], 8.9830, places=4)
        self.assertAlmostEqual(beta[1], -0.0360, places=4)
        self.assertAlmostEqual(beta[2], 0.0218, places=4)

    def test_calculate_model_with_update_callback(self):
        model = LogisticRegression.train(xs, ys, update_fn=show_progress)
        beta = model.beta
        self.assertAlmostEqual(beta[0], 8.9830, places=4)

    def test_classify(self):
        model = LogisticRegression.train(xs, ys)
        result = LogisticRegression.classify(model, [6, -173.143442352])
        self.assertEqual(result, 1)
        result = LogisticRegression.classify(model, [309, -271.005880394])
        self.assertEqual(result, 0)

    def test_calculate_probability(self):
        model = LogisticRegression.train(xs, ys)
        q, p = LogisticRegression.calculate(model, [6, -173.143442352])
        self.assertAlmostEqual(p, 0.993242, places=6)
        self.assertAlmostEqual(q, 0.006758, places=6)
        q, p = LogisticRegression.calculate(model, [309, -271.005880394])
        self.assertAlmostEqual(p, 0.000321, places=6)
        self.assertAlmostEqual(q, 0.999679, places=6)

    def test_model_accuracy(self):
        correct = 0
        model = LogisticRegression.train(xs, ys)
        predictions = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(predictions)):
            prediction = LogisticRegression.classify(model, xs[i])
            self.assertEqual(prediction, predictions[i])
            if prediction == ys[i]:
                correct += 1
        self.assertEqual(correct, 16)

    def test_leave_one_out(self):
        correct = 0
        predictions = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        for i in range(len(predictions)):
            model = LogisticRegression.train(xs[:i] + xs[i + 1 :], ys[:i] + ys[i + 1 :])
            prediction = LogisticRegression.classify(model, xs[i])
            self.assertEqual(prediction, predictions[i])
            if prediction == ys[i]:
                correct += 1
        self.assertEqual(correct, 15)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
