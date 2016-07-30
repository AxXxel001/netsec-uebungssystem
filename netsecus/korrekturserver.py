from __future__ import unicode_literals

import logging
import os

import tornado.ioloop
import tornado.web

from .webhandler.DownloadHandler import DownloadHandler
from .webhandler.OverviewHandler import OverviewHandler
from .webhandler.GradingPreviewMailsHandler import GradingPreviewMailsHandler
from .webhandler.GradingSendMailsHandler import GradingSendMailsHandler
from .webhandler.SheetCreateHandler import SheetCreateHandler
from .webhandler.SheetDeleteHandler import SheetDeleteHandler
from .webhandler.SheetEditEndHandler import SheetEditEndHandler
from .webhandler.SheetHandler import SheetHandler
from .webhandler.SheetRestoreHandler import SheetRestoreHandler
from .webhandler.SheetsHandler import SheetsHandler
from .webhandler.StudentHandler import StudentHandler
from .webhandler.StudentsHandler import StudentsHandler
from .webhandler.SubmissionAssignHandler import SubmissionAssignHandler
from .webhandler.SubmissionDetailHandler import SubmissionDetailHandler
from .webhandler.SubmissionGradeAllHandler import SubmissionGradeAllHandler
from .webhandler.SubmissionsListAllHandler import SubmissionsListAllHandler
from .webhandler.SubmissionsListCurrentHandler import SubmissionsListCurrentHandler
from .webhandler.SubmissionsListUnfinishedHandler import SubmissionsListUnfinishedHandler
from .webhandler.SubmissionStudentSheetHandler import SubmissionStudentSheetHandler
from .webhandler.TaskCreateHandler import TaskCreateHandler
from .webhandler.TaskDeleteHandler import TaskDeleteHandler
from .webhandler.TaskEditHandler import TaskEditHandler
from .webhandler.UpdateDatabaseHandler import UpdateDatabaseHandler
from .webhandler.contact import (
    ContactCraftHandler,
    ContactSendHandler,
    ContactAllCraftHandler,
    ContactAllSendHandler,
)
from .webhandler.merge import (
    MergeSelectHandler,
    MergePreviewHandler,
    MergeHandler,
)

from . import database


class KorrekturApp(tornado.web.Application):
    realm = 'netsec Uebungsabgabesystem'

    def __init__(self, config, handlers):
        super(KorrekturApp, self).__init__(handlers)
        for handler in handlers:
            handler[1].config = config
        self.config = config

    @property
    def users(self):
        return self.config('korrektoren')


def web_main(config):
    try:
        mainloop(config)
    except BaseException as e:
        logging.exception(e)
        raise


def mainloop(config):
    application = KorrekturApp(config, [
        (r"/", OverviewHandler),
        (r"/sheets", SheetsHandler),
        (r"/sheet/create", SheetCreateHandler),
        (r"/sheet/([0-9]+)/delete", SheetDeleteHandler),
        (r"/sheet/([0-9]+)/editend", SheetEditEndHandler),
        (r"/sheet/([0-9]+)/restore", SheetRestoreHandler),
        (r"/sheet/([0-9]+)/task/create", TaskCreateHandler),
        (r"/task/([0-9]+)/edit", TaskEditHandler),
        (r"/task/([0-9]+)/delete", TaskDeleteHandler),
        (r"/sheet/.*", SheetHandler),
        (r"/students", StudentsHandler),
        (r"/student/(.*)", StudentHandler),
        (r"/submissions", SubmissionsListCurrentHandler),
        (r"/submissions/all", SubmissionsListAllHandler),
        (r"/submissions/unfinished", SubmissionsListUnfinishedHandler),
        (r"/submission/([0-9]+)", SubmissionDetailHandler),
        (r"/submission/([0-9]+)/([0-9]+)", SubmissionStudentSheetHandler),
        (r"/submission/([0-9]+)/grade_all", SubmissionGradeAllHandler),
        (r"/submission/([0-9]+)/assign", SubmissionAssignHandler),
        (r"/grading/mails/preview", GradingPreviewMailsHandler),
        (r"/grading/mails/send_all", GradingSendMailsHandler),
        (r"/merge/([0-9]+)/select", MergeSelectHandler),
        (r"/merge/([0-9]+)/preview", MergePreviewHandler),
        (r"/merge/([0-9]+)/merge", MergeHandler),
        (r"/contact/([0-9]+)", ContactCraftHandler),
        (r"/contact/([0-9]+)/send", ContactSendHandler),
        (r"/contact/all", ContactAllCraftHandler),
        (r"/contact/all/send", ContactAllSendHandler),
        (r"/download/(.*)", DownloadHandler),
        (r"/updb", UpdateDatabaseHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {
            "path": os.path.join(config.module_path, "static")
        }),
    ])
    application.db = database.Database(config)

    addr = config('httpd.address')
    port = config('httpd.port')
    application.listen(port, address=addr)
    logging.debug("Web server started on port %i.", port)
    tornado.ioloop.IOLoop.instance().start()
