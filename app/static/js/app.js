
$('#user_message').focus();

$('#submit').on('click', function(e) {
    e.preventDefault();
    $.ajax({
        url: $SCRIPT_ROOT + '/_response',
        type: 'POST',
        data:  $('form').serialize(),
        success: function(response) {

            var input = $('#user_message').val()
            $("#chatbox").append( "<div class='message'>"+input+"</div>" );
            $("#chatbox").append( "<div class='message bot'>"+response['reply']+"</div>" );
            $('#user_message').val("");
            $('#user_message').focus();
        },
        error: function(error) {
            console.log(error);
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