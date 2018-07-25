
var submit = $('#submit');
var user_message = $('#user_message')
var chat_msg = $("#chatmsg")
document.getElementById('user_message').focus();
var nb_responses = 0;

$.getScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyAqlMjGomKCRX2zpADXcv11liLI9H2f1ac", function() {

    function initializeMap(name, json, id){


        var myLatLng = json.candidates[0].geometry.location;
        console.log("coordonnées point :"+myLatLng);

        var map = new google.maps.Map(id, {
            zoom: 15,
            center: myLatLng
        });

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: name,
            animation: google.maps.Animation.DROP,
        });
        function toggleBounce() {
          if (marker.getAnimation() !== null) {
            marker.setAnimation(null);
          } else {
            marker.setAnimation(google.maps.Animation.BOUNCE);
          }
        }

        marker.setMap(map);
        toggleBounce();

        var ne_lat = json.candidates[0].geometry.viewport.northeast.lat;
        var ne_lng = json.candidates[0].geometry.viewport.northeast.lng;
        var sw_lat = json.candidates[0].geometry.viewport.southwest.lat;
        var sw_lng = json.candidates[0].geometry.viewport.southwest.lng;

        var ne_bound = new google.maps.LatLng(ne_lat, ne_lng);
        var sw_bound = new google.maps.LatLng(sw_lat,sw_lng);
        var bounds = new google.maps.LatLngBounds();
        bounds.extend(ne_bound);
        bounds.extend(sw_bound);
        map.fitBounds(bounds);


    }
    // initializeMap(48.856614, 2.3522219, document.getElementById('map0'));


    submit.on('click', function(e) {
        e.preventDefault();
        if (user_message.val()){
            $.ajax({
                url: $SCRIPT_ROOT + '/_response',
                type: 'POST',
                data:  $('form').serialize(),
                success: function(response) {

                    var input = user_message.val();
                    user_message.val("");
                    user_message.focus();
                    nb_responses ++;
                    var id_map = "map"+nb_responses;
                    chat_msg.append( "<div class='row'><div class='message'>"+input+"</div></div>" );
                    chat_msg.append( "<div class='row'><div class='message bot'>"+response['wiki_reply']+"</div></div>" );
                    // chat_msg.append( "<div class='row'><div class='message bot'> Latitude : "+response['gmaps_reply_lat']+" Longitude : "+response['gmaps_reply_lng']+"</div></div>" );
                    if (response['gmaps_reply'] !== "No result"){
                        chat_msg.append( "<div class='row'><div class='message bot'>" +
                            "Voici une carte de "+response['gmaps_name']+" à l'adresse : "+response['gmaps_address']+
                            "<div class='map' id='"+id_map+"'></div></div></div>");
                        }
                    else{
                        chat_msg.append( "<div class='row'><div class='message bot'>Je n'ai pas trouvé de carte à ce sujet.</div></div>");

                    }
                    var elem = document.getElementById('chatbox');
                    elem.scrollTop = elem.scrollHeight;

                    initializeMap(response['gmaps_name'],
                                  response['gmaps_json'],
                                  document.getElementById(id_map));

                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

});



//
//
//
// form.addEventListener("submit", function (ev) {
//     ev.preventDefault();
//     $.getJSON($SCRIPT_ROOT + '/_response', {
//     user_message: $('input[name="user_message"]').val()
//     }, function(data) {
//
//     var nodeUsr = document.createElement("LI");
//     var textnodeUsr = document.createTextNode($('input[name="user_message"]').val());
//     nodeUsr.appendChild(textnodeUsr);
//     document.getElementById("userMessagesList").appendChild(nodeUsr);
//
//     var nodeBot = document.createElement("LI");
//     var textnodeBot = document.createTextNode(data.result);
//     nodeBot.appendChild(textnodeBot);
//     document.getElementById("botMessagesList").appendChild(nodeBot);
//     // $("#chat_history").append(data.result);
//     //
//     // $("#chat_history").append('\n');
//
//     userMessageElt.value ="";
//     });
// });

// // Affiche de toutes les données saisies ou choisies
// form.addEventListener("submit", function (e) {
//     var message = user_message.value;
//     var nouvMessageElt = document.createElement("p");
//     nouvMessageElt.id = "msg";
//     nouvMessageElt.textContent = message;
//     document.getElementById("chatbox").appendChild(nouvMessageElt);
//     user_message.value = "";
//     // e.preventDefault(); // Annulation de l'envoi des données
//
// });





//
// //working :
// $(function(){
//     $("form").submit(function(e) {
//         e.preventDefault();
//         $.getJSON($SCRIPT_ROOT + '/_response', {
//
//         user_message: $('input[name="user_message"]').val()
//
//         }, function(data) {
//         $("#chat_history").text(data.result);
//         });
//
//         return false;
//
//     });
// });