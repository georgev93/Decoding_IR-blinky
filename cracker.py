#!/bin/python
import csv

codeBitWidth = 19

decodedAddressArray = {}
numOfDecodedAddresses = 0


class csvReader:
    def __init__(self, csvInput):
        with open(csvInput, 'r', newline='') as csvInputFile:
            reader = csv.DictReader(csvInputFile, fieldnames=['address', 'code'])
            for row in reader:
                if(str(row['address'])[0] != '#'):
                    decodedAddressArray[row['address']] = row['code'].lstrip()
        globals()['numOfDecodedAddresses'] = decodedAddressArray.__len__()


class comparisonObject:

    def __init__(self, operation):
        self.compareDict = {}
        self.listOfAddresses = []
        self.buildCompareDict(operation)

    def buildCompareDict(self, operation):
        for address in list(decodedAddressArray):
            self.compareDict[address] = getattr(type(self), operation)(decimalToBinary(int(address), 7))
            self.listOfAddresses.append(address)

    @staticmethod
    def Noop(input):
            return input

    @staticmethod
    def minusOne(input):
        originalLength = str(input).__len__()
        return decimalToBinary(binaryToDecimal(input)+1, originalLength)
    
    @staticmethod
    def manchester(input):
        outputStr = ''
        for char in str(input):
            if char == '0':
                outputStr = outputStr + '01'
            elif char == '1':
                outputStr = outputStr + '10'
        return outputStr

    @staticmethod
    def manchesterMinusOne(input):
        return comparisonObject.manchester(comparisonObject.minusOne(input))
    
    @staticmethod
    def binaryPerDigit(input):
        decimalNumber = int(binaryToDecimal(input))
        if str(decimalNumber).__len__() == 1:
            decimalNumber = '0' + str(decimalNumber)
        return decimalToBinary(int(str(decimalNumber)[0]), 4) + decimalToBinary(int(str(decimalNumber)[1]), 4)
    
    @staticmethod
    def binaryPerDigitMinusOne(input):
        decimalNumber = int(binaryToDecimal(input))
        decimalNumber = decimalNumber - 1
        if str(decimalNumber).__len__() == 1:
            decimalNumber = str('0' + str(decimalNumber))
        return decimalToBinary(int(str(decimalNumber)[0]), 4) + decimalToBinary(int(str(decimalNumber)[1]), 4)


class bitChangeMatrix:
    def __init__(self, name, operation):
        self.name = name
        self.outputMatrix = [['' for x in range(numOfDecodedAddresses)] for y in range(numOfDecodedAddresses)]
        self.decodedMin = 100
        self.decodedMax = 0
        self.compareMin = 100
        self.compareMax = 0
        self.comparison = comparisonObject(operation)
        self.buildOutputMatrix()
        self.printArray()

    def buildOutputMatrix(self):
        # Compare discovered codes
        for row in range(numOfDecodedAddresses):
            for column in range(row):
                differentBits = self.numOfBitsDifferent(decodedAddressArray.get(self.comparison.listOfAddresses[row]), decodedAddressArray.get(self.comparison.listOfAddresses[column]))
                self.outputMatrix[row][column] = differentBits
                if differentBits < self.decodedMin:
                    self.decodedMin = differentBits
                if differentBits > self.decodedMax:
                    self.decodedMax = differentBits

        # Compare this object's "compare" values
        for row in range(numOfDecodedAddresses):
            for column in range(row+1, numOfDecodedAddresses):
                differentBits = self.numOfBitsDifferent(self.comparison.compareDict.get(self.comparison.listOfAddresses[row]), self.comparison.compareDict.get(self.comparison.listOfAddresses[column]))
                self.outputMatrix[row][column] = differentBits
                if differentBits < self.compareMin:
                    self.compareMin = differentBits
                if differentBits > self.compareMax:
                    self.compareMax = differentBits


    def printArray(self):
        # Print Name
        print(str(self.name).center(3*numOfDecodedAddresses))
        for address in list(decodedAddressArray):
            print(str(address).rjust(2)+',', end='')
        print()
        print('---'*numOfDecodedAddresses)
        for row in range(numOfDecodedAddresses):
            for column in range(numOfDecodedAddresses):
                if(row > column):
                    printColors.printColorScale(self.outputMatrix[row][column], self.decodedMin, self.decodedMax, 2)
                elif(row < column):
                    printColors.printColorScale(self.outputMatrix[row][column], self.compareMin, self.compareMax, 2)
                else:
                    print('XX', end='')
                print(',', end='')
            print()
        print()

    @staticmethod
    def numOfBitsDifferent(num1, num2):
        size = str(num1).__len__()
        retVal = 0
        for i in range(size):
            if(str(num1)[i] != str(num2)[i]):
                retVal = retVal + 1
        return retVal

class bitEntropy:
    def __init__(self, name, operation):
        self.name = name
        self.comparison = comparisonObject(operation)
        self.decodedEntropyArray = self.buildEntropyArray(list(decodedAddressArray.values()))
        self.comparisonEntropyArray = self.buildEntropyArray(list(self.comparison.compareDict.values()))
        self.printEntropyReport()
    
    def buildEntropyArray(self, input):
        numOfBits = str(input[0]).__len__()
        listLength = list(input).__len__()
        retList = [0 for x in range(numOfBits)]

        for digit in range(numOfBits):
            digitSum = 0
            for element in input:
                digitSum = digitSum + int(str(element)[digit])
            entropyPercentage = digitSum/listLength
            if entropyPercentage > 0.5:
                entropyPercentage = 1 - entropyPercentage
            retList[digit] = int(100*entropyPercentage)

        return retList
    
    def printEntropyReport(self):
        printWidth = 20 + 19*3
        print(str(self.name).center(printWidth))
        print('-'*printWidth)
        print('Decoded entropy:    ', end='')
        for number in self.decodedEntropyArray:
            printColors.printColorScale(number, 0, 50, 2)
            print(',', end='')
        print()
        print('Comparison entropy: ', end='')
        for number in self.comparisonEntropyArray:
            printColors.printColorScale(number, 0, 50, 2)
            print(',', end='')
        print()
        print()
        

class printColors:
    CYNBKG = 46
    GRNBKG = 42
    YLWBKG = 43
    REDBKG = 41
    ENDCOLOR = 0

    @staticmethod
    def colorEscapeCode(input):
        return str('\033[' + str(input) + 'm')
    
    def printColorScaleAltText(input, min, max, text):
        percentage = (input-min)/(max-min)
        if(percentage < 0.25):
            print(printColors.colorEscapeCode(printColors.CYNBKG), end='')
        elif(percentage < 0.5):
            print(printColors.colorEscapeCode(printColors.GRNBKG), end='')
        elif(percentage < 0.75):
            print(printColors.colorEscapeCode(printColors.YLWBKG), end='')
        else:
            print(printColors.colorEscapeCode(printColors.REDBKG), end='')
        print(str(text) + printColors.colorEscapeCode(printColors.ENDCOLOR), end='')

    @staticmethod
    def printColorScale(input, min, max, digits):
        printColors.printColorScaleAltText(input, min, max, str(input).rjust(digits))


class codeViewer:
    def __init__(self, name, operation):
        self.name = name
        self.comparison = comparisonObject(operation)
        self.printCodeView()

    def printCodeView(self):
        addressList = list(decodedAddressArray.keys())
        codeList = list(decodedAddressArray.values())
        compareList = list(self.comparison.compareDict.values())
        viewWidth = 2 + 2 + codeBitWidth + 2 + str(compareList[0]).__len__()
        print(str(self.name).center(viewWidth))
        print('-'*viewWidth)
        for element in range(numOfDecodedAddresses):
            print(addressList[element] + ': ', end='')
            self.printCode(codeList[element])
            print(', ', end='')
            self.printComparisonNumber(compareList[element])
            print()
        print()

    def printCode(self, number):
        print(number, end='')

    def printComparisonNumber(self, number):
        print(number, end='')


class codeViewerWithEntropy(codeViewer, bitEntropy):
    def __init__(self, name, operation):
        self.name = name
        self.comparison = comparisonObject(operation)
        self.decodedEntropyArray = self.buildEntropyArray(list(decodedAddressArray.values()))
        self.comparisonEntropyArray = self.buildEntropyArray(list(self.comparison.compareDict.values()))
        self.printCodeView()

    def printCode(self, number):
        for bit in range(str(number).__len__()):
            printColors.printColorScaleAltText(self.decodedEntropyArray[bit], 0, 50, str(number)[bit])

    def printComparisonNumber(self, number):
        for bit in range(str(number).__len__()):
            printColors.printColorScaleAltText(self.comparisonEntropyArray[bit], 0, 50, str(number)[bit])



def decimalToBinary(decimalNumber, width):
    return bin(decimalNumber).removeprefix('0b').rjust(width, '0')

def binaryToDecimal(binaryNumber):
    return int(binaryNumber, 2)

if __name__ == '__main__':
    csvReader('./discovered.csv')
    NoopAnalysis = bitChangeMatrix('No op', 'Noop')
    addOneAnalysis = bitChangeMatrix('Minus One', 'minusOne')
    #manchesterAnalysis = bitChangeMatrix('Manchester', 'manchester')
    entropyNoop = bitEntropy('No op', 'Noop')
    entropyAddOne = bitEntropy('Minus One', 'minusOne')
    #manchesterEntropy = bitEntropy('Manchester', 'manchester')
    codeViewerWithEntropy('No op', 'Noop')
    codeViewerWithEntropy('Minus One', 'minusOne')
    codeViewerWithEntropy('Binary Per Digit', 'binaryPerDigit')
    #codeViewer('Manchester', 'manchester')
