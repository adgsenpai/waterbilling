import pdfplumber

# find all .pdfs in data folder
import os
import streamlit as st
import pandas as pd
import plotly.express as px
def find_pdfs(path):
    pdfs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".PDF"):
                pdfs.append(os.path.join(root, file))
                
    return pdfs

datafiles = find_pdfs("./data")

def parse_pdf(pdf_file):
    data = {}
    finaldata = {}

    with pdfplumber.open(pdf_file) as pdf:
        pages = pdf.pages
        for i,pg in enumerate(pages):
            data[i] = pg.extract_text()
            for line in data[i].splitlines():                
                if "Account summary" in line:                
                    finaldata["Date"] = line.split()[4]                          
                    break     
                if "WATER" in line:  
                    finaldata["Consumption"] = float(line.split()[7].replace("kl",""))
                    break 
    return finaldata
 

graphdata = []

for file in datafiles:
    graphdata.append(parse_pdf(file))

df = pd.DataFrame(graphdata)
df.to_csv("./data/data.csv")

st.title("Water Consumption @ 10 Oleander Street")

st.subheader("Water Dataset")
st.write(df)

st.subheader("Line Graph of Water Consumption @ 10 Oleander Street")

fig = px.line(df, x="Date", y="Consumption", title="Water Consumption @ 10 Oleander Street")
# change y axis title
fig.update_yaxes(title="Water Consumption (kl)")
st.plotly_chart(fig)