README v0.0 / 08 MARCH 2017

# Bleeding Pineapple

[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()


BleedingPineapple is a python package for empirical evaluation on real-time scheduling algorithms.


## Usage Overview



### Software Requirements

`python`  2.7 (or later) 

`numpy` 1.7.1 (or later) (download [numpy](http://www.numpy.org/ ""))

`scipy` (download [scipy](http://www.scipy.org/install.html ""))

`python-matplotlib` (download [python-matplotlib](http://matplotlib.org/users/installing.html ""))



## Installation

Install via `git clone`

```bash
$ git clone https://kevinwhere@bitbucket.org/kevinwhere/bleeding-pineapple.git
$ cd bleeding-pineapple
```

or from `pip`

TODO

## (Very short)tutorial 

Enter source folder and select topic

```bash
$ cd source/multimode
```
Run schedulability tests

```bash
$ python multimode.py
```

Plot the results

1. Change to the directory in which `multimode-plot.py` is put

```bash
$ cd plot
```

2. plot the result

```bash
$ python multimode-plot.py
```



## LICENSE

MIT license. See the LICENSE file for details.