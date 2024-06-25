from os import listdir
from os.path import isfile, join
from collections import Counter
import json

class CONFIG:
    PATH = r"MUST UPDATE THIS"
    RECORDS = 500

    DISPLAY_INPUT = True
    DISPLAY_INPUT_DETAIL = False

    DISPLAY_OUTPUT = True
    DISPLAY_OUTPUT_DETAIL = False
    
    DISPLAY_COLOURS = True
    DISPLAY_CELLS = True
    DISPLAY_SIZE = True  

class Task:
    def __init__(self, filename, file):
        self._filename = filename
        self._file = file
        self._content = file.read()
    # Assuming 'content' contains the JSON data
        self._data = json.loads(self._content)
        self._train_data = self._data.get("train", [])
        self._samples = []

    def set_samples(self):  
        for i, item in enumerate(self._train_data, start=1):
            input_matrix = item.get("input", [])
            output_matrix = item.get("output", [])
            self._samples.append(Sample(input_matrix, output_matrix))

    def calculate_stats(self):
        self.num_samples = len(self._train_data)
        self._are_input_rows_and_columns_common = self.are_input_rows_and_columns_common()
        self._are_output_rows_and_columns_common = self.are_output_rows_and_columns_common()
        self._are_sample_rows_and_columns_common = self.are_sample_rows_and_columns_common()
        print(f"Are input dimensions common: {self._are_input_rows_and_columns_common}")
        print(f"Are output dimensions common: {self._are_output_rows_and_columns_common}")
        print(f"Are sample dimensions common: {self._are_sample_rows_and_columns_common}")
        
        is_greyscale_common = False
        for sample in self._samples:
            is_greyscale_common = Test.is_greyscale_shape_common(sample)   
        print(f"Greyscale: {is_greyscale_common}")    

    def are_input_rows_and_columns_common(self):
        compare = []
        for sample in self._samples:
            compare.append(sample._input)
        return Test.are_rows_and_columns_common(compare)

    def are_output_rows_and_columns_common(self):
        compare = []
        for sample in self._samples:
            compare.append(sample._output)
        return Test.are_rows_and_columns_common(compare)

    def are_sample_rows_and_columns_common(self):
        for sample in self._samples:
            compare = []
            compare.append(sample._input)
            compare.append(sample._output)
            if Test.are_rows_and_columns_common(compare) == False:
                return False
        return True

    def __str__(self):
        string = f"; {self._filename}: Samples: {self.num_samples}\n"
        for i, sample in enumerate(self._samples, start=1):
            string += f"Sample {i}: {sample}\n"
        return string
    
class Sample:
    def __init__(self, input, output):
        self._input = Input(input)
        self._output = Output(output)

    def __str__(self):
        return f"Input: {self._input}; Output: {self._output}"

class Test:
    def __init__(self, data):
        self._data = data
        # print(data)
        self.rows = len(data)
        self.cols = len(data[0])
        flattened_list = [item for sublist in data for item in sublist]
        self.cells = len(flattened_list)
        self._counted_colours = Counter(flattened_list)
        self._sorted_colours = sorted(self._counted_colours.items(), key=lambda x: x[0])

    @classmethod
    def are_rows_and_columns_common(cls, test_objects_list):
        # Get the rows and columns from the first test object
        first_test = test_objects_list[0]
        common_rows = first_test.rows
        common_cols = first_test.cols

        # Compare with other test objects
        for test in test_objects_list[1:]:
            if test.rows != common_rows or test.cols != common_cols:
                return False

        return True

    @classmethod
    def is_greyscale_shape_common(cls, sample):
        is_greyscale_common = False
        greyscale_input = [[-1 if num != 0 else num for num in row] for row in sample._input._data]
        greyscale_output = [[-1 if num != 0 else num for num in row] for row in sample._output._data]
        if greyscale_input == greyscale_output:
            is_greyscale_common = True
        return is_greyscale_common

    def __str__(self):
        string = ""
        string = f"{self.rows} x {self.cols}: Cells={self.cells} "
        if CONFIG.DISPLAY_COLOURS == True:
            for num, count in self._sorted_colours:
                string += f"C{num}={count}; "
        return string
              
class Input(Test):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        if CONFIG.DISPLAY_INPUT == True:
            return super().__str__()
        else: 
            return ""
    
class Output(Test):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        if CONFIG.DISPLAY_OUTPUT == True:
            return super().__str__()
        else: 
            return ""
    
def create_data():
    
    files = [f for f in listdir(CONFIG.PATH) if isfile(join(CONFIG.PATH, f))]
    
    counter = 0
    
    for filename in files:
        with open(join(CONFIG.PATH, filename), 'r') as file:
            counter += 1
            if counter > CONFIG.RECORDS:
                print("stop")
                break
            # process_file(filename, file)
            task = Task(filename, file)
            tasks.append(task)


tasks = []
print("Start")
create_data()
print(f"Total Tasks: {len(tasks)}")
for i, task in enumerate(tasks, start = 1):
    task.set_samples()
    task.calculate_stats()
    print(f"Task No. {i} {task}")
print("end")
