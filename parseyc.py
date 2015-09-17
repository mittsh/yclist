import re
import json

YC_LINE = re.compile(r'^' +
  '(?P<name>.+?)' + '\s+' +
  '(?:' + '(?P<url>http[^\s]+)\s+' + ')?' +
  '(?P<batch>\w*)\s+' +
  '(?:' + '(?P<status>(?:Exited|Dead))\s+' + ')?' +
  '(?P<description>.*)' +
  '$'
)

MD_HEAD_TPL = '''# A list of [Y Combinator](https://www.ycombinator.com/) funded companies

'''
MD_COMPANY_TPL = '''## {name}

URL: [{url}]({url})
Batch: {batch}
Status: {status}

{description}


'''

class ParseYC(object):

  def __init__(self):
    self.yc_companies = []

  def parse_yc_line(self, line):
    m = YC_LINE.match(line)
    if not m:
      raise StandardError('Line does not match regex: {0}'.format(line))
    
    print('-'*20)
    print('Name: {0}'.format(m.group('name')))
    print('URL: {0}'.format(m.group('url')))
    print('Batch: {0}'.format(m.group('batch')))
    print('Status: {0}'.format(m.group('status')))
    print('Description: {0}'.format(m.group('description')))
  
    self.yc_companies.append({
      'name':(m.group('name') or None),
      'url':(m.group('url') or None),
      'batch':(m.group('batch') or None),
      'status':(m.group('status') or 'Active'),
      'description':(m.group('description') or None),
    })

  def generate_md(self):
    md = MD_HEAD_TPL
    for company in self.yc_companies:
      md += MD_COMPANY_TPL.format(
        name=company.get('name') or 'N.A.',
        url=company.get('url') or 'N.A.',
        batch=company.get('batch') or 'N.A.',
        status=company.get('status') or 'Active',
        description=company.get('description') or 'N.A.',
      )
    return md

  def load(self):
    with open('./list.txt', 'r') as fp:
      for line in fp:
        if line:
          self.parse_yc_line(line)

  def write(self):
    with open('./list.json', 'w') as fp:
      fp.write(json.dumps(self.yc_companies, indent=2, sort_keys=True))

    with open('./list.md', 'w') as fp:
      fp.write(self.generate_md())

if __name__ == '__main__':
  p = ParseYC()
  p.load()
  p.write()
