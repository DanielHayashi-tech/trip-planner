// load the things we need
var express = require('express');
var app = express();

const bodyParser  = require('body-parser');
const { default: axios } = require('axios');
// required module to make calls to a REST API
const { response } = require('express');
const req = require('express/lib/request');
var selectedID = "";
app.use(bodyParser.urlencoded());


// testing git
// set the view engine to ejs
app.set('view engine', 'ejs');

// OUR WELCOME PAGE (WISHES YOU A NICE MESSAGE)
app.get('/home', function(req, res){
    res.render('pages/home');

});


// LOGIN PAGE
app.get('/', function(req, res) {
    var flag = 0;
    res.render('pages/login', {flag: flag
    });
});

app.post('/login', function(req, res){
    axios.get('http://127.0.0.1:5000/api/authenticate', {
        data:
            {
                username: req.body.username,
                password: req.body.password
            }
    }).then((response)=>
        {
            if (response.data === "Successfully Logged in") {
                res.render('redirects/loggedin', {body: req.body})
            }
            else {
                var flag = 1;
                var response = response.data
                res.render('pages/login', {body: req.body, flag: flag, response: response})
            }
        }
    )
});

// LOGIN OUT PAGE
app.get('/logout', function(req, res){
    res.render('redirects/loggedout');
});



// ADD DATA TO TABLE
app.get('/index', function(req, res) {
    axios.get('http://127.0.0.1:5000/api/tripz')
        .then((response)=>{
            var tripz_data = response.data
            if (tripz_data === "No Active User Detected" || tripz_data === "Session Timed Out! Please Log Back in") {
                var flag = 1;
                var response = tripz_data
                res.render('pages/login', {flag: flag, response: response})
            }
            else {
                res.render('pages/index', {trips_list: tripz_data});
            }
        });
});


// ADD DATA TO TABLE
app.get('/des', function(req, res) {
    axios.get('http://127.0.0.1:5000/api/destinationz')
        .then((response)=>{
            var destinationz_data = response.data
            if (destinationz_data === "No Active User Detected" || destinationz_data === "Session Timed Out! Please Log Back in") {
                var flag = 1;
                var response = destinationz_data
                res.render('pages/login', {flag: flag, response: response})
            }
            else {
                res.render('pages/des', {destinationz_list: destinationz_data});
            }
        });
});




// Add destination
app.post('/des/new', function(req, res) {
    axios.post('http://127.0.0.1:5000/api/destinationz/add',
        {
            country: req.body.country,
            city : req.body.city,
            sightseeing : req.body.sightseeing

        })
        .then((response)=>{
            var message = response.data
            {
                res.render('redirects/redirecthome', {message : message});
            }
        });
});


// Add trip
app.post('/index/new', function(req, res) {
    axios.post('http://127.0.0.1:5000/api/tripz/add',
        {
            transportation : req.body.transportation,
            startdate : req.body.startdate,
            enddate : req.body.enddate,
            tripname : req.body.tripname,

        })
        .then((response)=>{
            var message = response.data
            {
                res.render('redirects/redirectindex', {message : message});
            }
        });
});



// Deletes destination by ID
app.post('/des/delete', function(req, res) {
    axios.delete('http://127.0.0.1:5000/api/destinationz/delete',{
            data:{
                id: req.body.id
            }
        }
    )
        .then((response)=>{
            var message = response.data

            {
                res.render('redirects/redirecthome', {message : message});
            }
        });
});

// Deletes trip by ID
app.post('/index/delete', function(req, res) {
    axios.delete('http://127.0.0.1:5000/api/tripz/delete',{
            data:{
                trip_id: req.body.trip_id
            }
        }
    )
        .then((response)=>{
            var message = response.data

            {
                res.render('redirects/redirectindex', {message : message});
            }
        });
});




// UDATING GOES HERE

// Pushes updated information to the database
app.post('/des/update', function(req, res) {
    axios.put('http://127.0.0.1:5000/api/destination/update',
        {
            id: req.body.id,
            country: req.body.country,
            city: req.body.city,
            sightseeing: req.body.sightseeing
        }
    )
        .then((response)=>{
            var service_data = response.data
            if (service_data === "Session Timed Out! Please Log Back in" || service_data ==="No Active User Detected"){
                var flag = 1;
                var response = service_data
                res.render('pages/login', {flag: flag, response: response})
            }
            else{
                var message = response.data
                res.render('redirects/redirecthome', {message : message});
            }
        });
});


app.listen(8080);
console.log('8080 is the magic port');

