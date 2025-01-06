# Example 1 : Two dataframes with reconciliation column key containing Matched/Mismatched elements, with reports
import pandas as pd

source_a = pd.DataFrame({
    'Transaction_ID': ['TXN001', 'TXN002', 'TXN003', 'TXN004'],
    'Account_Number': [12345, 12346, 12347, 12348],
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
    'Amount': [500.00, 1500.00, 750.00, 300.00]
})

source_b = pd.DataFrame({
    'Transaction_ID': ['TXN005', 'TXN006', 'TXN007', 'TXN008'],
    'Account_Number': [12345, 12346, 12349, 12347],
    'Date': ['2023-01-01', '2023-01-02', '2023-01-05', '2023-01-03'],
    'Amount': [500.00, 1500.00, 100.00, 700.00]
})

display(source_a)
display(source_b)

# Mismatches
# Solution A
reconciled = pd.merge(source_a, source_b, on='Account_Number', how='outer', suffixes=('_SourceA', '_SourceB'), indicator=True)

mismatches = reconciled[reconciled['_merge'] != 'both']
display(mismatches)
# Solution B
pd.concat([source_a,source_b],axis=0).drop_duplicates(subset='Account_Number',keep=False)
# Solution C
import numpy as np
diff = np.setxor1d(np.array(source_a.Account_Number), np.array(source_b.Account_Number))
pd.concat([source_a.loc[source_a['Account_Number'].isin(list(diff)),:],source_b.loc[source_b['Account_Number'].isin(list(diff)),:]])
# Matches
value_discrepancies = reconciled[
    (reconciled['_merge'] == 'both') & 
    (reconciled['Amount_SourceA'] != reconciled['Amount_SourceB'])
]
display(value_discrepancies)

# Reconciliation report
print(f"Total Transactions in Source A: {len(source_a)}")
print(f"Total Transactions in Source B: {len(source_b)}")
print(f"Mismatched Transactions: {len(mismatches)}")
print(f"Value Discrepancies: {len(value_discrepancies)}")

# Example 2 : Combine two DataFrame objects by filling null values in one DataFrame with non-null values from other DataFrame
import pandas as pd

source_a = pd.DataFrame({
    'Transaction_ID': ['TXN001', 'TXN002', 'TXN003', 'TXN004'],
    'Account_Number': [12345, 12346, 12347, 12348],
    'Date': [np.nan, '2023-01-02', '2023-01-03', '2023-01-04'],
    'Amount': [500.00, 1500.00, np.nan, 300.00]
})

source_b = pd.DataFrame({
    'Transaction_ID': ['TXN005', 'TXN006', 'TXN007', 'TXN008'],
    'Account_Number': [12345, 12346, 12349, 12347],
    'Date': ['2023-01-01', '2023-01-02', np.nan, '2023-01-03'],
    'Amount': [500.00, np.nan, 100.00, 300.00]
})

display(source_a)
display(source_b)
source_a.combine_first(source_b)
