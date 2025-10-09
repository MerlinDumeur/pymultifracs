import numpy as np
import jax.numpy as jnp
from jax.scipy.special import gammaln


def _integrate_jax(wt_coefs_values, gamint, max_level):

    wt_out = {}

    for scale in range(1, max_level + 1):

        wt_out[scale] = wt_coefs_values[scale] * 2 ** (gamint * scale)

    return wt_out


def _compute_leaders_jax(wt_coefs_values, p_exp, size, max_level, leader_flag):

    pleader_p = {}

    for scale in range(1, max_level + 1):

        coefs = jnp.power(jnp.abs(wt_coefs_values[scale]), p_exp)

        scale_contribution = jnp.zeros((size, *coefs.shape)) - 1

        if size > 1:
            idx_size = np.s_[(size-1)//2:-((size-1)//2)]
        else:
            idx_size = np.s_[:]

        scale_contribution = scale_contribution.at[:, idx_size].set(
            jnp.stack([
                coefs[size-i:-(i-1) or None] for i in range(1, size+1)
            ], axis=0))

        if scale == 1:

            leaders = np.sum(scale_contribution, axis=0)
            pleader_p[scale] = leaders

            continue

        max_index = pleader_p[scale-1].shape[0] // 2

        lower_contribution = jnp.zeros((2, *coefs.shape)) - 1

        lower_contribution = lower_contribution.at[0, :max_index].set(
            pleader_p[scale-1][::2][:max_index]
        )
        lower_contribution = lower_contribution.at[1, :max_index].set(
            pleader_p[scale-1][1::2][:max_index]
        )

        if leader_flag:

            pleader_p[scale] = np.max(np.r_[
                scale_contribution,
                .5 * lower_contribution
            ], axis=0)

        else:

            pleader_p[scale] = jnp.sum(jnp.r_[
                scale_contribution,
                .5 * lower_contribution
            ], axis=0)  # * ZPJCorr[:, scale-1]

    return pleader_p


def _binom(N, k):
    return jnp.exp(gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1))


def _compute_Cmj(pleader_p, j, p, ZPJCorr, validity, n_cumul):

    T_X_j = jnp.log(pleader_p ** (1/p) * ZPJCorr)

    Mu = jnp.stack([
        jnp.mean(T_X_j ** m, where=validity, axis=0)
        for m in range(1, n_cumul+1)
    ], axis=0)

    Cmj = jnp.zeros_like(Mu)

    for ind_m, m in enumerate(range(1, n_cumul+1)):

        aux = 0

        for ind_n, n in enumerate(range(1, m)):
            aux = aux + _binom(m-1, n-1) * Cmj[ind_n] * Mu[ind_m-ind_n-1]

        Cmj = Cmj.at[ind_m].set(Mu[ind_m] - aux)

    return Cmj


def _compute_Cm_jax(pleader_p, j1, j2, n_cumul, p, ZPJCorr, validity):

    Cm = jnp.stack(
        [
            _compute_Cmj(pleader_p[j], j, p, ZPJCorr[:, j-1], validity[j],
                         n_cumul)
            for ind_j, j in enumerate(range(j1, j2+1))
        ],
        axis=0
    )

    return Cm


def _compute_cm_jax(Cm, j_array, n_cumul):

    fits = [
        jnp.polyfit(j_array.astype(float), Cm[:, m], 1)
        for m in range(n_cumul)
    ]

    cm = jnp.stack([f[0] for f in fits], axis=0)
    cm0 = jnp.stack([f[1] for f in fits], axis=0)

    return cm, cm0


def get_validity_coef(values_dict):

    return {
        scale: ~np.isnan(val)
        for scale, val in values_dict.items()
    }


def get_validity_leader(values_dict):

    return {
        scale: ~(np.isnan(val) | (val < 0))
        for scale, val in values_dict.items()
    }


def _correct_pleaders_jax(eta_p, p_exp, max_level):

    j_array = jnp.arange(1, max_level + 1)
    JJ = j_array
    J1LF = 1
    JJ0 = JJ - J1LF + 1

    # eta_p shape (n_rep,)
    # JJ0 shape (n_level,)

    JJ0 = JJ0[None, :]
    # eta_p = wt_leaders.eta_p
    eta_p = eta_p[:, None]

    zqhqcorr = jnp.log2((1 - jnp.power(2., -JJ0 * eta_p))
                        / (1 - jnp.power(2., -eta_p)))
    ZPJCorr = jnp.power(2, (-1.0 / p_exp) * zqhqcorr)

    # ZPJCorr shape (n_ranges, n_rep, n_level)
    # ZPJCorr = ZPJCorr.at[eta_p <= 0].set(1)
    ZPJCorr = jnp.where(eta_p < 0, 1, ZPJCorr)

    return ZPJCorr


def compute_etap(wt_coefs, j1, j2, p, validity):

    Sj = jnp.zeros((j2-j1+1, wt_coefs[j1].shape[1]))

    Sj = jnp.stack([
        jnp.log2(jnp.mean(wt_coefs[scale] ** p, axis=0, where=validity[scale]))
        # jnp.log2(jnp.nanmean(wt_coefs[scale] ** p, axis=0))
        for scale in range(j1, j2+1)
    ], axis=0)

    return jnp.polyfit(jnp.arange(j1, j2+1).astype(float), Sj, 1)[0]


def integrate_wt(wt_coefs, gamint):

    return {
        scale: wt_coefs[scale] * 2 ** (scale * gamint)
        for scale in wt_coefs
    }
