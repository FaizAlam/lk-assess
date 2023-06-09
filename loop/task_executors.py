from concurrent.futures import ThreadPoolExecutor

from flask import current_app

def appCtxAsyncMethod(thisFlaskApp, method, args):
    with thisFlaskApp.app_context():
        method(*args)

def runInBg(executor:ThreadPoolExecutor, method, *args):
    print("----- run in bg service ----")
    res = executor.submit(appCtxAsyncMethod, current_app._get_current_object(), method, args)
    print("---- finished run in bg ----")
    return res


ReportExecutor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="report-generator")