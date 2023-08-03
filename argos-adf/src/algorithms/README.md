# Algorithms

### Understanding Axis Parameter in NumPy Aggregate Functions
<img src="https://gitlab.com/phanuwit.suriya/argos-demo/raw/develop-branch/static/img/numpy-axis.png">

When use the numpy aggregate functions, the axis parameter that specified is the axis that gets collapsed.

The axis parameter is a number that communicates to numpy arrays along which dimension you want your aggregate function to operate.

- axis = 0: Aggregate along the row (row-wise)  แถวเดียวกัน
- axis = 1: Aggregate along the column (column-wise) หลักเดียวกัน
- axis = 2: Aggregate along the depth (depth-wise) ลึกเท่ากัน