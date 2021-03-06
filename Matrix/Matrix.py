import numpy as np

# Exceptions
class Error(Exception):
    """Base Class For All Exceptions"""
    pass

class NonSquareMatrix(Error):
    """Raised When A Method Requires A Square Matrix But The Given One is Not"""
    def __init__(self, message="Square Matrix Required."):
        self.message = message
        super().__init__(self.message)

class MatrixInCompatibilityError(Error):
    """Raised When The Matrix Dimensions Are Incompatible With The Given List"""
    def __init__(self, message="The Matrix Dimensions Are Incompatible With The Given List"):
        self.message = message
        super().__init__(self.message)

class InvalidMatrixIndex(Error):
    """Raised When The Requested Matrix Index Is Invalid"""
    def __init__(self, message="Invalid Matrix Index"):
        self.message = message
        super().__init__(self.message)

class InvalidMatrixError(Error):
    """Raised When The Matrix Is Invalid"""
    def __init__(self, message="Invalid Matrix"):
        self.message = message
        super().__init__(self.message)

# The Matrix Class
class Matrix:
    # n = number of rows, m = number of columns
    def __init__(self,matrix=[],n=0,m=0):
        self._matrix = matrix
        self._rows_dim = n
        self._cols_dim = m
        try:
            self.validate_matrix()
        except Exception as e:
            self.__del__()
            raise e
    
    def is_square(self):
        return (self._rows_dim == self._cols_dim)

    def get_row(self, index):
        try:
            return self._matrix[index]
        except:
            raise InvalidMatrixIndex
    
    def get_column(self, index):
        try:
            column = []
            for row in range(0, len(self._matrix)):
                column.append(row[index])
            return column
        except:
            raise InvalidMatrixIndex

    def get_matrix(self):
        return self._matrix

    def validate_matrix(self):
        # Checks Whether The Matrix is Valid
        if not isinstance(self._matrix, list):
            raise InvalidMatrixError
        if not isinstance(self._matrix[0], list):
            raise InvalidMatrixError
        # Checks Whether The Matrix Dimensions are Compatible
        if not (self._rows_dim > 0 and self._cols_dim > 0) or (self._rows_dim != len(self._matrix)):
            raise MatrixInCompatibilityError        
        for row in range(len(self._matrix)):
            if len(self._matrix[row]) != self._cols_dim:
                raise MatrixInCompatibilityError
    
    def get_rows_dimension(self):
        return self._rows_dim
    
    def get_columns_dimension(self):
        return self._cols_dim
    
    def multiplyScalar(self, scalar):
        try:
            for row in range(self._rows_dim):
                for column in range(self._cols_dim):
                    self._matrix[row][column] *= scalar
        except:
            raise TypeError("Invalid Scalar.")
    
    # Overloading the + operator to work for matrices
    def __add__(self, SecondMatrix):
        try:  
            if not (self.get_rows_dimension() == SecondMatrix.get_rows_dimension() and self.get_columns_dimension() == SecondMatrix.get_columns_dimension()):
                print("Invalid Matrices Dimensions")
                return
            resultList = []
            for row in range(self.get_rows_dimension()):
                rowList = []
                for column in range(self.get_columns_dimension()):
                    rowList.append(self._matrix[row][column] + SecondMatrix[row][column])
                resultList.append(rowList)
            resultMatrix = Matrix(resultList, len(resultList), len(resultList[0]))
            
            return resultMatrix

        except:
            print("Undefined Addition")
    
    # Overloading the - operator to work for matrices
    def __sub__(self, SecondMatrix):
        try:  
            if not (self.get_rows_dimension() == SecondMatrix.get_rows_dimension() and self.get_columns_dimension() == SecondMatrix.get_columns_dimension()):
                print("Invalid Matrices Dimensions")
                return
            resultList = []
            for row in range(self.get_rows_dimension()):
                rowList = []
                for column in range(self.get_columns_dimension()):
                    rowList.append(self._matrix[row][column] - SecondMatrix[row][column])
                resultList.append(rowList)
            ResultMatrix = Matrix(resultList, len(resultList), len(resultList[0]))
            
            return ResultMatrix
        
        except:
            print("Undefined Subtraction")

    # Overloading the * Opearator to work for matrices
    def __mul__(self, SecondMatrix):
        try:
            result = np.matmul(self.get_matrix(), SecondMatrix.get_matrix()).tolist()
            return Matrix(result, self.get_rows_dimension(), SecondMatrix.get_columns_dimension())
        except:
            if type(SecondMatrix) == int or float:
                self.__rmul__(SecondMatrix)
                return
            print("Undefined Multiplication")

    def __rmul__(self, num):
        if not(type(num) == int or float):
            print("Invalid Multiplication")
            return
        self.multiplyScalar(num)
        return 1

    def __getitem__(self, index):
        try:
            return self._matrix[index]
        except:
            print("Invalid Element Position!")

    def __del__(self):
        print("The Matrix Has Been Deleted!")


# General Functions
def getDeterminant(matrix: Matrix) -> float:
    # Checks Whether The Matrix is Square
    if not matrix.is_square():
        raise NonSquareMatrix

    return np.linalg.det(matrix.get_matrix())

def generateIdentityMatrix(IdentityDimension) -> Matrix:
    identity_entries=[[1 if row==col else 0 for col in range(IdentityDimension)] for row in range(IdentityDimension)]
    IdentityMatrix = Matrix(identity_entries, IdentityDimension, IdentityDimension)
    return IdentityMatrix

def getInverse(matrix: Matrix) -> Matrix:
    # Checks Whether The Matrix is Square
    if not matrix.is_square():
        raise NonSquareMatrix
    
    givenMatrix = np.array(matrix.get_matrix())
    invertedNumpyMatrix = np.linalg.inv(givenMatrix)
    invertedMatrix = invertedNumpyMatrix.tolist()
    invertedMatrix = Matrix(invertedMatrix, len(invertedMatrix), len(invertedMatrix))
    return invertedMatrix