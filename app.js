const express = require('express')
const app = express()

// 주소를 만들어주는 도구 get
app.get('/', function (req, res) {
  res.send('Hello World')
})

app.listen(3000)