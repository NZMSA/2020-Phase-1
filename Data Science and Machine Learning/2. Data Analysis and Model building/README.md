## Video tutorial
* [Data cleaning, exploration and model building](https://youtu.be/5wyIAAtaRbI)
	* [Notebook for this tutorial can be found here](https://notebooks.azure.com/rivindu/projects/auto-mpg/html/auto-mpg.ipynb)
* [Assignment starter](https://youtu.be/9p8c0edPBXI)

## General approaches to data cleaning, exploratory analysis and modelling

Here I am listing some general guidelines to cleaning:  
* Check data type of each column - this is useful, for example, if you see a "Price" column that is cast as a string type, then you will need to investigate, as more likely than not it means there are letters in the column when there should be no letters in a "Price" column.
* Check basic statistics for each numerical column - min., max., mean... etc. This allows you to identify outliers/improbable values, and the describe() function does this very well. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html
* Check for NaN values. Scikit-Learn's regression model doesn't handle NaN values well. 
* How do we handle NaN values? Preferably you should try to find out whether there is a pattern to how NaN values occur and investigate why such a pattern exists. I know it is not what you want to hear but how NaN should be handled is based on a case by case basis. Some of the methods include
	* Fill NaN with the mean/median value
	* Create a model to predict the NaN values. For example, if there are NaN's in "Land_Area", we build a classifier using the other attributes such as "Bedrooms", "Bathrooms" to predict for the "Land_Area" values that are missing. 
	* Drop rows with NaNs  
* Pairs plot of the explanatory variables are always valuable.
* Correlation matrix for the explanatory variables are also very useful. 
* Income or prices usually are skewed so it makes sense to transform it with logarithm if we are running a linear regression. 

