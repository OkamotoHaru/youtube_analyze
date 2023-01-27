import csvClient
import youtube
import utils
import sys
import analyze
import copy

def main():
    # youtubeクライアント初期化
    args = sys.argv
    apiKey= args[1] if len(args) > 1 else ''
    publishedAfter=utils.lastYear()
    publishedBefore=utils.yesterdayLastDate()
    returnCode = 'Char(10)'
    youtube.createInstance(apiKey, returnCode)
    # 検索
    csvData = youtube.search(
        searchWords='モトブログ',
        publishedAfter=publishedAfter,
        publishedBefore=publishedBefore,
        count=50,
    )
    # CSV出力。pathは現在のディレクトリから指定する
    path = '/output/'
    fileName = f'{publishedAfter}_{publishedBefore}'.replace(':', '-')
    try:
        csvClient.output(path, fileName, csvData, 'utf_8_sig')
    except Exception as e:
        print(e)
    # 分析
    analyze.analyze(copy.deepcopy(csvData), returnCode)

print(__name__)
if (__name__ == '__main__'):
    main()