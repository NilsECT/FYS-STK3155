# Project 1

Hello and welcome to our repository for Project 1 in the course FYS-STK4155/3155.
Here we explore three methods for linear regression which are Ordianry Least Squares, Ridge regression and LASSO regression.
We'll also be taking a look at some resampling techniques and finally apply these methods on some real terrain data.

If you want to have a look at the project description you can find it here: [compphysics.github.io/MachineLearning/doc/Projects/2022/Project1/](https://compphysics.github.io/MachineLearning/doc/Projects/2022/Project1/pdf/Project1.pdf).

## Classes

We have decided to take an object oriented approach so here we'll give a simple overview of the classes (they all start with capital letters). The classes are commented and documented for easier understanding of these.

#### The OLS, Ridge and LASSO classes

These three classes contain a single method each:
`beta_ols(design, known)`, `beta_ridge(design, known, lmbd)` and `beta_lasso(design, known, lmbd)`, respectively.

The functionality of these methods is to calculate the estimator of the respective model. They each return their respective estimator.

These classes are not meant to be initialized as they are inherited in the more general class LinearRegression.

#### LinearRegression

This class is the core of the project.

This is a general class for the different regression models where the models' only difference lies in generating the estimator. The class inherits from OLS, Ridge and LASSO and the method which is used is chosen when an instance of LinearRegression is created. It needs the Error and OutOfBounds classes as well as helper.py to fully function ( and OLS, Ridge and LASSO of course).

To initialize an instance of this class you call
`LinearRegression(order, x, y, z, method, lmbd, scale)`

Here are the parameters explained as in the documentation:

    order : int
        order of the polynomial fit. The initialization of the object will create a design matrix for the chosen order.

    x, y, z : numpy arrays
        x and y should be be meshgrids. That is a consequence of hoe the class was built.

    method : int (1, 2 or 3)
        Default 1
        Chosen method for linear regression. 1 is OLS, 2 is Ridge and 3 is LASSO.

    lmbd : float
        Default None
        Lambda to which we will make a fit for either Ridge or LASSO

    scale : boolean
        Default False
        If True the design matrix will be normalized.

This class contains multiple methods which may not be relevent in all cases, the class is tuned to work mostly for this specific project but should be moldable for other sorts of data.

The methods are listed here and the ones that are made to connect with other classes are marked with * followed by the class they are made for (or the class they need to create an instance of). The get and set methods are not listed here as they are intuitive.

    predict_resample(design_train, z_train, design_test) *Resample
    predict(design_test, z_test)
    design(scale=False)
    beta()
    mse(own=None) *Errors
    r2(own=None) *Errors
    conf_int() Note: only for OLS
    split_predict_eval(test_size=0.2, fit=False, train=False, random_state=None)

Each method is explained in their docstring if their name doesn't tell you much. `mse()`, `r2` and `conf_int()` require that you've already made a fit.

#### Resample

This class is exclusive for resampling techniques. It contains a bootstrap method and a cross-validation method.
This class relies on a LinearRegression instance so it can perform the resampling on the desired data with the desired regression method.

To initialize this class you call
`Resample(regression)`

where regression is an instance of LinearRegression.

The methods contained in this class are:
    bootstrap(N, random_state)
    k_folds(k)
    cross_validation(k)

where `k_folds()` is used by `cross_validation()`.

The main methods (bootstrap and cross_validation) return the evaluation of the resampling, that is the MSE and R2 score. For bootstrap it also returns the bias and the variance of the model.

#### Errors

This is a simple class used to calculate the MSE and R2 score of a fit. For OLS it can calculate the confidence intervals of the estimator.

To initialize the class you call
`Errors(expected, predicted)`

The class contains set methods for the expected and predicted values as well as:

    mse()
    r2()
    conf_int(beta, design)

#### OutOfBounds

To keep it short: it's an Exception subclass that is raised when the method (OLS, Ridge or LASSO) is chosen wrong.

## Other files

#### `helper.py`

This file contains some functions that are useful (and used in the classes). We haven't found a fitting place for these in the class hierarchy.

This class has the following funcitons:
    triangular_number(n)
    franke(x, y)
    our_tt_split(X, y, test_size=0.33, train_size = None, random_state=None)

`triangular_number` calculates the triangular number of the input parameter which has to be an `int`. It's a function used to find the number of features the design matrix will contain, the input parameter will be the polynomial degree.

`franke` computes and returns the Franke function evaluated at the parameters `x` and `y`.

`our_tt_split` stands for 'our train test split'. We decided to make our own data splitting function as an exercise and so we will also use it in our code. The input parameters are the design matrix and the known output which we want to split accordingly. We are aware that scikit-learn has such a functionality.

#### `plot.py`

This cript does what you think it does. It plots the relevant plots which are included in the report. It's also a handy way to see how the classes are supposed to be used.

#### `SRTM_data_Norway_1.tif`

Contains the terrain data on which we apply our linear regression methods. The data file is taken from the project description.
