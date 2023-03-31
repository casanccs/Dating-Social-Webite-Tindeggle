let loc = window.location;
let wsStart = 'ws://';
if (loc.protocol == 'https:'){
    wsStart = 'wss://';
}
let endPoint = wsStart + loc.host + '/' + room_name;
console.log(endPoint);

let webSocket = new WebSocket(endPoint);
let mapPeers = {}

webSocket.addEventListener('open', (e) => {
    console.log("Connection opened")
    sendSignal('new-peer', {});
})

webSocket.addEventListener('message', webSocketMessage)

webSocket.addEventListener('close', (e) => {
    console.log("Connection closed")
})

webSocket.addEventListener('error', (e) => {
    console.log("Connection error")
})

console.log('In main.js!');

function webSocketMessage(event){
    let parsedData = JSON.parse(event.data) //equivalent to json.loads()
    let peerUsername = parsedData['peer'];
    let action = parsedData['action'];
    let message = parsedData['message'];
    console.log('message: ', message);

    if (uValue == peerUsername){
        return;
    }
    let receiver_channel_name = parsedData['message']['receiver_channel_name']

    if (action == 'new-peer'){
        createOfferer(peerUsername, receiver_channel_name);
        return;
    }

    if (action == 'new-offer'){
        let offer = parsedData['message']['sdp'];
        createAnswerer(offer, peerUsername, receiver_channel_name);
    }

    if (action == 'new-answer'){
        let answer = parsedData['message']['sdp'];
        let peerConnection = mapPeers[peerUsername][0];
        peerConnection.setRemoteDescription(answer);
        return;
    }
}

let localStream = new MediaStream();
let localVideo = document.querySelector('#localVideo');
let toggleVideo = document.querySelector('#toggleVideo');
let toggleAudio = document.querySelector('#toggleAudio');
let messageInput = document.querySelector('#msg')

let toVideo = true
let userMedia = navigator.mediaDevices.getUserMedia({'video': toVideo, 'audio': true})
    .then(stream =>{
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;

        let audioTracks = stream.getAudioTracks();
        audioTracks[0].enabled = true;
        toggleAudio.addEventListener('click', () => {
            audioTracks[0].enabled = !audioTracks[0].enabled;
            if (audioTracks[0].enabled){
                toggleAudio.innerHTML = "Audio Mute";
                return
            }
            toggleAudio.innerHTML = "Audio Unmute";
        })

        if (toVideo){
            let videoTracks = stream.getVideoTracks();
            videoTracks[0].enabled = true;
            toggleVideo.addEventListener('click', () => {
                videoTracks[0].enabled = !videoTracks[0].enabled;
                if (videoTracks[0].enabled){
                    toggleVideo.innerHTML = "Video Off";
                    return
                }
                toggleVideo.innerHTML = "Video On";
            })
        }
    })
    .catch(error => {
        console.log('Error: ' , error)
    })

let sendMsg = document.querySelector('#sendMsg');
let msgList = document.querySelector('#msgList');
let msg = document.querySelector('#msg');
sendMsg.addEventListener('click', sendMsgOnClick);
function sendMsgOnClick(){
    let message = msg.value;
    let li = document.createElement('li');
    li.appendChild(document.createTextNode('Me: ' + message));
    msgList.appendChild(li);

    let dataChannels = getDataChannels();
    message = uValue + ": " + message;
    for (index in dataChannels){
        dataChannels[index].send(message);
    }
    messageInput.value = '';
}

function sendSignal(action, message){
    let jsonStr = JSON.stringify({
        'peer': uValue,
        'action': action,
        'message': message,
    })    
    webSocket.send(jsonStr)
}

function createOfferer(peerUsername, receiver_channel_name){
    let peerConnection = new RTCPeerConnection(null); //Won't work with two devices in diff network

    addLocalTracks(peerConnection);

    let dc = peerConnection.createDataChannel('channel');
    dc.addEventListener('open', () => {
        console.log('Connection open!');
    })
    dc.addEventListener('message', dcOnMessage);

    let remoteVideo = createVideo(peerUsername);
    setOnTrack(peerConnection, remoteVideo);

    mapPeers[peerUsername] = [peerConnection, dc];

    peerConnection.addEventListener('iceconnectionstatechange', () => {
        let iceConnectionState = peerConnection.iceConnectionState;
        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
            delete mapPeers[peerUsername]
            if (iceConnectionState != 'closed'){
                peerConnection.close();
            }
            removeVideo(remoteVideo);
        }
    })

    peerConnection.addEventListener('icecandidate', (event) => {
        if (event.candidate){
            console.log('New ice candidate');
            return;
        }
        sendSignal('new-offer', {
            'sdp': peerConnection.localDescription,
            'receiver_channel_name': receiver_channel_name,
        })
    })

    peerConnection.createOffer()
        .then(o => peerConnection.setLocalDescription(o))
        .then(() => {
            console.log('Local Desc set successfully');
        })
}

function createAnswerer(offer, peerUsername, receiver_channel_name){
    let peerConnection = new RTCPeerConnection(null); //Won't work with two devices in diff network

    addLocalTracks(peerConnection);


    let remoteVideo = createVideo(peerUsername);
    setOnTrack(peerConnection, remoteVideo);

    peerConnection.addEventListener('datachannel', e => {
        peerConnection.dc = e.channel;
        peerConnection.dc.addEventListener('open', () => {
            console.log('Connection open!');
        })
        peerConnection.dc.addEventListener('message', dcOnMessage);

        mapPeers[peerUsername] = [peerConnection, peerConnection.dc];
    })

    peerConnection.addEventListener('iceconnectionstatechange', () => {
        let iceConnectionState = peerConnection.iceConnectionState;
        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed') {
            delete mapPeers[peerUsername]
            if (iceConnectionState != 'closed'){
                peerConnection.close();
            }
            removeVideo(remoteVideo);
        }
    })

    peerConnection.addEventListener('icecandidate', (event) => {
        if (event.candidate){
            console.log('New ice candidate: '/*JSON.stringify(peerConnection.localDescription)*/);
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

function addLocalTracks(peerConnection){
    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    })
    return;
}


function dcOnMessage(event){
    let message = event.data;
    let li = document.createElement('li');
    li.appendChild(document.createTextNode(message));
    msgList.appendChild(li);
}

function createVideo(peerUsername){
    let videoCont = document.querySelector('#videoCont')
    let remoteVideo = document.createElement('video')
    let videoWrapper = document.createElement('div')
    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;
    videoCont.appendChild(videoWrapper);
    videoWrapper.appendChild(remoteVideo);

    return remoteVideo;
}

function setOnTrack(peer, remoteVideo){
    let remoteStream = new MediaStream();
    remoteVideo.srcObject = remoteStream;
    peer.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    })
}

function removeVideo(video){
    let videoWrapper = video.parentNode;

    videoWrapper.parentNode.removeChild(videoWrapper);
}

function getDataChannels(){
    let dataChannels = [];
    for (peerUsername in mapPeers){
        let dataChannel = mapPeers[peerUsername][1];
        dataChannels.push(dataChannel);
    }
    return dataChannels;
}