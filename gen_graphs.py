import pandas as pd
import glob 
import os
import plotly.graph_objects as go



list_of_files = glob.glob('./data/*') 
# latest_file = max(list_of_files, key=os.path.getctime)
latest_file = sorted(list_of_files, key=os.path.getctime ,reverse=True)[0]
print (latest_file)

data=pd.read_csv(latest_file)


data_columns=["id",'snippet.publishedAt','snippet.title','snippet.channelTitle','contentDetails.duration',\
'statistics.viewCount','statistics.likeCount','statistics.dislikeCount','statistics.favoriteCount',\
'statistics.commentCount',"snippet.channelId","snippet.categoryId",'country_origin', 'topicDetails.relevantTopicIds',\
'topicDetails.topicCategories', 'snippet.defaultLanguage','snippet.defaultAudioLanguage','localizations.ta.title','localizations.ml.title']


videoCat_df=pd.read_json("./info/videoCategories.json")

videoCat_df["id"]=videoCat_df["items"].apply(lambda x: x["id"])
videoCat_df["title"]=videoCat_df["items"].apply(lambda x: x["snippet"]["title"])
cate_maper=videoCat_df[["id","title"]].set_index("id").to_dict()["title"]

data_df_rd=data[data_columns]

data_df_rd["category"]=data_df_rd["snippet.categoryId"].apply(str).map(cate_maper)

nvideo_by_country_ncat = data_df_rd.groupby(["country_origin","category"],as_index=False)["statistics.viewCount"].count()
nvideo_pivot = nvideo_by_country_ncat.pivot(index='country_origin', columns='category', values='statistics.viewCount')
nvideo_pivot = nvideo_pivot.fillna(0)
nvideo_pivot = nvideo_pivot.loc[['BR', 'DE', 'GB', 'IN', 'US']]


views_by_country_ncat = data_df_rd.groupby(["country_origin","category"],as_index=False)["statistics.viewCount"].sum()
views_pivot = views_by_country_ncat.pivot(index='country_origin', columns='category', values='statistics.viewCount')
views_pivot = views_pivot.fillna(0)
views_pivot = views_pivot.loc[['BR', 'DE', 'GB', 'IN', 'US']]


def stacked_plot(pivot_data):
    categories = pivot_data.index.values.tolist()
    bar_list=[]
    for column_name in views_pivot.columns:
        bar_list.append(go.Bar(name=column_name,x=categories,y=pivot_data[column_name].values.tolist(),orientation='v'))
    fig = go.Figure(data=bar_list)
    fig.update_layout(barmode='stack',plot_bgcolor='black',paper_bgcolor='black',font=dict(size = 13, color = 'white'))
    return fig

stacked_plot(views_pivot).update_layout(title_text='Daily Views In Trending Videos').write_html("./charts/Views.html",include_plotlyjs="cdn")
stacked_plot(nvideo_pivot).update_layout(title_text='Video Category Of Trending Videos').write_html("./charts/Count.html",include_plotlyjs="cdn")