import csvClient
import youtube
import utils
import sys

def main():
    args = sys.argv
    apiKey= args[1] if len(args) > 1 else ''
    publishedAfter=utils.lastYear()
    publishedBefore=utils.yesterdayLastDate()
    youtube.createInstance(apiKey)
    csvData = youtube.search(
        searchWords='モトブログ',
        publishedAfter=publishedAfter,
        publishedBefore=publishedBefore,
        count=100,
    )

    # CSV出力。pathは現在のディレクトリから指定する
    path = '/output/'
    fileName = f'{publishedAfter}_{publishedBefore}'.replace(':', '-')
    try:
        csvClient.output(path, fileName, csvData, 'utf_8_sig')
    except Exception as e:
        print(e)

print(__name__)
if (__name__ == '__main__'):
    main()