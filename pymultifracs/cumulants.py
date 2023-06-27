"""
Authors: Omar D. Domingues <omar.darwiche-domingues@inria.fr>
         Merlin Dumeur <merlin@dumeur.net>
"""

from dataclasses import dataclass, field, InitVar
from multiprocessing.sharedctypes import Value
from typing import List, Tuple, Dict

import numpy as np
from scipy.special import binom as binomial_coefficient
from scipy.stats import norm as Gaussian
from statsmodels.robust.scale import qn_scale
# from .robust import qn
from statsmodels.robust.norms import estimate_location, TukeyBiweight
from statsmodels.tools.validation import array_like, float_like

from .viz import plot_cumulants
from .ScalingFunction import ScalingFunction
from .regression import linear_regression, prepare_regression, prepare_weights
from .utils import fast_power, MFractalVar
from .multiresquantity import MultiResolutionQuantity, \
    MultiResolutionQuantityBase
# from ._robust import _qn
# from .robust import _qn


def qn_scale2(a, c=1 / (np.sqrt(2) * Gaussian.ppf(5 / 8)), axis=0):
    """
    Computes the Qn robust estimator of scale

    The Qn scale estimator is a more efficient alternative to the MAD.
    The Qn scale estimator of an array a of length n is defined as
    c * {abs(a[i] - a[j]): i<j}_(k), for k equal to [n/2] + 1 choose 2. Thus,
    the Qn estimator is the k-th order statistic of the absolute differences
    of the array. The optional constant is used to normalize the estimate
    as explained below. The implementation follows the algorithm described
    in Croux and Rousseeuw (1992).

    Parameters
    ----------
    a : array_like
        Input array.
    c : float, optional
        The normalization constant. The default value is used to get consistent
        estimates of the standard deviation at the normal distribution.
    axis : int, optional
        The default is 0.

    Returns
    -------
    {float, ndarray}
        The Qn robust estimator of scale
    """

    # arr, mask = _replace_nan(a, 0)

    a = array_like(
        a, "a", ndim=None, dtype=np.float64, contiguous=True, order="C"
    )
    c = float_like(c, "c")

    if a.ndim == 0:
        raise ValueError("a should have at least one dimension")
    elif a.size == 0:
        return np.nan
    else:
        out = np.apply_along_axis(_qn, axis=axis, arr=a, c=c)
        if out.ndim == 0:
            return float(out)
        return out


def compute_robust_cumulants(X, m_array, alpha=1):
    # shape X (n_j, n_rep)

    n_j, n_rep = X.shape
    moments = np.zeros((len(m_array), n_rep))
    values = np.zeros_like(moments)

    idx_unreliable = (~np.isnan(X)).sum(axis=0) < 3

    # compute robust moments
    for rep in range(n_rep):

        if idx_unreliable[rep]:
            values[:, rep] = np.nan
            continue

        X_norm = X[~np.isinf(X[:, rep]) & ~np.isnan(X[:, rep]), rep]

        if X_norm.shape[0] > 10000:
            values[:, rep] = np.nan
            continue

        q_est = qn_scale(X_norm)

        if np.isclose(q_est, 0):
            values[m_array == 1, rep] = np.median(X_norm, axis=0)
            continue

        try:
            m_est = estimate_location(X_norm, q_est, norm=TukeyBiweight(),
                                      maxiter=1000)
        except ValueError:

            if X_norm.shape[0] < 20:
                values[:, rep] = np.nan
                continue

            print(q_est, X_norm.shape)
            print(X_norm)

            m_est = np.median(X_norm)

        X_norm -= m_est
        X_norm /= q_est

        # X_norm -= X_norm.mean()
        # X_norm /= X_norm.std()

        # print(X_norm.mean(), X_norm.std())

        for ind_m, m in enumerate(m_array):

            decaying_factor = (alpha
                               * np.exp(-.5 * (alpha ** 2 - 1) * X_norm ** 2))

            moments[ind_m, rep] = np.mean(
                fast_power(alpha * X_norm, m) * decaying_factor, axis=0)

            if m == 1:
                values[ind_m, rep] = m_est
            elif m == 2:
                values[ind_m, rep] = q_est ** 2
            else:
                aux = 0

                for ind_n, n in enumerate(np.arange(1, m)):

                    if m_array[ind_m - ind_n - 1] > 2:
                        temp_moment = moments[ind_m - ind_n - 1, rep]
                    elif m_array[ind_m - ind_n - 1] == 2:
                        temp_moment = X_norm.var()
                    elif m_array[ind_m - ind_n - 1] == 1:
                        temp_moment = X_norm.mean()

                    if m_array[ind_n] > 2:
                        temp_value = values[ind_n, rep]
                    elif m_array[ind_n] == 2:
                        temp_value = X_norm.var()
                    elif m_array[ind_n] == 1:
                        temp_value = X_norm.mean()

                    aux += (binomial_coefficient(m-1, n-1)
                            * temp_value * temp_moment)

                values[ind_m, rep] = moments[ind_m, rep] - aux

    return values


@dataclass
class Cumulants(MultiResolutionQuantityBase, ScalingFunction):
    r"""
    Computes and analyzes cumulants

    Parameters
    ----------
    mrq : MultiResolutionQuantity
        Multi resolution quantity to analyze.
    n_cumul : int
        Number of cumulants to compute.
    j1 : int
        Lower-bound of the scale support for the linear regressions.
    j2 : int
        Upper-bound of the scale support for the linear regressions.
    weighted: str | None
        Whether to used weighted linear regressions.


    Attributes
    ----------
    formalism : str
        Formalism used. Can be any of 'wavelet coefs', 'wavelet leaders',
        or 'wavelet p-leaders'.
    nj : dict(ndarray)
        Number of coefficients at scale j.
        Arrays are of the shape (n_rep,)
    values : ndarray, shape (n_cumulants, n_scales, n_rep)
        :math:`C_m(j)`.
    n_cumul : int
        Number of computed cumulants.
    j1 : int
        Lower-bound of the scale support for the linear regressions.
    j2 : int
        Upper-bound of the scale support for the linear regressions.
    weighted : str | None
        Whether weighted regression was performed.
    m : ndarray, shape (n_cumulants,)
        List of the m values (cumulants), in order presented in the value
        arrays.
    j : ndarray, shape (n_scales,)
        List of the j values (scales), in order presented in the value arrays.
    log_cumulants : ndarray, shape (n_cumulants, n_rep)
        :math:`(c_m)_m`, slopes of the curves :math:`j \times C_m(j)`.
    var_log_cumulants : ndarray, shape (n_cumulants, n_rep)
        Estimates of the log-cumulants

        .. warning:: var_log_cumulants
                     was not debugged
    n_rep : int
        Number of realisations

    """
    mrq: InitVar[MultiResolutionQuantity]
    n_cumul: int
    scaling_ranges: List[Tuple[int]]
    bootstrapped_mfa: InitVar[MFractalVar] = None
    weighted: str = None
    robust_kwargs: Dict[str, object] = field(default_factory=dict)
    robust: InitVar[bool] = False
    m: np.ndarray = field(init=False)
    j: np.ndarray = field(init=False)
    values: np.ndarray = field(init=False)
    log_cumulants: np.ndarray = field(init=False)
    var_log_cumulants: np.ndarray = field(init=False)

    def __post_init__(self, mrq, bootstrapped_mfa, robust):

        self.formalism = mrq.formalism
        self.nj = mrq.nj
        self.n_sig = mrq.n_sig
        self.j = np.array(list(mrq.values))

        if bootstrapped_mfa is not None:
            self.bootstrapped_mrq = bootstrapped_mfa.cumulants

        self.m = np.arange(1, self.n_cumul+1)
        self.values = np.zeros((len(self.m), len(self.j), mrq.n_rep))

        self._compute(mrq, robust)
        self._compute_log_cumulants(mrq.n_rep)

    def __repr__(self):

        out = "Cumulants"
        display_params = (
            'formalism scaling_ranges weighted n_cumul').split(' ')

        for param in display_params:
            out += f" {param} = {getattr(self, param)}"

        return out

    def _compute(self, mrq, robust):

        moments = np.zeros((len(self.m), len(self.j), mrq.n_rep))
        aux = np.zeros_like(moments)

        for ind_j, j in enumerate(self.j):

            T_X_j = np.abs(mrq.values[j])

            log_T_X_j = np.log(T_X_j)

            # dropping infinite coefsx
            log_T_X_j[np.isinf(log_T_X_j)] = np.nan

            if robust:

                values = compute_robust_cumulants(
                    log_T_X_j, self.m, **self.robust_kwargs)

                self.values[:, ind_j] = values

            else:
                # Non-robust estimation
                for ind_m, m in enumerate(self.m):

                    moments[ind_m, ind_j] = np.nanmean(
                        fast_power(log_T_X_j, m), axis=0)

                    idx_unreliable = (~np.isnan(log_T_X_j)).sum(axis=0) < 3
                    moments[ind_m, ind_j, idx_unreliable] = np.nan

                    if m == 1:
                        self.values[ind_m, ind_j] = moments[ind_m, ind_j]
                    else:
                        aux = 0

                        for ind_n, n in enumerate(np.arange(1, m)):
                            aux += (binomial_coefficient(m-1, n-1)
                                    * self.values[ind_n, ind_j]
                                    * moments[ind_m-ind_n-1, ind_j])

                        self.values[ind_m, ind_j] = moments[ind_m, ind_j] - aux

    def _compute_log_cumulants(self, n_rep):
        """
        Compute the log-cumulants
        (angular coefficients of the curves j->log[C_p(j)])
        """

        x, n_ranges, j_min, j_max, j_min_idx, j_max_idx = prepare_regression(
            self.scaling_ranges, self.j
        )

        self.log_cumulants = np.zeros((len(self.m), n_ranges, n_rep))
        self.var_log_cumulants = np.zeros_like(self.log_cumulants)
        self.slope = np.zeros_like(self.log_cumulants)
        self.intercept = np.zeros_like(self.log_cumulants)
        self.weights = np.zeros((len(self.m), int(j_max - j_min + 1), n_ranges,
                                 n_rep))

        log2_e = np.log2(np.exp(1))

        # shape (n_moments, n_scales, n_scaling_ranges, n_rep)
        y = self.values[:, int(j_min_idx):int(j_max_idx), None, :]

        if self.weighted == 'bootstrap':

            # case where self is the bootstrapped mrq
            if self.bootstrapped_mrq is None:
                std = self.STD_values[:, j_min_idx:j_max_idx]

            else:

                if j_min < self.bootstrapped_mrq.j.min():
                    raise ValueError(
                        f"Bootstrap minimum scale "
                        f"{self.bootstrapped_mrq.j.min()} inferior to minimum "
                        f"scale {j_min} used in estimation")

                start = int(j_min - self.bootstrapped_mrq.j.min())
                end = int(j_max - self.bootstrapped_mrq.j.min()) + 1

                std_slice = np.s_[
                    int(j_min - self.bootstrapped_mrq.j.min()):
                    int(j_max - self.bootstrapped_mrq.j.min() + 1)]

                std = self.bootstrapped_mrq.STD_values[:, std_slice]

        else:
            std = None

        self.weights = prepare_weights(self, self.weighted, n_ranges,
                                       j_min, j_max,
                                       self.scaling_ranges, std)

        nan_weighting = np.ones_like(y)
        nan_weighting[np.isnan(y)] = np.nan

        try:
            self.weights * nan_weighting
        except Exception:
            print("")

        self.weights = self.weights * nan_weighting

        # pylint: disable=unbalanced-tuple-unpacking
        self.slope, self.intercept, self.var_log_cumulants = \
            linear_regression(x, y, self.weights, return_variance=True)

        self.var_log_cumulants *= (log2_e ** 2)

        self.log_cumulants = log2_e * self.slope

    def compute_R(self):

        values = self.values.reshape(*self.values.shape[:2], self.n_sig, -1)
        slope = self.slope.reshape(*self.slope.shape[:2], self.n_sig, -1)
        intercept = self.intercept.reshape(
            *self.intercept.shape[:2], self.n_sig, -1)

        return super()._compute_R(values, slope, intercept)

    def compute_R2(self):
        return super()._compute_R2(self.values, self.slope, self.intercept,
                                   self.weights)

    def __getattribute__(self, __name: str):

        if __name == 'n_sig' and super().__getattribute__('n_sig') is None:
            return 1

        # return self.__getattr__(__name)

        # try:
        return super().__getattribute__(__name)
        # except AttributeError:
        #     return self.__getattr__(__name)

    def __getattr__(self, name):

        if name[0] == 'c' and len(name) == 2 and name[1:].isdigit():

            out = self.log_cumulants[self.m == int(name[1])][0]
            out = out.reshape(out.shape[0], self.n_sig, -1)

            return out

        if name[0] == 'C' and len(name) == 2 and name[1:].isdigit():

            out = self.values[self.m == int(name[1])][0]
            out = out.reshape(out.shape[0], self.n_sig, -1)

            return out

        if name == 'M':
            return -self.c2

        if name == 'n_rep':
            return self.log_cumulants.shape[-1]

        return super().__getattr__(name)

    def plot(self, figsize=(8, 6), fignum=1, nrow=3, j1=None, filename=None,
             scaling_range=0, n_cumul=None, signal_idx=0, **kwargs):

        return plot_cumulants(
            self, figsize, fignum, nrow, j1, filename, scaling_range,
            n_cumul=n_cumul, signal_idx=signal_idx, **kwargs)
