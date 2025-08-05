import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Withdrawn/Rejected Reference Filter")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    data_df = xls.parse('data')

    # Normalize statuses
    data_df['Live_Order_Status_cleaned'] = data_df['Live_Order_Status'].astype(str).str.strip().str.lower()

    # Excluded statuses
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
        'proofread received',
        'copyright form received',
        'acceptance given by our team',
        'required reviews completed',
        'under review - revised version (reviewer assigned by eic)'
    ]

    included_keywords = ['withdrawn', 'rejected', 'client need to withdraw']
    excluded_set = set(excluded_keywords)
    included_set = set(included_keywords)

    grouped = data_df.groupby('Reference_No')
    withdrawn_or_rejected_refs = []
    client_withdraw_refs = []

    for ref_no, group in grouped:
        statuses = set(group['Live_Order_Status_cleaned'].dropna())

        has_excluded = any(ek in status for ek in excluded_set for status in statuses)
        has_withdrawn_or_rejected = any(
            ('withdrawn' in status and 'client need to withdraw' not in status) or 'rejected' in status
            for status in statuses
        )
        has_client_withdraw = any('client need to withdraw' in status for status in statuses)

        if not has_excluded:
            if has_withdrawn_or_rejected:
                withdrawn_or_rejected_refs.append(ref_no)
            elif has_client_withdraw:
                client_withdraw_refs.append(ref_no)

    # Filter dataframes
    withdrawn_df = data_df[data_df['Reference_No'].isin(withdrawn_or_rejected_refs)][['Client_ID', 'Reference_No', 'Live_Order_Status']]
    client_withdraw_df = data_df[data_df['Reference_No'].isin(client_withdraw_refs)][['Client_ID', 'Reference_No', 'Live_Order_Status']]

    # Show in tabs
    tab1, tab2 = st.tabs(["Withdrawn / Rejected", "Client Need to Withdraw"])

    with tab1:
        st.success(f"Found {len(withdrawn_df)} withdrawn/rejected records.")
        st.dataframe(withdrawn_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            withdrawn_df.to_excel(writer, index=False)
        st.download_button("Download Withdrawn/Rejected", data=output.getvalue(), file_name="withdrawn_rejected.xlsx")

    with tab2:
        st.info(f"Found {len(client_withdraw_df)} 'Client Need to Withdraw' records.")
        st.dataframe(client_withdraw_df)

        output2 = BytesIO()
        with pd.ExcelWriter(output2, engine='xlsxwriter') as writer:
            client_withdraw_df.to_excel(writer, index=False)
        st.download_button("Download Client Need to Withdraw", data=output2.getvalue(), file_name="client_need_to_withdraw.xlsx")
