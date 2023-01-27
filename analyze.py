import utils
import itertools
import csvClient
import copy

outputList = []
returnCode = ''

def analyze(csvData, _returnCode):
    print('---analyze.py analyze---')
    global returnCode
    returnCode = _returnCode
    headerList = []
    for (index, value) in enumerate(csvData[0]):
        if (value == 'search.list.id.videoId'):
            headerList.append('動画URL')
            appendOutputList(csvData, index, 'https://www.youtube.com/watch?v=')
        elif (value == 'videos.list.snippe_t.snippet.title'):
            headerList.append('タイトル')
            appendOutputList(csvData, index)
        elif (value == 'videos.list.snippe_t.snippet.description'):
            headerList.append('説明文')
            appendOutputList(csvData, index)
        elif (value == 'videos.list.snippe_t.snippet.tags'):
            headerList.append('タグ')
            appendOutputList(csvData, index)
        elif (value == 'videos.list.statistics.statistics.viewCount'):
            headerList.append('再生数')
            appendOutputList(csvData, index)
        elif (value == 'videos.list.statistics.statistics.likeCount'):
            headerList.append('ライク数')
            appendOutputList(csvData, index)
        elif (value == 'videos.list.statistics.statistics.commentCount'):
            headerList.append('コメント数')
            appendOutputList(csvData, index)
    headerList.append('ショート動画')
    for item in outputList:
        isShort = utils.containsOr(item, ['Short', 'short'])
        item.append(isShort)
    # print(f'headerList: {headerList}')
    print(f'outputList: {outputList}')

    # CSV出力。pathは現在のディレクトリから指定する
    outputData = copy.deepcopy(outputList)
    outputData.insert(0, headerList)
    try:
        csvClient.output('/output/', 'analyze', outputData, 'utf_8_sig')
    except Exception as e:
        print(e)
    
    # タグ分析
    # print('タグ分析結果---')
    # allTags = []
    # for item in outputList:
    #     index = utils.index(headerList, 'タグ')
    #     if (index != -1):
    #         allTags.append(item[index].split('、'))
    # allTags = list(filter(lambda a: a != '', list(itertools.chain.from_iterable(allTags))))
    # tagDict = dict()
    # for tag in allTags:
    #     if (tagDict.get(tag) == None):
    #         tagDict[tag] = 1
    #     else:
    #         tagDict[tag] += 1
    # tagSortedList = sorted(tagDict.items(), key = lambda tag : tag[1], reverse=True)
    # for tag in tagSortedList:
    #     print(tag)
    print('------')

def appendOutputList(
    csvData,
    index, 
    prefix = '',
):
    for i in range(len(csvData)):
        if (i == 0): continue
        value = f'{prefix}{csvData[i][index]}'
        global returnCode
        # splitValues = value.split(returnCode)
        # if len(splitValues) > 1:
        #     for splitIndex in range(len(splitValues)):
        #         splitValues[splitIndex] = f'"{splitValues[splitIndex]}"'
        #     appendValue = f'&{returnCode}&'.join(splitValues)
        # else:
        #     appendValue = value
        appendValue = ''
        if returnCode in value:
            print('replace:')
            print(value)
            replaceValue = value.replace(returnCode, f'"&{returnCode}&"')
            appendValue = f'="{replaceValue}"'
            print(appendValue)
        else:
            appendValue = value
        if (len(outputList) >= i):
            outputList[i - 1].append(appendValue)
        else:
            outputList.append([appendValue])
        