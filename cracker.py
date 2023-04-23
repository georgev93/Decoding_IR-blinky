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
                decodedAddressArray[row['address']] = row['code'].lstrip()
        globals()['numOfDecodedAddresses'] = decodedAddressArray.__len__()


class bitChangeComparison:

    def __init__(self, name, operation):
        self.name = name
        self.compareDict = {}
        self.listOfAddresses = []
        self.outputMatrix = []
        self.decodedMin = 100
        self.decodedMax = 0
        self.compareMin = 100
        self.compareMax = 0
        self.buildCompareDict(operation)
        self.buildOutputMatrix()
        self.printArray()

    def buildCompareDict(self, operation):
        for address in list(decodedAddressArray):
            #self.compareDict[address] = globals()[operation](decimalToBinary(int(address)))
            self.compareDict[address] = getattr(type(self), operation)(decimalToBinary(int(address)))
            self.listOfAddresses.append(address)

    def buildOutputMatrix(self):
        # Build an empty matrix
        for address in list(self.compareDict):
            row = []
            for address2 in list(self.compareDict):
                row.append('  ')
            self.outputMatrix.append(row)
        
        # Compare discovered codes
        for row in range(numOfDecodedAddresses):
            for column in range(row):
                differentBits = self.numOfBitsDifferent(decodedAddressArray.get(self.listOfAddresses[row]), decodedAddressArray.get(self.listOfAddresses[column]))
                self.outputMatrix[row][column] = differentBits
                if differentBits < self.decodedMin:
                    self.decodedMin = differentBits
                if differentBits > self.decodedMax:
                    self.decodedMax = differentBits

        # Compare this object's "compare" values
        for row in range(numOfDecodedAddresses):
            for column in range(row+1, numOfDecodedAddresses):
                differentBits = self.numOfBitsDifferent(self.compareDict.get(self.listOfAddresses[row]), self.compareDict.get(self.listOfAddresses[column]))
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

    @staticmethod
    def Noop(input):
            return input

    @staticmethod
    def addOne(input):
        return decimalToBinary(binaryToDecimal(input)+1)
    
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
    def manchesterPlusOne(input):
        return bitChangeComparison.manchester(bitChangeComparison.addOne(input))

class printColors:
    CYNBKG = 46
    GRNBKG = 42
    YLWBKG = 43
    REDBKG = 41
    ENDCOLOR = 0

    @staticmethod
    def colorEscapeCode(input):
        return str('\033[' + str(input) + 'm')
    
    @staticmethod
    def printColorScale(input, min, max, digits):
        percentage = (input-min)/(max-min)
        if(percentage < 0.25):
            print(printColors.colorEscapeCode(printColors.CYNBKG), end='')
        elif(percentage < 0.5):
            print(printColors.colorEscapeCode(printColors.GRNBKG), end='')
        elif(percentage < 0.75):
            print(printColors.colorEscapeCode(printColors.YLWBKG), end='')
        else:
            print(printColors.colorEscapeCode(printColors.REDBKG), end='')
        print(str(input).rjust(digits) + printColors.colorEscapeCode(printColors.ENDCOLOR), end='')



def decimalToBinary(decimalNumber):
    return bin(decimalNumber).removeprefix('0b').rjust(codeBitWidth, '0')

def binaryToDecimal(binaryNumber):
    return int(binaryNumber, 2)

if __name__ == '__main__':
    csvReader('./discovered.csv')
    NoopAnalysis = bitChangeComparison('Noop', 'Noop')
    addOneAnalysis = bitChangeComparison('addOne', 'addOne')
    machesterAnalysis = bitChangeComparison('machester', 'manchester')
    machesterAnalysis2 = bitChangeComparison('Machester Plus One', 'manchesterPlusOne')
