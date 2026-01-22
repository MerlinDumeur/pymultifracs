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
    affiliation: '2'

  - name:
      given-names: Roberto Fabio
      surname: Leonarduzzi
    affiliation: '4'

  - name: Guillaume Saës
    affiliation: '5'

  - name: Herwig Wendt
    affiliation: '6'

  - name: Stéphane Jaffard
    affiliation: '5'

  - name: Patrice Abry
    affiliation: '4'

  - name: Philippe Ciuciu
    affiliation: '1, 2'

affiliations:
 - name: Neurospin, CEA Saclay, France
   index: 1
   ror: 03n15ch10
 - name: MIND, INRIA Saclay, France
   index: 2
   ror: 0315e5x55
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
<!-- A description of the high-level functionality and purpose of the software for a diverse, non-specialist audience -->

`PyMultiFracs` is a Python package that provides tools for wavelet-based multifractal analysis of 1D signals. It allows users to compute wavelet-based multi-resolution quantities, from which the appropriate scaling functions are estimated. Additional features offered by the toolbox are: bivariate multifractal analysis; bootstrap-based confidence intervals and automated scaling range selection; outlier detection. This package is designed to be a comprehensive tool for researchers and developers working with multifractal analysis in Python.

# Statement of need

The `PyMultiFracs` toolbox addresses the need for a Python-based implementation of wavelet-based multifractal analysis for 1D signals. This toolbox includes features such as computation of multiresolution quantities, statistical analyses, multifractal spectrum estimation, bivariate analysis, confidence interval calculations, and outlier detection, making it a comprehensive tool for multifractal analysis in Python.

# State of the field

The (discrete) wavelet-based approach to multifractal analysis[@Jaffard2004a], and particularly the properly formulated wavelet leader[@Jaffard2006] and wavelet $p$-leader[@Leonarduzzi2016] formalisms, are a relatively mathematical development of the analysis of scale invariant processes, and thus has very few implementations available. `PyMultiFracs`' first implementation was based on converting the code from the `PLBMF` toolbox[^PLBMF] in MATLAB, however it has since then taken a different direction.

The unique contribution of `PyMultiFracs` is to provide a Python implementation with publicly documented and automatically tested code.
Not all functionality of the `PLBMF` toolbox has yet been implemented in `PyMultiFracs`, but its API makes it easy to extend in the future.

# Software design

<!-- structure -->
`PyMultiFracs` relies on an object-oriented design where data is stored in Python dataclasses, following the conventions used in [@Gramfort2013]. Polymorphism and abstract classes are used to define a common API for all multifractal formalisms, which also enables easy extensions of the code base.

<!-- xarray -->
As the intermediary results of multifractal analysis generate N-dimensional arrays with a large and variable number of dimensions, keeping track of what information is contained within the axes becomes difficult. This is why `PyMultiFracs` uses the `xarray`[@Hoyer2017] API to label axes, which provides easily examinable outputs, and also allows for simple plotting functions.

<!-- plotting -->
Both multi-resolution quantities and scaling functions have plotting methods which enable the users to visualize the data, final results, and intermediary computed quantities.

# Research impact statement

The `PyMultiFracs` toolbox has already enabled research in the fields of neuroscience[@Dumeur2025a], physics[@Dumeur2024_model]. It has been used to produce results ... TO-COMPLETE

[^PLBMF]: http://www.ens-lyon.fr/PHYSIQUE/Equipe3/MultiFracs/software.html

# AI usage disclosure

No generative AI tools were used in software creation, documentation, nor paper authoring.

# Acknowledgements
Development of this toolbox was supported by the following funding sources:
- ADI-IDEX Paris Saclay
- 

# References