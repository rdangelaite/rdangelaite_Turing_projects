import pandas as pd
import duckdb as db


def remove_outliers_iqr(df: pd.DataFrame, cols: list[str] | None = None, factor: float = 3.0) -> pd.DataFrame:
    """
    Removes extreme outliers based on IQR.
    Only removes values outside Q1 - factor * IQR or Q3 + factor * IQR.
    Skips columns with binary data

    Parameters:
    - df: The input DataFrame.
    - cols: List of columns to check for outliers. If None, all numeric columns are used.
    - factor: The IQR multiplier threshold (default is 3.0).

    Returns:
    - A DataFrame with outliers replaced by NaN
    """
    df_cleaned = df.copy()
    if cols is None:
        cols = df_cleaned.select_dtypes(include='number').columns

    for col in cols:
        if df[col].nunique(dropna=True) <= 2:
            continue
        else:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - factor * iqr
            upper = q3 + factor * iqr
            mask = (df_cleaned[col] < lower) | (df_cleaned[col] > upper), col
            df_cleaned.loc[mask] = np.nan

    return df_cleaned


def choosing_params(params: str) -> list:
    '''
     Helper function for model building that selects which building parameters to keep.

    Given a parameter name (e.g., 'mean', 'median', or 'mode'), it returns a list of
    features that should be dropped based on the chosen parameter.

    Args:
        params (str): The name of the parameter selection strategy ('mean', 'median',
        or 'mode').

    Returns:
        list: A list of feature names to drop.
    '''
    building_avg = [
        'APARTMENTS_AVG',
        'BASEMENTAREA_AVG',
        'YEARS_BEGINEXPLUATATION_AVG',
        'YEARS_BUILD_AVG',
        'COMMONAREA_AVG',
        'ELEVATORS_AVG',
        'ENTRANCES_AVG',
        'FLOORSMAX_AVG',
        'FLOORSMIN_AVG',
        'LANDAREA_AVG',
        'LIVINGAPARTMENTS_AVG',
        'LIVINGAREA_AVG',
        'NONLIVINGAREA_AVG',
    ]

    building_mod = [
        'APARTMENTS_MODE',
        'BASEMENTAREA_MODE',
        'YEARS_BEGINEXPLUATATION_MODE',
        'YEARS_BUILD_MODE',
        'COMMONAREA_MODE',
        'ELEVATORS_MODE',
        'ENTRANCES_MODE',
        'FLOORSMAX_MODE',
        'FLOORSMIN_MODE',
        'LANDAREA_MODE',
        'LIVINGAPARTMENTS_MODE',
        'LIVINGAREA_MODE',
        'NONLIVINGAREA_MODE',
    ]

    building_med = [
        'APARTMENTS_MEDI',
        'BASEMENTAREA_MEDI',
        'YEARS_BEGINEXPLUATATION_MEDI',
        'YEARS_BUILD_MEDI',
        'COMMONAREA_MEDI',
        'ELEVATORS_MEDI',
        'ENTRANCES_MEDI',
        'FLOORSMAX_MEDI',
        'FLOORSMIN_MEDI',
        'LANDAREA_MEDI',
        'LIVINGAPARTMENTS_MEDI',
        'LIVINGAREA_MEDI',
        'NONLIVINGAREA_MEDI',
    ]

    drop_list = []
    if params == 'mean':
        drop_list.extend(building_med)
        drop_list.extend(building_mod)
    elif params == 'median':
        drop_list.extend(building_avg)
        drop_list.extend(building_mod)
    else:
        drop_list.extend(building_avg)
        drop_list.extend(building_med)
    return drop_list


def preprocess_bureau_feat(bur: pd.DataFrame, bur_balance: pd.DataFrame) -> pd.DataFrame:
    """
    A function made for the preprocessor pipeline for bureau and bureau balance
    data.
    It needs pandas dataframe as an argument and returns the modified dataframe.
    """
    bureau = bur.copy()
    bureau_balance = bur_balance.copy()

    bureau['CREDIT_ENDDATE_MISSING_FLAG'] = bureau['DAYS_CREDIT_ENDDATE'].isnull().astype(int)
    bureau['AMT_CREDIT_MAX_OVERDUE_MISSING_FLAG'] = bureau['AMT_CREDIT_MAX_OVERDUE'].isnull().astype(int)
    bureau['HAS_ANNUITY_INFO'] = bureau['AMT_ANNUITY'].notnull().astype(int)

    def simplify_credit_type(x: str) -> str:
        """
        Helper function to simplify credit type into broader categories.
        Keeps 'Consumer credit', 'Credit card', 'Car loan', and 'Mortgage' as-is.

        Parameters: x (str): original credit type.
        Returns: str: Simplified credit type.
        """
        if x in ['Consumer credit', 'Credit card', 'Car loan', 'Mortgage']:
            return x
        else:
            return 'Other'

    def simplify_credit_active(x: str) -> str:
        """
        Helper function to simplify credit active into broader categories.
        Keeps 'Closed' and 'Active' as-is.

        Parameters: x (str): original credit type.
        Returns: str: Simplified credit category.
        """
        if x in ['Closed', 'Active']:
            return x
        else:
            return 'Other'

    bureau['CREDIT_TYPE_GROUPED'] = bureau['CREDIT_TYPE'].apply(simplify_credit_type)
    bureau['CREDIT_ACTIVE_GROUPED'] = bureau['CREDIT_ACTIVE'].apply(simplify_credit_active)
    bureau['CREDIT_CURRENCY_GROUPED'] = bureau['CREDIT_CURRENCY'].apply(
        lambda x: 'currency 1' if x == 'currency 1' else 'other currency'
    )
    bureau['WAS_CREDIT_PROLONGED'] = (bureau['CNT_CREDIT_PROLONG'] != 0).astype(int)

    bureau['CREDIT_LENGTH'] = bureau['DAYS_ENDDATE_FACT'] - bureau['DAYS_CREDIT']
    bureau['DEBT_CREDIT_RATIO'] = bureau.apply(
        lambda row: row['AMT_CREDIT_SUM_DEBT'] / row['AMT_CREDIT_SUM'] if row['AMT_CREDIT_SUM'] != 0 else np.nan, axis=1
    )
    bureau['OVERDUE_TO_DEBT_RATIO'] = bureau.apply(
        lambda row: (
            row['AMT_CREDIT_SUM_OVERDUE'] / row['AMT_CREDIT_SUM_DEBT'] if row['AMT_CREDIT_SUM_DEBT'] != 0 else np.nan
        ),
        axis=1,
    )
    bureau['HAS_OVERDUE'] = (bureau['AMT_CREDIT_SUM_OVERDUE'] > 0).astype(int)
    bureau['CREDIT_ACTIVE_FLAG'] = bureau['CREDIT_ACTIVE'].isin(['Active']).astype(int)

    bureau['OVERDUE_WITH_NO_DEBT_FLAG'] = (
        (bureau['AMT_CREDIT_SUM_DEBT'] == 0) & (bureau['AMT_CREDIT_SUM_OVERDUE'] > 0)
    ).astype(int)

    mask = bureau['CREDIT_LENGTH'] < 0
    bureau.loc[mask, 'CREDIT_LENGTH'] = np.nan

    query = """
        SELECT 
            SK_ID_BUREAU,
            AVG(MONTHS_BALANCE) MONTHS_BALANCE,
            CASE 
                WHEN COUNT_IF(STATUS IN ('0','1','2','3','4','5')) > 0 
                    THEN MAX(CASE WHEN STATUS IN ('0','1','2','3','4','5') 
                    THEN STATUS ELSE NULL END)
                WHEN COUNT_IF(STATUS = 'C') > 0 
                    THEN 'C'
                ELSE 'X'
            END AS STATUS
        FROM bureau_balance
        GROUP BY SK_ID_BUREAU;    
    """

    bb_agg = db.sql(query).df()
    query = '''
    SELECT *
    FROM bureau b
    LEFT JOIN bb_agg bb
    ON b.SK_ID_BUREAU = bb.SK_ID_BUREAU
    '''

    bureau_all = db.sql(query).df().drop(['SK_ID_BUREAU_1'], axis=1)

    aggregations = {
        'DAYS_CREDIT': ['mean'],
        'CREDIT_DAY_OVERDUE': ['mean'],
        'DAYS_CREDIT_ENDDATE': ['mean'],
        'DAYS_ENDDATE_FACT': ['min', 'mean'],
        'AMT_CREDIT_MAX_OVERDUE': ['mean'],
        'CNT_CREDIT_PROLONG': ['mean'],
        'AMT_CREDIT_SUM': ['mean'],
        'AMT_CREDIT_SUM_DEBT': ['mean'],
        'AMT_CREDIT_SUM_LIMIT': ['mean'],
        'AMT_CREDIT_SUM_OVERDUE': ['mean'],
        'DAYS_CREDIT_UPDATE': ['mean'],
        'AMT_ANNUITY': ['mean'],
        'CREDIT_ENDDATE_MISSING_FLAG': ['max'],
        'AMT_CREDIT_MAX_OVERDUE_MISSING_FLAG': ['max'],
        'HAS_ANNUITY_INFO': ['max'],
        'WAS_CREDIT_PROLONGED': ['max'],
        'CREDIT_LENGTH': ['mean', 'max'],
        'DEBT_CREDIT_RATIO': ['mean'],
        'OVERDUE_TO_DEBT_RATIO': ['mean'],
        'HAS_OVERDUE': ['max'],
        'CREDIT_ACTIVE_FLAG': ['max'],
        'OVERDUE_WITH_NO_DEBT_FLAG': ['max'],
        'MONTHS_BALANCE': ['mean'],
    }

    bureau_agg = bureau_all.groupby('SK_ID_CURR').agg(aggregations)
    bureau_agg.columns = ['BUR_' + '_'.join(col).upper() for col in bureau_agg.columns]
    bureau_agg.reset_index(inplace=True)

    query = '''
    with t1 as (
        SELECT 
            SK_ID_CURR,
            COUNT(DISTINCT SK_ID_BUREAU) AS NUM_BUREAU,
            CASE WHEN COUNT(DISTINCT SK_ID_BUREAU) > 0 THEN 1 ELSE 0 END AS HAS_BUREAU,
           
            SUM(CASE WHEN CREDIT_ACTIVE_GROUPED = 'Active' THEN 1 ELSE 0 END) AS CREDIT_ACTIVE_ACTIVE,
            SUM(CASE WHEN CREDIT_ACTIVE_GROUPED = 'Closed' THEN 1 ELSE 0 END) AS CREDIT_ACTIVE_CLOSED,
            SUM(CASE WHEN CREDIT_ACTIVE_GROUPED = 'Other' THEN 1 ELSE 0 END) AS CREDIT_ACTIVE_OTHER,
    
            SUM(CASE WHEN CREDIT_TYPE_GROUPED = 'Credit card' THEN 1 ELSE 0 END) AS CREDIT_TYPE_CREDIT_CARD,
            SUM(CASE WHEN CREDIT_TYPE_GROUPED = 'Consumer credit' THEN 1 ELSE 0 END) AS CREDIT_TYPE_CONSUMER_CREDIT,
            SUM(CASE WHEN CREDIT_TYPE_GROUPED = 'Mortgage' THEN 1 ELSE 0 END) AS CREDIT_TYPE_MORTGAGE,
            SUM(CASE WHEN CREDIT_TYPE_GROUPED = 'Car loan' THEN 1 ELSE 0 END) AS CREDIT_TYPE_CAR_LOAN,
            SUM(CASE WHEN CREDIT_TYPE_GROUPED = 'Other' THEN 1 ELSE 0 END) AS CREDIT_TYPE_OTHER,
            
            COUNT(DISTINCT CREDIT_CURRENCY) AS NUM_DISTINCT_CURRENCIES,
            SUM(CASE WHEN CREDIT_CURRENCY = 'currency 2' THEN 1 ELSE 0 END) AS NUM_CURRENCY_2,
            SUM(CASE WHEN CREDIT_CURRENCY = 'currency 3' THEN 1 ELSE 0 END) AS NUM_CURRENCY_3,
            SUM(CASE WHEN CREDIT_CURRENCY_GROUPED = 'other currency' THEN 1 ELSE 0 END) AS NUM_CURRENCY_OTHER,
            CASE 
                WHEN COUNT_IF(STATUS IN ('0','1','2','3','4','5')) > 0 
                    THEN MAX(CASE WHEN STATUS IN ('0','1','2','3','4','5') 
                    THEN STATUS ELSE NULL END)
                WHEN COUNT_IF(STATUS = 'C') > 0 
                    THEN 'C'
                ELSE 'X'
            END AS STATUS,
            CASE 
                WHEN COUNT(*) FILTER (WHERE STATUS IN ('1','2','3','4','5')) > 0 
                    THEN 1
                ELSE 0
            END AS STATUS_FLAG
        FROM bureau_all
        GROUP BY SK_ID_CURR
        )
        
    SELECT *
    FROM bureau_agg b
    LEFT JOIN t1
    ON b.SK_ID_CURR = t1.SK_ID_CURR
    '''

    bureau_agg = db.sql(query).df().drop(['SK_ID_CURR_1'], axis=1)

    x_num = bureau_agg.select_dtypes(exclude='object').reset_index(drop=True)
    x_cat = bureau_agg.select_dtypes(include='object')

    encoder = OneHotEncoder(sparse_output=False)
    x_encoded = encoder.fit_transform(x_cat)

    # create the names for the one-hot encoded categorical features
    categorical_columns = [f'{col}_{cat}' for i, col in enumerate(x_cat.columns) for cat in encoder.categories_[i]]

    # put the features into a dataframe and join with the original
    # numerical features

    one_hot_features = pd.DataFrame(x_encoded, columns=categorical_columns)

    # Dropping missing and some of rare categories
    one_hot_features = one_hot_features.drop(
        [
            'STATUS_X',
            'STATUS_3',
            'STATUS_4',
            'STATUS_C',
        ],
        axis=1,
    )

    bureau_agg = x_num.join(one_hot_features)

    mask = bureau_agg['BUR_AMT_CREDIT_MAX_OVERDUE_MEAN'] < 2e7
    realistic_median = bureau_agg.loc[mask, 'BUR_AMT_CREDIT_MAX_OVERDUE_MEAN'].median()

    # Replace suspiciously value with the realistic median
    mask = bureau_agg['BUR_AMT_CREDIT_MAX_OVERDUE_MEAN'] > 2e7
    bureau_agg.loc[mask, 'BUR_AMT_CREDIT_MAX_OVERDUE_MEAN'] = realistic_median
    bureau_agg['BUR_AMT_CREDIT_MAX_OVERDUE_MEAN'] = bureau_agg['BUR_AMT_CREDIT_MAX_OVERDUE_MEAN'].fillna(0)

    mask = bureau_agg['BUR_AMT_CREDIT_SUM_MEAN'] < 5e7
    realistic_median = bureau_agg.loc[mask, 'BUR_AMT_CREDIT_SUM_MEAN'].median()

    # Replace suspiciously value with the realistic median
    mask = bureau_agg['BUR_AMT_CREDIT_SUM_MEAN'] > 5e7
    bureau_agg.loc[mask, 'BUR_AMT_CREDIT_SUM_MEAN'] = realistic_median

    return bureau_agg


def preprocess_credit_card_balance(cc_balance: pd.DataFrame) -> pd.DataFrame:
    '''
    A function made for the preprocessor pipeline for credit card balance data.
    It needs pandas dataframe as an argument and returns the modified dataframe.
    '''
    credit_card_balance = cc_balance.copy()
    credit_card_balance['HAD_DPD'] = credit_card_balance['SK_DPD'].apply(lambda x: 1 if x > 0 else 0)
    credit_card_balance['HAD_DPD_DEF'] = credit_card_balance['SK_DPD_DEF'].apply(lambda x: 1 if x > 0 else 0)

    aggregations = {
        'MONTHS_BALANCE': ['mean'],
        'AMT_BALANCE': ['mean'],
        'AMT_DRAWINGS_ATM_CURRENT': ['mean'],
        'AMT_DRAWINGS_CURRENT': ['mean'],
        'AMT_DRAWINGS_POS_CURRENT': ['mean'],
        'AMT_PAYMENT_CURRENT': ['mean'],
        'AMT_PAYMENT_TOTAL_CURRENT': ['mean'],
        'CNT_DRAWINGS_ATM_CURRENT': ['mean'],
        'CNT_DRAWINGS_CURRENT': ['mean'],
        'CNT_DRAWINGS_POS_CURRENT': ['mean'],
        'CNT_INSTALMENT_MATURE_CUM': ['mean'],
        'SK_DPD_DEF': ['mean'],
        'HAD_DPD': ['max'],
        'HAD_DPD_DEF': ['max'],
    }

    cc_bal_agg = credit_card_balance.groupby('SK_ID_CURR').agg(aggregations)
    cc_bal_agg.columns = ['CC_' + '_'.join(col).upper() for col in cc_bal_agg.columns]
    cc_bal_agg.reset_index(inplace=True)

    query = """
    with t1 as (
        SELECT 
            SK_ID_CURR,
            COUNT(DISTINCT SK_ID_PREV) AS NUM_CREDIT_CARD,
        FROM credit_card_balance
        GROUP BY SK_ID_CURR
        ), 
    
        t2 as (
        SELECT 
        SK_ID_CURR,
        COUNT(DISTINCT CASE WHEN has_completed = 1 THEN SK_ID_PREV ELSE NULL END) AS CC_COMPLETED
        FROM (
            SELECT 
                SK_ID_CURR,
                SK_ID_PREV,
                MAX(CASE WHEN NAME_CONTRACT_STATUS = 'Active' THEN 1 ELSE 0 END) AS has_active,
                MAX(CASE WHEN NAME_CONTRACT_STATUS = 'Completed' THEN 1 ELSE 0 END) AS has_completed,
            FROM credit_card_balance
            GROUP BY SK_ID_CURR, SK_ID_PREV
        ) AS loan_flags
        GROUP BY SK_ID_CURR
        )
    
    SELECT *
    FROM cc_bal_agg cc
    JOIN t1
    ON cc.SK_ID_CURR = t1.SK_ID_CURR
    LEFT JOIN t2
    ON cc.SK_ID_CURR = t2.SK_ID_CURR;
    """

    cc_bal_agg = db.sql(query).df().drop(['SK_ID_CURR_1', 'SK_ID_CURR_2'], axis=1)
    return cc_bal_agg


def preprocess_installments_payments(inst_payments: pd.DataFrame) -> pd.DataFrame:
    '''
    A function made for the preprocessor pipeline for installment payments data.
    It needs pandas dataframe as an argument and returns the modified dataframe.
    '''

    installments_payments = inst_payments.copy()
    installments_payments['DAYS_INST_PAY_DIFF'] = (
        installments_payments['DAYS_INSTALMENT'] - installments_payments['DAYS_ENTRY_PAYMENT']
    )
    installments_payments['AMT_INST_PAY_DIFF'] = (
        installments_payments['AMT_INSTALMENT'] - installments_payments['AMT_PAYMENT']
    )
    installments_payments['AMT_INST_PAY_RATIO'] = installments_payments.apply(
        lambda row: row['AMT_INSTALMENT'] / row['AMT_PAYMENT'] if row['AMT_PAYMENT'] != 0 else np.nan, axis=1
    )
    installments_payments['AMT_INST_PAY_RATIO'] = installments_payments['AMT_INST_PAY_RATIO'].clip(upper=10)

    aggregations = {
        'NUM_INSTALMENT_VERSION': ['mean'],
        'NUM_INSTALMENT_NUMBER': ['max', 'mean'],
        'DAYS_ENTRY_PAYMENT': ['mean'],
        'DAYS_INST_PAY_DIFF': ['mean', 'min'],
        'AMT_PAYMENT': ['mean'],
        'AMT_INST_PAY_DIFF': ['mean', 'max'],
        'AMT_INST_PAY_RATIO': ['mean'],
    }

    inst_pay_agg = installments_payments.groupby('SK_ID_CURR').agg(aggregations)
    inst_pay_agg.columns = ['IP_' + '_'.join(col).upper() for col in inst_pay_agg.columns]
    inst_pay_agg.reset_index(inplace=True)

    query = '''
    with t1 as (
        SELECT 
            SK_ID_CURR,
            COUNT(DISTINCT SK_ID_PREV) AS NUM_INSTALMENT_PAYMENTS,
            CASE WHEN COUNT(DISTINCT SK_ID_PREV) > 0 THEN 1 ELSE 0 END AS HAD_INSTALMENT_PAYMENTS
        FROM installments_payments
        GROUP BY SK_ID_CURR
        ) 
    
    SELECT *
    FROM inst_pay_agg ip
    JOIN t1
    ON ip.SK_ID_CURR = t1.SK_ID_CURR;
    '''

    inst_pay_agg = db.sql(query).df().drop(['SK_ID_CURR_1'], axis=1)
    return inst_pay_agg


def preprocess_pos_cash(p_cash: pd.DataFrame) -> pd.DataFrame:
    '''
    A function made for the preprocessor pipeline for POS cash data.
    It needs pandas dataframe as an argument and returns the modified dataframe.
    '''
    pos_cash = p_cash.copy()
    pos_cash['HAD_DPD'] = pos_cash['SK_DPD'].apply(lambda x: 1 if x > 0 else 0)
    pos_cash['HAD_DPD_DEF'] = pos_cash['SK_DPD_DEF'].apply(lambda x: 1 if x > 0 else 0)

    aggregations = {
        'MONTHS_BALANCE': ['min', 'mean'],
        'CNT_INSTALMENT': ['mean', 'max'],
        'CNT_INSTALMENT_FUTURE': ['mean', 'sum'],
        'SK_DPD': ['mean'],
        'SK_DPD_DEF': ['mean'],
        'HAD_DPD': ['max'],
        'HAD_DPD_DEF': ['max'],
    }

    pos_agg = pos_cash.groupby('SK_ID_CURR').agg(aggregations)
    pos_agg.columns = ['POS_' + '_'.join(col).upper() for col in pos_agg.columns]
    pos_agg.reset_index(inplace=True)

    query = """
    with t1 as (
        SELECT 
            SK_ID_CURR,
            CASE WHEN COUNT(DISTINCT SK_ID_PREV) > 0 THEN 1 ELSE 0 END AS HAS_PREVIOUS_POS
        FROM pos_cash
        GROUP BY SK_ID_CURR
        ), 
    
        t2 as (
        SELECT 
        SK_ID_CURR,
        COUNT(DISTINCT CASE WHEN has_active = 1 THEN SK_ID_PREV ELSE NULL END) AS POS_ACTIVE_LOANS
        FROM (
            SELECT 
                SK_ID_CURR,
                SK_ID_PREV,
                MAX(CASE WHEN NAME_CONTRACT_STATUS = 'Active' THEN 1 ELSE 0 END) AS has_active,
            FROM pos_cash
            GROUP BY SK_ID_CURR, SK_ID_PREV
        ) AS loan_flags
        GROUP BY SK_ID_CURR
        )
    
    SELECT *
    FROM pos_agg pa
    JOIN t1
    ON pa.SK_ID_CURR = t1.SK_ID_CURR
    LEFT JOIN t2
    ON pa.SK_ID_CURR = t2.SK_ID_CURR;
    """

    pos_agg = db.sql(query).df().drop(['SK_ID_CURR_1', 'SK_ID_CURR_2'], axis=1)
    return pos_agg


def preprocess_previous_application(p_application: pd.DataFrame) -> pd.DataFrame:
    '''
    A function made for the preprocessor pipeline for previous application data.
    It needs pandas dataframe as an argument and returns the modified dataframe.
    '''

    previous_application = p_application.copy()
    previous_application['NAME_TYPE_SUITE'] = previous_application['NAME_TYPE_SUITE'].fillna('Unknown')
    previous_application['FLAG_LAST_APPL_PER_CONTRACT'] = previous_application['FLAG_LAST_APPL_PER_CONTRACT'].map(
        {'Y': 1, 'N': 0}
    )

    previous_application['DAYS_FIRST_DRAWING'] = previous_application['DAYS_FIRST_DRAWING'].replace(365243, np.nan)
    previous_application['DAYS_FIRST_DUE'] = previous_application['DAYS_FIRST_DUE'].replace(365243, np.nan)
    previous_application['DAYS_LAST_DUE_1ST_VERSION'] = previous_application['DAYS_LAST_DUE_1ST_VERSION'].replace(
        365243, np.nan
    )
    previous_application['DAYS_LAST_DUE'] = previous_application['DAYS_LAST_DUE'].replace(365243, np.nan)
    previous_application['DAYS_TERMINATION'] = previous_application['DAYS_TERMINATION'].replace(365243, np.nan)

    aggregations = {
        'AMT_ANNUITY': ['mean'],
        'AMT_APPLICATION': ['mean', 'max'],
        'AMT_CREDIT': ['mean'],
        'AMT_DOWN_PAYMENT': ['min', 'mean'],
        'AMT_GOODS_PRICE': ['mean'],
        'HOUR_APPR_PROCESS_START': ['mean'],
        'RATE_DOWN_PAYMENT': ['mean'],
        'RATE_INTEREST_PRIVILEGED': ['mean'],
        'DAYS_DECISION': ['mean'],
        'SELLERPLACE_AREA': ['mean'],
        'DAYS_FIRST_DRAWING': ['mean'],
        'DAYS_FIRST_DUE': ['mean'],
        'DAYS_TERMINATION': ['mean'],
        'FLAG_LAST_APPL_PER_CONTRACT': ['min'],
        'NFLAG_LAST_APPL_IN_DAY': ['min'],
        'NFLAG_INSURED_ON_APPROVAL': ['mean', 'max'],
    }

    prev_app_agg = previous_application.groupby('SK_ID_CURR').agg(aggregations)
    prev_app_agg.columns = ['PREV_' + '_'.join(col).upper() for col in prev_app_agg.columns]
    prev_app_agg.reset_index(inplace=True)

    query = """
    with t1 as (
        SELECT 
            SK_ID_CURR,
            COUNT(DISTINCT SK_ID_PREV) AS NUM_PREV_APPLICATIONS,
            CASE WHEN COUNT(DISTINCT SK_ID_PREV) > 0 THEN 1 ELSE 0 END AS HAS_PREV_APPLICATION,
            SUM(CASE WHEN NAME_CONTRACT_TYPE = 'Cash loans' THEN 1 ELSE 0 END) AS CASH_LOAN,
            SUM(CASE WHEN NAME_CONTRACT_TYPE = 'Consumer loans' THEN 1 ELSE 0 END) AS CONSUMER_LOAN,
            SUM(CASE WHEN NAME_CONTRACT_TYPE = 'Revolving loans' THEN 1 ELSE 0 END) AS REVOLVING_LOAN,
            SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) AS CONTRACT_APPROVED,
            SUM(CASE WHEN NAME_PAYMENT_TYPE = 'Cash through the bank' THEN 1 ELSE 0 END) AS PAY_TYPE_BANK,
            SUM(CASE WHEN NAME_PORTFOLIO = 'POS' THEN 1 ELSE 0 END) AS PORTFOLIO_POS,
            SUM(CASE WHEN NAME_PORTFOLIO = 'Cash' THEN 1 ELSE 0 END) AS PORTFOLIO_CASH,
            SUM(CASE WHEN NAME_PORTFOLIO = 'Cards' THEN 1 ELSE 0 END) AS PORTFOLIO_CARDS,
            SUM(CASE WHEN NAME_PORTFOLIO = 'Cars' THEN 1 ELSE 0 END) AS PORTFOLIO_CARS,
            SUM(CASE WHEN NAME_PRODUCT_TYPE = 'x-sell' THEN 1 ELSE 0 END) AS PRODUCT_XSELL,
            SUM(CASE WHEN NAME_PRODUCT_TYPE = 'walk-in' THEN 1 ELSE 0 END) AS PRODUCT_WALKIN,
            SUM(CASE WHEN NAME_YIELD_GROUP = 'low_action' THEN 1 ELSE 0 END) AS YIELD_LOW_ACTION,
            SUM(CASE WHEN NAME_YIELD_GROUP = 'low_normal' THEN 1 ELSE 0 END) AS YIELD_LOW_NORMAL,
            SUM(CASE WHEN NAME_YIELD_GROUP = 'middle' THEN 1 ELSE 0 END) AS YIELD_MIDDLE,
            SUM(CASE WHEN NAME_YIELD_GROUP = 'high' THEN 1 ELSE 0 END) AS YIELD_HIGH,
            SUM(CASE WHEN NAME_CASH_LOAN_PURPOSE NOT IN ('XAP', 'XNA') THEN 1 ELSE 0 END) AS CASH_LOAN_PURPOSE_OTHER,
            SUM(CASE WHEN CODE_REJECT_REASON = 'XAP' THEN 1 ELSE 0 END) AS CODE_REJECT_REASON_XAP,
            SUM(CASE WHEN CODE_REJECT_REASON NOT IN ('XAP', 'XNA') THEN 1 ELSE 0 END) AS CODE_REJECT_REASON_OTHER,
            SUM(CASE WHEN NAME_TYPE_SUITE = 'Unknown' THEN 1 ELSE 0 END) AS TYPE_SUITE_UNKNOWN,
            SUM(CASE WHEN NAME_TYPE_SUITE = 'Family' THEN 1 ELSE 0 END) AS TYPE_SUITE_FAMILY,
            SUM(CASE WHEN NAME_TYPE_SUITE NOT IN ('Unknown', 'Unaccompanied', 'Family') THEN 1 ELSE 0 END) AS TYPE_SUITE_OTHER,
            SUM(CASE WHEN NAME_GOODS_CATEGORY = 'Mobile' THEN 1 ELSE 0 END) AS GOODS_CATEGORY_MOBILE,
            SUM(CASE WHEN NAME_GOODS_CATEGORY = 'Consumer Electronics' THEN 1 ELSE 0 END) AS GOODS_CATEGORY_ELECTRONICS,
            SUM(CASE WHEN NAME_GOODS_CATEGORY = 'Computers' THEN 1 ELSE 0 END) AS GOODS_CATEGORY_COMPUTERS,
            SUM(CASE WHEN NAME_GOODS_CATEGORY = 'Audio/Video' THEN 1 ELSE 0 END) AS GOODS_CATEGORY_AUDIOVID,
            SUM(CASE WHEN NAME_GOODS_CATEGORY = 'Furniture' THEN 1 ELSE 0 END) AS GOODS_CATEGORY_FURNITURE,
            SUM(CASE WHEN NAME_GOODS_CATEGORY NOT IN ('Mobile', 'Consumer Electronics', 'Computers',
            'Audio/Video', 'Furniture', 'XNA') THEN 1 ELSE 0 END) AS GOODS_CATEGORY_OTHER,
            SUM(CASE WHEN CHANNEL_TYPE = 'Credit and cash offices' THEN 1 ELSE 0 END) AS CHANNEL_OFFICES,
            SUM(CASE WHEN CHANNEL_TYPE = 'Stone' THEN 1 ELSE 0 END) AS CHANNEL_STONE,
            SUM(CASE WHEN CHANNEL_TYPE = 'Regional / Local' THEN 1 ELSE 0 END) AS CHANNEL_REGLOCAL,
            SUM(CASE WHEN CHANNEL_TYPE NOT IN ('Credit and cash offices', 'Country-wide', 'Stone',
            'Regional / Local') THEN 1 ELSE 0 END) AS CHANNEL_OTHER,
            SUM(CASE WHEN NAME_SELLER_INDUSTRY = 'Consumer electronics' THEN 1 ELSE 0 END) AS SELLER_INDUSTRY_ELECTRONICS,
            SUM(CASE WHEN NAME_SELLER_INDUSTRY = 'Connectivity' THEN 1 ELSE 0 END) AS SELLER_INDUSTRY_CONNECTIVITY,
            SUM(CASE WHEN NAME_SELLER_INDUSTRY NOT IN ('Consumer electronics', 'Connectivity', 'XNA') THEN 1 ELSE 0 END) AS SELLER_INDUSTRY_OTHER,
            SUM(CASE WHEN PRODUCT_COMBINATION = 'Cash' THEN 1 ELSE 0 END) AS PRODUCT_COMBO_CASH,
            SUM(CASE WHEN PRODUCT_COMBINATION IN ('POS household with interest', 'POS mobile with interest', 
            'POS other with interest', 'POS industry with interest') THEN 1 ELSE 0 END) AS PRODUCT_COMBO_POS_WITH_INTEREST,
            SUM(CASE WHEN PRODUCT_COMBINATION IN ('POS household without interest', 'POS mobile without interest', 
            'POS industry without interest', 'POS others without interest') THEN 1 ELSE 0 END) AS PRODUCT_COMBO_POS_WITHOUT_INTEREST,
            SUM(CASE WHEN PRODUCT_COMBINATION IN ('Cash X-Sell: low', 'Cash X-Sell: high',  
            'Cash X-Sell: middle', 'Card X-Sell') THEN 1 ELSE 0 END) AS PRODUCT_COMBO_XSELL,
            SUM(CASE WHEN PRODUCT_COMBINATION IN ('Cash Street: high', 'Card Street', 
            'Cash Street: low', 'Cash Street: middle') THEN 1 ELSE 0 END) AS PRODUCT_COMBO_CASHSTREET
        FROM previous_application
        GROUP BY SK_ID_CURR
        )
    
    SELECT *
    FROM prev_app_agg pa
    JOIN t1
    ON pa.SK_ID_CURR = t1.SK_ID_CURR;
    """

    prev_app_agg = db.sql(query).df().drop(['SK_ID_CURR_1'], axis=1)
    return prev_app_agg
