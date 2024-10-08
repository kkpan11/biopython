# Copyright 2014-2016 Marco Galardini.  All rights reserved.
# Adapted from test_Mymodule.py by Jeff Chang
#
# This file is part of the Biopython distribution and governed by your
# choice of the "Biopython License Agreement" or the "BSD 3-Clause License".
# Please see the LICENSE file that should have been included as part of this
# package.
"""Tests for the Bio.phenotype module's fitting functionality."""

try:
    import numpy as np

    del np
except ImportError:
    from Bio import MissingExternalDependencyError

    raise MissingExternalDependencyError(
        "Install NumPy if you want to use Bio.phenotype."
    ) from None
try:
    import scipy

    del scipy
    from scipy.optimize import OptimizeWarning
except ImportError:
    from Bio import MissingExternalDependencyError

    raise MissingExternalDependencyError(
        "Install SciPy if you want to use Bio.phenotype fit functionality."
    ) from None

import json
import unittest
import warnings

from Bio import BiopythonExperimentalWarning

with warnings.catch_warnings():
    warnings.simplefilter("ignore", BiopythonExperimentalWarning)
    from Bio import phenotype

# Example plate files
JSON_PLATE = "phenotype/Plate.json"


class TestPhenoMicro(unittest.TestCase):
    """Tests for phenotype module."""

    def test_WellRecord(self):
        """Test basic functionalities of WellRecord objects."""
        with open(JSON_PLATE) as handle:
            p = json.load(handle)

        times = p["measurements"]["Hour"]
        w = phenotype.phen_micro.WellRecord(
            "A10",
            signals={times[i]: p["measurements"]["A10"][i] for i in range(len(times))},
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", OptimizeWarning)
            w.fit()
        self.assertAlmostEqual(w.area, 20879.5)
        self.assertEqual(w.model, "gompertz")
        self.assertAlmostEqual(w.lag, 6.0425868725090357, places=5)
        self.assertAlmostEqual(w.plateau, 188.51404344898586, places=4)
        self.assertAlmostEqual(w.slope, 48.190618284831132, places=3)
        self.assertAlmostEqual(w.v, 0.10000000000000001, places=5)
        self.assertAlmostEqual(w.y0, 45.879770069807989, places=4)
        self.assertEqual(w.max, 313.0)
        self.assertEqual(w.min, 29.0)
        self.assertEqual(w.average_height, 217.82552083333334)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
