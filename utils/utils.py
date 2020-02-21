import json

def readJsonFile(file_path):
    with open(file_path, encoding='utf8') as f:
        data = json.load(f)
    return data

def writeJsonFile(file_path, data):
    with open(file_path, 'w', encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
        print('finish writing...')

def writeTXT(file_path, data):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(data)
