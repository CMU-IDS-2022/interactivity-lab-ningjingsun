import streamlit as st
import pandas as pd
import altair as alt
#Terminal: streamlit run demo.py

st.header("My First Streamlit App")

def load(url):
    return pd.read_json(url)

df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

if st.checkbox("Show Raw Data"):
    st.write(df)

scatter = alt.Chart(df).mark_point().encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
)
#without filters:
#st.write(scatter)



st.write("1. with filters:")
min_weight = st.slider("Minimum Body Mass", 2500, 6500)
st.write(min_weight)

scatter_filtered = scatter.transform_filter(f"datum['Body Mass (g)'] >= {min_weight}")
st.write(scatter_filtered)



st.write("2. let users pick datapoints:")
#picked = alt.selection_single(on="mouseover", empty="none")
#picked = alt.selection_multi()
#picked = alt.selection_interval()
#picked = alt.selection_interval(encodings=["x"])
picked = alt.selection_single(on="mouseover", fields=["Species", "Island"])
scatter = alt.Chart(df).mark_circle(size=100).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    color = alt.condition(picked, "Species", alt.value("lightgray"))
).add_selection(picked)
st.write(scatter)



st.write("3. binding:")
input_dropdown = alt.binding_select(options=["Adelie", "Chinstrap", "Gentoo"], name="Species of")
picked = alt.selection_single(encodings=["color"], bind=input_dropdown)
scatter = alt.Chart(df).mark_circle(size=100).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    color = alt.condition(picked, "Species", alt.value("lightgray"))
).add_selection(picked)
st.write(scatter)



st.write("4. zoom & pan:")
scatter = alt.Chart(df).mark_circle(size=100).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
).interactive()
st.write(scatter)



st.write("5. link multiple interactions together:")
brush = alt.selection_interval(encodings=["x"])

scatter = alt.Chart(df).mark_circle(size=100).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
).add_selection(brush)

hist = alt.Chart(df).mark_bar().encode(
    alt.X("Body Mass (g)", bin=True),
    alt.Y("count()"),
    alt.Color("Species")
).transform_filter(brush)

st.write(scatter & hist)