import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json

usecols = ['序號', '年', '月', '日', '時', '區', '天候', '死亡數量' , '受傷數量', '飲酒情形', '肇事因素個別', '肇事因素主要', '事故類型及型態', '事故類別', 'GPS座標X', 'GPS座標Y']
df = pd.read_csv('rawdata/11207.csv', usecols=usecols)
df['date'] = df['日'].map('2023-07-{:02d}'.format)

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/api/statics/accident_type', methods=['GET'])
def accident_type():
    res = df.groupby('事故類型及型態')['序號'].count().reset_index(name='count').rename(columns={'事故類型及型態':'type'})

    response_object = {'data': json.loads(res.reset_index().to_json(orient='records', force_ascii=False))}
    return jsonify(response_object)

@app.route('/api/statics/district_accident', methods=['GET'])
def district_accident():
    res = df.groupby('區')['序號'].count().reset_index(name='count').rename(columns={'區':'district'})

    response_object = {'data': json.loads(res.reset_index().to_json(orient='records', force_ascii=False))}
    return jsonify(response_object)

@app.route('/api/statics/rush_hour', methods=['GET'])
def rush_hour():
    res = df.groupby('時')['序號'].count().reset_index(name='count').rename(columns={'時':'hour'})

    response_object = {'data': json.loads(res.reset_index().to_json(orient='records', force_ascii=False))}
    return jsonify(response_object)

@app.route('/api/accident/geo', methods=['GET'])
def geo():
    # area_filter = df['區']=='西屯區'
    # res = df[area_filter][['GPS座標X', 'GPS座標Y']].rename(columns = {'GPS座標X':'x', 'GPS座標Y':'y'})
    res = df[['GPS座標X', 'GPS座標Y']].rename(columns = {'GPS座標X':'x', 'GPS座標Y':'y'})

    response_object = {'data': json.loads(res.reset_index().to_json(orient='records', force_ascii=False))}
    return jsonify(response_object)

@app.route('/api/accident/weather', methods=['GET'])
def weather():
    area_filter = df['區']=='西屯區'
    res = df.groupby('天候').apply(func=lambda df_gr: pd.Series({
    ('事故總數'): len(df_gr),
    ('發生天數'): len(df_gr.groupby('日')),
    ('每日事故平均數'): len(df_gr)/len(df_gr.groupby('日')),
    ('每日事故中位數'): df_gr.groupby('日')['序號'].count().reset_index(name='count')['count'].median(),
    ('單日最大事故數'): df_gr.groupby('日')['序號'].count().reset_index(name='count').sort_values('count', ascending=False).iloc[0]['count'],
    ('最多事故日'): df_gr.groupby('日')['序號'].count().reset_index(name='count').sort_values('count', ascending=False).iloc[0]['日'],
    })).rename(columns = {'事故總數':'amount', '發生天數':'badDays', '每日事故平均數': 'avg', '每日事故中位數': 'median', '單日最大事故數': 'max', '最多事故日': 'badDay'})

    response_object = {'data': json.loads(res.reset_index().to_json(orient='records', force_ascii=False))}
    return jsonify(response_object)

@app.route('/api/accident/daybyday', methods=['GET'])
def daybyday():
    area_filter = df['區']=='西屯區'
    res = df.groupby(['區', 'date'])['序號'].count().reset_index(name='count').rename(columns = {'區':'district'})

    response_object = {'data': json.loads(res.reset_index().to_json(orient='records', force_ascii=False))}
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()
