from collections import namedtuple

from sklearn.linear_model import Ridge

from .psd import welch_estimation, wavelet_estimation, _log_plot, _log_psd


def plot_fractal(signal, s_freq, log='log2', cutoff_freq=8, n_moments=2,
                 n_fft=4096, segment_size=None):
    """
    Plot the superposition of Welch and Wavelet-based estimation of PSD, along
    with the estimation of the $beta$ coefficient on a log-log graphic.

    Parameters
    ----------
    signal: 1D-array_like
        Time series to process

    s_freq: float
        Sampling frequency of the signal

    log: str
        Log function to use on the PSD

    cutoff_freq: int, optional
        Frequency (in Hertz) which delimitates the higher bound of frequencies
        to use during the estimation of $beta$

    n_moments: int, optional
        Number of vanishing moments of the Daubechies wavelet used in the
        Wavelet decomposition.

    n_fft: int, optional
        Length of the FFT desired.
        If `segment_size` is greater, ``n_fft = segment_size``.

    segment_size: int | None
        Length of Welch segments.
        Defaults to None, which sets it equal to `n_fft`

    """

    # Compute the PSD
    freq_fourier, psd_fourier = welch_estimation(signal, s_freq, n_fft,
                                                 segment_size)
    freq_wavelet, psd_wavelet = wavelet_estimation(signal, s_freq, n_moments)

    # Estimate the 1/f slope
    slope = estimate_beta(freq_wavelet, psd_wavelet, log, cutoff_freq)

    # Compute values to plot the 1/f slope
    psd_slope = slope.beta * slope.freq + slope.log_C

    # Plot
    freq = [freq_fourier, freq_wavelet]
    psd = [psd_fourier, psd_wavelet]
    legend = ['Fourier', 'Wavelet', f'Slope: {slope.beta:.2f}']

    _log_plot(freq, psd, legend, slope=(slope.freq, psd_slope), log=log)


def fractal_analysis(signal, s_freq, n_moments=2, cutoff_freq=8, log='log2'):
    """
    Perform the estimation of the value of beta and the logged value of C, \
    where beta and log_C are defined in relation with the PSD:
        PSD(f) = C|f|^-beta

    signal: 1D-array_like
        Time series to process

    s_freq: float
        Sampling frequency of the signal

    n_moments: int, optional
        Number of vanishing moments of the Daubechies wavelet used in the
        Wavelet decomposition.

    cutoff_freq: int, optional
        Frequency (in Hertz) which delimitates the higher bound of frequencies
        to use during the estimation of `beta`

    log: str
        Log function to apply to the PSD

    """

    freq, psd = wavelet_estimation(signal, s_freq, n_moments)
    fractal = estimate_beta(freq, psd, log, cutoff_freq)

    return fractal.beta, fractal.log_C


FractalValues = namedtuple('FractalValues', ['beta',
                                             'log_C',
                                             'freq'])


def estimate_beta(freq, psd, cutoff_freq=8, log='log2'):
    """
    From the PSD and its frequency support, estimate the C and beta variables, where
        PSD(f) = C|f|^-beta

    Parameters
    ----------
    freq: 1D-array_like
        Frequencies at which the PSD has been estimated

    psd: 1D-array_like
        Power spectral density

    cutoff_freq: int, optional
        Frequency (in Hertz) which delimitates the higher bound of frequencies
        to use during the estimation of $beta$

    log: str
        Log function to use on the PSD before fitting the slope

    """

    # Low-pass the PSD
    support = [freq < cutoff_freq][0]
    freq = freq[support].reshape(-1, 1)
    psd = psd[support]

    # Log the values
    freq, psd = _log_psd(freq, psd, log)

    # Fit ridge regressor
    regressor = Ridge()
    regressor.fit(freq, psd)

    return FractalValues(beta=regressor.coef_[0],
                         log_C=regressor.intercept_,
                         freq=freq)