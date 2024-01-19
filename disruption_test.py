# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:05:31 2024

@author: lzein
"""

#import necessary programs
import pandas as pd

#load csv file
df = pd.read_csv("C:/Users\lzein\Downloads\disruptions-2022.csv")

#view information
#print(df.head(5))
#df.info()

#clean dataset
dfclean = df.drop((['rdt_id',
           'rdt_lines',
           'rdt_lines_id', 
           'rdt_station_names',
           'rdt_station_codes',
           'cause_en',
           'statistical_cause_nl',
           'statistical_cause_en',
           'start_time',
           'end_time']),axis=1)


#dfclean.info()
#print(dfclean.head(5))


#reorganize dataframe
dfclean3 = dfclean.groupby(['ns_lines', 'cause_nl']).agg({'cause_nl':'count', 'duration_minutes':'sum'})
dfclean4 = dfclean.groupby(['cause_nl']).agg({'cause_nl':'count', 'duration_minutes':'sum'})
dfclean5 = dfclean.groupby(['cause_nl']).agg({'cause_nl':'count', 'duration_minutes':'mean'})
dfclean6 = dfclean.groupby(['ns_lines']).agg({'cause_nl':'count', 'duration_minutes':'sum'})


#filter dataframe
filtered_df = dfclean6[(dfclean6['duration_minutes']<40000) & (dfclean6['duration_minutes']>10) & (dfclean6['cause_nl']>3) ]
uitschieters = dfclean3[(dfclean3['duration_minutes']>39000) & (dfclean3['duration_minutes']>10)]

#rename cause_nl to disruption_amount
filtered_df_renamed = filtered_df.rename(columns={'cause_nl': 'disruption_amount'})
dfclean4_renamed = dfclean4.rename(columns={'cause_nl': 'disruption_amount'})

#add ascending
filter_df_minutes = filtered_df.sort_values(by='duration_minutes', ascending=False)
filter_df_cause = filtered_df_renamed.sort_values(by='disruption_amount', ascending=False)
filter_minutespercause_sum = dfclean4.sort_values(by='duration_minutes', ascending=False)
filter_minutespercause_mean = dfclean5.sort_values(by='duration_minutes', ascending=False)
filter_cause = dfclean4_renamed.sort_values(by='disruption_amount', ascending=False)

#filter to top 15 of values
filter_cause_15 = filter_df_cause[(filter_df_cause['disruption_amount']>59)]
filter_minutes_15 = filter_df_minutes[(filter_df_minutes['duration_minutes']>9040)]
filter_minutesum_15 = filter_minutespercause_sum[(filter_minutespercause_sum["duration_minutes"]>12500)]
filter_minutemean_15 = filter_minutespercause_mean[(filter_minutespercause_mean["duration_minutes"]>550)]
filter_causeamount_15 = filter_cause[(filter_cause["disruption_amount"]>69)]

#df check date zandvoort grandprix
zandvoort_filter = df[(df['cause_nl']=='aangepaste dienstregeling')]

#bar plot disruption amount and duration 
filter_cause_15.plot.bar(y='disruption_amount', color= {'pink'}, xlabel='Lijn namen', ylabel='Aantal disrupties')
filter_minutes_15.plot.bar(y='duration_minutes', color= {'green'}, xlabel='Lijn namen', ylabel='Totale vertraging in minuten')
filter_minutesum_15.plot.bar(y='duration_minutes', color= {'orange'}, xlabel='type disruptie', ylabel='totaal aantal minuten')
filter_minutemean_15.plot.bar(y='duration_minutes', color={'purple'}, xlabel='type disruptie', ylabel='gemiddeld aantal minuten')
filter_causeamount_15.plot.bar(y='disruption_amount', xlabel='type disruptie', ylabel='hoeveelheid')

#filter venlo dusseldorf
venlo_dusseldorf_filter = dfclean[(dfclean['ns_lines']=='Venlo-Mönchengladbach-Düsseldorf')]

#filter beperkingen materieel inzet
materieelinzet_filter = dfclean[(dfclean['cause_nl']=='beperkingen in de materieelinzet')]

#filter corona effect
personeel_corona_filter = df[(df['cause_nl']=='Minder personeel bij NS als gevolg van corona')]

#bar plot uitschieters 
uitschieters.plot.bar(y='duration_minutes', ylabel='Totaal aantal minuten', xlabel='traject', color='red')

#filter hengelo bielefied
hengelobielefeld_filter = df[(df['ns_lines']=='Hengelo-Bielefeld')]