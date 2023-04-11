from sickle import Sickle

sickle = Sickle('https://zenodo.org/oai2d')

params = {
    'metadataPrefix': 'oai_dc',
    # 'set': 'user-cfa',
    # 'from': '2019-01-01'
}

records = sickle.ListRecords(**params)
xmls = []

for i in range(10000):
    r = records.next()
    xmls.append(r.raw)
    print(i)

print(len(xmls))


# 44 Sekunden für 10_000
