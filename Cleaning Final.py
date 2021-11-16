#!/usr/bin/env python
# coding: utf-8

# In[251]:


import pandas as pd


# In[252]:


df = pd.read_csv(r"C:\Users\Ahmed Abouslima\Desktop\dpschool2a (2).csv", delimiter=";")


# In[253]:


df = df[['title', 'short_description', 'description', 'latitude', 'longitude', 'address', 'addr_no', 
         'zip_code', 'city', 'country', 'additional_fields', 'image', 'icons', 'modified']]


# In[254]:


import json
df["additional_fields"] = df["additional_fields"].map(lambda x: json.loads(x))
df["image"] = df["image"].map(lambda x: json.loads(x))


# In[255]:


df = df[df['latitude'].notna()]


# In[256]:


from pandas import isnull
df["icons"] = df["icons"].map(lambda x: {} if isnull(x) else x)
df["icons"] = df["icons"].map(lambda x: x if isinstance(x, str) else str(x))
df["icons"] = df["icons"].map(lambda x: json.loads(x))


# In[257]:


df["modified"] = pd.to_datetime(df["modified"], errors="coerce")


# In[258]:


df['longitude'] = df['longitude'].map(lambda x: x.replace('.', "")[:6]).astype(float) / 10000
df['latitude'] = df['latitude'].map(lambda x: x.replace('.', "")[:6]).astype(float) / 10000


# In[259]:


df["description"] = df["description"].map(lambda x: "" if isnull(x) else x)
df["short_description"] = df["short_description"].map(lambda x: "" if isnull(x) else x)
df["addr_no"] = df["addr_no"].map(lambda x: "" if isnull(x) else x)


# In[260]:


df["address"] = df["address"] + " " + df["addr_no"]


# In[261]:


df.drop(["addr_no"], axis=1, inplace=True)


# In[262]:


df["geometry"] = None
for i in df.index:
    df.at[i, 'geometry'] = (df.loc[i]['latitude'], df.loc[i]['longitude'])


# In[263]:


icons = {"Toilette für Alle": 10, "Rolli WC": 11, "Rolli WC -DIN fern": 20, "WC eng": 17, "kein Rolli WC vorhanden": 21,
        "Parken": 7, "Stufe": 1, "WC - unisex": 4, "WC getrennt": 6, "Rollstuhl": 5, "Lift groß": 12, "Lift klein": 13,
        "Kino-Untertitel": 15, "Induktionsschleife": 14, "low-vision": 18, "kognitiv beeinträchtigt": 19, "Umkleide": 9,
        "Dusche": 8, "nicht rollstuhlgerecht": 16, "Rampe": 2, "keine Steigung - eben": 26, "moderate Steigung / Gefälle": 22,
        "weitere moderate Steigungen / Gefälle": 23, "heftige Steigung / Gefälle": 25, "weitere heftige Steigung / Gefälle": 24}
new_dict = {v: k for k, v in icons.items()}
new_dict.update({40: "Euro Key", 41: "Ramp Incline", 42: "Door Width"})


# In[264]:


df["icons"] = df["icons"].map(lambda x: list(map(int, list(x.values()))))


# In[265]:


df[40] = df["additional_fields"].map(lambda x: x["wc_euro"] if "wc_euro" in x.keys() else "0")
df[40] = df[40].map(lambda x: int(x) if x in ["1", "0"] else 0)


# In[266]:


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

df[41] = df["additional_fields"].map(lambda x: x["wc_ramp_incline"])
df[41] = df[41].map(lambda x: x.replace(",","."))
df[41] = df[41].map(lambda x: float(x) if isfloat(x) else 0)
#need to check further as some have extra text


# In[267]:


df[42] = df["additional_fields"].map(lambda x: x["wc_door_width"])
df[42] = df[42].map(lambda x: int(x) if x != "" else 150)


# In[270]:


x = pd.get_dummies(df.icons.apply(pd.Series).stack()).sum(level=0)
x = x.rename(int, axis="columns")
col = list(x.columns)
for i in [40, 41, 42]:
    col.append(i)


# In[271]:


df.drop(["icons"], axis=1, inplace=True)
df = pd.concat([df, x], axis=1)


# In[272]:


def check(series):
    x = {}
    for i in series.index:
        if i in col:
            x.update({i: series[i]})
        else:
            continue
    return x


# In[273]:


df["options"] = df.apply(lambda x: check(x), axis=1)


# In[280]:


df.drop(col, axis=1, inplace=True)


# In[294]:


columns = pd.DataFrame.from_dict(new_dict, orient="index", columns=["option_name"])
columns.index.name = "id"


# In[295]:


columns.to_csv("options.csv")


# In[291]:


df.to_json("toilets_v3.json")

