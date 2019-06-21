# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:55:17 2019

@author: guye0
"""

import pandas as pd
pd.set_option('display.max_columns',15)
pd.set_option('display.width',120)
Stud = pd.read_csv('students_complete.csv',sep=',')
Sch = pd.read_csv('schools_complete.csv',sep=',')
Stud_df = pd.DataFrame(Stud)
Sch_df = pd.DataFrame(Sch)

#District Summary --Create a high level snapshot of the district's key metrics'
#Is there any missing data anywhere in the dataframe?
Stud_df.isnull().values.any()  #code from my Assessment model script works here
#False so we proceed accordingly with a pre-cleaned dataset. Thanks for clean data
List = Stud_df.groupby(["school_name"]).count()
#Stud_df["reading_score"].mean()
Stud_df.loc[:,"grade"].replace("th","",regex=True,inplace=True)  #Phew this to ensure grades are properly sorted for later
Stud_df["grade"] = pd.to_numeric(Stud_df["grade"])
MathPass = (Stud_df.iloc[:,6] >= 70)*1
ReadPass = (Stud_df.iloc[:,5] >= 70)*1
Stud_df["% Passing Math"] = MathPass
Stud_df["% Passing Reading"] = ReadPass
PassMath = sum(MathPass) / len(Stud_df) #create logical vector of 1=pass,0=fail, sum it, divide by total
PassMPer = ("{:.2%}".format(PassMath))
PassRead = sum(ReadPass) / len(Stud_df) #create logical vector of 1=pass,0=fail, sum it, divide by total
PassRPer = ("{:.2%}".format(PassRead))
PassOv = ("{:.2%}".format((PassMath+PassRead)/2))

print("Results reported assume a pass criterion of 70% or higher")
print("Summary of the District Schools:")
print("-------------------------------------------------------------")
print(f"Total Schools: {len(List)}")
print(f"Total Students: {sum(List['grade'])}")
print(f"Total Budget: {sum(Sch_df['budget'])}")
print(f"Average Math Score: {Stud_df['math_score'].mean():.2f}")
print(f"Average Reading Score: {Stud_df['reading_score'].mean():.2f}")
print(f"% Passing Math: {PassMPer}")
print(f"% Passing Reading: {PassRPer}")
print(f"Overall Passing Rate: {PassOv}")
print("-------------------------------------------------------------")

#Next for the School Summary, fun stuff

Anchor = Stud_df.groupby(["school_name"]).mean()
Anchor = Anchor.drop(columns=["Student ID","grade"])
Anchor = pd.DataFrame(Anchor)
Merge_df = pd.merge(Anchor,Sch_df,on="school_name")
Merge_df[["% Passing Math","% Passing Reading"]] = Merge_df[["% Passing Math","% Passing Reading"]].round(4) *100
Merge_df["Overall Passing Rate"] = Merge_df.iloc[:,3:5].mean(axis=1)
Merge_df["Per Student Budget"] = round(Merge_df["budget"]/Merge_df["size"],2)
Fin_df = Merge_df.rename(columns={"school_name":"School Name","reading_score":"Avg Reading Score","math_score":
                                  "Avg Math Score","type":"School Type","size":"Total Students","budget":"Total Budget"})
#apologies for this messiness but I love ILOC!!!!
Fin_df = Fin_df.iloc[:,[0,6,7,8,10,2,1,3,4,9]]
print(Fin_df)

#Sorting then reporting top 5
Place_df = Fin_df.sort_values(by=["Overall Passing Rate"],ascending=False)
Place_df = pd.DataFrame(Place_df)
TopFin_df = Place_df.head(5)
print(TopFin_df)

#Bottom Five Schools
BotFin_df = Place_df.tail(5)
print(BotFin_df)

#Math Scores by Grade
MBG_df = Stud_df.groupby(["school_name","grade"])[["math_score"]].mean()
print(round(MBG_df,2))

RBG_df = Stud_df.groupby(["school_name","grade"])[["reading_score"]].mean()
print(round(RBG_df,2))

#Cutting the dataframe into intervals: 575-599, 600 to 629, 630 to 649, 650+
Fin_df["Spending Ranges"] = pd.cut(Fin_df["Per Student Budget"],[575,599,629,649,674],labels=
       ["Below $600","$600-$629","$630-$649","At Least $650"])
#scores by school spending
BySpend_df = Fin_df.groupby(["Spending Ranges"])[["Avg Math Score","Avg Reading Score",
                       "% Passing Math","% Passing Reading","Overall Passing Rate"]]
print(round(BySpend_df.mean(),2))

#Cutting the data into 3 groups by School Size
Fin_df["Size Ranges"] = pd.cut(Fin_df["Total Students"],[0,1499,2999,5000],labels=
       ["Small","Medium","Large"])

BySize_df = Fin_df.groupby(["Size Ranges"])[["Avg Math Score","Avg Reading Score",
                       "% Passing Math","% Passing Reading","Overall Passing Rate"]]
print(round(BySize_df.mean(),2))

#Breaking the data down by School Type... Then DONE!!! 10:19 AM Friday 6/21. Slacking this week :)
BySize_df = Fin_df.groupby(["School Type"])[["Avg Math Score","Avg Reading Score",
                       "% Passing Math","% Passing Reading","Overall Passing Rate"]]
print(round(BySize_df.mean(),2))