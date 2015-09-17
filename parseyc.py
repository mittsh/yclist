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

yc_companies = []

def parse_yc_line(line):
  m = YC_LINE.match(line)
  if not m:
    raise StandardError('Line does not match regex: {0}'.format(line))
  
  print('-'*20)
  print('Name: {0}'.format(m.group('name')))
  print('URL: {0}'.format(m.group('url')))
  print('Batch: {0}'.format(m.group('batch')))
  print('Status: {0}'.format(m.group('status')))
  print('Description: {0}'.format(m.group('description')))
  
  yc_companies.append({
    'name':(m.group('name') or None),
    'url':(m.group('url') or None),
    'batch':(m.group('batch') or None),
    'status':(m.group('status') or 'Active'),
    'description':(m.group('description') or None),
  })

with open('./list.txt', 'r') as fp:
  for line in fp:
    if line:
      parse_yc_line(line)

with open('./list.json', 'w') as fp:
  fp.write(json.dumps(yc_companies, indent=2, sort_keys=True))
