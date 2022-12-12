from basketball_reference_scraper.shot_charts import get_shot_chart
from basketball_reference_scraper.seasons import get_schedule, get_standings
import pandas as pd

stat = get_shot_chart('2020-01-13', 'CHI', 'BOS')
# print(stat)
dps=[]
for x in stat:
    print(x)
    dps.append(stat[x])

# print(dps[0])
# print(dps[1])
relevant_data1=dps[1].loc[:,['QUARTER','TIME_REMAINING','PLAYER','MAKE_MISS','VALUE']].loc[dps[1].PLAYER=='Jayson Tatum']
# print(relevant_data1)
years_Bryant_active = [i for i in range(1996,2017)]
schedule=get_schedule(2018, playoffs=False)
LALschedule=schedule.loc[(schedule.VISITOR=='Los Angeles Lakers') | (schedule.HOME=='Los Angeles Lakers')]
print(LALschedule['Date'])
