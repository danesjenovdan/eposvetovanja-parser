import pandas

df = pandas.read_json('out.json')

newdf = df.query('parent_id != parent_id').filter(items=['id','institution','title','start','end','expected_publication','status'])
# newdf = df.query('parent_id == parent_id').filter(items=['parent_id', 'id', 'user', 'area', 'comment', 'status', 'response']).astype({'parent_id': 'int32'}).groupby(['parent_id'])
print(newdf.head())

newdf.to_csv('summary.csv')

# for k, gr in newdf:
#     gr.to_csv(f'report-{k}.csv')
