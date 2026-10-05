import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.error import URLError
from urllib.request import Request, urlopen

NBRM_URL = 'https://www.nbrm.mk/KLServiceNOV/GetExchangeRate'
TRACKED = ('EUR', 'USD')
_cache = {}


class NbrmError(Exception):
    pass


def _window(iso_date):
    day = datetime.strptime(iso_date, '%Y-%m-%d')
    start = day - timedelta(days=10)
    return start.strftime('%d.%m.%Y'), day.strftime('%d.%m.%Y')


def _load(iso_date, force=False):
    start, end = _window(iso_date)
    key = (start, end)
    cached = _cache.get(key)
    if not force and cached and datetime.now().timestamp() - cached['at'] < 3600:
        return cached['rows']
    url = f'{NBRM_URL}?StartDate={start}&EndDate={end}'
    request = Request(url, headers={'User-Agent': 'office-log'})
    try:
        with urlopen(request, timeout=15) as response:
            payload = response.read()
    except (URLError, TimeoutError, OSError) as exc:
        raise NbrmError('NBRM rate list is unavailable') from exc
    text = payload.decode('utf-8-sig', errors='replace')
    text = text.replace('encoding="utf-16"', 'encoding="utf-8"', 1)
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise NbrmError('NBRM rate list could not be read') from exc
    rows = []
    for node in root.findall('GetExchangeRate'):
        code = (node.findtext('Oznaka') or '').strip().upper()
        if code not in TRACKED:
            continue
        try:
            middle = float(node.findtext('Sreden') or '')
            nomin = float(node.findtext('Nomin') or '1') or 1
            list_day = (node.findtext('Datum') or '')[:10]
        except ValueError:
            continue
        if not list_day:
            continue
        rows.append({
            'currency': code,
            'rate': middle / nomin,
            'middle': middle,
            'nomin': nomin,
            'list_date': list_day,
        })
    _cache[key] = {'at': datetime.now().timestamp(), 'rows': rows}
    return rows


def lookup_rate(currency, iso_date, force=False):
    code = (currency or '').upper()
    if code == 'MKD':
        return {'currency': 'MKD', 'rate': 1.0, 'list_date': iso_date, 'source': 'local'}
    if code not in TRACKED:
        raise NbrmError('Unsupported currency')
    if not iso_date:
        raise NbrmError('Date is required')
    rows = [row for row in _load(iso_date, force) if row['currency'] == code and row['list_date'] <= iso_date]
    if not rows:
        raise NbrmError('No NBRM rate for this date')
    found = max(rows, key=lambda row: row['list_date'])
    return {
        'currency': code,
        'rate': found['rate'],
        'list_date': found['list_date'],
        'source': 'nbrm',
    }
