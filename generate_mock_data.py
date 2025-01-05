import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def generate_pnl_data(num_records=50):
    data = []

    price_bands = ['Peak', 'Off Peak', 'Hourly']
    cash_flow_types = ['None', 'Physical Settlement', 'Cash Settlement']
    currencies = ['JPY', 'USD']
    settlement_types = ['Physical Settlement', 'Cash Settlement']
    tran_status = ['Validated', 'Known', 'Fixed']
    rate_status = ['Known', 'Fixed']
    strategies = ["EastCoal1", "EastCoal2", "WestGas1", "NorthPower"]
    new_deal_flags = ['Existing Deal', 'New Deal']

    for i in range(num_records):
        deal_num = random.randint(24000,26000)
        tran_num = random.randint(24000,26000)
        param_seq_num = random.randint(0,4)
        param_seq_num_1 = random.randint(0,4)
        profile_seq_num = 0
        ins_seq_num = 0
        instrument_source_id = random.randint(0,2)
        price_band = random.choice(price_bands)
        commodity_option_exercised_flag = random.choice(['Yes','No'])
        cash_flow_type = random.choice(cash_flow_types)
        start_date = fake.date_between(start_date='-6m', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+6m')
        payment_date = fake.date_between(start_date=end_date, end_date='+3m')
        rate_dtmn_date = fake.date_between(start_date=start_date, end_date=end_date)
        currency = random.choice(currencies)
        settlement_type = random.choice(settlement_types)
        volume = round(random.uniform(-10000,100000),2)
        price = round(random.uniform(10,200),2)
        strike = 0
        pymt = round(volume * price,2)
        total_value = round(volume * price * random.uniform(0.9,1.1),2)
        realized_value = round(total_value * random.uniform(0,0.5),2)
        unrealized_value = round(total_value-realized_value,2)
        base_total_value = round(volume * price * random.uniform(0.8,1.2),2)
        base_realized_value = round(base_total_value * random.uniform(0,0.7),2)
        base_unrealized_value = round(base_total_value - base_realized_value,2)
        df = 1
        tran_status = random.choice(tran_status)
        rate_status = random.choice(rate_status)
        strategy = random.choice(strategies)
        previous_pymt = round(pymt * random.uniform(0.8,1.2),2)
        previous_total_value = round(total_value* random.uniform(0.8,1.2),2)
        previous_realized_value = round(realized_value* random.uniform(0,1),2)
        previous_unrealized_value = round(unrealized_value* random.uniform(0,1),2)
        previous_base_total_value = round(base_total_value* random.uniform(0.8,1.2),2)
        previous_base_realized_value = round(base_realized_value* random.uniform(0,1),2)
        previous_base_unrealized_value = round(base_unrealized_value* random.uniform(0,1),2)
        change_in_total_value = round(total_value-previous_total_value,2)
        previous_tran_status = random.choice(tran_status)
        new_deal = random.choice(new_deal_flags)
        event_source = 'Profile'
        param_id = random.randint(0,5)
        param_id_1 = random.randint(0,5)
        previous_volume = round(volume * random.uniform(0.8,1.2),2)
        previous_price = round(price * random.uniform(0.8,1.2),2)


        data.append({
            'Deal Num': deal_num,
            'Tran Num': tran_num,
            'Param Seq Num':param_seq_num,
            'Param Seq Num_1':param_seq_num_1,
            'Profile Seq Num': profile_seq_num,
            'Ins Seq Num': ins_seq_num,
            'Instrument Source ID': instrument_source_id,
            'Price Band': price_band,
            'Commodity Option Exercised Flag':commodity_option_exercised_flag,
            'Cash Flow Type': cash_flow_type,
            'Start Date': start_date,
            'End Date': end_date,
            'Payment Date': payment_date,
            'Rate Dtmn Date': rate_dtmn_date,
            'Currency': currency,
            'Settlement Type': settlement_type,
            'Volume': volume,
            'Price': price,
            'Strike': strike,
            'Pymt': pymt,
            'Total Value': total_value,
            'Realized Value': realized_value,
            'Unrealized Value': unrealized_value,
            'Base Total Value': base_total_value,
            'Base Realized Value': base_realized_value,
            'Base Unrealized Value': base_unrealized_value,
            'Df': df,
            'Tran Status': tran_status,
            'Rate Status': rate_status,
            'Strategy': strategy,
            'Previous Pymt': previous_pymt,
            'Previous Total Value': previous_total_value,
            'Previous Realized Value': previous_realized_value,
            'Previous Unrealized Value': previous_unrealized_value,
            'Previous Base Total Value': previous_base_total_value,
            'Previous Base Realized Value': previous_base_realized_value,
            'Previous Base Unrealized Value': previous_base_unrealized_value,
            'Change in Total Value': change_in_total_value,
            'Previous Tran Status': previous_tran_status,
            'New Deal': new_deal,
            'Event Source': event_source,
            'Param ID': param_id,
            'Param ID_1': param_id_1,
            'Previous Volume': previous_volume,
            'Previous Price': previous_price
        })
    return pd.DataFrame(data)

if __name__ == '__main__':
    df = generate_pnl_data(1000)
    print(df.head())
    df.to_csv('mock_pnl_data.csv', index=False)
    print("Mock data generated and saved to mock_pnl_data.csv")
