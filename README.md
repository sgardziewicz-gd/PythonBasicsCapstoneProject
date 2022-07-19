# PythonBasicsCapstoneProject
Capstone project for Python Basics course

Console utility that allows to generate test jsonl files, or print to console, output filled with data based on provided data schema.

Example data schema: 
```
{“date”:”timestamp:”, “name”: “str:rand”, “type”:”[‘client’, ‘partner’, ‘government’]”, “age”: “int:rand(1, 90)”}
```
will generate such data:
```
{"date":"1534717897.967033", "name": "f82a44ac-daa7-4b8f-8569-83898fb9b312", "type":" partner", "age": 45}
```

User can also specify parameters that can, for example change number of data lines generated, 
specify amount of files, what prefix to add to file if generating multiple files, use multiprocessing, and other.

Required packages are specified in requirements.txt.
