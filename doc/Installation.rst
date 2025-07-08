There are two ways to install this package: either by using a package manager to install the package only, which will make
the code only usable as an import,
or by cloning the repository first, and then installing the package which will make it editable

Installing the package
----------------------

.. .. code:: shell

..     wget https://raw.githubusercontent.com/neurospin/pymultifracs/master/env.yml
..     conda env update -f env.yml --name $ENVNAME

.. ----

.. code:: shell

    pip install git+https://github.com/neurospin/pymultifracs


Cloning the whole repository (including examples)
*************************************************

.. code:: shell

    git clone https://github.com/neurospin/pymultifracs
    pip install -e pymultifracs

For examples to get started, look into the `example/` folder


Optional features
*****************

In order to avoid download unnecessary packages, by default only the essential dependencies are installed.
To use all the features of the toolbox, you can do a full install by providing :code:`[full]`. For instance, after cloning the repository:

.. code:: shell

    pip install -e pymultifracs[full]
