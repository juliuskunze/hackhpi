import json

import html_parsing


def simplify(attr):
    if len(attr) == 0:
        return None
    return html_parsing.strip_tags(attr[0])


def convert(file='data/resumes2.json'):
    resumes = []

    with open(file) as data_file:
        data = json.load(data_file)

    for resume in data:
        entries = []
        resumes.append(entries)
        for entry in resume['entries']:
            company = simplify(entry['company'])
            dates = simplify(entry['dates'])
            title = simplify(entry['title'])
            if company is not None and dates is not None:
                entries.append((title, company, dates))

    return resumes


def save_csv(file='data/resumes.csv'):
    resumes = convert()
    wf = open(file, mode='w')
    wf.write('person, title, company, dates\n')
    for index, resume in enumerate(resumes):
        for entry in resume:
            wf.write("'{}', '{}', '{}', '{}'\n".format(index, entry[0], entry[1], entry[2]))
    wf.close()

