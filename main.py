import streamlit as st
# importing pandas for file handling.
import pandas as pd
from io import BytesIO


st.set_page_config(page_title="📂 File Convertor & Cleaner", layout="wide")

st.title("📂 File Convertor & Cleaner")
st.write("### This is a simple web application that can convert and clean CSV files.")
st.write("You can upload a CSV file or excel file, select the conversion type and the application will do your work to make you feel ease.")


files =st.file_uploader("Upload CSV or EXCEL File", type=["csv", "xlsx"], accept_multiple_files= True)

if files:
    # jo file upload hogi usko process krega.
    for file in files:
        # file ko read krega or split krega.
        # -1 last element ke hisaab se procss krega.
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if  ext == "csv" else pd.read_excel(file)

        st.subheader=(f"🪕 {file.name} - Preview")
        st.dataframe(df.head())

        # ye condition missing values ko fill krega average value dega.
        if st.checkbox(f"Fill Missing Values- {file.name}"):
            df.fillna(df.select_dtypes(include = "number").mean(), inplace=True)
            st.success("Missing values filled successfully")
            st.dataframe(df.head())
            # ye condition duplicate values ko remove krega.
        selected_coloums= st.multiselect(f"select coloums - {file.name}", df.columns, default=df.columns)   
        df =df[selected_coloums]
        st.dataframe(df.head())

        # user checkboc ko tick krega toh chart dikhega 
        # and number columns ko check krega
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            chart_df = df.select_dtypes(include="number").iloc[:, :2]
            chart_df = chart_df.apply(pd.to_numeric, errors="coerce").dropna()

            if not chart_df.empty:
                st.bar_chart(chart_df)
            else:
                st.warning("No valid numeric data available to display chart.")             
            # if st.checkbox(f" Show chart - {file.name}"):

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel" ], key=file.name)
        
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            output.seek(0)
            st.download_button("⬇ Download File", file_name=new_name, data=output, mime=mime) 
        
        st.success("Successfully Completed!")       