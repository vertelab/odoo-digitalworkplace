import { login, Observable } from '@nativescript/core';
import { Http } from '@nativescript/core';
import { Utils } from "@nativescript/core";
import { AppSettings } from '@nativescript/core';

function getMessage(counter) {
  if (counter <= 0) {
    return 'Hoorraaay! You unlocked the NativeScript clicker achievement!'
  } else {
    return `${counter} taps left`
  }
}

export function createViewModel() {
  const viewModel = new Observable()
  viewModel.counter = 2
  viewModel.message = getMessage(viewModel.counter)

  viewModel.onTap = () => {
    viewModel.counter--
    viewModel.set('message', getMessage(viewModel.counter))

//    login('Please login to your Odoo account','Name','Password');

    Http.request({
      url: "https://calendarapp.azzar.net/web/session/authenticate",
      method: "POST",
      headers: { "Content-Type": "application/json" },
      content: JSON.stringify({
          params:{
            db: "calendarapp",
            login: "admin",
            password: "<insert_password_here>",
          }
      }),
    })
    .then(
      (result) => {
        var jsonobj = JSON.parse(result.content);
//        viewModel.set('getStringResult', jsonobj.error['message']);
//        console.log(jsonobj);
        if (jsonobj.error) {
          if (jsonobj.error.data.name === 'psycopg2.OperationalError') {console.log('Database error!');}
          else if (jsonobj.error.data.name === 'odoo.exceptions.AccessDenied') {console.log('Authentication error!');}
        }
        else if (jsonobj.result) {
/*           Http.getJSON('https://calendarapp.azzar.net/calendar_sync')
          .then((result) => {
            viewModel.set('getStringResult', result.test)
            },
          e => {console.log(e);}
          ) */
            getEvents().then(function(events) {
                console.log(JSON.stringify(events))
                Http.request({
                    url: "https://calendarapp.azzar.net/calendar_sync",
                    method: "POST",
                    // headers: { "Content-Type": "application/json" },
                    content: JSON.stringify(
                        events,
                    ),
                })
                .then(
                    (response) => {
                      // Argument (response) is HttpResponse
                      console.log('---------------------------------');
                      console.log(java.util.TimeZone.getDefault().getID())
                      console.log(java.util.Locale.getDefault())
                        var data = JSON.parse(response.content)
                        console.log(data)

                        for (const key of data) {
                          if (key['event_id'] == 38) {
                            const date = key['start_time']+' UTC'
                            console.log(new Date(date))

                            const options = {
                              title: key['name'],
                              startDate: new Date(date),
                              endDate: new Date(key['end_time']+' UTC'),
                              calendar: {
                                name: "NativeScript Cal",
                                color: "#00AA00",
                                accountName: "My App Name"
                              }
                            }
                            console.log(options)

                            Calendar.createEvent(options).then(
                                function(createdId) {
                                  console.log("Created Event with ID: " + createdId);
                                },
                                function(error) {
                                  console.log("Error creating an Event: " + error);
                                }
                            );





//                            viewModel.set('getStringResult', key.description)
//                            console.log(key)
                          }
                        }
                        console.log(`Response Status Code: ${response.statusCode}`)
                        console.log(`Response Content: ${response.content}`)
                    },
                    e => {}
                    )
                })
        }
      },
      e => {console.log(e);}
      )
    }







  return viewModel
}






var Calendar = require("nativescript-calendar");
Calendar.hasPermission().then((g)=> console.log("Permission granted?", g ? "YES" : "NO"));
// Calendar.requestPermission().then( function() {

  // Only the `title`, `startDate` and `endDate` are mandatory, so this would suffice:
  var options = {
    title: 'Get brains',
    // Make sure these are valid JavaScript Date objects.
    // In this case we schedule an Event for now + 1 hour, lasting 1 hour.
    startDate: new Date(new Date().getTime() ),
    endDate: new Date(new Date().getTime() + (1000*60*60*24))
  };

  // You can however add lots of properties to enrich the Event:
  options.location = 'The shop';
  options.notes = 'This event has reminders';

  // iOS has a separate 'url' field, but on Android the plugin appends this to the 'notes' field.
  options.url = 'http://my.shoppinglist.com';

  // You can also override the default reminder(s) of the Calendar (in minutes):
  options.reminders = {
    first: 60,
    second: 10
  };

  // You can make this Event recurring (this one repeats every other day for 10 days):
/*   options.recurrence = {
    frequency: "daily", // daily | weekly | monthly | yearly
    interval: 2, // once every 2 days
    endDate: new Date(new Date().getTime() + (10*24*60*60*1000)) // 10 days
  }; */

  options.attendees = {name:'test testing', email:'test@test.com', url:'myurl', status:'', role:'', type:'Optional'}


  // Want to use a custom calendar for your app? Pass in the 'name'.
  // If the name doesn't yet exist the plugin will create it for you.
  options.calendar = {
    name: "NativeScript Cal",
    // the color, in this case red
    color: "#00AA00",
    // Can be used on Android to group the calendars. Examples: Your app name, or an emailaddress
    accountName: "My App Name"
  };

/*   Calendar.createEvent(options).then(
      function(createdId) {
        console.log("Created Event with ID: " + createdId);
      },
      function(error) {
        console.log("Error creating an Event: " + error);
      }
  ); */


/*   Calendar.listCalendars().then(
    function(calendars) {
      // a JSON array of Calendar objects is returned, each with an 'id' and 'name'
      console.log("Found these Calendars on the device: " + JSON.stringify(calendars));
    },
    function(error) {
      console.log("Error while listing Calendars: " + error);
    }
) */


async function getEvents() {
  var options = {
  // when searching, dates are mandatory - the event must be within this interval
  startDate: new Date(new Date().getTime() - (1000*60*60*24*7)*1 ),
  endDate: new Date(new Date().getTime() + (1000*60*60*24*30)*6)
  };
  console.log('START: '+options.startDate);
  console.log('END: '+options.endDate);
// if you know the Event ID, set it here:
//options.id = '72';

// you can optionally pass in a few other properties, any event containing these will be returned:
//options.title = 'Android';
//options.location = 'foo';
//options.notes = 'bar'; // iOS only


return await Calendar.findEvents(options).then(
    function(events) {
//      console.log(JSON.stringify(events));
        console.log('calendar');
        var calendars = [];
        for (const obj of events) {
            if (obj['calendar']['name'].includes('NativeScript')){
            console.log(obj);
            calendars.push(obj);
            }
        }
//        console.log(calendars);
        return Promise.resolve(calendars)
    },
    function(error) {
      alert({
        title: "Error finding events:",
        message: error,
        okButtonText: "Ok"
      })
    }
  );
//  console.log(obj);
}



function calendarEvents(calendarname) {
  var options = {
    startDate: new Date(new Date().getTime() - (50*24*60*60*1000)),
    endDate: new Date(new Date().getTime() + (50*24*60*60*1000))
  };

  Calendar.findEvents(options).then(
    function(events) {
      for (const obj of events) {
          if (obj['calendar']['name'].includes(calendarname))
            console.log(obj);
      }
    },
    function(error) {
      console.log("Error finding Events: " + error);
    }
  )
}
