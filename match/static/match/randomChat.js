var randomChatUrl = window.location.href
console.log(randomChatUrl)
function sendSignal(action, message){
    let jsonStr = JSON.stringify({
        'peer': uValue,
        'action': action,
        'message': message,
    })    
    webSocket.send(jsonStr)
}

function createPeerConnection(peerUsername, type){
    peerConnection = new RTCPeerConnection(servers)

    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream)
    })

    remoteVideo = document.querySelector('#remoteVideo')
    remoteStream = new MediaStream()
    remoteVideo.srcObject = remoteStream
    peerConnection.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    })

    let dc;
    if (type === 'offer'){ //ERROR COULD OCCUR HERE
        dc = peerConnection.createDataChannel('channel');
        //Data Channels is what is used to exchange messages from user to user
        dc.addEventListener('open', () => {
            console.log('Connection open!');
        })
        //dc.addEventListener('message', dcOnMessage);
    
    
        mapPeers[peerUsername] = [peerConnection, dc];
    }
    else{
        peerConnection.addEventListener('datachannel', e => {
            peerConnection.dc = e.channel;
            peerConnection.dc.addEventListener('open', () => {
                console.log('Connection open!');
            })
            //peerConnection.dc.addEventListener('message', dcOnMessage);
    
            mapPeers[peerUsername] = [peerConnection, peerConnection.dc];
        })
    }
    /*
    At this point, the data channel and peer connection of the other person is always persistent.
    Remember that we know its another user, not ourselves.
    */

    //It is at this point where iceconnection gets confusing
    peerConnection.addEventListener('iceconnectionstatechange', () => {
        let iceConnectionState = peerConnection.iceConnectionState;
        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
            delete mapPeers[peerUsername]
            if (iceConnectionState != 'closed'){
                peerConnection.close();
            }
        }
    })
}

function createOffer(peerUsername, receiver_channel_name){
    createPeerConnection(peerUsername, 'offer')

    peerConnection.addEventListener('icecandidate', (event) => {
        if (event.candidate){
            console.log('New ice candidate');
            return;
        }
        sendSignal(
            'new-offer', 
            {
            'sdp': peerConnection.localDescription,
            'receiver_channel_name': receiver_channel_name,
            }
        )
    })

    peerConnection.createOffer()
        .then(o => peerConnection.setLocalDescription(o))
        .then(() => {
            console.log('Local Desc set successfully');
        })
}

function createAnswer(offer, peerUsername, receiver_channel_name){
    createPeerConnection(peerUsername, 'answer')
    console.log("Trying to create answer")
    peerConnection.addEventListener('icecandidate', (event) => {
        if (event.candidate){
            //console.log('New ice candidate: ', JSON.stringify(peerConnection.localDescription));
            return;
        }
        sendSignal('new-answer', {
            'sdp': peerConnection.localDescription,
            'receiver_channel_name': receiver_channel_name,
        })
    })

    peerConnection.setRemoteDescription(offer)
        .then(() => {
            console.log('Remote Desc set successfully for', peerUsername);
            return peerConnection.createAnswer();
        })
        .then(a => {
            console.log('Answer created');
            peerConnection.setLocalDescription(a)
        })
}

let text = document.querySelector('.text');
let submit = document.querySelector('.submit');
let body = document.querySelector('body');
let uValue = document.querySelector('#uValue').textContent;
let remoteVideo;
let localStream;
let remoteStream;
let peerConnection;
let webSocket;
let mapPeers = {}
let servers = {
    iceServers: [
        {
            urls: ['stun:stun1.1.google.com:19302', 'stun:stun2.1.google.com:19302']
        }
    ]
}

let init = async () => {
    let toVideo = true;
    localStream = await navigator.mediaDevices.getUserMedia({video:toVideo ,audio:false})
    document.getElementById('userVideo').srcObject = localStream
    let room_name = document.querySelector('#room_name').textContent
    webSocket = new WebSocket('wss://' + window.location.host + '/' + room_name);
    webSocket.addEventListener('close', (e) => {
        console.log("Connection closed")
    })
    
    webSocket.addEventListener('error', (e) => {
        console.log("Connection error")
    })
    webSocket.addEventListener('message', (e) => {
        let parsedData = JSON.parse(e.data)
        /*
            In this case parsedData could look like:
            {
                'peer': 'aUsername',
                'action': 'new-peer',
                'message': {
                    receiver_channel_name: "somename",
                    something else: something else,
                }
            }
        */
        let peerUsername = parsedData['peer'];
        let action = parsedData['action'];
        let message = parsedData['message'];
        console.log('message: ', message);
        console.log(action)
        if (action == 'new-message'){
            let p = document.createElement('p');
            p.innerHTML = parsedData['message']['text-content'];
            body.appendChild(p);
            text.value = '';
            return;
        }
        if (uValue == peerUsername){ //So that only other people can get this "message"
            return;
        }
        let receiver_channel_name = parsedData['message']['receiver_channel_name']
        if (action == 'new-peer'){
            createOffer(peerUsername, receiver_channel_name);
            return;
        }
        if (action == 'new-offer'){
            let offer = parsedData['message']['sdp'];
            createAnswer(offer, peerUsername, receiver_channel_name);
        }
        if (action == 'new-answer'){
            let answer = parsedData['message']['sdp'];
            let peerConnection = mapPeers[peerUsername][0];
            peerConnection.setRemoteDescription(answer);
            return;
        }
    })
    
    webSocket.addEventListener('open', (e) => {
        console.log("Connection opened")
        sendSignal('new-peer', {})
    })
}
init()

text.onkeyup = (e) => {
    if (e.keyCode === 13 && text.value != ''){ //This is the enter button
        submit.click();
    }
}

submit.onclick = (e) => {
    let message = text.value;
    sendSignal('new-message', {'text-content': message})
}

window.addEventListener('beforeunload', function(e){
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf_token); //csrf_token is from base.html script
    fetch(randomChatUrl, {
        method: 'POST',
        body: formData,
    })
    return "Do something"
})