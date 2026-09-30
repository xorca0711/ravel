"""Read exact XLSX cells without modifying source workbooks."""
import io,re,zipfile,xml.etree.ElementTree as ET
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read_cells(blob):
 out={}
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)] if 'xl/sharedStrings.xml' in z.namelist() else []
  # Source workbooks all have one explicitly named sheet; record its name.
  wb=ET.fromstring(z.read('xl/workbook.xml'));sheets=wb.findall('m:sheets/m:sheet',NS);assert len(sheets)==1
  sheet=sheets[0].get('name');path='xl/worksheets/sheet1.xml'
  for c in ET.fromstring(z.read(path)).findall('.//m:c',NS):
   value=c.find('m:v',NS);inline=c.find('m:is',NS);formula=c.find('m:f',NS)
   if value is None and inline is None:continue
   kind=c.get('t');raw=value.text if value is not None else ''.join(inline.itertext())
   val=strings[int(raw)] if kind=='s' else raw if kind in ['str','inlineStr'] else float(raw)
   out[c.get('r')]=dict(value=val,formula=formula.text if formula is not None else None)
 return sheet,out
