"""Memory-bounded TPS Jacobian evaluation with the original FlowMap formula."""
import numpy as np


def _batched_tps_jacobians(self, evaluation_points, eps=1e-10):
    points = np.asarray(evaluation_points)
    weights = self.radial_coefficients
    result = np.empty((len(points), weights.shape[1], points.shape[1]))
    for start in range(0, len(points), 512):
        block = points[start:start + 512]
        differences = block[:, None, :] - self.control_points[None, :, :]
        distances = np.linalg.norm(differences, axis=2)
        # Match FlowMap's legacy fixed threshold (its eps argument is unused).
        valid = distances > 1e-10
        factor = np.zeros_like(distances)
        factor[valid] = 1 + 2 * np.log(distances[valid])
        for axis in range(points.shape[1]):
            basis = np.ascontiguousarray(factor * differences[:, :, axis])
            result[start:start + len(block), :, axis] = (
                basis @ weights + self.polynomial_coefficients[axis + 1, :]
            )
    return result


def enable_batched_tps_jacobians():
    """Use equivalent matrix contractions; do not change spline fits or inputs."""
    from flowmap.core.thin_plate_spline import ThinPlateSpline
    ThinPlateSpline.compute_jacobians = _batched_tps_jacobians
