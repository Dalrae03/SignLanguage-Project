const express = require('express'); //서버를 만들기 위해 필한 express도구 불러오기
const router = express.Router(); //주소를 만들 때 사용하는 도구
//express안의 app을 통해서도 주소를 만들 수 있긴 한다.

const bcrypt = require('bcrypt');
const pool = require('../model/db');
const { name } = require('ejs');
const saltRounds = 10;



// 주소를 만들어주는 도구 get
router.get('/', function(req, res){
  //let query = req.query;
  //console.log(query)
  //res.render('Main Page/index')
  // res.send({"Key":"Value"})
  //그림파일 전달할 때 데이터 파일까지 크롬브라우저에 같이 전달
  if (req.session.is_logined) {
    // 로그인된 경우
    res.render('firstLayout2', {
        title: "CTH 메인페이지",
        content: "Main Page/index",
        username: req.session.nickname // 사용자 이름 전달
    });
} else {
    // 로그인되지 않은 경우
    res.render('firstLayout', { // 다른 레이아웃 파일 사용
        title: "CTH 메인페이지",
        content: "Main Page/index"
    });
}  
})

  
router.get('/signup', function(req, res){
  res.render('layout',{title: "CTH 회원가입 페이지", content: "SignUp Page/signup"})
  })

// 회원가입 로직
router.post('/signup', async function(req,res){
  let username = req.body.name;
  let email = req.body.email;
  let password = req.body.password;  
  if (username && email && password) {
      try {

          pool.query('SELECT * FROM users WHERE email = ?', [email], async function(error, results, fields) { // pool에 같은 이름의 이메일이 있는지 확인
              if (error){
                  console.error('Database query error:', error);
                  res.status(500).send('Database query error');
                  return;
              } 
              if (results.length === 0) {  
                // pool에 같은 이름의 이메일이 없는 경우
                  pool.query('INSERT INTO users (name, email, password) VALUES(?,?,?)', [username, email, password], function (error, data) {
                      if (error) {
                          console.error('Database insertion error:', error);
                          res.status(500).send('Database insertion error');
                          return;
                      }
                      res.redirect('/?signup=success');//메인페이지로 이동하고싶다... 이거 될까..?
                  });
              } else {// pool에 같은 이름의 이메일이 있는 경우
                res.redirect('/?signup=useing');    
              }            
          });

      } catch (error) {
          console.error('Error during hashing password:', error);
          res.status(500).send('Server error');  
      }
  } else {
      res.status(400).send('Required fields are missing');
  }
});
  



router.get('/login', function(req, res){
  res.render('layout',{title: "CTH 로그인 페이지", content: "Login Page/login"})
  })

// 로그인 로직
router.post('/login', async function (req, res) {
  let email = req.body.email;
  let password = req.body.password;
  if (email && password) {        
      pool.query('SELECT * FROM users WHERE email = ? AND password = ?', [email, password], async function(error, results, fields) {
        const user = results[0];
        if (error) throw error;
        if (results.length > 0) {       // db에서의 반환값이 있으면 로그인 성공
          req.session.is_logined = true;      // 세션 정보 갱신
          req.session.nickname = user.name;
            req.session.save(function () {
              res.redirect('/?login=success');
            });
        } else {  //이메일과 비밀번호가 일치하지 않을경우 
          res.redirect('/?login=error');              
        }            
    });

  } else {
    // 빈 칸을 보냈을 경우 (에초에 form에 필수 입력요소라고 지정하긴했지만...)
    res.redirect('/?login=noinput');    
  }
});

router.get('/studying', function(req, res){
  if (req.session.is_logined) {
    // 로그인된 경우
    res.render('firstLayout2', {
        title: "CTH 수어 학습하기",
        content: "Main Page/studying",
        username: req.session.nickname // 사용자 이름 전달
    });
} else {
    // 로그인되지 않은 경우
    res.redirect('/?nologin');
}   
})

// 로그아웃
router.get('/logout', function(req, res) {
  req.session.destroy(function(err) {
      if (err) {
          console.log(err);
          res.send("로그아웃 중 에러가 발생했습니다.");
      } else {
          res.redirect('/'); // 세션 파괴 후 홈페이지로 리다이렉트
      }
  });
});



router.get('/lecture', function(req, res){
  res.render('firstLayout2', {
    title: "CTH 자화 자음 학습하기",
    content: "Main Page/lecture",
    username: req.session.nickname // 사용자 이름 전달
});
  })




router.get('/flashCard', function(req, res){
  if (req.session.is_logined) {
    // 로그인된 경우
    res.render('firstLayout2', {
        title: "CTH 플래시카드",
        content: "Main Page/flashCard",
        username: req.session.nickname // 사용자 이름 전달
    });
} else {
    // 로그인되지 않은 경우
    res.redirect('/?nologin');
}   
})


router.get('/acidRain', function(req, res){
  if (req.session.is_logined) {
    // 로그인된 경우
    res.render('firstLayout2', {
        title: "CTH 산성비",
        content: "Main Page/acidRain",
        username: req.session.nickname // 사용자 이름 전달
    });
} else {
    // 로그인되지 않은 경우
    res.redirect('/?nologin');
}
})


router.get('/class', function(req, res){
  res.render('firstLayout2', {
    title: "CTH 자화 자음 1강",
    content: "Main Page/class",
    username: req.session.nickname // 사용자 이름 전달
});
  })



//res.send('About Page') 응답으로 문자, 숫자, 딕셔너리같이 데이터를 전달할때는 send 사용


module.exports = router  //router이라는 변수 밖으로 내보내기 -> app.js에서 사용하기 위함