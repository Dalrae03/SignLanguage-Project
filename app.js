const express = require('express')
const helmet = require('helmet')
const app = express()
app.use(helmet())

// 주소를 만들어주는 도구 get
app.get('/', function (req, res) {
  res.send('Hello World')
})

app.get('/about', function (req, res) {
  res.send('About Page')
})

app.listen(3000, function(req,res){
  console.log("서버 실행 중")
})