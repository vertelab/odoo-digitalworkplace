import { Observable } from '@nativescript/core';
import { Http } from '@nativescript/core';
import { Utils } from "@nativescript/core";

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

    Http.request({
      url: "https://calendarapp.azzar.net/web/session/authenticate",
      method: "POST",
      headers: { "Content-Type": "application/json" },
      content: JSON.stringify({
          params:{
            db: "calendarapp",
            login: "admin",
            password: "<Paste your password here>",
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
          Http.getJSON('https://calendarapp.azzar.net/calendar_sync')
          .then((result) => {
            viewModel.set('getStringResult', result.test)
            },
          e => {console.log(e);}
          )
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
    startDate: new Date(new Date().getTime() + (60*60*1000)),
    endDate: new Date(new Date().getTime() + (2*60*60*1000))
  };

  // You can however add lots of properties to enrich the Event:
  options.location = 'The shop';
  options.notes = 'This event has reminders';

  // iOS has a separate 'url' field, but on Android the plugin appends this to the 'notes' field.
  options.url = 'http://my.shoppinglist.com';

  // You can also override the default reminder(s) of the Calendar (in minutes):
  options.reminders = {
    first: 30,
    second: 10
  };

  // You can make this Event recurring (this one repeats every other day for 10 days):
  options.recurrence = {
    frequency: "daily", // daily | weekly | monthly | yearly
    interval: 2, // once every 2 days
    endDate: new Date(new Date().getTime() + (10*24*60*60*1000)) // 10 days
  };

  options.attendees = {name:'test testing', email:'test@test.com', url:'myurl', status:'', role:'', type:'Optional'}


  // Want to use a custom calendar for your app? Pass in the 'name'.
  // If the name doesn't yet exist the plugin will create it for you.
  options.calendar = {
    name: "NativeScript Cal",
    // the color, in this case red
    color: "#FF0000",
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


var options = {
  // when searching, dates are mandatory - the event must be within this interval
  startDate: new Date(new Date().getTime() - (50*24*60*60*1000)),
  endDate: new Date(new Date().getTime() + (50*24*60*60*1000))
};

// if you know the Event ID, set it here:
options.id = '71';

// you can optionally pass in a few other properties, any event containing these will be returned:
options.title = 'brains';
options.location = 'foo';
options.notes = 'bar'; // iOS only

Calendar.findEvents(options).then(
    function(events) {
      console.log(JSON.stringify(events));
    },
    function(error) {
      console.log("Error finding Events: " + error);
    }
);
