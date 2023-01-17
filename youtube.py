from apiclient.discovery import build
import math
import utils
import copy
import myToken

youtube = build('youtube', 'v3', developerKey=myToken.my_token)
headerList = []
outputList = []

def search(
    searchWords,
    publishedAfter,
    publishedBefore,
    count
):
    print('---youtube.py search---')
    print(f'searchWords: {searchWords}')
    print(f'publishedAfter: {publishedAfter}')
    print(f'publishedBefore: {publishedBefore}')
    print(f'count: {count}')
    part = 'snippet'
    descendingType = 'viewCount'    # 指定した値で降順で取得
    _type = 'video' # 検索結果に含ませる動画種類。video,channel,playlistがある
    maxResults = 50
    loop = math.ceil(count / maxResults)
    print(f'loop: {loop}')
    nextPageToken = None
    headerList.clear()
    outputList.clear()
    for _ in range(loop):
        result = searchList(
            part=part,
            searchWords=searchWords,
            descendingType=descendingType,
            _type=_type,
            publishedAfter=publishedAfter,
            publishedBefore=publishedBefore,
            maxResults=str(maxResults),
            nextPageToken=nextPageToken
        )
        nextPageToken = result['nextPageToken']
        resultItems = result['items']
        for item in resultItems:
            itemValuesList.clear()
            global appendCount
            appendCount = 0
            # 基本情報取得
            appendList('search.list', item)
            # タグ情報取得
            videoId = item['id']['videoId']
            videoSnippetResult = videosList('snippet', videoId)
            videoSnippetItems = videoSnippetResult['items']
            for itemDict in videoSnippetItems:
                appendList('videos.list.snippe_t', itemDict)
            # いいね数や再生数など取得
            videoStatisticsResult = videosList('statistics', videoId)
            videoStatisticsItems = videoStatisticsResult['items']
            for itemDict in videoStatisticsItems:
                appendList('videos.list.statistics', itemDict)
            # CSV出力情報に設定
            outputList.append(copy.deepcopy(itemValuesList))
    outputList.insert(0, headerList)
    print('------')
    return outputList

def searchList(
    part: str,
    searchWords: str,
    descendingType,
    _type,
    publishedAfter: str,
    publishedBefore: str,
    maxResults: str,
    nextPageToken = None,
):
    if (nextPageToken is None):
        search_response = youtube.search().list(
            part=part,
            q=searchWords,
            order=descendingType,
            type=_type,
            publishedAfter=publishedAfter,
            publishedBefore=publishedBefore,
            maxResults=maxResults,
        ).execute()
        return search_response
    else:
        search_response = youtube.search().list(
            part=part,
            q=searchWords,
            order=descendingType,
            type=_type,
            publishedAfter=publishedAfter,
            publishedBefore=publishedBefore,
            maxResults=maxResults,
            pageToken=nextPageToken,
        ).execute()
        return search_response

def appendList(tag, item):
    for key, value in item.items():
        addTag = f'{tag}.{key}'
        if (type(value) is dict):
            # 末尾のvalueにたどり着くまで再帰する
            appendList(addTag, value)
        elif (type(value) is str):
            # スプレッドシート上でCSVとして読み込むときに改行されてしまうため、別の文字に置き換える
            addValue = value.replace('\n', 'uchidamasato')
            # 値としてのカンマはCSVの都合上セル分けされてしまうため、句読点に置き換える
            addValue = addValue.replace(',', '、')
            appendItemValueList(addTag, addValue)
        elif (type(value) is list):
            addValue = '、'.join(value)
            appendItemValueList(addTag, addValue)
        else:
            appendItemValueList(addTag, value)

itemValuesList = []
appendCount = 0
def appendItemValueList(tag, value):
    appendKey(tag)
    itemValuesList.append(value)
    global appendCount
    appendCount += 1

def appendKey(tag):
    indexResult = utils.index(headerList, tag)
    global appendCount
    if (indexResult == -1):
        # 新規タグならキーリストに新規タグを挿入
        headerList.insert(appendCount, tag)
        # 新規タグなら出力リストに空データを挿入
        for list in outputList:
            list.insert(appendCount, '')
    else:
        # 値リストとキーリストのインデックスに誤差があるなら空データを挿入して補完する
        if (indexResult != appendCount):
            diff = indexResult - appendCount
            for n in range(diff):
                itemValuesList.append('')
                appendCount += 1

def videosList(part, videoId):
    fetch_response = youtube.videos().list(
        part=part,
        id=videoId,
    ).execute()
    return fetch_response