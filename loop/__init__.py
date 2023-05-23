import os

from flask import Flask, render_template, send_file


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'loop.sqlite'),
    )

    isConfigLoaded = app.config.from_pyfile(os.path.join(app.root_path, 'config.py'),
                                        silent=False)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # databse connection
    from . import db
    db.init_app(app)


    from .apis import ReportApis
    from .config_keeper import ConfigKeeper

    # routers
    @app.route('/')
    def hello():
        return render_template("index.html", reportData=None)
    
    @app.route('/trigger_report/')
    # @app.route('/trigger_report/<int:pivotepoch>')
    def triggerReport():
        reportData = ReportApis.generate()
        return render_template("index.html", reportData=reportData)
    
    @app.route('/get_report/<reportId>')
    def getReport(reportId:str):
        reportData = ReportApis.get((reportId))
        return render_template("index.html", reportData=reportData)

    @app.route('/download_report/<filename>')
    def downloadReport(filename:str):
        return send_file(f"./reports/{filename}.csv", as_attachment=True)
    
    return app