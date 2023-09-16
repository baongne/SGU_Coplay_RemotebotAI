const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
app.use('/socket.io', express.static(__dirname + '/node_modules/socket.io/client-dist'));
app.use(express.static('C://Users//LENOVO//Desktop//SGU_Coplay'));
//C:\\Users\\Nguyen Ngoc Huy\\OneDrive\\Documents\\GitHub\\SGU_Coplay
// Tạo io được hiểu là một socket instance nằm trên server
const io = require('socket.io')(server);

server.listen(3000, () => {
    console.log('Server đang lắng nghe cổng 3000')
})

app.get('/', (req, res) => {
    console.log("Loading web socket")
    res.sendFile(__dirname + '/client.html')
})

// Xu li ket noi tu client
io.on('connection', (socket) => {
    console.log("Client đã kết nối")
    // Xu li event khi client gui video len moth server
    socket.on('videoClient', (stream) => {
        // Gui video tu server toi robot
        io.emit('videoRobot', stream)
        console.log('Nhận được video từ client', stream)
    })
    // Xu li event khi robot gui video ve server
    socket.on('videoRobot', (stream) => {
        // Gui video tu server toi client
        io.emit('videoClient', stream)
        console.log('Nhận được video từ robot', stream)
    })
    // Xu li event khi client ngat ket noi
    socket.on('disconnect', () => {
        console.log('Client đã ngắt kết nối')
    })
})

