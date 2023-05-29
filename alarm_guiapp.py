#
import PySimpleGUI as sg
import datetime
from pygame import mixer

plan_list = [['e.g.', 'hh:mm']]
headings = ['予定', '時間']
widths = [30, 8]

mixer.init()

# デザインテーマ設定
sg.theme('DarkBlue')

# ウィンドウレイアウト
l_time = [[sg.Text('JST', size = (6, 1)), sg.Text('00月00日 00:00:00', key = '-jstclock-')],
          [sg.Text('UTC', size = (6, 1)), sg.Text('00月00日 00:00:00', key = '-utcclock-')],
          [sg.Text('EST', size = (6, 1)), sg.Text('00月00日 00:00:00', key = '-estclock-')]]
l_plan = [[sg.Text('予定'), sg.InputText(key = '-plan-')],
          [sg.Text('時間'), sg.InputText(key = '-planT-')],
          [sg.Button('追加', key = '-add-'), sg.Button('削除', key = '-del-')],
          [sg.Table(plan_list, headings, key = '-act-', auto_size_columns = False, col_widths = widths)]]
l_sound = [[sg.Input(key = '-sound-'),sg.FileBrowse('select a sound file', key = '-inputFilePath-'), sg.Button('再生', key = '-play-')]]

layout = [
    [sg.Frame('予定', l_plan), sg.Frame('現在時刻', l_time)],
    [sg.Frame('音声を設定してください', l_sound)]
]

# ウィンドウ作成
win = sg.Window('時報', layout, resizable=True)

# イベントループ
while True:
    event, values = win.read(timeout=100)
    
    # 予定を追加
    if event == '-add-':
        if values['-plan-'] and values['-planT-']:
            plan = values['-plan-']
            planT = values['-planT-']
            plan_list.append([plan, planT])
            win['-act-'].update(values = plan_list)
        else:
            sg.popup('入力してください')
    # 予定を削除
    elif event == '-del-':
        if values['-plan-'] and values['-planT-']:
            plan = values['-plan-']
            planT = values['-planT-']
            plan_list.remove([plan, planT])
            win['-act-'].update(values = plan_list)
        else:
            sg.popup('入力してください')
    elif event == sg.WIN_CLOSED:
        break

    # 時報
    nowtime = datetime.datetime.now().strftime('%H:%M')

    for i in range(len(plan_list)):
        for l in plan_list[i][1]:
            if nowtime == plan_list[i][1]:
                if values['-sound-']:
                    sound = values['-sound-']
                    mixer.music.load(sound)
                    mixer.music.play(1)
                    sg.popup(plan_list[i][0] + 'の時間です')
                    del plan_list[i]
                    win['-act-'].update(values = plan_list)
                else:
                    sg.popup('音声を設定してください')
                break
            break

    # 再生ボタン
    if event == '-play-':
        sound = values['-sound-']
        mixer.music.load(sound)
        mixer.music.play(1)
    
    # 時計更新
    jstnow = datetime.datetime.now().strftime('%m月%d日 %H:%M:%S')
    win['-jstclock-'].update(jstnow)
    utcnow = datetime.datetime.now(datetime.timezone.utc).strftime('%m月%d日 %H:%M:%S')
    win['-utcclock-'].update(utcnow)
    estnow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%m月%d日 %H:%M:%S')
    win['-estclock-'].update(estnow)

win.close()
