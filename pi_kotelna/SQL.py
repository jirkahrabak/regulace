import urllib

from sqlalchemy import create_engine


engine = create_engine('mssql+pyodbc:///?odbc_connect=' +
    urllib.quote_plus('DRIVER=FreeTDS;SERVER=topeni.database.windows.net;PORT=1433;DATABASE=topeni;UID=jirkaadm;PWD=Laky85@@@@@@;TDS_Version=8.0;')
)
for row in engine.execute('select 6 * 7 as [Result];'):
    print row.Result
