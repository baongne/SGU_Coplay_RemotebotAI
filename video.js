let videoStream; // Biến lưu trữ stream từ camera
const videoClient = document.getElementById('videoClient');
const videoRobot = document.getElementById('videoRobot');
const openButton = document.getElementById('openButton');
const stopButton = document.getElementById('stopButton');




let isSendingFrames = false;

// function handleVideoStream(stream) {
//   // Gửi video từ client lên server
//   socket.emit('videoClient', stream);
// }

var socket1 = io.connect('http://127.0.0.1:5000/');
socket1.on('connect', function() {
    socket1.emit('my event', {data: "Hello"})
});

socket1.on('test event', function(data) {
    console.log(data['data']);
    
});





function openCamera() {
  // Kiểm tra xem trình duyệt có hỗ trợ truy cập camera không
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Truy cập camera
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
      // Gán stream từ camera vào thẻ video
      isSendingFrames = true;
      // videoClient.srcObject = stream;
      videoStream = stream;
      handleVideoStream(stream);   
    })
      .catch(function(error) {
        console.error('Lỗi truy cập camera: ', error);
      });
  } else {
    console.error('Trình duyệt không hỗ trợ truy cập camera.');
  }
  // Vô hiệu hóa nút "Open"
  openButton.disabled = true;
  // Kích hoạt nút "Close"
  stopButton.disabled = false;
}

function stopCamera() {
  if (videoStream) {
    // Dừng stream từ camera
    isSendingFrames = false;
    videoStream.getTracks().forEach(function(track) {
      track.stop();
    });
    videoStream = null;
    // Xóa stream từ thẻ video
    videoClient.srcObject = null; 
  }
  // Vô hiệu hóa nút "Close"
  stopButton.disabled = true;
  // Kích hoạt nút "Open"
  openButton.disabled = false;
}

function sendFramesToRobot() {
  const frameRate = 20;
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  canvas.width = videoClient.videoWidth;
  canvas.height = videoClient.videoHeight;

  function sendFrameToRobot() {
    if (isSendingFrames) {
      context.drawImage(videoClient, 0, 0, canvas.width, canvas.height);
      const imageData = canvas.toDataURL('image/jpeg');
      // Gửi dữ liệu hình ảnh lên cho robot thông qua máy chủ moth
      console.log("Send frames to robot successfully");
    }
    setTimeout(sendFrameToRobot, 1000 / frameRate);
  }
  sendFrameToRobot();
}