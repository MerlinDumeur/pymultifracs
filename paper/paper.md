---
title: 'Pymultifracs: A Python package for multifractal analysis'
tags:
    - Python
    - scale invariance
    - signal processing
    - time series
authors:
  - name: Merlin Dumeur
    affiliation: '1, 2'

  - name:
      given-names: Omar Darwiche
      surname: Domingues

  - name: Patrice Abry
    affiliation: '4'

  - name: Guillaume Saës
    affiliation: '5'

  - name:
      given-names: Roberto Fabio
      surname: Leonarduzzi
    affiliation: '4'

  - name: Stéphane Jaffard
    affiliation: '5'
  
  - name: Herwig Wendt
    affiliation: '6'

  - name: Philippe Ciuciu
    affiliation: '1, 2'

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
 - name: Laboratoire d'Analyse et de Mathématiques Appliquées, Université Paris-Est Créteil, France
   index: 5
   ror: 0581g8849
 - name: IRIT Laboratory, INP Tououse, France
   index: 6
   ror: 05wfw4946


date: XX January 2026

bibliography: paper.bib
---

# Summary

`PyMultiFracs` is a Python package that provides tools for wavelet-based multifractal analysis of 1D signals. It allows users to compute various multiresolution quantities such as wavelet coefficients, wavelet-leaders, and p-leaders; perform statistical computations including structure functions, cumulants, and log-cumulants; estimate the multifractal spectrum; conduct bivariate multifractal analysis; compute confidence intervals using bootstrap methods with automated scaling range selection; and detect outliers. This package is designed to be a comprehensive tool for researchers and developers working with multifractal analysis in Python.

# Statement of need

The `PyMultiFracs` toolbox addresses the need for a Python-based implementation of wavelet-based multifractal analysis for 1D signals. While there exists a Matlab toolbox (PLBMF) that provides similar functionality, `PyMultiFracs` offers a Python alternative, which is beneficial for researchers and developers who prefer or require Python for their workflows. This toolbox includes features such as computation of multiresolution quantities, statistical analyses, multifractal spectrum estimation, bivariate analysis, confidence interval calculations, and outlier detection, making it a comprehensive tool for multifractal analysis in Python.

# State of the field

The (discrete) wavelet-based approach to multifractal analysis[@Jaffard2004a], and particularly the properly formulated wavelet leader[@Jaffard2006] and wavelet $p$-leader[@Leonarduzzi2016] formalisms, are a relatively mathematical development of the analysis of scale invariant processes, and thus has very few implementations available. `PyMultiFracs`' first implementation was based on converting the code from the `PLBMF` toolbox[^PLBMF] in MATLAB, however it has since then taken a different direction, with the focus being placed on reaching a wide audience of scientists with publicly documented and tested code. Not all functionality of the `PLBMF` toolbox has yet been implemented in `PyMultiFracs`, as the emphasis has instead been placed on creating an API which will be easy to extend in the future.

# Software design

`PyMultiFracs` uses an object-oriented design where data is stored in Python dataclasses which are defined 

# Research impact statement

The `PyMultiFracs` toolbox has enabled publications in 

[^PLBMF]: http://www.ens-lyon.fr/PHYSIQUE/Equipe3/MultiFracs/software.html

# Acknowledgements
- Financial support
