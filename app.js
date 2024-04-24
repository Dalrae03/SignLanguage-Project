// 컴퓨터 본체의 스위치 역할을 하는 기본 루트 자바스크립트 파일
const express = require('express');
const helmet = require('helmet'); //서버 어플리케이션의 보안 강화. 노드 보안 모듈
const app = express();

const ejs = require('ejs')

//ejs사용하려면 써야하는 것들
app.set('view engine', 'ejs'); //그림파일을 전달을 할때 어떠한 뷰파일을 전달해주는 엔진(도구)를 사용할건지 명시 - 그 도구가 ejs
// 그림만 전달하는게 아니라 데이터 전달까지 동시에 할 수 있다.
// 그림파일 확장자 명이 ejs여야한다... 흠...
app.set('views', './views') //내가만든 html파일은 전부 views파일에 있다. 알려줌
app.use('/public', express.static(__dirname + '/public')); //css나 이미지 같은 정적인 파일들, 화면을 그릴 때 필요한(사용되는) 도구들 위치
//express.static(__dirname - 퍼블릭 폴더가 app.js 폴더로부터 어디에 있는지 상대적인 주소를 나타내는 도구


app.use(helmet());
app.use(express.json()); //post방식 api사용시 필요한 설정
app.use(express.urlencoded()); //post방식 api사용시 필요한 설정


//미들웨어 - 요청과 응답사이 규칙설정 및 알려주기
// 사이트 -> 요청 -> middleware -> Node.js
const mainRouter = require('./router/mainRouter')
app.use('/', mainRouter) //미들웨어 통해 상세 주소지정(규칙지정) 가능

app.listen(3000, function(req,res){
  console.log("서버 실행 중")
})