from jnius import autoclass


def get_call_state():
    TelephonyManager = autoclass('android.telephony.TelephonyManager')
    Context = autoclass('android.content.Context')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

    context = PythonActivity.mActivity.getApplicationContext()
    telephony_manager = context.getSystemService(Context.TELEPHONY_SERVICE)

    state = telephony_manager.getCallState()

    if state == TelephonyManager.CALL_STATE_IDLE:
        return "IDLE"
    elif state == TelephonyManager.CALL_STATE_RINGING:
        return "RINGING"
    elif state == TelephonyManager.CALL_STATE_OFFHOOK:
        return "OFFHOOK"
    else:
        return "UNKNOWN"


call_state = get_call_state()
print(f"Current call state: {call_state}")
