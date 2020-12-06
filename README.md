# CSCE 4110 Final Project

Create a solution for hybrid Multidimensional 0/1 Knapsack Travelling Salesman Problem.

### Usage

Our most practical solution is in [`mkp_mst_ratio.py`](mkp_mst_ratio.py). To run this or 
any other solution, simply execute the script with Python 3.6+. Note that 
[`delivery.py`](delivery.py) is required to run any of the scripts.

We recommend running this program locally, instead of on the CSE servers, so that
matplotlib can be installed to visualize our solutions. However, the scripts will
still execute on the CSE servers, and the scripts can be easily modified to
print different data.

The parameters with which the each script is executed can be configured by modifying the
`if \_\_name\_\_ == '\_\_main\_\_' clause at the bottom of each script.

To perform a direct comparison of the results of each algorithm, place all of them in the
same directory and execute [`compare_mkp.py`](compare_mkp.py).
