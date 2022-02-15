from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import requests
import json
from requests.structures import CaseInsensitiveDict
from django.http import HttpResponse
import ast
import csv


def analytic3(request):

    data = {}
    if 'time' in request.GET:
        time = request.GET['time']

        url = "https://pndc.lumen.live/documents/external/filter"

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        if time == 'day':

            data = """
            {
                "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54", "limit": 48}
            """
        elif time == 'day2':

            data = """
            {
                "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54", "limit": 96}
            """
        elif time == 'week':

            data = """
            {
                "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54", "limit": 336}
            """
        else:

            data = """
            {
                "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54"}
            """            


        response = requests.post(url, headers=headers, data=data)

        json_data = json.loads(response.text)
        power = []
        reactive = []
        volts = []
        losses = []
        power.append(['time', 'Power (kW)'])
        reactive.append(['time', 'Reactive Power (VAR)'])
        volts.append(['time', 'Max Voltage', 'Min Voltage'])
        losses.append(['time', 'losses (kWh)'])
        
        for i in range(len(json_data)-1, 0, -1):
            time_increment=dict(json_data[i])
            i_results=time_increment['execution-results']
            power.append([i_results['Timestamp'], i_results['feeder_power']])
            reactive.append([i_results['Timestamp'], i_results['feeder_reactive']])
            volts.append([i_results['Timestamp'], i_results['feeder_max_volt'], i_results['feeder_min_volt']])
            losses.append([i_results['Timestamp'], i_results['losses']])
        
        max_power = max(item[1] for item in power[1:])
        max_power_time = [item[0] for item in power[1:]][[item[1] for item in power[1:]].index(max_power)]
        
        max_vs = max([item[1] for item in volts[1:]])
        max_vs_time = [item[0] for item in volts[1:]][[item[1] for item in volts[1:]].index(max_vs)]

        min_vs = min([item[2] for item in volts[1:]])
        min_vs_time = [item[0] for item in volts[1:]][[item[2] for item in volts[1:]].index(min_vs)]

        data = {'array': json.dumps(power), 'reactive': json.dumps(reactive),
        'volts': json.dumps(volts), 'losses': json.dumps(losses), 'max_power': max_power,
        'max_power_time': max_power_time, 'max_vs': max_vs, 'max_vs_time': max_vs_time,
        'min_vs': min_vs, 'min_vs_time': min_vs_time}

    return render(request, 'analytics/analytic3.html', data)

def analytic3_data(request):

    time = request.GET['time']

    url = "https://pndc.lumen.live/documents/external/filter"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    if time == 'day':

        data = """
        {
            "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54", "limit": 48}
        """
    elif time == 'day2':

        data = """
        {
            "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54", "limit": 96}
        """
    elif time == 'week':

        data = """
        {
            "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54", "limit": 336}
        """
    else:

        data = """
        {
            "access_key": "ff029efa-3f81-4127-bd7c-ab2e08c15b54"}
        """            

    response = requests.post(url, headers=headers, data=data)

    json_data = json.loads(response.text)

    response_csv = HttpResponse(content_type='text/csv')
    response_csv['Content-Disposition'] = 'attachment; filename="data_' + time +'.csv"'

    writer = csv.writer(response_csv)
    writer.writerow(['Datetime', 'Power (kW)', 'Reactive Power (kVAR)', 'Max Voltage', 'Min Voltage'])

    output = []
    for i in range(len(json_data)-1, 0, -1):
            time_increment=dict(json_data[i])
            i_results=time_increment['execution-results']
            output.append([i_results['Timestamp'], i_results['feeder_power'],
            i_results['feeder_reactive'], i_results['feeder_max_volt'], i_results['feeder_min_volt']])
    
    for rows in output:
        writer.writerow(rows)

    return response_csv



def analytic1(request):

    url = "https://pndc.lumen.live/documents/external/filter"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = """
    {
        "access_key": "79d8cae7-ce20-4d49-811c-c9336d1fcae5", "limit": 1}
    """

    response = requests.post(url, headers=headers, data=data)

    json_data = json.loads(response.text)

    time_increment=dict(json_data[0])
    i_results=time_increment['execution-results']
    ds = list(ast.literal_eval(i_results['day-schedule']).values())
    da = list(ast.literal_eval(i_results['dem-actually']).values())
    df = list(ast.literal_eval(i_results['dem-forecast']).values())
    ga = list(ast.literal_eval(i_results['gen-actually']).values())
    gf = list(ast.literal_eval(i_results['gen-forecast']).values())
    ts = list(ast.literal_eval(i_results['timestamps']).values())

    d_act_forecast = []
    d_act_forecast.append(['time', 'Actual (MW)', 'Forecast (MW)'])
    daf_values = [list(x) for x in zip(ts, da, df)]
    for x in daf_values:
        d_act_forecast.append(x)

    g_act_forecast = []
    g_act_forecast.append(['time', 'Actual (MW)', 'Forecast (MW)'])
    gaf_values = [list(x) for x in zip(ts, ga, gf)]
    for x in gaf_values:
        g_act_forecast.append(x)
    
    schedule = []
    schedule.append(['time', 'Power (MW)'])
    schedule_values = [list(x) for x in zip(ts, ds)]
    for x in schedule_values:
        schedule.append(x)

    flow_zip = zip(da, ga)
    flow = []
    for da_i, ga_i in flow_zip:
        flow.append(da_i - ga_i)
    
    flow_es_zip = zip(da, ds, ga)
    flow_es = []
    for da_i, ds_i, ga_i in flow_es_zip:
        flow_es.append(da_i + ds_i - ga_i)
    
    flows_all = []
    flows_all.append(['time', 'without storage', 'with storage'])
    flow_values = [list(x) for x in zip(ts, flow, flow_es)]
    for x in flow_values:
        flows_all.append(x)


    data = {'d_act_forecast': d_act_forecast,
            'g_act_forecast': g_act_forecast,
            'schedule': schedule,
            'flows_all': flows_all
            }

    return render(request, 'analytics/analytic1.html', data)
