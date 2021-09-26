"""
 # Evolutionary Computation HW #02

 - Student ID: 7110064490
 - Name: Huang Sin-Cyuan(黃新荃)
 - Email: dec880126@icloud.com
"""

import optparse
import sys
import yaml

# Parameter Setting
SECTION_NAME = "EC_Engine"

class YAML_Files():
    """
    This class can dynamically create attributes at run time.

    The perfect YAML Form:

    EC_Engine:
        populationSize: 100     #[mandatory parameter, type int]
        generationCount: fifty  #[mandatory parameter, type int]
        randomSeed: 10          #[optional parameter, type int]
        evaluatorType: parabola #[mandatory parameter, type string]
        jobName: test           #[optional parameter, type string]
        scalingParam: 2.5       #[optional parameter, type float]
    """

    def load_data(self, YAML_data: dict) -> None:
        """
        Load data and dynamically create attributes.
        """

        SECTION_NAME = tuple(YAML_data.keys())[0]
        for item in YAML_data[SECTION_NAME].keys():
            setattr(self, item, YAML_data[SECTION_NAME][item])

    def check_mandatories(self) -> list:
        """
        Check if input contains the Mandatory parameters and return the illegal list.

        MANDATORY_PARAM: 
         - populationSize
         - generationCount
         - evaluatorType')
        """

        missingParams = []
        try:
            self.populationSize
        except AttributeError:
            missingParams.append('populationSize')

        try:
            self.generationCount
        except AttributeError:
            missingParams.append('generationCount')

        try:
            self.evaluatorType
        except AttributeError:
            missingParams.append('evaluatorType')

        return missingParams

    def check_DataType(self) -> list:
        """
        Check data type of every parameters is correct and return the illegal list.

        'populationSize': int,
        'generationCount': int,
        'evaluatorType': str,
        'randomSeed': int,
        'jobName': str,
        'scalingParam': float
        """

        DATATYPES = {
            'populationSize': int,
            'generationCount': int,
            'evaluatorType': str,
            'randomSeed': int,
            'jobName': str,
            'scalingParam': float
        }
        incorrectTypes = []

        for name, value in vars(self).items():
            if name == "REAL_sectionName":
                continue
            if type(value) is not DATATYPES[name] and value != "":
                incorrectTypes.append(name)

        return incorrectTypes

    def check_sectionName(self, YAML_data: dict, SECTION_NAME: str) -> bool:
        """
        Check that the name is the same as the input.
        """

        return True if SECTION_NAME in set(YAML_data.keys()) else False


class Miss_param(Exception):
    def __init__(self) -> None:
        print("[!]Miss some mandatory parameters.")


class Incorrect_DataType(Exception):
    def __init__(self) -> None:
        print("[!]Some parameters have the wrong data type.")


class Both_Error(Exception):
    def __init__(self) -> None:
        print("[!]Some parameters have the wrong data type and miss some mandatory parameters.")


class Wrong_sectionName(Exception):
    def __init__(self) -> None:
        print(f"[!]The sectione name of the yaml file is incorrect. (Not '{SECTION_NAME}')")

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
    (options, *_) = parser.parse_args(argv)

    with open(options.inputFile, 'r') as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    yamlFiles = YAML_Files()
    yamlFiles.load_data(YAML_data=data)

    # GET REAL SECTION NAME
    yamlFiles.REAL_sectionName = list(data.keys())[0]
    
    # CHECK FOR MANDATORY　PARAMETERS
    missingParams = yamlFiles.check_mandatories()

    # CHECK FOR　CORRECT DATATYPE
    incorrectTypes = yamlFiles.check_DataType()

    #　OUTPUT
    missingParams.sort()
    incorrectTypes.sort()

    CORRECT_SECTION_NAME = yamlFiles.check_sectionName(YAML_data = data, SECTION_NAME = SECTION_NAME)

    with open(str(options.outputFile), 'w') as f:        
        f.write(f'missingParams: {missingParams}\n')
        f.write(f'incorrectTypes: {incorrectTypes}')
        if not CORRECT_SECTION_NAME:
            f.write("\nNotes: INCORRECT SECTION NAME!")

    # ERROR HANDLING
    try:
        if not CORRECT_SECTION_NAME:
            raise Wrong_sectionName
    except:
        pass

    try:
        if missingParams and incorrectTypes:
            raise Both_Error
        elif missingParams:
            raise Miss_param
        elif incorrectTypes:
            raise Incorrect_DataType
    except Both_Error:
        if not options.quietMode:
            print(f"[>]\t{missingParams=}")
            print(f"[>]\t{incorrectTypes=}")
    except Miss_param:
        if not options.quietMode:
            print(f"[>]\t{missingParams=}")
    except Incorrect_DataType:
        if not options.quietMode:
            print(f"[>]\t{incorrectTypes=}")
    finally:
        if not options.quietMode:
            print("[*]All tasks have been completed.")


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("[!]No such file or directory, Please check the parameter: inputFile! ")
    
