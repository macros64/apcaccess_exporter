import apcData
import re
import datetime

NAME_VALUE_DELIM = ":"
LINE_END = "\n"

def parseUpsData(data: str) -> apcData.APCData:
    ret = apcData.APCData()
    ret.model = extractValueStr(data, "MODEL")
    ret.serial = extractValueStr(data, "SERIALNO")
    ret.status = extractValueStr(data, "STATUS")
    ret.lineV = extractValueNum(data, "LINEV")
    ret.battPct = extractValueNum(data, "BCHARGE")
    ret.loadPct = extractValueNum(data, "LOADPCT")
    ret.lastStartTime = extractValueDate(data, "STARTTIME")
    return ret

def extractValueStr(data: str, valName: str) -> str:
    ret = ""
    i = data.find(valName)
    if i > 0:
        j = data.find(NAME_VALUE_DELIM, i)
        if j > 0:
            k = data.find(LINE_END, j)
            ret = data[j + 1:k].strip()

    return ret
    
def extractValueNum(data: str, valName: str) -> float:
    ret = 0.0
    strVal = extractValueStr(data, valName)
    if len(strVal) > 0:
        ret = re.search("[\d\.]+", strVal).group(0)
        ret = float(ret)
    return ret

def extractValueDate(data: str, valName: str) -> datetime.datetime:
    ret = ""
    strVal = extractValueStr(data, valName)
    if len(strVal) > 0:
        ret = datetime.datetime.fromisoformat(strVal)
    return ret