# dev or deploy

ENVIRONMENT_ = 'deploy'

if ENVIRONMENT_ == 'dev':
    DATABASE_URL = 'postgresql+psycopg2://@5432/tigerballdb'
    database_ = 'tigerballdb'
elif ENVIRONMENT_ == 'deploy':
    DATABASE_URL = 'postgresql://fjoacapxjmfqdq:6bc7c2106fefb7d79382461eaa98fe8cab9b686892fd9022c20abcfd88ace07c@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d5olnm6egr5314'
    database_ = 'd5olnm6egr5314'


# normal or whatever username you want
USERNAME_ = 'lisa'