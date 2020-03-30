# coding:utf-8
import math
import pandas

# arr:需要循环加字母的数组
# level：需要加的层级


def cycle_letter(arr, level):
    tempArr = []
    letterArr = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z']
    arrNum = len(arr)
    if (level == 0 or arrNum == 0):
        return letterArr
    for index in range(arrNum):
        for letter in letterArr:
            tempArr.append(arr[index] + letter)
    return tempArr


# arr:需要生成的Excel列名称数目
def reduce_excel_col_name(num):
    tempVal = 1
    level = 1
    while (tempVal):
        tempVal = num / (math.pow(26, level))
        if (tempVal > 1):
            level += 1
        else:
            break

    excelArr = []
    tempArr = []
    for index in range(level):
        tempArr = cycle_letter(tempArr, index)
        for numIndex in range(len(tempArr)):
            if (len(excelArr) < num):
                excelArr.append(tempArr[numIndex])
            else:
                return excelArr
    return excelArr


def merge_cell(data, ser, ser1, list_change):
    if ser1 in list_change:
        column = reduce_excel_col_name(len(data.columns))[
            list(data.columns).index(ser1)]
        ser1 = '商品编码'
    else:
        column = reduce_excel_col_name(len(data.columns))[
            list(data.columns).index(ser1)]
    data_all = pandas.DataFrame()
    for i in data[ser].unique():
        data_2 = data.loc[data[ser] == i]
        for i2 in data_2[ser1].unique():
            temp = data_2.loc[data_2[ser1] == i2]
            temp['groupby_paixu'] = range(1, len(temp) + 1)
            temp['count'] = len(temp)
            data_all = data_all.append(temp)
    data_all['paixu'] = range(2, len(data_all) + 2)
    data_all['count'] = data_all.paixu + data_all['count'] - 1
    data_all['paixu'] = column + data_all['paixu'].astype('str')
    data_all['count'] = column + data_all['count'].astype('str')
    data_all = data_all.loc[data_all.groupby_paixu == 1, ['paixu', 'count']]
    data_all['relust'] = data_all.paixu + ':' + data_all['count']
    return list(data_all.relust)
