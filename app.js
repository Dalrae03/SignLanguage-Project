const express = require('express');
const helmet = require('helmet');
const app = express();
app.use(helmet());
app.use(express.json()); //post방식 api사용시 필요한 설정
app.use(express.urlencoded()); //post방식 api사용시 필요한 설정


//미들웨어 - 요청과 응답사이 규칙설정 및 알려주기
const mainRouter = require('./router/mainRouter')
app.use('/', mainRouter) //미들웨어 통해 상세 주소지정(규칙지정) 가능

app.listen(3000, function(req,res){
  console.log("서버 실행 중")
})