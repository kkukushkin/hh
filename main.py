# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
skills = pd.read_csv('/Users/kuzma/PycharmProjects/dash/skills.csv', sep = ';')
id_descr = pd.read_csv('/Users/kuzma/PycharmProjects/dash/id_descr.csv', sep = ';')

def define_professions():
    s = id_descr.spec_name
    counts = s.value_counts()
    counts1 = counts.reset_index()
    return counts1


def define_skills():
    s = skills.skill
    counts = s.value_counts()
    percent = s.value_counts(normalize=True)
    percent100 = s.value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    abc2 = pd.DataFrame({'counts': counts})
    abc2.reset_index()
    abc2['proc'] = round(abc2.counts / 4948 * 100, 2)
    new1 = abc2['proc'].loc[lambda x : x>5].reset_index()
    new1.sort_values(['proc'], ascending = True)
    return new1

def aerospace_skills():
    new = skills.loc[skills.spec_name == 'Авиационная промышленность']
    s = new.skill
    counts = s.value_counts()
    percent = s.value_counts(normalize=True)
    percent100 = s.value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    abc2 = pd.DataFrame({'counts': counts})
    abc2.reset_index()
    abc2['proc'] = round(abc2.counts / 295 * 100, 2)
    new1 = abc2['proc'].loc[lambda x : x>4].reset_index()
    new1.sort_values(['proc'], ascending = True)
    return new1

def count_salary_by_skills():
    skills[["salary_from", "salary_to"]] = skills[["salary_from", "salary_to"]].apply(pd.to_numeric)
    counts = skills['skill'].value_counts().reset_index(name="times")
    counts.drop(counts.index[[0]]).reset_index(drop = True)
    counts = counts.rename(columns={'index': 'skill'})
    skills1 = skills.merge(counts, on='skill', how='outer')
    skills1.drop(skills1.index[[0]]).reset_index(drop = True)
    new = skills1.loc[skills1.times > 250]
#    new1 = new.loc[skills1.spec_name == column_chosen]
    filtered_tab = new.dropna(how='all', subset=['salary_from', 'salary_to'])
    filtered_tab['salary_to'].fillna(filtered_tab['salary_from']) #, inplace = True)
    skills2 = filtered_tab.groupby('skill').aggregate({'salary_from' : 'mean', 'salary_to' : 'mean'})
    skills2['total'] = (skills2.salary_from + skills2.salary_to)/2
    skills2.drop('salary_to', axis=1, inplace=True)
    skills2.drop('salary_from', axis=1, inplace=True)
    skills2.sort_values(['total'], ascending = False, inplace = True)
    skills3 = skills2['total'].round(decimals=0).reset_index()
    return skills3

def count_salary_by_skills_aerospace():
    skills[["salary_from", "salary_to"]] = skills[["salary_from", "salary_to"]].apply(pd.to_numeric)
    counts = skills['skill'].value_counts().reset_index(name="times")
    counts.drop(counts.index[[0]]).reset_index(drop = True)
    counts = counts.rename(columns={'index': 'skill'})
    skills1 = skills.merge(counts, on='skill', how='outer')
    skills1.drop(skills1.index[[0]]).reset_index(drop = True)
    new = skills1.loc[skills1.times > 170]
    new1 = new.loc[new.spec_name == 'Авиационная промышленность']
    filtered_tab = new1.dropna(how='all', subset=['salary_from', 'salary_to'])
    filtered_tab['salary_to'].fillna(filtered_tab['salary_from']) #, inplace = True)
    skills2 = filtered_tab.groupby('skill').aggregate({'salary_from' : 'mean', 'salary_to' : 'mean'})
    skills2['total'] = (skills2.salary_from + skills2.salary_to)/2
    skills2.drop('salary_to', axis=1, inplace=True)
    skills2.drop('salary_from', axis=1, inplace=True)
    skills2.sort_values(['total'], ascending = False, inplace = True)
    skills2.dropna(subset=['total'], inplace=True)
    skills3 = skills2['total'].round(decimals=0).reset_index()
    return skills3




new = define_skills()
#new.reset_index()
skills_all = count_salary_by_skills()
profs = define_professions()
aer = aerospace_skills()
aerpay = count_salary_by_skills_aerospace()

#skills_all['total'].round(decimals = 0).reset_index()
#skills1 = skills_all.reset_index()

fig0 = px.bar(profs.sort_values(['spec_name']), x="spec_name", y="index", labels={"spec_name": "ед.", "index": "Профессии"}, color="spec_name", title='Выборка по запросу "инженер" на hh.ru, ед., 4948 вакансий')
fig0.update_traces(textfont_size=20, texttemplate='%{x:d3-format} ед.', textposition="outside", cliponaxis=False)
fig0.update_xaxes(categoryorder='category ascending')
fig0.update_layout(yaxis = dict(tickfont = dict(size=10)),
    font_family="Arial",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


fig = px.bar(new.sort_values(['proc']), x="proc", y="index", labels={"proc": "%", "index": "Навыки"}, color="proc", title='Наиболее востребованные навыки по запросу "инженер" на hh.ru, %, 4948 вакансий')
fig.update_traces(textfont_size=20, texttemplate='%{x:d3-format}%', textposition="outside", cliponaxis=False)
fig.update_xaxes(categoryorder='category ascending')
fig.update_layout(yaxis = dict(tickfont = dict(size=10)),
    font_family="Arial",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig3 = px.bar(aer.sort_values(['proc']), x="proc", y="index", labels={"proc": "%", "index": "Навыки"}, color="proc", title='Наиболее востребованные навыки по запросу "инженер-авиастроитель" на hh.ru, %, 295 вакансий')
fig3.update_traces(textfont_size=20, texttemplate='%{x:d3-format}%', textposition="outside", cliponaxis=False)
fig3.update_xaxes(categoryorder='category ascending')
fig3.update_layout(yaxis = dict(tickfont = dict(size=10)),
    font_family="Arial",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


fig2 = px.bar(skills_all.sort_values(['total']).reset_index(), x="total", y="skill", labels={"total": "руб.", "skill": "Навыки"}, color="total", title='Наиболее высокооплачиваемые навыки по запросу "инженер" на hh.ru, руб., 4948 вакансий')
fig2.update_traces(textfont_size=20, texttemplate='%{x:2f} руб.', textposition="outside", cliponaxis=False)
fig2.update_xaxes(categoryorder='category ascending')
fig2.update_layout(yaxis = dict(tickfont = dict(size=10)),
    font_family="Arial",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig1 = px.bar(aerpay.sort_values(['total']).reset_index(), x="total", y="skill", labels={"total": "руб.", "skill": "Навыки"}, color="total", title='Наиболее высокооплачиваемые навыки по запросу "инженер-авиастроитель" на hh.ru, руб., 295 вакансий')
fig1.update_traces(textfont_size=20, texttemplate='%{x:2f} руб.', textposition="outside", cliponaxis=False)
fig1.update_xaxes(categoryorder='category ascending')
fig1.update_layout(yaxis = dict(tickfont = dict(size=10)),
    font_family="Arial",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div(children=[
    html.H1(children='Дэшборд по инженерным вакансиям hh.ru. Центр НТИ СПбПУ©. 2022.', style={'text-align':'center', 'color': 'black', 'font-family': 'Arial', 'fontSize': 18}),
    dcc.Graph(
        id='График выборка',
        figure=fig0
    ),
    dcc.Graph(
        id='График востребованности навыков',
        figure=fig
    ),
    dcc.Graph(
        id='График навыков, востребованных в авиастроении',
        figure=fig3
    ),
    dcc.Graph(
        id='График оплаты навыков',
        figure=fig2
    ),
    dcc.Graph(
        id='График оплаты навыков инженеры-авиаторы',
        figure=fig1
    ),
    html.Div(children='''Дэшборд подготовлен специалистами Отдела технологического и промышленного форсайта СПбПУ.''', style={'text-align':'center', 'color': 'black', 'font-family': 'Arial', 'fontSize': 12})
])


if __name__ == '__main__':
    app.run_server(debug=True)