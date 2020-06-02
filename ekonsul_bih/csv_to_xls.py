import pandas

df = pandas.read_csv('consultations.csv')

print(df.info())

df['CreatedDate'] = df['CreatedDate'].replace(r"/Date\(", '', regex=True).replace(r"\)/", '', regex=True).astype('int64')
df['ConsultationCreatedDate'] = df['ConsultationCreatedDate'].replace(r"/Date\(", '', regex=True).replace(r"\)/", '', regex=True).astype('int64')
df['StartDate'] = df['StartDate'].replace(r"/Date\(", '', regex=True).replace(r"\)/", '', regex=True).astype('int64')
df['EndDate'] = df['EndDate'].replace(r"/Date\(", '', regex=True).replace(r"\)/", '', regex=True).astype('int64')

# df['CreatedDate'] = df['CreatedDate'].astype('int64').div(1000).astype('int64')
# df['ConsultationCreatedDate'] = df['ConsultationCreatedDate'].astype('int64').div(1000).astype('int64')
# df['StartDate'] = df['StartDate'].astype('int64').div(1000).astype('int64')
# df['EndDate'] = df['EndDate'].astype('int64').div(1000).astype('int64')

df['CreatedDate'] = pandas.to_datetime(df['CreatedDate'], unit='ms')
df['ConsultationCreatedDate'] = pandas.to_datetime(df['ConsultationCreatedDate'], unit='ms')
df['StartDate'] = pandas.to_datetime(df['StartDate'], unit='ms')
df['EndDate'] = pandas.to_datetime(df['EndDate'], unit='ms')

df['CreatedDate'] = df['CreatedDate'].dt.tz_localize('UTC').dt.tz_convert('Europe/Ljubljana').dt.tz_localize(None)
df['ConsultationCreatedDate'] = df['ConsultationCreatedDate'].dt.tz_localize('UTC').dt.tz_convert('Europe/Ljubljana').dt.tz_localize(None)
df['StartDate'] = df['StartDate'].dt.tz_localize('UTC').dt.tz_convert('Europe/Ljubljana').dt.tz_localize(None)
df['EndDate'] = df['EndDate'].dt.tz_localize('UTC').dt.tz_convert('Europe/Ljubljana').dt.tz_localize(None)

print(df.info())

writer = pandas.ExcelWriter('consultations.xlsx')
df.to_excel(writer)
writer.save()
