# how divisive is the issue? (standard deviation of opinions on the issue... polarization variable)
# opinion = slope * political alignment + intercept
# slope = correlation between alignment and issue * SD issue opinion / SD political alignment 
# intercept = mean opinion - slope * mean political alignment

# can pregenerate agents with matching correlations, standard deviations and means using Cholesky decomposition.

import random
import numpy as np
import cvxpy as cp #using this for finding nearest valid covariance matrix
from scipy.stats import multivariate_normal

class Issue:
    allIssues = []
    covmatrix = []
    issueCount = -1
    def __init__(self, issueName, customize):
        self.issueName = issueName
        self.correlationsToMe = [] # will have elements of type (issue, R-value), where R-value represents correlation between -1.0 and 1.0
        if customize == 3:  
            self.complexity = 5 # values centered on 5
            self.politCorrelation = 0.0 # values from -1 to 1, centered on 0 by default
            self.polarization = 0.33 # standard deviation number where 68% of people will be (put as 0.33 to be about where normal distribution would be if range of available values is -1 to 1, centered on 0)
            self.globalOp = 0.0 # mean opinion value of this issue, from -1 to 1 centered on 0
        elif customize == 1:
            self.complexity = input("On a scale of 1 to 10, how complex is this issue? ")
            self.politCorrelation = input("Please enter a value between -1 and 1 for political alignment (correlation of how much a positive opinion of this issue correlates with the political right, 0 if both left and right like it the same): ")
            self.polarization = input("Please enter a value between 0 and 1 for polarization (anticipated standard deviation for political opinion): ")
            self.globalOp = input("Please enter a value between -1 and 1 for the mean global opinion on this issue (-1 against, 1 for): ")
        elif customize == 2:
            self.complexity =  random.randint(1, 10)
            self.politCorrelation = int(random.uniform(-1, 1)*100)/100.
            self.polarization = int(random.uniform(0, 1)*100)/100.
            self.globalOp = random.randint(0, 100)
        Issue.issueCount += 1
        self.issueID = Issue.issueCount
        Issue.allIssues.append(self)
    
    @property
    def complexity(self):
        return self._complexity
    
    @complexity.setter
    def complexity(self, value):
        while True:
            try:
                value = float(value)
                if (value >= 1 and value <= 10):
                    self._complexity = 1+(value-5)/5 # to generate numbers centered on 1, +- complexity, to give modifier %
                    break
                else:
                     value = float(input("Please enter a value between 1 to 10 for complexity: "))
            except ValueError:
                print("\nThis isn't a valid number. ") 
    
    @property
    def politCorrelation(self):
        return self._politCorrelation
    
    @politCorrelation.setter
    def politCorrelation(self, value):
        while True:
            try:
                n = float(value)
                if (n >= -1 and n <= 1):
                    self._politCorrelation = value
                    break
                else:
                    value = float(input("Please enter a value between -1 and 1 for for political alignment (correlation of how much a positive opinion of this issue correlates with the political right, 0 if both left and right like it the same): "))
            except ValueError:
                print("\nThis isn't a valid number. ") 
    
    @property
    def polarization(self):
        return self._polarization
    
    @polarization.setter
    def polarization(self, value):
        while True:
            try:
                value = float(value)
                if (value >= -1 and value <= 1):  
                    self._polarization = value  
                    break
                else:
                    value = float(input("Please enter a value between 0 and 1 for divisiveness of issue: "))    
            except ValueError:
                print("\nThis isn't a valid number. ") 

    @property
    def globalOp(self):
        return self._globalOp
    
    @globalOp.setter
    def globalOp(self, value):
        while True:
            try:
                value = float(value)
                if (value >= 0 and value <= 100):
                    self._globalOp = value
                    break
                else:
                    value = float(input("Please enter a value between 0 and 100 for political alignment: "))
            except ValueError:
                print("\nThis isn't a valid number. ")         
    
    @staticmethod
    def makeCovMatrix():
        covmatrix = []         
        for i in Issue.allIssues:
            row = []
            for r in i.correlationsToMe:
                row.append(r[1])
            covmatrix.append(row)
        # add to this the correlation of each issue with politicalAlignment (politCorrelation)
        row = [1]
        j = 0
        for i in Issue.allIssues:
            row.append(i.politCorrelation)
            covmatrix[j].insert(0, i.politCorrelation)
            j += 1
        covmatrix.insert(0, row)
        return covmatrix    
    
    @staticmethod
    def findNearestPsd(matrix):
        # new empty matrix
        X = cp.Variable(matrix.shape, symmetric=True)
        
        # objective: minimize Frobenius norm btwn X and original
        objective = cp.Minimize(cp.norm(X - matrix, 'fro'))
        constraints = [X >> 0] # PSD
        constraints += [X[i, i] == 1 for i in range(matrix.shape[0])]

        # Define the problem and solve it
        problem = cp.Problem(objective, constraints)
        problem.solve()
        return X.value
    
    @staticmethod
    def correlateIssues(customize=False):
        for i in range(0, len(Issue.allIssues)):
            for j in range(0, len(Issue.allIssues)):
                if i == j:
                    Issue.allIssues[i].correlationsToMe.append((Issue.allIssues[j], 1))   
                if i < j:
                    if customize==False:
                        r = int(random.uniform(-1, 1)*100)/100.
                        Issue.allIssues[i].correlationsToMe.append((Issue.allIssues[j], r))
                        Issue.allIssues[j].correlationsToMe.append((Issue.allIssues[i], r))
                    else:
                        while True:                        
                            try:
                                r = float(input(f'What is the correlation between issue {Issue.allIssues[i].issueID} and {Issue.allIssues[j].issueID}? (-1 to 1): '))
                                if (r >= -1 and r <= 1):
                                    break
                            except ValueError:
                                print("\nThis isn't a valid number. ")
                        Issue.allIssues[i].correlationsToMe.append((Issue.allIssues[j], r))
                        Issue.allIssues[j].correlationsToMe.append((Issue.allIssues[i], r))
        # we need to check that these correlations are mathematically possible, so let's create a covariance matrix
        Issue.covmatrix = Issue.makeCovMatrix()
        npmatrix = np.array(Issue.covmatrix) # need to do this because Cholesky functions only work with nparray
        # check using Cholesky decomposition to see if this combination is possible
        # adica, all eigenvalues have to be non-negative
        try:
            np.linalg.cholesky(npmatrix)
            if customize==True:
                print("Correlation matrix is valid.")
            if customize==False:
                for i in npmatrix:
                    print(i)
        except np.linalg.LinAlgError:
            if customize==True:  
                print("This particular combination of correlations doesn't work. Finding the next nearest viable covariance matrix.")
            # need positive semi-definite matrix... 
            npmatrix = Issue.findNearestPsd(npmatrix)
            # replace in lists with new values, truncated to 2 decimal places
            for issue in Issue.allIssues:
                issue.correlationsToMe = []
            for i in range(0, len(Issue.allIssues)):
                for j in range(0, len(Issue.allIssues)):
                    if i == j:
                        Issue.allIssues[i].correlationsToMe.append((Issue.allIssues[j], 1))   
                    if i < j:
                        Issue.allIssues[i].correlationsToMe.append((Issue.allIssues[j], int(npmatrix[i, j]*100)/100.))
                        Issue.allIssues[j].correlationsToMe.append((Issue.allIssues[i], int(npmatrix[j, i]*100)/100.))
            print("New matrix generated:")
            Issue.covmatrix = Issue.makeCovMatrix()
            # update politCorrelation also, for each issue
            for i in range(0, len(Issue.allIssues)):
                Issue.allIssues[i].politCorrelation = Issue.covmatrix[0][1+i]
            for row in Issue.covmatrix:
                print(row)
    
    @staticmethod
    def generateIssueOpinions(meanPoliticalView, agentPolitAlign):
        npmatrix = np.array(Issue.covmatrix)
        means = []
        for issue in Issue.allIssues:
            means.append(issue.globalOp)
        meanVector = np.array(means)
        # partition mean vector, covariance matrix
        # formula for conditional mean... condMean = vector with means + all the Rs / Rww * (specific value for W for this agent - mean W)
        condMean = means +  npmatrix[1:, 0] / 1 * (agentPolitAlign - meanPoliticalView)
        '''
        try:
            np.linalg.cholesky(npmatrix)
            print("Verified PSD")
        except np.linalg.LinAlgError:
            print("Not PSD")
        '''
        # formula for conditional covariance... condCov = submatrix with correlations apart from the W row and column - outer product of all the Rs with all the Rs / Rww
        condCov = npmatrix[1:, 1:] - np.outer(npmatrix[1:, 0], npmatrix[0, 1:]) / 1
        checkPositive = False
        while not checkPositive:
            checkPositive = True
            randomSampledValue = multivariate_normal.rvs(condMean, condCov)
            for i in randomSampledValue:
                if i < 0:
                    checkPositive = False
        return randomSampledValue
          
    def __str__(self):
        print(f"Issue {self.issueName} has complexity {self.complexity} with political correlation {self.politCorrelation}, polarization {self.polarization}, and global opinion {self.globalOp}.")
        for i in self.correlationsToMe:
            print(f"\nIssue {self.issueName} is correlated to {i[0].issueName} by {i[1]}.")
        return ""