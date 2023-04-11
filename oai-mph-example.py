from sickle import Sickle

sickle = Sickle('https://zenodo.org/oai2d')


params = {
    'metadataPrefix': 'oai_dc',
    # 'set': 'user-cfa',
    # 'from': '2019-01-01'
}

records = sickle.ListRecords(**params)
sets = sickle.ListSets()

r = sickle.GetRecord(identifier='oai:zenodo.org:1213051', metadataPrefix='oai_dc')
print(r)





