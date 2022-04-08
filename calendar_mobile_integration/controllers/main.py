# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class CalendarSync(http.Controller):
    @http.route('/calendar_sync/', auth='user')
    def index(self, **kw):
        _logger.error(f'{self=}')
        _logger.error(f'{kw=}')
#        mydict = {'test': 'Hello, world'}
        mydict = {}
        restdata = {}
        events = request.env['calendar.event'].search([])
        _logger.error(f'SEARCH: {events}')
        for event in events:
            name = event.browse(event.id).name
            display_time = event.browse(event.id).display_time
            allday = event.browse(event.id).allday
            recurrency = event.browse(event.id).recurrency
            location = event.browse(event.id).location
            description = event.browse(event.id).description
            rrule_type = event.browse(event.id).rrule_type
            interval = event.browse(event.id).interval
            until = event.browse(event.id).until
            alarm_ids = event.browse(event.id).alarm_ids

            mydict['name'] = name
            if allday == False:
                start_date = display_time.split()[0]
                start_time = display_time.split()[2].strip('(')
                if len(display_time.split()) <= 6:
                    end_date = start_date
                    end_time = display_time.split()[4].strip(')')
                else:
                    end_date = display_time.split()[4]
                    end_time = display_time.split()[6]
                mydict['start_date'] = start_date
                mydict['start_time'] = start_time
                mydict['end_date'] = end_date
                mydict['end_time'] = end_time
#            mydict['display_time'] = display_time
            mydict['allday'] = allday
            mydict['recurrency'] = recurrency
            mydict['location'] = location
            mydict['description'] = description
            mydict['rrule_type'] = rrule_type
            mydict['interval'] = interval
            if until:
                mydict['until'] = until.strftime('%m/%d/%Y')
#            mydict[event.id] = {'alarm_ids': alarm_ids}
            restdata[event.id] = mydict
            mydict = {}
        return json.dumps(restdata)
#        return http.request.render("calendar_sync.index", {
#            'test': "Hello, world",
#        })


# name            = event name
# display_time    = start stop with timezone
# allday          = true if event is all day
# recurrency      = true if event is recurring
# location        = location
# description     = notes of the event
# rrule_type      = daily / weekly / monthly / yearly
# interval        = interval between recurrence
# until           = recurrence end_date
# alarm_ids       = reminders (recordset of calandar.alarm)
