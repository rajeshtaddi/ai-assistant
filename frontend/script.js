async function sendMessage(){

    let input = document.getElementById("user-input");
    let message = input.value.trim();

    if(message === "") return;

    addMessage(message,"user");

    input.value="";

    showTyping();

    let response = await fetch(
        "http://127.0.0.1:9000/chat?message=" + encodeURIComponent(message)
    );

    let data = await response.json();

    removeTyping();

    addMessage(data.response,"ai");
}


function addMessage(text,sender){

    let chatBox = document.getElementById("chat-box");

    let messageDiv = document.createElement("div");
    messageDiv.className="message "+sender;

    let bubble = document.createElement("div");
    bubble.className="bubble";
    bubble.innerText=text;

    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);

    chatBox.scrollTop=chatBox.scrollHeight;
}


/* Typing animation */

function showTyping(){

    let chatBox=document.getElementById("chat-box");

    let typing=document.createElement("div");
    typing.className="message ai";
    typing.id="typing";

    typing.innerHTML=`<div class="bubble">AI is typing...</div>`;

    chatBox.appendChild(typing);
}

function removeTyping(){

    let typing=document.getElementById("typing");
    if(typing) typing.remove();
}


/* Enter key support */

document.getElementById("user-input")
.addEventListener("keypress",function(e){

    if(e.key==="Enter"){
        sendMessage();
    }

});