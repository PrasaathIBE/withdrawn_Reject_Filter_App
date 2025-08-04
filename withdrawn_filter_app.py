
# import streamlit as st
# import pandas as pd
# from io import BytesIO

# st.title("Withdrawn/Rejected Reference Filter")

# uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# if uploaded_file:
#     # Read Excel file
#     xls = pd.ExcelFile(uploaded_file)
#     data_df = xls.parse('data')

#     # Normalize Live_Order_Status
#     data_df['Live_Order_Status_cleaned'] = data_df['Live_Order_Status'].astype(str).str.strip().str.lower()

#     # Keywords
#     excluded_keywords = [
#         'under review (reviewer assigned by eic)',
#         'under review (reviewer assigned by our team)',
#         'wo full paper submitted',
#         'revised paper uploaded',
#         'revision received by author',
#         'submitted',
#         'paper sent back to author',
#         'po paper submitted',
#         'published',
#         'revised paper started preparing',
#         'acceptance received by author',
#         'comments started posting'
#     ]
#     included_keywords = ['withdrawn', 'rejected', 'client need to withdraw']

#     excluded_set = set(excluded_keywords)
#     included_set = set(included_keywords)

#     grouped = data_df.groupby('Reference_No')
#     valid_refs = []

#     for ref_no, group in grouped:
#         statuses = set(group['Live_Order_Status_cleaned'].dropna())
#         if any(ek in status for ek in excluded_set for status in statuses):
#             continue
#         if any(ik in status for ik in included_set for status in statuses):
#             valid_refs.append(ref_no)

#     filtered_df = data_df[data_df['Reference_No'].isin(valid_refs)][['Client_ID', 'Reference_No', 'Live_Order_Status']]

#     st.success(f"Found {len(filtered_df)} matching rows.")
#     st.dataframe(filtered_df)

#     # Download
#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         filtered_df.to_excel(writer, index=False)
#     st.download_button("Download Result as Excel", data=output.getvalue(), file_name="filtered_output.xlsx")


import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Withdrawn/Rejected Reference Filter")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel file
    xls = pd.ExcelFile(uploaded_file)
    data_df = xls.parse('data')

    # Normalize Live_Order_Status
    data_df['Live_Order_Status_cleaned'] = data_df['Live_Order_Status'].astype(str).str.strip().str.lower()

    # Excluded statuses (normal flow)
    excluded_keywords = [
        'under review (reviewer assigned by eic)',
        'under review (reviewer assigned by our team)',
        'wo full paper submitted',
        'revised paper uploaded',
        'revision received by author',
        'submitted',
        'paper sent back to author',
        'po paper submitted',
        'published',
        'revised paper started preparing',
        'acceptance received by author',
        'comments started posting',
        'comments prepared and shared',
        'comments started preparing',
        'e-acceptance given by our team',
        'e-paper sent back to author',
        'e-acceptance received by author',
        'e-comments prepared and shared',
        'e-comments requested',
        'e-comments started posting',
        'e-comments started posting- revised version',
        'e-copyright form received',
        'e-po paper submitted',
        'e-proofread received',
        'e-required reviews completed',
        'e-revised paper started preparing',
        'e-revised paper uploaded',
        'e-revision given by our team',
        'e-revision received by author',
        'e-submitted',
        'e-under review - revised version (reviewer assigned by our team)',
        'e-under review (reviewer assigned by eic)',
        'e-under review (reviewer assigned by our team)',
        'erevision received by author',
        'client need to withdraw',
        'proofread received',
        'copyright form received',
        'acceptance given by our team',
        'required reviews completed',
        'under review - revised version (reviewer assigned by eic)'
    ]

    # Included (withdrawn/rejected only)
    included_keywords = ['withdrawn', 'rejected']

    excluded_set = set(excluded_keywords)
    included_set = set(included_keywords)

    grouped = data_df.groupby('Reference_No')
    valid_refs = []

    for ref_no, group in grouped:
        statuses = set(group['Live_Order_Status_cleaned'].dropna())
        if any(ek in status for ek in excluded_set for status in statuses):
            continue
        if any(ik in status for ik in included_set for status in statuses):
            valid_refs.append(ref_no)

    filtered_df = data_df[data_df['Reference_No'].isin(valid_refs)][['Client_ID', 'Reference_No', 'Live_Order_Status']]

    st.success(f"Found {len(filtered_df)} matching rows.")
    st.dataframe(filtered_df)

    # Download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        filtered_df.to_excel(writer, index=False)
    st.download_button("Download Result as Excel", data=output.getvalue(), file_name="filtered_output.xlsx")
