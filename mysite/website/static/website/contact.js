document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#contact-form').addEventListener('submit', add_message)
    document.querySelector('#chatbar-icon').addEventListener('click', () => open_chat())
    document.querySelector('#dropdown').addEventListener('click', () => open_dropdown());
    document.addEventListener('click', close_dropdown);

    get_unread()

})

function show_messages(){

    var msg_sender = document.querySelector(".sender").value;

    if (msg_sender === 'kellysuperuser'){
        var user = document.querySelector(".receiver").value;
    }
    else {
        var user = msg_sender;
    }
    fetch (`getMessages/${user}`)
        .then (response => response.json())
        .then (messages => {
            var view = document.querySelector('#message-view');
            view.innerHTML = "";

            for (var message in messages){
                var sender = messages[message]["sender"];
                var content = document.createElement('div');
                content.innerHTML = messages[message]["content"];
                content.style.position = "relative";
                content.style.width = "175px";
                content.style.borderRadius = "5px";
                content.style.marginTop = "10px";
                content.style.wordWrap = "break-word";
                if (sender === msg_sender){
                    content.style.backgroundColor = "#e3e0cc";
                    content.style.left = "75px";
                }
                else {
                    content.style.backgroundColor = "#f0f0f0";
                    if(messages[message]["read"]== false){
                        content.style.fontWeight = 'bold';
                    }
                }
                view.appendChild(content);
            }
        })
}

function add_message (event){
    
    event.preventDefault();
    var sender = document.querySelector('.sender').value;
    var receiver = document.querySelector('.receiver').value;
    var content = document.querySelector('#compose-message').value;

    fetch('messages',{
        method: "POST",
        body: JSON.stringify({
            "sender": sender,
            "receiver": receiver,
            "content": content
        }),
    })
    document.querySelector('#compose-message').value = '';
    var view = document.querySelector('#message-view');
    var message = document.createElement('div');
    message.innerHTML = content;
    message.style.position = "relative";
    message.style.width = "175px";
    message.style.borderRadius = "5px";
    message.style.marginTop = "10px";
    message.style.wordWrap = "break-word";
    message.style.backgroundColor = "#e3e0cc";
    message.style.left = "75px";
    view.appendChild(message);
}

function get_sender(value){
    var receiver = value;
    document.querySelector(".receiver").value = receiver;
    document.querySelector(".receiver").innerHTML = receiver;
    show_messages();
}

function open_chat() {
    var sender = document.querySelector('.sender').value;
    var receiver = document.querySelector('.receiver').value;

    fetch('readMessages',{
        method: "PUT",
        body: JSON.stringify({
            "sender": sender,
            "receiver": receiver,
        }),
    })

    var chat = document.querySelector('#chat-popup');
    var icon = document.querySelector("#chatbar-icon");
    if (icon.innerHTML === '▲') {
        chat.style.display = 'block';
        icon.innerHTML = '▼';
        show_messages();
    }
    else{
        chat.style.display = 'none';
        icon.innerHTML = '▲';
    }
}
function get_unread(){
    fetch('unread')
        .then(response => response.json())
        .then(unread_messages => {
            console.log(unread_messages.length);
            const chatbar = document.querySelector('#chat-w-us');
            chatbar.innerHTML += " (" + unread_messages.length + ")";
        })

    if (document.querySelector(".sender").value === 'kellysuperuser'){
        const senders = document.getElementsByClassName("get-sender");

        for (var i = 0; i < senders.length; i++){
            var name = senders[i].innerHTML;
            
            fetch (`unread/${name}`)
                .then (response => response.json())
                .then (messages =>{
                    var element = document.createElement("div");
                    element.innerHTML += " (" + messages.length + ")"
                    document.querySelector('.unread').appendChild(element);
                })
        }
    }
}

function open_dropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function close_dropdown(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
