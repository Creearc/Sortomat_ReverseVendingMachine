modelFeatures = [1, 0, 0, 1]
preprocessingFeatures = [1, 1, 0, 0, 0, 0, 0, 0]

def getCode(features, n):
  if len(features) > n:
    return features[n]
  else:
    return 0

def getModelCode(n):
  return getCode(modelFeatures, n)

def getPreprocessingCode(n):
  return getCode(preprocessingFeatures, n)

def setModelCode(n, val):
  modelFeatures[n] = val

def setPreprocessingCode(n, val):
  preprocessingFeatures[n] = val

def setPreprocessingFromBinCodes(codes):
    for idx, code in enumerate(codes):
        setPreprocessingCode(idx, int(code))

def getDecimalCodeFromBinCodes(codes):
    decimalCode = 0
    for idx, code in enumerate(codes[::-1]):
        decimalCode += int(code) * (2 ** idx)
    return decimalCode
