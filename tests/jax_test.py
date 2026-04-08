from pymultifracs.wavelet import wavelet_analysis
from pymultifracs.jax.


def test_wavelet(mrw_file):

    fname = mrw_file[0]

    with open(fname, 'rb') as f:
        X = np.load(f)

    WT = wavelet_analysis(X)
    WT_int = WT.integrate(1)
    WTpL = WT.get_leaders(2)
