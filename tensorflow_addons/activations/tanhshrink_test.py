# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import sys

import pytest
from absl.testing import parameterized

import numpy as np
import tensorflow as tf
from tensorflow_addons.activations import tanhshrink
from tensorflow_addons.activations.tanhshrink import _tanhshrink_py
from tensorflow_addons.utils import test_utils


@test_utils.run_all_in_graph_and_eager_modes
class TanhshrinkTest(tf.test.TestCase, parameterized.TestCase):
    @parameterized.named_parameters(
        ("float16", np.float16), ("float32", np.float32), ("float64", np.float64)
    )
    def test_same_as_py_func(self, dtype):
        np.random.seed(1234)
        for _ in range(20):
            self.verify_funcs_are_equivalent(dtype)

    def verify_funcs_are_equivalent(self, dtype):
        x_np = np.random.uniform(-10, 10, size=(4, 4)).astype(dtype)
        x = tf.convert_to_tensor(x_np)
        with tf.GradientTape(persistent=True) as t:
            t.watch(x)
            y_native = tanhshrink(x)
            y_py = _tanhshrink_py(x)
        self.assertAllCloseAccordingToType(y_native, y_py)
        grad_native = t.gradient(y_native, x)
        grad_py = t.gradient(y_py, x)
        self.assertAllCloseAccordingToType(grad_native, grad_py)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
