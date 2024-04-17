const express = require('express'); //서버를 만들기 위해 필한 express도구 불러오기
const router = express.Router(); //주소를 만들 때 사용하는 도구
//express안의 app을 통해서도 주소를 만들 수 있긴 한다.


// 주소를 만들어주는 도구 get
router.get('/', function(req, res){
  //let query = req.query;
  //console.log(query)
  //res.render('Main Page/index')
  // res.send({"Key":"Value"})  
  res.render('layout',{title: "CTH 메인페이지"}) //그림파일 전달할 때 데이터 파일까지 크롬브라우저에 같이 전달
  })
  
router.get('/about', function(req, res){
    res.send('About Page')  //응답으로 문자, 숫자, 딕셔너리같이 데이터를 전달할때는 send 사용
  })


router.post("/postapi", function(req, res){
  let body = req.body;
  console.log(body)
  res.send('POST API')
})
  
module.exports = router  //router이라는 변수 밖으로 내보내기 -> app.js에서 사용하기 위함