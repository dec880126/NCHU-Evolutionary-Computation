"""
 # Evolutionary Computation HW #01

 - Student ID: 7110064490
 - Name: Huang Sin-Cyuan(黃新荃)
 - Email: dec880126@icloud.com
"""

import optparse
import sys
import yaml


MANDATORY_PARAM = ('populationSize', 'generationCount', 'evaluatorType')

DATATYPES = {
    'populationSize': int,
    'generationCount': int,
    'evaluatorType': str,
    'randomSeed': int,
    'jobName': str,
    'scalingParam': float
}

SECTION_NAME = 'EC_Engine'
missingParams = []
incorrectTypes = []

def main(argv=None):   
    if argv is None:
        argv = sys.argv

    parser = optparse.OptionParser()
    parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
    parser.add_option(
        "-i", "--inputFile",
        action="store",
        dest="inputFile",
        help="read the PATH of inputFile"
    )
    parser.add_option(
        "-o", "--outputFile",
        action="store",
        dest="outputFile",
        help="read the PATH of outputFile",
        default='output_result.txt'
    )
    (options, args) = parser.parse_args(argv)

    with open(options.inputFile, 'r') as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    CORRECT_SECTION_NAME = True if SECTION_NAME in set(data.keys()) else False

    REAL_SECTIONE_NAME = list(data.keys())[0]
    
    # CHECK FOR MANDATORY　PARAMETERS
    for mandatory_items in MANDATORY_PARAM:
        try:
            data[REAL_SECTIONE_NAME][mandatory_items]
        except KeyError:
            missingParams.append(mandatory_items)

    # CHECK FOR　CORRECT DATATYPE
    for parameters in data[REAL_SECTIONE_NAME]:
        if type(data[REAL_SECTIONE_NAME][parameters]) is not DATATYPES[parameters]:
            incorrectTypes.append(parameters)  

    #　OUTPUT
    missingParams.sort()
    incorrectTypes.sort()

    if not options.quietMode:
        print(f'missingParams: {missingParams}')
        print(f'incorrectTypes: {incorrectTypes}')    
        if not CORRECT_SECTION_NAME:
            print(f"Notes:\tINCORRECT SECTION NAME!\n\tYour section name is {REAL_SECTIONE_NAME}, but it should be {SECTION_NAME}")

    with open(str(options.outputFile), 'w') as f:        
        f.write(f'missingParams: {missingParams}\n')
        f.write(f'incorrectTypes: {incorrectTypes}')
        if not CORRECT_SECTION_NAME:
            f.write("\nNotes: INCORRECT SECTION NAME!")


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("No such file or directory, Please check the parameter: inputFile! ")
    
