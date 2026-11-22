# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import datetime
import logging

_logger = logging.getLogger(__name__)

class CalendarSync(http.Controller):
    @http.route('/calendar_sync/', auth='user', csrf=False)
    def index(self, **kw):

        def dateformat(date):
            date = date.replace('T',' ')
            date = date.replace('.',' ')
            return date.split()[0]+' '+date.split()[1]

###     Handle the recieved Android events
        _logger.error(f'{self=}')
        events = []
        for x in kw:
            events = json.loads(x)

        for event in events:
#            _logger.error(f'{event["title"]=}')

            vals = {
            'name': event['title'],
            'description': event['notes'],
            'location': event['location'],
            'start': dateformat(event['startDate']) ,
            'stop': dateformat(event['endDate']),
            'allday': event['allDay'],
            }

            if 'recurrence' in event:
                vals['recurrency'] = True
                vals['rrule_type'] = event['recurrence']['frequency']
                if 'count' in event['recurrence']:
                    vals['interval'] = event['recurrence']['count']

            event_id = request.env.ref(f'__sync__.native_calendar_{event["id"]}')
            if not event_id:
                event_id = request.env['calendar.event'].create(vals)
#                request.env['ir.model.data'].create({'module':'__sync__', 'name':f'native_calendar_{event['id']}','model':'calendar.event', 'res_id': event_id.id})
            else:
                event_id.write(vals)

            if 'attendees' in event:
                for attendee in event['attendees']:
                    name = attendee["name"]
                    email = attendee["email"],
                    if not name:
                        name = email
                    if not email:
                        continue
#                    partner_id = request.env['res.partner'].search([('email', '=', email)], limit=1)):
                    if not partner_id:
#                        partner_id = request.env['res.partner'].create({'name':name, 'email':email}
                        pass
                    attendee_vals={'event_id':event_id.id, 'partner_id':partner_id.id}
                    

            _logger.error(f'{vals}')



###     Odoo events below

        reminders = []
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
            for alarm in alarm_ids:
                this_alarm = alarm.browse(alarm.id).duration_minutes
                reminders.append(this_alarm)
            mydict['reminders'] = reminders
            reminders = []

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
