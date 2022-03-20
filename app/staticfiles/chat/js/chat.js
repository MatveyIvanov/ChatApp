current_active_room = null;
const user_id = document.querySelector('#user_id').innerHTML;

var new_chat = false;
var chatSocketCopy = null;

function initChatSocket(companion_id) {
    const roomName = user_id + '-' + companion_id + (new_chat ? '-new':'');
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
    );
    chatSocketCopy = chatSocket;
    console.log("Opened: " + chatSocket.url);

    chatSocket.onopen = function() {
        $.ajax({
            url: '',
            type: 'get',
            success: function(data) {
                $('#card').html(data);
                chat_box = document.querySelector('#chat_box');
                chat_box.scrollTop = chat_box.scrollHeight;
            },
            error: function(e) {
                console.log(e);
            }
        });
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
    
        new_msg = document.createElement('div');
        inner_div = document.createElement('div');

        inner_div.innerHTML = data.message;

        time_span = document.createElement('span');
        time_span.className = 'msg_time_send';
        time_span.innerHTML = data.time;

        inner_div.appendChild(time_span);
    
        img_div = document.createElement('div');
        img = document.createElement('img');
        img.src = "chat/img/avatar.png";
        img.class = "rounded-circle user_img_msg";

        img_div.appendChild(img);

        if (data.sender == user_id) {
            new_msg.className = 'd-flex justify-content-end mb-4';
            inner_div.className = 'msg_cotainer_send';
            new_msg.appendChild(inner_div);
            new_msg.appendChild(img_div);
        }
        else {
            new_msg.className = 'd-flex justify-content-start mb-4';
            inner_div.className = 'msg_cotainer';
            new_msg.appendChild(img_div);
            new_msg.appendChild(inner_div);
        }
    
        document.getElementsByClassName('card-body msg_card_body')[0].appendChild(new_msg);
    
        chat_box = document.querySelector('#chat_box');
        chat_box.scrollTop = chat_box.scrollHeight;
    };
    
    chatSocket.onclose = function(e) {
        console.log("Closed: " + this.url);
    };
    
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };
    
    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        if (message == "") {
            console.log("Empty");
            return
        }
        chatSocket.send(JSON.stringify({
            'message': message,
            'sender': user_id
        }));
        messageInputDom.value = '';
    };
}

window.onbeforeunload = function() {
    if (chatSocketCopy) {
        chatSocketCopy.onclose = function () {}; // disable onclose handler first
        chatSocketCopy.close();
    }
};

window.onload = function() {
    var chat_window = document.querySelector('#chat_window');
    if (window.location.pathname.match(/\/chat\/[\w]+/g) == null) {
        chat_window.style.visibility = 'hidden';
        contacts = document.getElementsByClassName('contacts')[0].children
        if (contacts == null || contacts.length == 0 || contacts[0].tagName != 'LI') {
            console.log('asd');
            document.querySelector('#global_search_btn').style.display = 'inline-block';
        }
    }
    else {
        chat_window.style.visibility = 'visible';
        
        setActive();

        chat_box = document.querySelector('#chat_box');
        chat_box.scrollTop = chat_box.scrollHeight;

        initChatSocket(companion_id);
    }
}

function setActive() {
    companion_id = $('#chat_window_user_info').text().split(' ');
    companion_id = companion_id[companion_id.length - 1];
    spans = document.querySelector('#contacts_list').getElementsByTagName('span');
    for (i = 0; i < spans.length; i++) {
        if (spans[i].textContent == companion_id) {
            span = spans[i];
            break;
        }
    }
    li = span.closest('li');
    li.className = 'active';

    current_active_room = li;
}


$(document).ready(function(){
    $('#action_menu_btn').click(function(){
        $('.action_menu').toggle();
    });
});


/*
    --------------------------------------------
    Enter new chat room by clicking on a contact
    --------------------------------------------
*/

function updateContacts() {
    contacts = document.getElementsByClassName('contacts')[0].children

    for (i = 0; i < contacts.length; i++) {
        if (contacts[i].tagName == 'LI')
            contacts[i].onclick = contactClick;
    }
}

updateContacts();

function contactClick() {
    document.querySelector('#chat-message-input').value = "";

    document.querySelector('#chat_window').style.visibility = 'visible';

    roomName = this.getElementsByClassName('user_info')[0].getElementsByTagName('span')[0].innerHTML
    temp = roomName;

    roomName = roomName.replace(' ', '_');

    pathname = '/chat/' + user_id + '-' + roomName;
    nextState = { additionalInformation: 'Updated with JS' };
    nextTitle = temp
    window.history.pushState(nextState, nextTitle, pathname);
    window.history.replaceState(nextState, nextTitle, pathname);

    if (current_active_room != null)
        current_active_room.className = '';

    this.className = 'active';
    current_active_room = this;

    if (chatSocketCopy) {
        chatSocketCopy.close();
    }

    initChatSocket(roomName);
}



/* SEARCH */


document.querySelector('#search').oninput = function() {
    var contacts = document.querySelector('#contacts_list').getElementsByTagName('li');
    for (i=0; i < contacts.length; i++) {
        id = contacts[i].querySelector('.user_info').querySelector('span').innerHTML;
        if (id.toLowerCase().includes(this.value.toLowerCase())) {
            contacts[i].style.display = "list-item";
        }
        else {
            contacts[i].style.display = "none";
        }
    }

    gs_btn = document.querySelector('#global_search_btn');
    if (this.value != "") {
        gs_btn.style.display = "inline-block";
    }
    else {
        gs_btn.style.display = "none";
    }
}

document.querySelector('#global_search_btn').onclick = function() {
    document.querySelector('#global_search').click();
}

document.querySelector('#global_search').onclick = function() {
    substr = document.querySelector('#search').value;
    if (substr == '')
        return

    var pathname = '/chat/global_search';
    var nextState = { additionalInformation: 'Updated with JS' };
    var nextTitle = pathname;
    window.history.pushState(nextState, nextTitle, pathname);
    window.history.replaceState(nextState, nextTitle, pathname);

    $.ajax({
        url: 'chat/global_search',
        type: 'get',
        data: {'search_substring': substr},
        success: function(data) {
            $('#contacts_list').html(data);

            egs_btn = document.querySelector('#exit_global_search_btn');
            egs_btn.style.display = 'inline-block';
            egs_btn.onclick = exitGlobalSearch;

            new_chat = true;
            updateContacts();
        },
    });
}

function exitGlobalSearch() {
    var pathname = '/chat';
    var nextState = { additionalInformation: 'Updated with JS' };
    var nextTitle = pathname;
    window.history.pushState(nextState, nextTitle, pathname);

    document.querySelector('#exit_global_search_btn').style.display = 'none';
    document.querySelector('#search').value = "";

    $.ajax({
        url: 'chat',
        type: 'get',
        success: function(data) {
            $('#contacts_list').html(data);

            new_chat = false;
            updateContacts();
            setActive();

            document.querySelector('#global_search_btn').style.display = 'none';
        },
    });
}
