---
title: 'Pymultifracs: A Python package for multifractal analysis'
tags:
    - Python
    - scale invariance
    - signal processing
authors:
  - name: Merlin Dumeur
    affiliation: '1, 2'

  - name: Philippe Ciuciu
    affiliation: '1, 2'

  - name: Patrice Abry
    affiliation: '4'

  - name: Guillaume Saës
    affiliation: '5'

  - name:
      given-names: Roberto Fabio
      surname: Leonarduzzi
    affiliation: '4'

affiliations:
 - name: Neurospin, CEA Saclay, France
   index: 1
   ror: 03n15ch10
 - name: MIND, INRIA Saclay, France
   index: 2
   ror: 0315e5x55
 - name: NBE, Aalto University, Finland
   index: 3
   ror: 020hwjq30
 - name: Laboratoire de Physique, ENS Lyon, France
   index: 4
   ror: 00w5ay796

date: XX August 2025

bibliography: paper.bib
---

# Summary

PyMultiFracs is a Python package that provides tools for wavelet-based multifractal analysis of 1D signals. It allows users to compute various multiresolution quantities such as wavelet coefficients, wavelet-leaders, and p-leaders; perform statistical computations including structure functions, cumulants, and log-cumulants; estimate the multifractal spectrum; conduct bivariate multifractal analysis; compute confidence intervals using bootstrap methods with automated scaling range selection; and detect outliers. This package is designed to be a comprehensive tool for researchers and developers working with multifractal analysis in Python.

# Statement of need

The pymultifracs toolbox addresses the need for a Python-based implementation of wavelet-based multifractal analysis for 1D signals. While there exists a Matlab toolbox (PLBMF) that provides similar functionality, pymultifracs offers a Python alternative, which is beneficial for researchers and developers who prefer or require Python for their workflows. This toolbox includes features such as computation of multiresolution quantities, statistical analyses, multifractal spectrum estimation, bivariate analysis, confidence interval calculations, and outlier detection, making it a comprehensive tool for multifractal analysis in Python.

# References
<!-- Key references, including other software addressing related needs -->

- Jaffard, S., Lashermes, B., & Abry, P. (2006). Wavelet Leaders in Multifractal Analysis. In Wavelet Analysis and Applications (pp. 201-246). Birkhäuser Basel.
- Wendt, H., & Abry, P. (2007). Multifractality Tests Using Bootstrapped Wavelet Leaders. IEEE Transactions on Signal Processing, 55(10), 4811-4820.
- Abry, P., Jaffard, S., & Wendt, H. (2008). When wavelets analyze multifractals. In T. Qian, X. Li, P. Yip, & Y. Wang (Eds.), Wavelet Analysis: From One Dimension to Multidimensions (pp. 1-22). Higher Education Press, Beijing, China.
- Wendt, H., Abry, P., Jaffard, S., Helgason, H., Goncalves, P., Pereira, E., ... & Doret, M. (2010). Methodology for Multifractal Analysis of Heart Rate Variability: From LF/HF Ratio to Wavelet Leaders. In Computing in Cardiology (Vol. 37, pp. 41-44).
- PLBMF Matlab toolbox: http://www.ens-lyon.fr/PHYSIQUE/Equipe3/MultiFracs/software.html

# Projects using the repository
<!-- past or ongoing  -->

- Dumeur, M., Ciuciu, P., et al. (2023). Multifractality in critical neural field dynamics. arXiv:2312.03219 [cond-mat.dis-nn]

# Acknowledgements
- Financial support
