# 2022-06-22 Investigation of Zenodo 

## Goal

> Understand how Zenodo structures their datasets and identify how the meta data can be accessed programmatically.

## Summary
* General
    * Zenodo is a collection of scientific datasets with metadata. The site is offered by CERN in support to the project OpenAIRE. All metadata is CC0.
    * Zenodo makes a difference between the concept of a dataset and the versions it consists of. This could potentially also be a way forward in the UnknownData project.
    * Zenodo has the concept of Communities. One third of datasets belong to a community, the most common communities are ('dryad', 1909), ('biosyslit', 203), ('spacephysics', 124)
    * Datasets in Zenodo are not strongly linked to any dblp stream. Some of them are combined into collections. Thus, we have to think about how and if we want to collect datasets in a similar way to dblp records.
    Data Quality
    * In the recent dataset we got 40k signatures, 16k of which have orcids. 60% of datasets have at least one author with orcid, 20% have at least one author with an orcid we have in dblp.
    * Most dataset have a low number of creators and versions, but there are outliers that go wild. In out sample dataset we saw up to 92 authors and up to 405 versions of a dataset. We have to think about how and if we want to model this for the UnknownData project.
    * Historic datasets have on average less versions (avg. 1.03, max. 11), and way less orcids.
        Versions of historic datasets do change quite fast, but not often. More than 20% are updated on avg within 2.5 days, but they have mostly only a few versions.
* Data access
    * The REST API access is quite nice and usable. Bulk load is realizable with a combination of a filter on created  timestamp and a sorting by most recent.
    * We CAN get all versions of a concept via the REST API
    * I didn't find a way to filter the datasets to only contain computer science datasets when only looking ad Zenodo data. Also, how would we define this? In general any dataset could be used in computer science papers. To me it seems at the moment, that we have to load metadata based on DOIs we see quoted in papers.
    * Also offers access via OAI-PMH, but only shows limited metadata there.

Generated Code: https://sidonia.dagstuhl.de:9000/dblp/unknowndata/-/tree/main/investigations/zenodo-api


## Metadata of Datasets

Zenodo has two layers in dataset metadata: The concepts of datasets and versions of actual datasets. All metadata is licensed under CC0 and thus can be freely used.

The concept of a dataset does not represent any specific dataset files directly but rather the idea of a dataset. This concept can consist out of several versions of actual datasets. It does not represent any specific set of files directly, but rather points towards the most recent version of the dataset. It does not consists of metadata itself, except an unique DOI. The versions of datasets represent the actual released datasets and contain metadata, such as individual DOI, the list of creators and other metadata. They also contain most of the time a link to the DOI of the concept of the dataset they represent. These dataset versions also link to actual files that contain the relevant data.

Concepts of metadata can also be combined into communities. Communities are managed by their creator and can be created by verified users. They are often linked to specific projects, but only via their name and a description.

Sources:
* https://developers.zenodo.org/
* https://about.zenodo.org/terms/
* https://help.zenodo.org/features/

## Data Access

The data can be accessed through two different APIs, the REST API and the OAI-PMH.
### OAI-PMH

The Open Archives Initiative Protocol for Metadata Harvesting is a standard protocol for harvesting and sharing metadata. It can be accessed through the endpoint https://zenodo.org/oai2d and supports the harvesting of the entire repository and returns records as XMLs. It is possible to filter by the community the dataset belongs to, and or to only get metadata of specific records, including records to versions of datasets that are not the most recent.

The API calls themselves return only a subset of the metadata of a dateset. Below you can see an example of a metadata set for the hdblp dataset. Notably, it is missing the ordicd and affiliation of the creators, and information about the versions of the datasets concept.

The OAI-PMH is limited to 120 requests per minute.
```xml
<record xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <header>
        <identifier>oai:zenodo.org:3051910</identifier>
        <datestamp>2020-01-24T19:26:18Z</datestamp>
        <setSpec>openaire_data</setSpec>
    </header>
    <metadata>
        <oai_dc:dc xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
            <dc:creator>Hoffmann, Oliver</dc:creator>
            <dc:creator>Reitz, Florian</dc:creator>
            <dc:date>2019-05-20</dc:date>
            <dc:description>This data set contains historical data of the dblp collection (https://dblp.org). I.e., for each metadata record, the collection contains all known revisions that existed in dblp. \n\nWith hdblp, the state of dblp can be restored for each day between June 2 1999 and December 17 2018. hdblp can be used to study the development of the dblp collection.\n\nCorrection of version 2 which omitted the data set description. </dc:description>
            <dc:description>dblp is a joint project of the University of Trier, Germany and the Schloss Dagstuhl – Leibniz Center for Informatics, Wadern, Germany. Former and current members of the team are listed on http://dblp.org/db/about/team.html .</dc:description>
            <dc:identifier>https://zenodo.org/record/3051910</dc:identifier>
            <dc:identifier>10.5281/zenodo.3051910</dc:identifier>
            <dc:identifier>oai:zenodo.org:3051910</dc:identifier>
            <dc:relation>doi:10.5281/zenodo.1213050</dc:relation>
            <dc:rights>info:eu-repo/semantics/openAccess</dc:rights>
            <dc:rights>https://opendatacommons.org/licenses/by/1.0/</dc:rights>
            <dc:subject>dblp</dc:subject>
            <dc:subject>historical metadata</dc:subject>
            <dc:title>hdblp: historical data of the dblp collection</dc:title>
            <dc:type>info:eu-repo/semantics/other</dc:type>
            <dc:type>dataset</dc:type>
        </oai_dc:dc>
    </metadata>
</record>
```


### REST API

The REST API is a generic approach to allow access to several Zenodo features, including the querying of metadata. It can be accessed through the endpoint https://zenodo.org/api and returns the records by default as JSON. You can either get either metadata of individual records using the endpoint GET api/records/:id or you can freely query the metadata using the endpoint GET /api/records/ .

If you do a query, you can paginate though the results, but with a query you can only get up to 10.000 results, even with pagination.
But with the use of elasicsearch via the created  timestamp it is possible to adapt the query to load more datasets in several queries.

The filtering here allows you to select what kind of datatypes you want to get. This enables filtering to only datasets, which filters out presentations, articles, and other things that are also uploaded to the

The returned records contain all the metadata that the OAI-MPH returns and more. It contains affiliations and DOIs of the dataset creators, information about the amount of versions of the related dataset concept and the position of the current version in this concept, statistics about how much the dataset is being used, metadata about the files the dataset version consist of, and more. Below you find first a list of all metadata columns that were present in the latest 10.000 records on time of writing, and second an example of the returned json metadata of the hdblp dataset.

In the list of metadata columns, you can see how many of the 10.000 rows contained values for each. All of them contain doi, creators, and a title, among other metadata which are also filled to 100%.

Via a query with a search for the conceptrecid  on the api/records  endpoint it is possible to get all versions of a specific concept.


List of all returned metadata columns:
```
#   Column                          Non-Null
---  ------                          --------
 0   conceptdoi                      7760
 1   conceptrecid                    10000
 2   created                         10000
 3   doi                             10000
 4   files                           9087
 5   id                              10000
 6   owners                          10000
 7   revision                        10000
 8   updated                         10000
 9   links.badge                     10000
 10  links.bucket                    9087
 11  links.conceptbadge              7760
 12  links.conceptdoi                7760
 13  links.doi                       10000
 14  links.html                      10000
 15  links.latest                    10000
 16  links.latest_html               10000
 17  links.self                      10000
 18  metadata.access_right           10000
 19  metadata.access_right_category  10000
 20  metadata.creators               10000
 21  metadata.description            10000
 22  metadata.doi                    10000
 23  metadata.keywords               5324
 24  metadata.license.id             9174
 25  metadata.publication_date       10000
 26  metadata.related_identifiers    8813
 27  metadata.relations.version      10000
 28  metadata.resource_type.title    10000
 29  metadata.resource_type.type     10000
 30  metadata.title                  10000
 31  stats.downloads                 10000
 32  stats.unique_downloads          10000
 33  stats.unique_views              10000
 34  stats.version_downloads         10000
 35  stats.version_unique_downloads  10000
 36  stats.version_unique_views      10000
 37  stats.version_views             10000
 38  stats.version_volume            10000
 39  stats.views                     10000
 40  stats.volume                    10000
 41  metadata.embargo_date           117
 42  metadata.language               2335
 43  metadata.notes                  2460
 44  metadata.version                2502
 45  metadata.grants                 1042
 46  metadata.communities            3586
 47  metadata.subjects               196
 48  metadata.contributors           542
 49  metadata.method                 1192
 50  metadata.dates                  26
 51  metadata.references             442
 52  metadata.access_conditions      603
 53  metadata.journal.title          308
 54  metadata.thesis.supervisors     84
 55  metadata.thesis.university      67
 56  links.thumb250                  274
 57  links.thumbs.10                 274
 58  links.thumbs.100                274
 59  links.thumbs.1200               274
 60  links.thumbs.250                274
 61  links.thumbs.50                 274
 62  links.thumbs.750                274
 63  metadata.journal.issue          67
 64  metadata.journal.pages          82
 65  metadata.journal.volume         100
 66  metadata.alternate_identifiers  5
 67  metadata.meeting.acronym        78
 68  metadata.meeting.dates          74
 69  metadata.meeting.place          66
 70  metadata.meeting.title          93
 71  metadata.meeting.url            67
 72  metadata.meeting.session        9
 73  metadata.imprint.publisher      28
 74  metadata.part_of.pages          25
 75  metadata.part_of.title          28
 76  metadata.imprint.isbn           25
 77  metadata.imprint.place          27
 78  metadata.meeting.session_part   4
 79  metadata.locations              16
```

Example of hdblp record as returned json:
```json
{
                "conceptdoi": "10.5281/zenodo.1213050",
                "conceptrecid": "1213050",
                "created": "2019-05-20T09:55:44.798810+00:00",
                "doi": "10.5281/zenodo.3051910",
                "files": [
                    {
                        "bucket": "f5082013-5696-455f-8944-754b47c76faf",
                        "checksum": "md5:40f5c160b7b790bcdeec0219b28aef7e",
                        "key": "dblp-2018-12-17.dtd",
                        "links": {
                            "self": "https://zenodo.org/api/files/f5082013-5696-455f-8944-754b47c76faf/dblp-2018-12-17.dtd"
                        },
                        "size": 12984,
                        "type": "dtd"
                    },
                    {
                        "bucket": "f5082013-5696-455f-8944-754b47c76faf",
                        "checksum": "md5:d5e52bc23136acfe4b89fe8aaaa881d1",
                        "key": "hdblp-2018-12-17.xml.gz",
                        "links": {
                            "self": "https://zenodo.org/api/files/f5082013-5696-455f-8944-754b47c76faf/hdblp-2018-12-17.xml.gz"
                        },
                        "size": 630294866,
                        "type": "gz"
                    },
                    {
                        "bucket": "f5082013-5696-455f-8944-754b47c76faf",
                        "checksum": "md5:0b4b6b992a6eed01d88c2ab9184091cf",
                        "key": "hdblp.pdf",
                        "links": {
                            "self": "https://zenodo.org/api/files/f5082013-5696-455f-8944-754b47c76faf/hdblp.pdf"
                        },
                        "size": 172722,
                        "type": "pdf"
                    },
                    {
                        "bucket": "f5082013-5696-455f-8944-754b47c76faf",
                        "checksum": "md5:b94036b94345209da7258dc6a7b8723a",
                        "key": "LICENCE.txt",
                        "links": {
                            "self": "https://zenodo.org/api/files/f5082013-5696-455f-8944-754b47c76faf/LICENCE.txt"
                        },
                        "size": 20437,
                        "type": "txt"
                    }
                ],
                "id": 3051910,
                "links": {
                    "badge": "https://zenodo.org/badge/doi/10.5281/zenodo.3051910.svg",
                    "bucket": "https://zenodo.org/api/files/f5082013-5696-455f-8944-754b47c76faf",
                    "conceptbadge": "https://zenodo.org/badge/doi/10.5281/zenodo.1213050.svg",
                    "conceptdoi": "https://doi.org/10.5281/zenodo.1213050",
                    "doi": "https://doi.org/10.5281/zenodo.3051910",
                    "html": "https://zenodo.org/record/3051910",
                    "latest": "https://zenodo.org/api/records/3051910",
                    "latest_html": "https://zenodo.org/record/3051910",
                    "self": "https://zenodo.org/api/records/3051910"
                },
                "metadata": {
                    "access_right": "open",
                    "access_right_category": "success",
                    "creators": [
                        {
                            "affiliation": "LZI Schloss Dagstuhl, Wadern, Germany",
                            "name": "Hoffmann, Oliver",
                            "orcid": "0000-0002-3808-9042"
                        },
                        {
                            "affiliation": "LZI Schloss Dagstuhl, Wadern, Germany",
                            "name": "Reitz, Florian",
                            "orcid": "0000-0001-6114-3388"
                        }
                    ],
                    "description": "<p>This data set contains historical data of the dblp collection (https://dblp.org). I.e., for each metadata record, the collection contains all known revisions that existed in dblp. </p>\n\n<p>With hdblp, the state of dblp can be restored for each day between June 2 1999 and December 17 2018. hdblp can be used to study the development of the dblp collection.</p>\n\n<p>Correction of version 2 which omitted the data set description. </p>",
                    "doi": "10.5281/zenodo.3051910",
                    "keywords": [
                        "dblp",
                        "historical metadata"
                    ],
                    "license": {
                        "id": "ODC-By-1.0"
                    },
                    "notes": "dblp is a joint project of the University of Trier, Germany and the Schloss Dagstuhl \u2013 Leibniz Center for Informatics, Wadern, Germany. Former and current members of the team are listed on http://dblp.org/db/about/team.html .",
                    "publication_date": "2019-05-20",
                    "related_identifiers": [
                        {
                            "identifier": "10.5281/zenodo.1213050",
                            "relation": "isVersionOf",
                            "scheme": "doi"
                        }
                    ],
                    "relations": {
                        "version": [
                            {
                                "count": 3,
                                "index": 2,
                                "is_last": true,
                                "last_child": {
                                    "pid_type": "recid",
                                    "pid_value": "3051910"
                                },
                                "parent": {
                                    "pid_type": "recid",
                                    "pid_value": "1213050"
                                }
                            }
                        ]
                    },
                    "resource_type": {
                        "title": "Dataset",
                        "type": "dataset"
                    },
                    "title": "hdblp: historical data of the dblp collection"
                },
                "owners": [
                    32943
                ],
                "revision": 6,
                "stats": {
                    "downloads": 1887.0,
                    "unique_downloads": 212.0,
                    "unique_views": 318.0,
                    "version_downloads": 3158.0,
                    "version_unique_downloads": 1007.0,
                    "version_unique_views": 9003.0,
                    "version_views": 9839.0,
                    "version_volume": 1292125159131.0,
                    "views": 355.0,
                    "volume": 1063337273185.0
                },
                "updated": "2020-01-24T19:26:18.295904+00:00"
            }
```


Sources:

* https://developers.zenodo.org/#sets
* https://developers.zenodo.org/#add-metadata-to-your-github-repository-release
* https://developers.zenodo.org/#records

## Scraping

Because of the exhaustive APIs, scraping was not further investigated.

# Data Selection

Both APIs offer access to metadata of all records. While the OAI-MPH does only offers filtering based on time and collections, the REST API allows arbitrary filters based on the elastic search engine. Through further parameters we can limit the type of records and can limit it to datasets. While it is possible to filter based on collections, they are not as structured as streams are in dblp. I could not find a simple solution on how to filter the records to only contain datasets that are liked to computer sciences.

To collect the relevant data, I assume we have to map the Zenodo dataset with lists of datasets that are cited in relevant papers. We can either bulk load the metadata and match it locally, or do one call per quoted dataset to get the required metadata.

Sources:
* https://developers.zenodo.org/#list36

## Data Analysis

To analyse the data, I collected though the REST API the latest 10.000 records that don´t contain non recent versions of datasets, and the 10.000 latest records that do contain non recent versions of datasets.

```
In the past  10.000 unique hits there where
     * 7760 unique concept dois

Number of Creators
     * min(#creators) = 1
     * max(#creators) = 92
     * median(#creators) = 2.0
     * mean(#creators) = 4.0163
     * quantile(0.95, #creators) = 12.0


Number of Versions
     * min(#versions) = 1
     * max(#versions) = 405
     * median(#versions) = 1.0
     * mean(#versions) = 1.6685
     * quantile(0.95, #versions) = 3.0
    * count(#versions == 1) = 8465


Number of historic Versions ('2015-01-05T11:20:38+00:00', '2017-10-20T19:58:44.366466+00:00', 8304)
     * min(#versions) = 1
     * max(#versions) = 11
     * median(#versions) = 1.0
     * mean(#versions) = 1.0357658959537572
     * quantile(0.95, #versions) = 1.0


Communities
     * min(size(communities)) = 1
     * max(size(communities)) = 1909
     * median(size(communities)) = 1.0
     * mean(size(communities)) = 7.5060975609756095
     * quantile(0.95, size(communities)) = 10.899999999999977
     * Top 20 communities: [('dryad', 1909), ('biosyslit', 203), ('spacephysics', 124), ('iodp', 78), ('efsa-kj', 68), ('ccg', 56), ('attest-eu', 42), ('skyglow-was', 29), ('covid-19', 27), ('besta', 24), ('elte-dh', 22), ('synpop_world', 20), ('social_contact_data', 18), ('cranberrybacteria', 18), ('fi-xix-gramineae', 16), ('empirical-software-engineering', 15), ('crossbow-h2020', 15), ('ilopersiancorpus', 15), ('astronomy-general', 13), ('leo', 13)]

Changing Versions
     * Of the last 10000 non  unique updated datasets, there are
     * 645 datasets that have been updated at least once
     * of them 28 changed their author count

DBPL authors
     * Number of signatures in dataset = 40163
     * Number of signatures with orcid = 16865
     * Number of records with at least one orcid = 6076
     * Number of records with a least one dblp author = 1958
     * Number of records with a least one verified dblp author = 672
     * Number of verified dblp orcids = 703


DBPL authors historic dataset
     * Number of signatures in dataset = 27264
     * Number of signatures with orcid = 476
     * Number of records with at least one orcid = 347
     * Number of records with a least one dblp author = 248
     * Number of records with a least one verified dblp author = 26


Updates to concepts
     * MIN avg_time_between_updates_by_concept in days: 0.0007029592708333334
     * MAX avg_time_between_updates_by_concept in days: 2473.260918136366
     * MEAN avg_time_between_updates_by_concept in days: 102.81466587184201
     * MEDIAN avg_time_between_updates_by_concept in days: 47.44315781582176
     * QUANTILE 5% avg_time_between_updates_by_concept in days: 0.010558191488425926
```