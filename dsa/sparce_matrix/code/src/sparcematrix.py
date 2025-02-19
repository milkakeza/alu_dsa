import json
import os

class SparseMatrix:
    def __init__(self, matrix_file_path_or_num_rows, num_cols=None):
        self.elements = {} 

        if isinstance(matrix_file_path_or_num_rows, str):
            self.load_matrix(matrix_file_path_or_num_rows)
        else:
            self.rows = matrix_file_path_or_num_rows
            self.cols = num_cols

    def load_matrix(self, matrix_file_path):
        try:
            with open(matrix_file_path, 'r') as file:
                lines = file.read().splitlines()

            self.rows = int(lines[0].split('=')[1])
            self.cols = int(lines[1].split('=')[1])

            for line in lines[2:]:
                line = line.strip()
                if line:
                    # This is for removing parentheses and spliting by commas
                    row, col, value = map(int, line.strip('()').split(','))
                    self.set_element(row, col, value)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find matrix file at: {matrix_file_path}")
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {str(e)}")

    
    def get_element(self, curr_row, curr_col):
        return self.elements.get(f"{curr_row},{curr_col}", 0)

    def set_element(self, curr_row, curr_col, value):
        if value != 0:
            self.elements[f"{curr_row},{curr_col}"] = value
        else:
            self.elements.pop(f"{curr_row},{curr_col}", None)

    def add(self, other):
        if self.cols != other.cols or self.rows != other.rows:
            raise ValueError('Matrices dimensions do not match, hence addition is not possible')

        result = SparseMatrix(self.rows, self.cols)

        for key, value in self.elements.items():
            result.elements[key] = value

        for key, value in other.elements.items():
            row, col = map(int, key.split(','))
            new_value = result.get_element(row, col) + value
            result.set_element(row, col, new_value)

        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError('Matrices dimensions do not match, hence subtraction is not possible')

        result = SparseMatrix(self.rows, self.cols)

        for key, value in self.elements.items():
            result.elements[key] = value

        for key, value in other.elements.items():
            row, col = map(int, key.split(','))
            new_value = result.get_element(row, col) - value
            result.set_element(row, col, new_value)

        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError('Matrices dimensions do not match for multiplication')

        result = SparseMatrix(self.rows, other.cols)

        for key1, value1 in self.elements.items():
            row1, col1 = map(int, key1.split(','))
            for key2, value2 in other.elements.items():
                row2, col2 = map(int, key2.split(','))
                if col1 == row2:
                    new_value = result.get_element(row1, col2) + value1 * value2
                    result.set_element(row1, col2, new_value)

        return result

    def save_result(self, result_file_path):
        # Create directory if it doesn't exist already
        os.makedirs(os.path.dirname(result_file_path), exist_ok=True)
        
        content = [f"rows={self.rows}", f"cols={self.cols}"]
        for key, value in self.elements.items():
            row, col = key.split(',')
            content.append(f"({row}, {col}, {value})")
        
        with open(result_file_path, 'w') as file:
            file.write('\n'.join(content))

    def __str__(self):
        return f"rows={self.rows}\ncols={self.cols}\n(elements={json.dumps(self.elements)})"


def main():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    code_dir = os.path.dirname(current_dir)
    sparce_matrix_dir = os.path.dirname(code_dir)
    
    input_dir = os.path.join(sparce_matrix_dir, 'sample_inputs')
    output_dir = os.path.join(sparce_matrix_dir, 'sample_results')
    
    # Creating directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # input file paths
    firstmatrixFilePath = os.path.join(input_dir, 'matrix1.txt')
    secondmatrixFilePath = os.path.join(input_dir, 'matrix2.txt')
    
    # output file paths
    outputAddPath = os.path.join(output_dir, 'addition_result.txt')
    outputSubPath = os.path.join(output_dir, 'substration_result.txt')
    outputMultPath = os.path.join(output_dir, 'multiplication_result.txt')

    print("Looking for input files at:")
    print(f"- {firstmatrixFilePath}")
    print(f"- {secondmatrixFilePath}")

    try:
        matrix1 = SparseMatrix(firstmatrixFilePath)
        matrix2 = SparseMatrix(secondmatrixFilePath)

        resultAdd = matrix1.add(matrix2)
        resultSub = matrix1.subtract(matrix2)
        resultMult = matrix1.multiply(matrix1)

        resultAdd.save_result(outputAddPath)
        resultSub.save_result(outputSubPath)
        resultMult.save_result(outputMultPath)

        print(
            f"\nOutput saved for addition and subtraction processed successfully :)"
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure that the input files exist at the following locations:")
        print(f"- {firstmatrixFilePath}")
        print(f"- {secondmatrixFilePath}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()