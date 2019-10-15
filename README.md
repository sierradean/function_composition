# Function Composition

Autoquiz component to generate questions like #8 on CS10 Fall 2018 [Quest](http://cs10.org/fa19/exams/quest/2018Fa/exam.pdf)

![Question Example](assets/images/example_question.png)

## Contributors

- [Sierra Dean](https://github.com/sierradean)
- [Max Yao](https://github.com/bojinyao)
- [Bob Zhao](https://github.com/honglizhaobob)

## Table of Contents

- [Function Composition](#function-composition)
  - [Contributors](#contributors)
  - [Table of Contents](#table-of-contents)
  - [Get Started](#get-started)
    - [Software Requirement](#software-requirement)
  - [Usage](#usage)
  - [Bugs](#bugs)
  
## Get Started

### Software Requirement

- Python 3.6^

To get project code, either get the latest [RELEASE](https://github.com/sierradean/function_composition/releases) or clone the project directory:

```shell
git clone https://github.com/sierradean/function_composition.git
```

The project will be saved under `function_composition` directory. Since this project is written to be a python module, one can run the directory with python directly.

```shell
python3 function_composition -h
```

In the above example, `-h` option will show usage and help information

## Usage

Below is the printed help message out of the box. Currently, the module is capable of generating 6 different types of simple functions

```text
usage: [-h] [-o] [-f] [-c] [-q] [-b] [-l]

function composition program. Default output is stdout. Network Connection is
assumed but not required (see "--local")

optional arguments:
  -h, --help            show this help message and exit
  -o , --out            Path to file for output, create file if necessary, not
                        directories. Default output is stdout.
  -f , --num_functions
                        number of functions to have as answer, must be at
                        least 1, at most 6. Default 3
  -c , --num_choices    number of choices to present to the user, 1 < num
                        choice <= factorial(num functions). Default 5
  -q , --num_questions
                        number of questions to generate in file. Must be no
                        greater than factorial(num functions). Default 1
  -b, --body_only       output only the form and submit without the html
                        headers. Default False
  -l, --local           if flagged, will not fetch packages from CDN directly.
                        Instead, required packages will be written in the same
                        directory as file output within "packages/"
                        directory(except for stdout). Default False.
```

Without any option, program will output generated HTML form to standard-out.

## Bugs
